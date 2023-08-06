import inspect
from abc import ABC, abstractmethod
from enum import Enum
from types import FunctionType
from typing import get_args

from pyfields import make_init
from valid8 import ValidationFailure, validate
from valid8.validation_lib import non_empty

from optool.autocode import Attribute, autocomplete
from optool.containers.horizon import Horizon
from optool.containers.values import ValueWrapper
from optool.logging import LOGGER
from optool.math import is_symbolic, iscolumn, num_elements
from optool.optimization.constraints import OptimizationConstraint
from optool.optimization.problem import OptimizationProblem
from optool.types import SYMBOLIC_VARIABLES, UNITS


class NotAnOdeFunction(ValidationFailure, ValueError):
    """
    Custom ValidationFailure raised by :py:func:`~ode_function`.
    """
    help_msg = 'The value f={wrong_value} is either not a function or does not have two input arguments'


def ode_function(f):
    """
    Validates if a given function satisfies requirements to represent an `ode_function`.

    Raises a `NotAnOdeFunction` error in case of failure.
    """
    if not isinstance(f, FunctionType):
        raise NotAnOdeFunction(wrong_value=f)

    signature = inspect.signature(f)
    return len(signature.parameters) == 2


@autocomplete
class OrdinaryDifferentialEquation:

    def _check_consistency(self):
        num_state_variables = num_elements(self.state_variable)
        num_input_variables = num_elements(self.input_variable)

        state_units = ValueWrapper(self.state_variable).get_unit()
        input_units = ValueWrapper(self.input_variable).get_unit()
        expected_input_unit = UNITS.Hz if ValueWrapper(
            self.state_variable).is_dimensionless() else state_units / UNITS.second

        if not ValueWrapper(self.input_variable).is_compatible_with(expected_input_unit):
            raise ValueError(
                f"The input variable has units of {input_units}, which are not compatible with the units of "
                f"the state variable, i.e., '{state_units}' in order to formulate an ODE.")

        if num_state_variables != num_input_variables + 1:
            raise ValueError(f"The vector of state variables must have one element more than the vector of input "
                             f"variables, but have {num_state_variables=} and {num_input_variables=}.")

        try:
            time_derivative = self.function(self.state_variable[1:], self.input_variable)
        except Exception as e:
            raise ValueError(f"The given ODE function {self.name} failed with given state and input variables.") from e
        else:
            validate("Result of the ODE, i.e., time-derivative",
                     time_derivative,
                     instance_of=get_args(SYMBOLIC_VARIABLES),
                     custom=[is_symbolic, iscolumn])
            time_derivative_units = ValueWrapper(time_derivative).get_unit()
            num_time_derivative = num_elements(time_derivative)

            if not ValueWrapper(time_derivative).is_compatible_with(input_units):
                raise ValueError(
                    f"The time-derivative has units of {time_derivative_units}, which are not compatible with the "
                    f"units of the state and input variables, i.e., '{state_units}' and '{input_units}', respectively.")

            if num_time_derivative != num_input_variables:
                raise ValueError(
                    f"The vector of time-derivatives must have the same number of elements than the vector of "
                    f"input variables, but have {num_time_derivative=} and {num_input_variables=}.")

    __init__ = make_init(post_init_fun=_check_consistency)

    __slots__ = '_name', '_state_variable', '_input_variable', '_function'
    name: str = Attribute(read_only=True, validators=non_empty)
    """The name of the ordinary differential equation."""
    state_variable: SYMBOLIC_VARIABLES = Attribute(read_only=True, validators=[is_symbolic, iscolumn])
    input_variable: SYMBOLIC_VARIABLES = Attribute(read_only=True, validators=[is_symbolic, iscolumn])
    function: FunctionType = Attribute(read_only=True, validators=ode_function)


class BaseIntegrationMethod(ABC):

    @classmethod
    @abstractmethod
    def integrate(cls, prb: OptimizationProblem, ode: OrdinaryDifferentialEquation,
                  horizon: Horizon) -> OptimizationConstraint:
        raise NotImplementedError()


class ForwardEuler(BaseIntegrationMethod):

    @classmethod
    def integrate(cls, prb: OptimizationProblem, ode: OrdinaryDifferentialEquation,
                  horizon: Horizon) -> OptimizationConstraint:
        LOGGER.debug("Integrating {} with {}.", ode.name, cls.__name__)

        time_derivative = ode.function(ode.state_variable[1:], ode.input_variable)
        constraint = prb.add_equality_constraint(ode.state_variable[1:],
                                                 ode.state_variable[:-1] + horizon.time_intervals() * time_derivative)
        constraint.name = ode.name
        return constraint


class RungeKutta4(BaseIntegrationMethod):

    @classmethod
    def integrate(cls, prb: OptimizationProblem, ode: OrdinaryDifferentialEquation,
                  horizon: Horizon) -> OptimizationConstraint:
        LOGGER.debug("Integrating {} with {}.", ode.name, cls.__name__)
        time_steps = horizon.time_intervals()
        k1 = ode.function(ode.state_variable[1:], ode.input_variable)
        k2 = ode.function(ode.state_variable[1:] + time_steps / 2 * k1, ode.input_variable)
        k3 = ode.function(ode.state_variable[1:] + time_steps / 2 * k2, ode.input_variable)
        k4 = ode.function(ode.state_variable[1:] + time_steps * k3, ode.input_variable)
        next_state = ode.state_variable[1:] + time_steps / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

        constraint = prb.add_equality_constraint(ode.state_variable[1:], next_state)
        constraint.name = ode.name
        return constraint


class IntegrationMethod(Enum):
    FORWARD_EULER = ForwardEuler

    RUNGE_KUTTA_4 = RungeKutta4

    def __init__(self, value: BaseIntegrationMethod):
        validate("The Enum value", value, instance_of=type, subclass_of=BaseIntegrationMethod)

    def integrate(self, prb: OptimizationProblem, ode: OrdinaryDifferentialEquation,
                  horizon: Horizon) -> OptimizationConstraint:
        validate("The integration method", self, instance_of=IntegrationMethod)
        validate("The integration method", self.value, subclass_of=BaseIntegrationMethod)
        return self.value.integrate(prb, ode, horizon)
