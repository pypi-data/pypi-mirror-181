from __future__ import annotations

from typing import Optional, Union

import numpy as np
from pint import Unit
from pint.util import to_units_container
from pint_pandas import PintArray, PintType
from valid8 import validate

from optool.types import UNITS, Quantity


class QuantitySeries(PintArray):
    """
    Pandas dataframe array that allows to store quantities.

    The implementation is based on PintArray, which, however, cannot be pickled.
    """

    def __init__(self,
                 value: Union[np.ndarray, Quantity],
                 unit: Optional[Union[Unit, PintType]] = None,
                 copy: bool = True):
        if unit is None:
            validate("Value", value, instance_of=Quantity)
            unit = value.units  # type:ignore # we know that it is a Quantity here
            value = value.magnitude  # type: ignore # we know that it is a Quantity here
        else:
            validate("Value", value, instance_of=np.ndarray)
            validate("Unit", unit, instance_of=(Unit, PintType))

        super().__init__(value, unit, copy=copy)

    def copy(self, deep: bool = True) -> QuantitySeries:
        return self.__class__(self.data.copy(), self.units, copy=deep)

    @classmethod
    def _from_pickle(cls, magnitude, unit_as_dict):
        unit = UNITS.Unit(UNITS.UnitsContainer(unit_as_dict))
        return cls(magnitude, unit)

    def __reduce__(self):
        unit_as_dict = dict(to_units_container(self.quantity.u))
        return self.__class__._from_pickle, (self.quantity.m, unit_as_dict)
