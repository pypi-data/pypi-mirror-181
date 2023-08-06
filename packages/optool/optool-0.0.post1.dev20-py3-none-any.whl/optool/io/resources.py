import functools
from abc import ABC, abstractmethod
from types import FunctionType
from typing import Dict, Generic, List, TypeVar
from uuid import UUID

from pyfields import init_fields
from valid8 import validate

from optool.autocode import Attribute, autocomplete
from optool.containers.signals import Signal

T = TypeVar("T")


@autocomplete(make_hash=False, make_str=False, make_repr=False)
class DataEntry(Generic[T]):
    __slots__ = '_spec', '_loader'

    spec: Dict[str, str] = Attribute(read_only=True)

    @init_fields(init_args_before=False)
    def __init__(self, loader: FunctionType):
        validate("Loader", loader, instance_of=(FunctionType, functools.partial))
        self._loader = loader

    def load(self) -> T:
        return self._loader()


class DataServer(ABC):

    @abstractmethod
    def find_signals(self, name="*", source="*", uuid="*") -> List[DataEntry[Signal]]:
        raise NotImplementedError()

    def find_signal(self, name="*", source="*", uuid="*") -> DataEntry[Signal]:
        entries = self.find_signals(name=name, source=source, uuid=uuid)
        spec = f"{name=}, {source=}, {uuid=}"
        if len(entries) == 0:
            raise ValueError(f"No match found for the specified signal: {spec}.")
        if len(entries) > 1:
            raise ValueError(f"More than one match found ({len(entries)}) for the specified signal: {spec}")
        return entries[0]

    def find_signal_uuid(self, name="*", source="*") -> UUID:
        return UUID(self.find_signal(name=name, source=source).spec["uuid"])

    def get_signal(self, uuid: UUID) -> Signal:
        return self.find_signal(uuid=uuid.hex).load()

    @abstractmethod
    def add_signal(self, signal: Signal) -> UUID:
        raise NotImplementedError()
