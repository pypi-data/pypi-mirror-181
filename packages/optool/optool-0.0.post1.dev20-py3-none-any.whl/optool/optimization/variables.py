import math
from abc import ABC, abstractmethod
from typing import Optional, Union, get_args

import casadi
import numpy as np
from pint import Quantity, Unit
from pyfields import init_fields
from valid8 import validate
from valid8.validation_lib import non_empty

from optool.autocode import ArrayMutability, Attribute
from optool.containers.values import ValueWrapper
from optool.logging import LOGGER
from optool.math import has_offset, isarray, isnonnan, isnonzero, isscalar
from optool.types import NUMERIC_TYPES, OPTI_SYMBOLS, SYMBOLIC_VARIABLES
from optool.validation import all_


class OptimizationVariable(ABC):
    """
    Set of decision variables for an NLP formulation.

    This handle class allows to define a set of decision variables which is then used for an NLP formulation.

    The set of decision variables may be scalar or a vector.
    """

    def _check_consistency(self, field, val: NUMERIC_TYPES):
        description = f"the {field.name} of {self.name}"
        validate(f"A numeric value for {description}", val, instance_of=get_args(NUMERIC_TYPES))

        self._check_dimensions(val, description)
        self._check_unit(val, description)

    def _check_dimensions(self, val: NUMERIC_TYPES, description: str):
        try:
            var_size = self.length()
        except AttributeError:
            return  # Cannot check yet, since has class not been initialized completely

        if isscalar(val) or (isarray(val) and np.shape(val)[0] == var_size):  # type: ignore
            return
        shape = np.shape(val)  # type: ignore
        LOGGER.error("Provided neither a scalar nor an array but something of shape {}.", shape)
        raise ValueError(f"The value for {description} should be a scalar or an array of length {var_size}, "
                         f"but has shape {shape}.")

    def _check_unit(self, val: NUMERIC_TYPES, description: str):
        try:
            var_unit = self.unit
        except AttributeError:
            return  # Cannot check yet, since has class not been initialized completely

        if ValueWrapper(val).is_compatible_with(var_unit):
            return
        LOGGER.error("Provided {}, a value which is not compatible with {!r}.", val, var_unit)
        raise ValueError(f"The value for {description} should be a quantity compatible to '{var_unit}'.")

    # noinspection PyUnusedLocal
    def _check_frozen(self, field, val):
        if hasattr(self, "_frozen_nominal_values") and self._frozen_nominal_values:
            raise ValueError("Cannot change nominal value after retrieving the regular variable.")

    __slots__ = '_name', '_unit', '_initial_guess', '_lower_bounds', '_upper_bounds', '_nominal_values', '_solution', \
                '_lagrange_multipliers', '_frozen_nominal_values'

    name: str = Attribute(validators=non_empty)
    """The name of the decision variable."""

    unit: Optional[Unit] = Attribute(validators=lambda x: not has_offset(x))
    """The physical unit_of_scaling_variable of the decision variable."""

    initial_guess: NUMERIC_TYPES = Attribute(validators=[all_(np.isfinite), _check_consistency],
                                             array_mutability=ArrayMutability.MAYBE_LATER)
    """The initial values to provide to the solver."""

    lower_bounds: NUMERIC_TYPES = Attribute(validators=[all_(isnonnan), _check_consistency],
                                            array_mutability=ArrayMutability.MAYBE_LATER)
    """The minimum values allowed for the decision variable."""

    upper_bounds: NUMERIC_TYPES = Attribute(validators=[all_(isnonnan), _check_consistency],
                                            array_mutability=ArrayMutability.MAYBE_LATER)
    """The maximum values allowed for the decision variable."""

    nominal_values: NUMERIC_TYPES = Attribute(
        validators=[all_(np.isfinite, isnonzero), _check_consistency, _check_frozen],
        array_mutability=ArrayMutability.MAYBE_LATER)
    """The nominal values for scaling the variables."""

    solution: NUMERIC_TYPES = Attribute(default=None,
                                        validators=_check_consistency,
                                        array_mutability=ArrayMutability.NEVER)
    """The solution obtained after solving the NLP."""

    lagrange_multipliers: NUMERIC_TYPES = Attribute(default=None,
                                                    validators=_check_consistency,
                                                    array_mutability=ArrayMutability.NEVER)
    """The lagrange multipliers obtained after solving the NLP."""

    @init_fields
    def __init__(self):
        self._frozen_nominal_values = False

    @abstractmethod
    def length(self) -> int:
        """
        Gets the number of symbols.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def normed(self) -> OPTI_SYMBOLS:
        raise NotImplementedError()

    @property
    @abstractmethod
    def regular(self) -> SYMBOLIC_VARIABLES:
        raise NotImplementedError()

    def _freeze_nominal_values(self):
        LOGGER.debug("Freezing nominal values.")
        self._frozen_nominal_values = True

    @staticmethod
    def casadi(name: str, n: int, unit: Optional[Unit] = None, mutable_arrays: bool = False):
        return CasadiVariable(name, n, unit, mutable_arrays)


class CasadiVariable(OptimizationVariable):
    """
    Representation of a decision variable using the modeling language CasADi.
    """

    __slots__ = '_symbols'

    def __init__(self, name: str, n: int, unit: Optional[Unit] = None, mutable_arrays: bool = False):
        super().__init__(name=name,
                         unit=unit,
                         initial_guess=ValueWrapper(0.0).make_quantity_if_necessary(unit),
                         lower_bounds=ValueWrapper(-math.inf).make_quantity_if_necessary(unit),
                         upper_bounds=ValueWrapper(math.inf).make_quantity_if_necessary(unit),
                         nominal_values=ValueWrapper(1.0).make_quantity_if_necessary(unit))
        self._symbols = casadi.SX.sym(self.name, n, 1)
        Attribute.set_arrays_mutability_where_possible(self, mutable_arrays)

    @property
    def normed(self) -> casadi.SX:
        return self._symbols

    @property
    def regular(self) -> Union[casadi.SX, Quantity]:
        self._freeze_nominal_values()
        return self._symbols * self.nominal_values

    def length(self) -> int:
        return self._symbols.numel()
