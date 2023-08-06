from __future__ import annotations

from numbers import Number
from typing import Optional, Union, get_args

import numpy as np
from pint import Unit
from valid8 import validate
from valid8.validation_lib import non_empty

from optool.autocode import Attribute, autocomplete
from optool.math import is_compatible, is_dimensionless, isscalar
from optool.types import DIMENSIONLESS_TYPES, NUMERIC_TYPES, OPTI_SYMBOLS, UNITS, Quantity

_MAYBE_AS_QUANTITY = Union[NUMERIC_TYPES, OPTI_SYMBOLS]
_SURELY_WITHOUT_UNIT = Union[DIMENSIONLESS_TYPES, OPTI_SYMBOLS]


@autocomplete
class ValueWrapper:
    """
    A wrapper for any numeric value either with or without physical units.
    """

    __slots__ = '_value'

    value: _MAYBE_AS_QUANTITY = Attribute(read_only=True)

    def is_compatible_with(self, unit: Optional[Unit]) -> bool:
        return is_compatible(self.value, unit)

    def is_dimensionless(self) -> bool:
        return is_compatible(self.value, UNITS.parse_units(""))

    def make_quantity_if_necessary(self, unit: Optional[Unit]) -> _MAYBE_AS_QUANTITY:
        return self.value if unit is None else Quantity(self.value, unit)

    def make_dimensionless(self) -> _SURELY_WITHOUT_UNIT:
        return self.value.m_as(UNITS.dimensionless) if isinstance(self.value, Quantity) else self.value

    def get_magnitude(self) -> _SURELY_WITHOUT_UNIT:
        return self.value.magnitude if isinstance(self.value, Quantity) else self.value

    def get_magnitude_as(self, unit: Optional[Unit]) -> _SURELY_WITHOUT_UNIT:
        if not self.is_compatible_with(unit):
            raise ValueError(f"The wrapped value '{self.value}' is not compatible with '{unit}'.")
        if unit is None or is_dimensionless(unit):
            return self.make_dimensionless()
        if isinstance(self.value, Quantity):
            return self.value.m_as(unit)
        return self.value

    def get_unit(self) -> Optional[Unit]:
        return self.value.units if isinstance(self.value, Quantity) else None

    def inflate(self, n: int) -> NUMERIC_TYPES:
        """
        Inflate the value stored in the wrapper.

        Args:
            n: The number of elements

        Returns: A new array with the specified number of elements if the value was a scalar before. Otherwise, verifies
        the dimension and returns the internal value (without copying)
        """
        validate("The value", self.value, instance_of=get_args(NUMERIC_TYPES))
        if isscalar(self.value):
            if isinstance(self.value, Quantity):
                return Quantity(np.repeat(self.value.magnitude, n), self.value.units)
            return np.repeat(self.value, n)  # type: ignore
        validate("The value", self.value, length=n)
        return self.value


@autocomplete
class ValueRange:
    """
    Ranges of the normed values of the optimization variables.
    """

    __slots__ = '_name', '_min', '_avg', '_max', '_max_abs'

    name: str = Attribute(read_only=True, validators=non_empty)
    """The name of the decision variable."""

    min: Number = Attribute(read_only=True)
    avg: Number = Attribute(read_only=True)
    max: Number = Attribute(read_only=True)
    max_abs: Number = Attribute(read_only=True)

    @classmethod
    def of(cls, name: str, val: np.ndarray):
        """

        Args:
            name (str): The name of the decision variable.
            val (numpy.ndarray): The normed values as array.
        """
        return cls(name, min=np.min(val), avg=np.mean(val), max=np.max(val), max_abs=np.max(np.abs(val)))  # type:ignore
