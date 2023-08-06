from __future__ import annotations

from typing import Any, Callable, Union, get_args

import numpy as np
from mini_lambda.main import LambdaExpression
from valid8 import validate
from valid8.validation_lib import on_all_

from optool.logging import LOGGER
from optool.math import Direction, is_monotonic, is_value_satisfying, isscalar
from optool.types import NUMERIC_TYPES, Quantity


def is_for_arrays(the_callable: Callable[[NUMERIC_TYPES], Any]) -> bool:
    """
    Identifies if the provided callable can be applied to numpy arrays.
    """
    validate("A callable", the_callable, custom=callable)
    test_value = np.ones((3, 0))
    try:
        the_callable(test_value)
        return True
    except TypeError as e:
        expected_msg = "only size-1 arrays can be converted to Python scalars"
        if str(e) != expected_msg:
            LOGGER.warning("Expected {!r}, but got error message {!r} of {}.", expected_msg, str(e),
                           e.__class__.__name__)
        return False


def _get_name(arg: Callable) -> str:
    return arg.to_string() if isinstance(arg, LambdaExpression) else arg.__name__


def _evaluate(arg: Callable[[NUMERIC_TYPES], Union[bool, np.ndarray]], value: Any) -> Union[bool, np.ndarray]:
    return arg.evaluate(value) if isinstance(arg, LambdaExpression) else arg(value)  # type: ignore[attr-defined]


def all_(*args: Callable) -> Callable[[NUMERIC_TYPES], bool]:
    """
    Get a validator which performs numeric validation for all elements of an array.
    """
    validate("Array of callables", args, custom=on_all_([callable, is_for_arrays]))
    func_names = [_get_name(arg) for arg in args]

    def validate_all_elements(value):
        validate("A numeric value", value, instance_of=get_args(NUMERIC_TYPES))
        result = [np.all(_evaluate(arg, value)) for arg in args]
        if isscalar(value):
            LOGGER.debug("A scalar value {} is validated against {}, yielding {}.", value, func_names, result)
        else:
            LOGGER.debug("An array of shape {} is validated against {}, yielding {}.", np.shape(value),
                         [f"all({element})" for element in func_names], result)
        return all(result)

    return validate_all_elements


def criterion(expression: str) -> Callable[[Quantity], bool]:
    return lambda x: is_value_satisfying(x, expression)


def monotonicity(direction: Direction, strict: bool):
    return lambda x: is_monotonic(x, direction, strict)
