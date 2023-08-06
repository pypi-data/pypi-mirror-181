from typing import Tuple

from optool.optimization.problem import OptimizationProblem
from optool.types import Quantity


class ProblemSolution:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, name: str) -> Quantity:  # Tells MyPy that this attribute exists
        return self.__dict__[name]

    def __reduce__(self):
        """
        Helper for pickle.

        This function is necessary to pickle objects of this class since it does not exactly follow the Python
        standards.
        """
        return self._from_tuples, tuple(self.__dict__.items())

    @classmethod
    def _from_tuples(cls, *tuples: Tuple[str, Quantity]):
        return cls(**dict(tuples))

    @classmethod
    def from_problem(cls, prb: OptimizationProblem):
        return cls(**{var.name: var.solution for var in prb.variables})
