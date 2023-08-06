from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from pandas import DatetimeIndex

from optool.types import UNITS, Quantity


def convert_index_to_samples(time: DatetimeIndex) -> Quantity:
    duration = (time - time[0]).to_pytimedelta()
    sample_times_seconds = np.array([val.total_seconds() for val in duration])
    return Quantity(sample_times_seconds, UNITS.second)


def convert_samples_to_index(start: datetime, sample_times: Quantity) -> DatetimeIndex:
    sample_times_seconds = sample_times.m_as(UNITS.second)
    duration = [timedelta(0, float(second)) for second in sample_times_seconds]
    datetime_values = [start + val for val in duration]
    return pd.DatetimeIndex(datetime_values)
