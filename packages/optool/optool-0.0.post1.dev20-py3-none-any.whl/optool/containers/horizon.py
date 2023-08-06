from datetime import datetime

import numpy as np
from pandas import DatetimeIndex
from valid8 import validate

from optool.autocode import ArrayMutability, Attribute, autocomplete
from optool.math import Direction, num_elements
from optool.serialization.decorator import serializable
from optool.time import convert_index_to_samples, convert_samples_to_index
from optool.types import Quantity
from optool.validation import criterion, monotonicity


@serializable
@autocomplete
class Horizon:
    __slots__ = '_start', '_sample_times'

    start: datetime = Attribute(read_only=True)
    sample_times: Quantity = Attribute(read_only=True,
                                       array_mutability=ArrayMutability.NEVER,
                                       validators=[monotonicity(Direction.ASCENDING, True),
                                                   criterion(">= 0s")])

    @classmethod
    def from_index(cls, index: DatetimeIndex):
        validate("Index", index, instance_of=DatetimeIndex, custom=lambda x: x.is_monotonic_increasing)
        return Horizon(start=index[0].to_pydatetime(), sample_times=convert_index_to_samples(index))

    @property
    def time(self) -> DatetimeIndex:
        return convert_samples_to_index(self.start, self.sample_times)

    def length(self) -> int:
        return num_elements(self.sample_times)

    def time_intervals(self) -> Quantity:
        return np.diff(self.sample_times)  # type:ignore # (=> we know it's correct)

    def unique_time_step(self) -> Quantity:
        time_steps = self.time_intervals()
        # noinspection PyUnresolvedReferences
        unique_values = np.unique(time_steps.magnitude)
        if num_elements(unique_values) > 1:
            raise ValueError(f"There is no unique time interval, but there are {num_elements(unique_values)} "
                             f"unique values, i.e. {unique_values}.")
        # noinspection PyUnresolvedReferences
        return Quantity(unique_values, time_steps.units)
