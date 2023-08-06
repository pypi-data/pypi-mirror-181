import io
import re
from abc import ABC, abstractmethod
from contextlib import redirect_stdout
from typing import Any, Dict, Iterable, List, Optional, Tuple, Type, TypeVar, Union, get_args

import casadi
import numpy as np
from pint import Unit
from pyfields import init_fields, make_init
from valid8 import validate
from valid8.validation_lib import on_all_

from optool.autocode import Attribute
from optool.containers.generics import TypeCheckedList
from optool.containers.values import ValueRange, ValueWrapper
from optool.logging import LOGGER
from optool.math import is_symbolic, isarray, isvector, num_elements
from optool.optimization.constraints import ExpressionConstraint, IntervalConstraint, OptimizationConstraint
from optool.optimization.helpers import DebugInfo, IpoptOption, SolverResponse
from optool.optimization.variables import CasadiVariable, OptimizationVariable
from optool.types import NUMERIC_TYPES, OPTI_SYMBOLS, SCALAR_TYPES, Quantity

T = TypeVar("T", bound=OptimizationConstraint)


def _find_element(name: str, elements: TypeCheckedList[Any]) -> Optional[int]:
    """
    Finds the index at which the element with the specified name is located in the specified list of elements.

    Args:
        name (str): The name of the variable or constraint.
        elements (TypeCheckedList): The list of elements to search.

    Returns:
        The index at which the element is located, or `None` if the element is not present in the list.
    """

    validate("The elements", elements, instance_of=Iterable, custom=on_all_(lambda x: hasattr(x, "name")))
    index = [i for i, element in enumerate(elements) if name == element.name]
    if not index:
        return None
    if len(index) == 1:
        return index[0]

    if isinstance(elements[0], OptimizationVariable):
        element_type = "variable"
    elif isinstance(elements[0], OptimizationConstraint):
        element_type = "constraint"
    else:
        element_type = elements[0].__class__.__name__
    raise ValueError(f"There should be at most one {element_type} entitled '{name}', but found {len(index)}.")


def _get_dummy_solver(formulation, inputs):
    if formulation == "NLP":
        return casadi.nlpsol(*inputs)
    elif formulation == "QP":
        return casadi.qpsol(*inputs)
    else:
        raise ValueError(f"Unknown type '{formulation}'. Use either 'NLP' or 'QP'.")


class ProblemElements:
    __init__ = make_init()
    __slots__ = '_variables', '_constraints'

    variables: TypeCheckedList[OptimizationVariable] = Attribute(default=TypeCheckedList(OptimizationVariable))
    """A list of variables of the optimization problem."""

    constraints: TypeCheckedList[OptimizationConstraint] = Attribute(default=TypeCheckedList(OptimizationConstraint))
    """A list of constraints of the optimization problem."""

    def has_variable(self, name: str) -> bool:
        return _find_element(name, self.variables) is not None

    def get_variable(self, name: str) -> OptimizationVariable:
        index = _find_element(name, self.variables)
        if index is None:
            raise ValueError(f"The variable {name!r} is not present. Here is a list of all available variables:"
                             f"\n{[var.name for var in self.variables]}")
        return self.variables[index]

    def has_constraint(self, name: str) -> bool:
        return _find_element(name, self.constraints) is not None

    def get_constraint(self, name: str) -> OptimizationConstraint:
        index = _find_element(name, self.constraints)
        if index is None:
            raise ValueError(f"The constraint {name!r} is not present. Here is a list of all available constraints:"
                             f"\n{[var.name for var in self.constraints]}")
        return self.constraints[index]


class OptimizationProblem(ProblemElements, ABC):  # Abstract base class
    """
    Define and solve an optimization program.

    Convenient interface to define and solve an optimization problem without the need for cumbersome notation.
    """
    __slots__ = '_name', '_objective'

    name: str = Attribute(default="")
    """The name of the optimization problem."""

    objective: Union[OPTI_SYMBOLS, Quantity]  # is abstract
    """The objective to minimize."""

    @abstractmethod
    def parse(self, solver: str, options: Dict[str, Any]) -> None:
        """
        Parses the problem as specified such that it can be solved afterwards.

        Args:
            solver: A solver specified as string, e.g., `ipopt`
            options: A Dictionary of options

        Example::

        >>> obj.parse('ipopt')
        """
        raise NotImplementedError()

    @abstractmethod
    def solve(self) -> SolverResponse:
        """
        Solves the formulated optimization problem.

        Solves the optimization problem and writes the results into the solution fields of the optimization variables.

        Example::

        >>> status = obj.solve()
        """
        raise NotImplementedError()

    @abstractmethod
    def get_parser_options(self, type: str = "NLP", solver: str = "ipopt") -> Dict[str, Tuple[str, str]]:
        raise NotImplementedError()

    @abstractmethod
    def get_solver_options(self, formulation: str = "NLP", solver: str = "ipopt") -> TypeCheckedList[IpoptOption]:
        raise NotImplementedError()

    @abstractmethod
    def new_variable(self, name: str, n: int, unit: Optional[Unit] = None) -> OptimizationVariable:
        raise NotImplementedError()

    @abstractmethod
    def add_equality_constraint(self, lhs, rhs, nominal_value=None) -> OptimizationConstraint:
        raise NotImplementedError()

    @abstractmethod
    def add_interval_constraint(self,
                                lower_bound,
                                expression,
                                upper_bound,
                                nominal_value=None) -> OptimizationConstraint:
        raise NotImplementedError()

    @abstractmethod
    def add_greater_than_constraint(self, lower_bound, expression, nominal_value=None) -> OptimizationConstraint:
        raise NotImplementedError()

    @abstractmethod
    def add_less_than_constraint(self, expression, upper_bound, nominal_value=None) -> OptimizationConstraint:
        raise NotImplementedError()

    @staticmethod
    def casadi(name=""):
        return CasadiProblem(name)


# noinspection PyArgumentList
def robust_divide_units(numerator: Optional[Unit], denominator: Optional[Unit]) -> Optional[Unit]:
    if numerator is None and denominator is None:
        return None
    elif numerator is None:
        return 1 / denominator  # type: ignore
    elif denominator is None:
        return numerator
    return numerator / denominator


class CasadiProblem(OptimizationProblem):
    """
    Representation of an optimization problem using the modeling language CasADi.
    """

    __slots__ = '_solver'

    objective: Union[casadi.SX, Quantity] = Attribute(default=None, validators=is_symbolic)

    @init_fields(OptimizationProblem.name)
    def __init__(self):
        self._solver = None

    def parse(self, solver: str, options=None) -> None:
        if options is None:
            options = {}
        if self._solver is not None:
            raise ValueError("The problem has already been parsed.")
        self._check_constraint_types()

        LOGGER.info("Parsing the problem entitled {!r}", self.name)

        if unnamed_constraints := [val for val in self._get_constraints(OptimizationConstraint) if val.name == ""]:
            LOGGER.debug("There are {} unnamed constraints that are automatically named now.", len(unnamed_constraints))
            for i, val in enumerate(unnamed_constraints):
                val.name = f"(unnamed constraint {i})"

        g_constraints = self._get_constraints(IntervalConstraint)
        h_constraints = self._get_constraints(ExpressionConstraint)

        LOGGER.debug("Assembling {} variables with following names and sizes: {}.", len(self.variables),
                     [(val.name, val.length()) for val in self.variables])
        LOGGER.debug("Assembling the following {} constraints: {}.", len(self.constraints),
                     [f"{val.__class__.__name__}({val.name})" for val in self.constraints])

        # Assemble problem definition
        problem = {
            'f': ValueWrapper(self.objective).get_magnitude(),
            'x': casadi.vertcat(*[val.normed for val in self.variables]),
            'g': casadi.vertcat(*[val.get_symbols() for val in g_constraints]),
            # 'h': casadi.diagcat(*h_constraints)
        }

        # problem.p = vertcat(optParameters.regularVariable);

        # Create solver object
        solver_type = casadi.qpsol if h_constraints else casadi.nlpsol
        self._solver = solver_type("solver", solver, problem, options)

        LOGGER.info("Finished parsing the problem {!r}.", self.name)

    def solve(self) -> SolverResponse:
        if not self._solver:
            ValueError(f"The problem entitled {self.name!r} needs to be parsed first.")
        self._check_constraint_types()

        # Assemble problem definition
        inputs = {
            "x0": self._get_normed_replicated_variable_values('initial_guess'),
            "lbx": self._get_normed_replicated_variable_values('lower_bounds'),
            "ubx": self._get_normed_replicated_variable_values('upper_bounds'),
            "lbg": self._get_normed_replicated_constraint_bounds("get_dimensionless_lower_bound"),
            "ubg": self._get_normed_replicated_constraint_bounds("get_dimensionless_upper_bound")
        }

        # Constraints
        # inputs["p"] = vertcat(optParameters.value)

        # Solve the NLP
        LOGGER.info("Solving the optimization problem entitled {!r}.", self.name)
        sol = self._solver(**inputs)
        status = self._solver.stats()
        debug_info = DebugInfo(self.name)
        LOGGER.debug("Solver return status: {}", status["return_status"])
        LOGGER.debug("Solver iteration count: {}", status["iter_count"])
        LOGGER.info("Solved optimization problem entitled '{}.", self.name)

        # Get Solution
        unit_of_objective = ValueWrapper(self.objective).get_unit()
        function_value = ValueWrapper(float(sol["f"].full())).make_quantity_if_necessary(unit_of_objective)

        # Variables
        end_split_indices = np.cumsum([val.length() for val in self.variables])
        normed_values = np.split(sol["x"].full().squeeze(), end_split_indices)
        # lagrange_multipliers = np.split(sol["lam_x"].full().squeeze(), end_split_indices)

        for i, val in enumerate(self.variables):
            val.solution = normed_values[i] * val.nominal_values
            # val.lagrange_multipliers = lagrange_multipliers[i]
            debug_info.normed_variable_values.append(ValueRange.of(val.name, normed_values[i]))

        # Interval constraints
        interval_constraints = self._get_constraints(IntervalConstraint)
        constraint_lengths = [val.length() for val in interval_constraints]
        end_split_indices = np.cumsum(constraint_lengths)
        lagrange_multipliers = np.split(sol["lam_g"].full().squeeze(), end_split_indices)

        for i, val in enumerate(interval_constraints):
            lagrange_multipliers_unit = robust_divide_units(unit_of_objective, val.get_unit())
            val.lagrange_multipliers = ValueWrapper(
                lagrange_multipliers[i] / val.nominal_value).make_quantity_if_necessary(lagrange_multipliers_unit)
            debug_info.normed_constraints_lagrange_multipliers.append(ValueRange.of(val.name, lagrange_multipliers[i]))

        # Parameters
        # end_split_indices = np.cumsum([val.length() for val in obj.parameters])
        # lagrange_multipliers = np.split(sol["lam_p"].full().squeeze(), end_split_indices)
        # for i, val in enumerate(obj.parameters):
        #     val.lagrange_multipliers = lagrange_multipliers[i]

        return SolverResponse(self.name, function_value, status["success"], status, debug_info)

    def _get_normed_replicated_constraint_bounds(self, method_name: str):
        interval_constraints = self._get_constraints(IntervalConstraint)
        values = [ValueWrapper(getattr(val, method_name)()).inflate(val.length()) for val in interval_constraints]
        return np.concatenate(values)  # type: ignore

    def _get_constraints(self, constraint_type: Type[T]) -> List[T]:
        return list(filter(lambda x: isinstance(x, constraint_type), self.constraints))

    def _check_constraint_types(self):
        supported_constraint_types = IntervalConstraint  # use (IntervalConstraint, ...) if multiple
        validate(f"Constraints of {self.__class__.__name__}",
                 self.constraints,
                 custom=on_all_(lambda x: isinstance(x, supported_constraint_types)))

    def _concat_and_replicate(self, field_name: str) -> np.ndarray:
        val_size_pairs = [(getattr(val, field_name), val.length()) for val in self.variables]
        values = [ValueWrapper(val).inflate(n) for (val, n) in val_size_pairs]
        return np.concatenate(values)  # type: ignore

    def _get_normed_replicated_variable_values(self, field_name: str) -> np.ndarray:
        val_nom_and_size = [(getattr(val, field_name), val.nominal_values, val.length()) for val in self.variables]
        normed_values = [
            ValueWrapper(val).inflate(n) / ValueWrapper(nom).inflate(n)  # type: ignore
            for (val, nom, n) in val_nom_and_size
        ]
        dimensionless_values = [ValueWrapper(val).make_dimensionless() for val in normed_values]
        return np.concatenate(dimensionless_values)  # type: ignore

    def new_variable(self, name: str, n: int, unit: Optional[Unit] = None) -> CasadiVariable:
        variable = OptimizationVariable.casadi(name, n, unit)
        self.variables.append(variable)
        return variable

    def add_equality_constraint(self, lhs, rhs, nominal_value: SCALAR_TYPES = 1.0) -> IntervalConstraint:
        accepted_types = get_args(Union[OPTI_SYMBOLS, NUMERIC_TYPES])
        validate("The left-hand side (lhs)", lhs, instance_of=accepted_types, custom=isvector)
        validate("The right-hand side (rhs)", rhs, instance_of=accepted_types, custom=isvector)
        if num_elements(lhs) != num_elements(rhs):
            raise ValueError(f"The number of values on the right-hand side and on the left-hand side must be equal, "
                             f"but have {num_elements(lhs)} and {num_elements(rhs)}, respectively.")

        difference = lhs - rhs
        zero = ValueWrapper(0.0).make_quantity_if_necessary(ValueWrapper(difference).get_unit())
        constraint = IntervalConstraint(nominal_value, zero, difference / nominal_value, zero)
        self.constraints.append(constraint)
        return constraint

    def add_interval_constraint(self,
                                lower_bound,
                                expression,
                                upper_bound,
                                nominal_value: SCALAR_TYPES = 1.0) -> IntervalConstraint:
        accepted_types_expression = get_args(Union[OPTI_SYMBOLS, NUMERIC_TYPES])
        validate("The lower bound", lower_bound, instance_of=get_args(NUMERIC_TYPES), custom=isarray)
        validate("The expression", expression, instance_of=accepted_types_expression, custom=isvector)
        validate("The upper bound", upper_bound, instance_of=get_args(NUMERIC_TYPES), custom=isarray)
        if len({num_elements(val) for val in [lower_bound, expression, upper_bound]}) != 1:
            raise ValueError(f"The number of values of the lower bound, the value, and the upper bound are not equal, "
                             f"but have {num_elements(lower_bound)}, {num_elements(expression)}, "
                             f"and {num_elements(upper_bound)}, respectively.")

        constraint = IntervalConstraint(nominal_value, lower_bound / nominal_value, expression / nominal_value,
                                        upper_bound / nominal_value)
        self.constraints.append(constraint)
        return constraint

    def add_greater_than_constraint(self,
                                    lower_bound,
                                    expression,
                                    nominal_value: SCALAR_TYPES = 1.0) -> IntervalConstraint:
        accepted_types = get_args(Union[OPTI_SYMBOLS, NUMERIC_TYPES])
        validate("The lower bound", lower_bound, instance_of=accepted_types, custom=isvector)
        validate("The expression", expression, instance_of=accepted_types, custom=isvector)

        if is_symbolic(lower_bound):
            expression = expression - lower_bound
            lower_bound = ValueWrapper(0.0).make_quantity_if_necessary(ValueWrapper(expression).get_unit())
        constraint = IntervalConstraint(nominal_value, lower_bound / nominal_value, expression / nominal_value, None)
        self.constraints.append(constraint)
        return constraint

    def add_less_than_constraint(self,
                                 expression,
                                 upper_bound,
                                 nominal_value: SCALAR_TYPES = 1.0) -> IntervalConstraint:
        accepted_types = get_args(Union[OPTI_SYMBOLS, NUMERIC_TYPES])
        validate("The expression", expression, instance_of=accepted_types, custom=isvector)
        validate("The upper bound", upper_bound, instance_of=accepted_types, custom=isvector)

        if is_symbolic(upper_bound):
            expression = expression - upper_bound
            upper_bound = ValueWrapper(0.0).make_quantity_if_necessary(ValueWrapper(expression).get_unit())
        constraint = IntervalConstraint(nominal_value, None, expression / nominal_value, upper_bound / nominal_value)
        self.constraints.append(constraint)
        return constraint

    # noinspection PyMethodMayBeStatic
    def get_parser_options(self, formulation: str = "NLP", solver: str = "ipopt") -> Dict[str, Tuple[str, str]]:
        inputs = ("solver", solver, {'x': casadi.SX.sym("", 1, 1)})
        dummy_solver = _get_dummy_solver(formulation, inputs)

        output = io.StringIO()
        with redirect_stdout(output):
            dummy_solver.print_options()
        option_details = output.getvalue().splitlines()[1:]

        options = {}
        for line in option_details:
            if len(line) > 0:
                var_type = re.findall(r"(?<=\[).*?(?=\])", line)[0]  # not greedy search
                [option_name, description] = line.split(var_type)
                option_name = re.findall(r"(?<=\").*(?=\")", option_name)[0]  # greedy search
                description = re.findall(r"(?<=\").*(?=\")", description)[0]  # greedy search
                options[option_name] = (var_type, description)

        return options

    # noinspection PyMethodMayBeStatic
    def get_solver_options(self, formulation: str = "NLP", solver: str = "ipopt") -> TypeCheckedList[IpoptOption]:
        if solver == "ipopt":
            solver_opts = {"ipopt.print_options_documentation": "yes"}
        else:
            raise ValueError(f"Unknown solver '{solver}'. Currently only 'ipopt' is supported.")

        inputs = ("solver", solver, {'x': casadi.SX.sym("", 1, 1)}, solver_opts)

        output = io.StringIO()
        with redirect_stdout(output):
            _get_dummy_solver(formulation, inputs)
        option_details = output.getvalue().splitlines()

        options = TypeCheckedList(IpoptOption)
        category = None
        option_name = None
        option_values = None
        description: List[str] = []
        for line in option_details:
            if len(line.strip()) == 0:
                continue
            elif line.startswith("###"):
                category = re.findall(r"(?<=### ).*(?= ###)", line)[0]
            elif not line.startswith(" "):
                option_header = re.findall(r"^\w+", line)
                if option_name is not None and option_name != option_header[0]:
                    options.append(IpoptOption(category, option_name, option_values, "\n".join(description)))
                option_name = option_header[0]
                option_values = line.replace(option_name, "").strip()
                description = []
            else:
                description.append(line)

        return options
