import os
from multiprocessing import Pool, current_process
from pathlib import Path
from types import FunctionType, MethodType
from typing import Iterable, Union

from optool.autocode import Attribute, autocomplete
from optool.logging import LOGGER, LogFilter, setup_logger, timeit


@autocomplete
class ParallelExecutor:
    __slots__ = '_function', '_log_sink', '_log_level', '_processes'

    function: Union[FunctionType, MethodType] = Attribute()
    log_sink: Path = Attribute(validators=[Path.exists, Path.is_dir])
    log_level: str = Attribute(default="TRACE")
    processes: int = Attribute(default=os.cpu_count())

    @timeit(log_level="INFO")
    def run(self, *args):
        if len(args) == 1 and isinstance(args, Iterable):
            args = args[0]
        processes = min([self.processes, len(args)])
        LOGGER.info("Executing function {} on {} processes in parallel.", self.function.__name__, processes)
        # TODO: Figure out if this is actually necessary, and if so, how to extract the logger and add it again
        # LOGGER.remove()  # Default "sys.stderr" sink cannot be pickled
        with Pool(processes=processes) as pool:
            out = pool.map(self.run_subprocess, args)
        return out

    def run_subprocess(self, arg):
        self.setup_subprocess_logger()
        out = timeit(self.function, log_level="INFO")(arg)
        self.tear_down_subprocess_logger()
        return out

    def setup_subprocess_logger(self):
        process = current_process()
        log_file_name = str(self.log_sink.absolute() / f"log_{process.name}.log")
        setup_logger(sink=log_file_name, filter=LogFilter(), level=self.log_level)

    @staticmethod
    def tear_down_subprocess_logger():
        LOGGER.complete()  # make sure the queue (consumed by a thread started internally) is left in a stable state
