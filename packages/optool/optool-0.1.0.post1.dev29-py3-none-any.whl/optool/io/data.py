from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict

import numpy as np
import scipy.io

from optool.autocode import Attribute, autocomplete
from optool.logging import LOGGER


class DataHandler(ABC):
    __slots__ = '_file'

    file: Path = Attribute(read_only=True)

    @abstractmethod
    def load(self) -> Dict[str, Any]:
        raise NotImplementedError()


@autocomplete
class MatFileHandler(DataHandler):
    STRUCT_NAMES_IGNORED = ["__function_workspace__"]

    __slots__ = ()

    def load(self) -> Dict[str, Any]:
        try:
            return self._load_using_scipy()
        except Exception as e:
            # import h5py
            # f = h5py.File(self.file.absolute(), 'r')
            # data = f.get('data/variable1')
            # data = np.array(data)  # For converting to a NumPy array
            raise NotImplementedError("Missing implementation.") from e

    def _load_using_scipy(self) -> Dict[str, Any]:
        LOGGER.info("Loading data file {}.", self.file.absolute().as_posix())
        data = scipy.io.loadmat(self.file.absolute().as_posix(), squeeze_me=True, mat_dtype=True)

        metadata = {d: data.pop(d) for d in ['__header__', '__globals__', '__version__']}  # is removed from data
        variable_names = data.keys()
        LOGGER.debug("Loaded mat-file of version {} with {} variables: {}.", metadata["__version__"],
                     len(variable_names), list(variable_names))

        output = {}
        for (name, value) in data.items():
            if name in self.STRUCT_NAMES_IGNORED:
                LOGGER.debug("Skipping variable named {!r}.", name)
                continue

            if not isinstance(value, np.ndarray):
                raise NotImplementedError(f"No idea what to do with a {value.__class__.__name__}.")
            if value.dtype.isbuiltin != 0:
                raise NotImplementedError(f"Missing implementation for {value}.")

            fields = value.dtype.names
            LOGGER.debug("Presumably the variable {!r} is a Matlab struct with the following {} fields: {}.", name,
                         len(value.dtype), fields)
            if np.size(value) != 1:
                raise NotImplementedError(f"Expected an ndarray with one element, but got {np.size(value)}.")
            output[name] = self._load_struct(fields, value.flatten()[0])  # trick to get back access to element
        return output

    @staticmethod
    def _load_struct(fields, values):
        if len(fields) != len(values):
            raise ValueError(
                f"The number of fields must be equal to the number of values, but is {len(fields)} and {len(values)}.")
        return dict(zip(fields, values))
