import math
from abc import ABC
from typing import Optional, Union

import numpy as np
from pint import Quantity, Unit
from pyfields import make_init

from optool.autocode import Attribute, autocomplete
from optool.containers.values import ValueWrapper
from optool.math import is_symbolic, isscalar
from optool.types import DIMENSIONLESS_TYPES, NUMERIC_TYPES, OPTI_SYMBOLS, SCALAR_TYPES


# noinspection PyArgumentList
class OptimizationConstraint(ABC):
    """
    Constraint for an NLP formulation.

    This handle class allows to define a set of constraints which is then used for an NLP formulation.

    The set of constraints may be scalar or a vector.
    """

    __slots__ = '_name', '_nominal_value', '_lagrange_multipliers'

    name: str = Attribute(default="")
    """The name of the constraint."""

    nominal_value: SCALAR_TYPES = Attribute(read_only=True, validators=[math.isfinite, lambda x: x > 0])
    """The nominal value for scaling the constraint."""

    lagrange_multipliers: NUMERIC_TYPES = Attribute(default=None)
    """The lagrange multipliers obtained after solving the NLP."""


@autocomplete(make_eq=False)
class ExpressionConstraint(OptimizationConstraint):
    """
    Directly creates a constraint object from a CasADi or Yalmip expression.

    Note:
        Can specify a scalar nominal value as the last argument, if the constraint expression has been normalized BY THE
        CALLER. No internal normalization takes place in this method!

    Attribute:
        name: The name of the constraint.
        nominal_value: The nominal value for scaling the constraint. (Default: 1.0)
        expression: The constraint.
    """

    __slots__ = '_expression'

    expression: OPTI_SYMBOLS = Attribute(read_only=True)
    """The expression of the constraint."""


@autocomplete(make_eq=False)
class IntervalConstraint(OptimizationConstraint):
    """
    Creates an interval constraint.

    Attribute:
        name: The name of the constraint.
        nominal_value: The nominal value for scaling the constraint. (Default: 1.0)
        lower_bound: The smallest values the expression should be able to take.
        expression: The expression that formulates the constraint.
        upper_bound: The greatest values the expression should be able to take.
    """

    def _check_consistency(self):
        self._check_value(self.lower_bound, "lower bound")
        self._check_value(self.upper_bound, "upper bound")

    def _check_value(self, value, description):
        if value is None:
            return
        if not ValueWrapper(value).is_compatible_with(self.get_unit()):
            raise ValueError(f"The {description} '{value}' is not compatible with '{self.get_unit()}'.")
        if not (isscalar(value) or (np.ndim(value) == 1 and np.shape(value)[0] == self.length())):
            raise ValueError(
                f"The {description} should be None, a scalar, or a one-dimensional array of length {self.length()}, "
                f"but has shape {np.shape(value)}.")

    __init__ = make_init(post_init_fun=_check_consistency)
    __slots__ = '_lower_bound', '_expression', '_upper_bound'

    lower_bound: Optional[NUMERIC_TYPES] = Attribute(read_only=True)
    """The expression of the constraint."""

    expression: Union[OPTI_SYMBOLS, Quantity] = Attribute(read_only=True, validators=is_symbolic)
    """The expression of the constraint."""

    upper_bound: Optional[NUMERIC_TYPES] = Attribute(read_only=True)
    """The expression of the constraint."""

    def get_symbols(self) -> OPTI_SYMBOLS:
        return ValueWrapper(self.expression).get_magnitude()

    def get_dimensionless_lower_bound(self) -> DIMENSIONLESS_TYPES:
        if self.lower_bound is None:
            return -math.inf  # type: ignore
        return ValueWrapper(self.lower_bound).get_magnitude_as(self.get_unit())

    def get_dimensionless_upper_bound(self) -> DIMENSIONLESS_TYPES:
        if self.upper_bound is None:
            return math.inf  # type: ignore
        return ValueWrapper(self.upper_bound).get_magnitude_as(self.get_unit())

    def get_unit(self) -> Optional[Unit]:
        return ValueWrapper(self.expression).get_unit()

    def length(self):
        return self.get_symbols().numel()
