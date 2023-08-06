from enum import Enum
from numbers import Number
from typing import Union

import casadi
import numpy as np
import pint
import pint_pandas

UNITS = pint.get_application_registry()  # See for why this is a good idea https://stackoverflow.com/a/68089489
UNITS.define('square_meter = meter**2 = m² = m2')

# Exchange rates as of May 10, 2022, 3:48 p.m., taken from https://finance.yahoo.com/currency-converter/
UNITS.define('USD = [currency] = $ = usd')
UNITS.define('CHF = USD / 0.9918 = _ = chf')
UNITS.define('EUR = USD / 0.9484 = € = eur')

UNITS.setup_matplotlib(True)
Quantity = UNITS.Quantity  # Should use this registry, see https://github.com/hgrecco/pint/issues/1480
pint_pandas.PintType.ureg = UNITS

SCALAR_TYPES = Union[float, int]  #: Scalar values
CASADI_SYMBOLS = Union[casadi.SX]  #: Symbols used by CasADi
OPTI_SYMBOLS = Union[CASADI_SYMBOLS]  #: Symbols used by the supported modeling languages
SYMBOLIC_VARIABLES = Union[OPTI_SYMBOLS,
                           Quantity]  # type:ignore  #: Symbolic variables, might be wrapped in quantity objects
DIMENSIONLESS_TYPES = Union[Number, np.ndarray]  #: Numbers without units of measurement
NUMERIC_TYPES = Union[Number, np.ndarray, Quantity]  # type:ignore #: Numbers with or without units of measurement


class RobustEnum(Enum):
    """
    This enum class ensures that the values are equal to the names of the enums.
    """

    def __repr__(self):
        return f'<{self.__class__.__name__}.{self.name}>'

    def _prevent_duplicates(self, cls):
        if any(self.value == e.value for e in cls):
            raise ValueError(f"Duplicate values found in enum {cls.__name__!r}: {self.name} -> {cls(self.value).name}.")

    def __reduce_ex__(self, proto):
        if proto < 4:
            return getattr, (self.__class__, self._name_)
        return self.__class__.__qualname__ + '.' + self._name_
