from datetime import timedelta
from typing import Dict, Union

import pandas as pd
from matplotlib import pyplot as plt
from valid8.validation_lib import non_empty

from optool import orthography
from optool.autocode import Attribute, autocomplete
from optool.containers.generics import TypeCheckedList
from optool.containers.values import ValueRange
from optool.io.graphics import make_interactive
from optool.math import isnumeric, isscalar
from optool.types import Quantity


@autocomplete
class DebugInfo:
    """
    Container for debug information related to the solving of an optimization problem.
    """

    __slots__ = '_problem_name', '_normed_variable_values', '_normed_constraints_lagrange_multipliers'

    problem_name: str = Attribute(read_only=True, validators=non_empty)
    """The name of the optimization problem."""

    normed_variable_values: TypeCheckedList[ValueRange] = Attribute(default=TypeCheckedList(ValueRange))
    normed_constraints_lagrange_multipliers: TypeCheckedList[ValueRange] = Attribute(
        default=TypeCheckedList(ValueRange))

    def get_details(self) -> list[str]:
        prefix = "|   "
        separator = f"{prefix}{'-' * 60}"
        details = [
            f"Debug information for the optimization problem entitled '{self.problem_name}'",
            f"{prefix}Normed values of the decision variables (as seen by the solver):", separator
        ]

        self._append_normed_values(details, prefix, self.normed_variable_values)
        details.extend((separator, f"{prefix}Normed values of the lagrange multipliers of the constraints "
                        f"(as seen by the solver):"))

        self._append_normed_values(details, prefix, self.normed_constraints_lagrange_multipliers)
        details.append(separator)
        return details

    @staticmethod
    def _append_normed_values(details: list[str], prefix: str, normed_values: TypeCheckedList[ValueRange]) -> None:
        attributes_to_show = ["min", "avg", "max", "max_abs"]
        df = pd.DataFrame(index=attributes_to_show)
        for val in normed_values:
            df[f"{val.name}:  "] = [getattr(val, attr) for attr in attributes_to_show]
        table_rows = df.transpose().to_string().split("\n")
        details.extend(f"{prefix}{row}" for row in table_rows)


class UnsuccessfulOptimization(Exception):
    """
    Exception that should be raised if an optimization was not successful.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


@autocomplete
class SolverResponse:
    """
    The response returned by the solver.
    """

    __slots__ = '_problem_name', '_function_value', '_success', '_solver_status', '_debug_info'

    problem_name: str = Attribute(read_only=True)
    """The name of the optimization problem."""

    function_value: Union[float, Quantity] = Attribute(read_only=True, validators=[isscalar, isnumeric])
    success: bool = Attribute(read_only=True)
    solver_status: Dict = Attribute(read_only=True)
    debug_info: DebugInfo = Attribute(read_only=True)

    def get_return_status(self) -> str:
        return self.solver_status["return_status"]

    def get_number_of_iterations(self) -> int:
        return int(self.solver_status["iter_count"])

    def get_solver_time(self) -> timedelta:
        # See https://groups.google.com/g/casadi-users/c/dMSGV8KII30?pli=1 for an explanation of both
        # 't_wall_total' and 't_proc_total' and the difference between them.
        return timedelta(seconds=self.solver_status["t_wall_total"])

    def guarantee_success(self):
        if not self.success:
            raise UnsuccessfulOptimization(f"The problem entitled '{self.problem_name}' was not solved successfully, "
                                           f"but returned with '{self.get_return_status()}'.")

    def get_message(self):
        success_msg = "" if self.success else "NOT "
        duration_str = orthography.naturaldelta(self.get_solver_time(), minimum_unit="microseconds")
        return f"The optimization problem {self.problem_name!r} was {success_msg}solved successfully " \
               f"after {self.get_number_of_iterations()} iterations and {duration_str} " \
               f"with return status {self.get_return_status()!r}."

    def plot_convergence(self):

        fig, ax = plt.subplots(4, sharex="col")
        fig.suptitle(f"Convergence of {self.problem_name}")
        ax[-1].set(xlabel="Iteration number")

        ax[0].plot(self.solver_status["iterations"]["obj"], label='objective')

        ax[1].semilogy(self.solver_status["iterations"]["inf_pr"], label='Primal infeasibility')
        ax[1].semilogy(self.solver_status["iterations"]["inf_du"], label='Dual infeasibility')

        ax[2].semilogy(self.solver_status["iterations"]["mu"], label='Barrier mu')

        ax[3].semilogy(self.solver_status["iterations"]["alpha_pr"], label='Primal step size')
        ax[3].semilogy(self.solver_status["iterations"]["alpha_du"], label='Dual step size')

        for axis in ax:
            make_interactive(axis.legend())


@autocomplete
class IpoptOption:
    """
    The options available in Ipopt.

    See Also: `Ipopt documentation <https://coin-or.github.io/Ipopt/OPTIONS.html#OPT_print_options_documentation>`_
    """

    __slots__ = '_category', '_name', '_values', '_description'

    category: str = Attribute(read_only=True)
    """The category of the option."""

    name: str = Attribute(read_only=True)
    """The name of the option."""

    values: str = Attribute(read_only=True)
    """The possible values to set."""

    description: str = Attribute(read_only=True)
    """The description of the option."""

    def pretty_print(self):
        print(f"{self.name}: ({self.category})\t{self.values}:\n{self.description}")
