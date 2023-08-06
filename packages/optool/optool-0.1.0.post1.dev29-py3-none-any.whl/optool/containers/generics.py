from __future__ import annotations

from inspect import isclass
from typing import Generic, List, Type, TypeVar

from valid8 import validate
from valid8.validation_lib import on_all_

from optool.logging import LOGGER

T = TypeVar("T")


class TypeCheckedList(Generic[T]):

    def _validate_elements(self, *args: T):
        validate("The elements to hold", args, custom=on_all_(lambda x: isinstance(x, self._type)))

    @classmethod
    def of(cls, *args: T):
        arg_type = type(args[0])
        validate("The elements to hold", args, custom=on_all_(lambda x: isinstance(x, arg_type)))
        obj = cls(arg_type)
        obj._data.extend(args)
        return obj

    def __init__(self, holds: Type[T]):
        validate("The type of the elements to hold", holds, custom=isclass)
        self._type = holds
        self._data: List[T] = []
        LOGGER.debug("Creating a {} for holding elements of type {}.", self.__class__.__name__, self._type)

    def append(self, element: T) -> None:
        """
        Append an element to the end of the list.
        """
        self._validate_elements(element)
        self._data.append(element)

    def extend(self, iterable) -> None:
        """
        Append a series of elements to the end of the list.
        """
        for element in iterable:
            self.append(element)

    def clear(self):
        """
        Remove all items from list.
        """
        self._data.clear()

    def __iter__(self):
        yield from self._data

    def __len__(self):
        return self._data.__len__()

    def __getitem__(self, i):
        return self._data.__getitem__(i)

    def __setitem__(self, i, element):
        self._validate_elements(element)
        self._data[i] = element

    def __str__(self):
        return f"{self.__class__.__name__}({self._type.__name__}):{self._data}"

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
