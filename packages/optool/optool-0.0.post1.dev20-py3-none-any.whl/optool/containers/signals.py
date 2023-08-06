from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from functools import partial
from types import FunctionType
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Tuple, Type, TypeVar, Union
from uuid import UUID

import numpy as np
import pandas as pd
from matplotlib import colors, gridspec
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DatetimeIndex
from pint import Unit
from pyfields import init_fields
from valid8 import validate

from optool import orthography, validation
from optool.autocode import Attribute, autocomplete
from optool.containers.series import QuantitySeries
from optool.io.graphics import Coordinate, set_axis_properties, set_datetime_formatter
from optool.logging import LOGGER
from optool.math import isarray
from optool.serialization.converters import BinaryConvertible
from optool.serialization.decorator import serializable
from optool.time import convert_index_to_samples
from optool.types import Quantity

if TYPE_CHECKING:
    from optool.containers.horizon import Horizon
    from optool.io.resources import DataServer

T = TypeVar("T", bound="AbstractSignalDomain")


class AbstractSignalDomain(ABC):

    @abstractmethod
    def check_compatibility(self, values: Quantity) -> None:
        raise NotImplementedError()

    @abstractmethod
    def validate_requirement(self: T, requirement: T, field_name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_unit(self) -> Unit:
        raise NotImplementedError()


@autocomplete(make_hash=False, make_str=False, make_repr=False)
class Signal(BinaryConvertible):
    __slots__ = '_name', '_domain', '_source', '_dataframe'
    name: str = Attribute(read_only=True)
    domain: AbstractSignalDomain = Attribute(read_only=True)
    source: str = Attribute(read_only=True)

    @init_fields(init_args_before=False)
    def __init__(
            self,
            time,  # type: DatetimeIndex
            values  # type: QuantitySeries
    ):
        self._dataframe = pd.DataFrame.from_records({self.name: values}, index=time)
        self.domain.check_compatibility(values.quantity)

    @property
    def textual_name(self) -> str:
        return orthography.textualize(self.name)

    @property
    def time(self) -> DatetimeIndex:
        return self._dataframe.index  # type: ignore # we know it better

    @property
    def values(self) -> QuantitySeries:
        return self._dataframe[self.name].array

    @property
    def quantity(self) -> Quantity:
        return self.values.quantity

    @property
    def unit(self) -> Unit:
        return self.domain.get_unit()

    @property
    def sample_times(self):
        return convert_index_to_samples(self.time)

    def copy(self) -> Signal:
        return Signal(self.name, self.domain, self.source, self.time.copy(), self.values.copy())

    def interpolate(self, horizon: Horizon) -> Quantity:
        return np.interp(horizon.sample_times, self.sample_times, self.values.quantity)

    def resample(self, horizon: Horizon) -> Signal:
        return Signal(self.name, self.domain, self.source, horizon.time.copy(),
                      QuantitySeries(self.interpolate(horizon)))

    def integrate(self, criteria: Optional[FunctionType] = None) -> Quantity:
        if criteria is None:
            x = self.sample_times
            y = self.values.quantity
            return np.trapz(y, x)

        y = self.values.quantity[:-1]
        dx = np.diff(self.sample_times)[criteria(y)]
        y = y[criteria(y)]
        return np.sum(dx * y)

    def filter_time(self, month: Optional[Union[Iterable[int], int]] = None) -> Optional[Signal]:
        if month is None:
            return self.copy()
        if isinstance(month, int):
            time_is_month = self.time.month == month
        else:
            time_is_month = [any(self.time.month == m) for m in month]
        if time_is_month.any():
            return Signal(self.name, self.domain, self.source, self.time[time_is_month].copy(),
                          self.values[time_is_month].copy())
        return None

    def plot(self, axis=None, *args, **kwargs):
        target = plt.plot if axis is None else axis.plot
        self._draw_data(target, args, kwargs)

    def step(self, axis=None, *args, **kwargs):
        target = plt.step if axis is None else axis.step
        self._draw_data(target, args, kwargs)

    def histogram(self) -> Tuple[Figure, Tuple[Axes]]:

        bins = (np.arange(0, 24), 30)

        def _hist_counts(signal: Optional[Signal]):
            if signal is None:
                return 0
            return np.histogram2d(x=signal.time.hour, y=signal.quantity.magnitude, bins=bins)[0]

        # noinspection PyShadowingNames
        def _draw_histogram(signal, ax, color_min_value=None, color_max_value=None):
            return ax.hist2d(x=signal.time.hour,
                             y=signal.quantity.magnitude,
                             bins=bins,
                             norm=colors.LogNorm(vmin=color_min_value, vmax=color_max_value),
                             cmap=plt.get_cmap("YlGnBu"))

        fig: Figure = plt.figure()
        fig.suptitle(f"Histogram of the {self.textual_name} power")
        main_grid = gridspec.GridSpec(1, 2, figure=fig)

        handles: np.ndarray[Tuple, Any] = np.empty(13, dtype=tuple)
        axes: np.ndarray[Axes, Any] = np.empty(13, dtype=plt.Axes)
        ax_year = fig.add_subplot(main_grid[0])
        handles[0] = _draw_histogram(self, ax_year)
        axes[0] = ax_year

        x_lim = ax_year.get_xlim()
        y_lim = ax_year.get_ylim()

        month_grid = gridspec.GridSpecFromSubplotSpec(3, 4, subplot_spec=main_grid[1])
        monthly_signals = [self.filter_time(i + 1) for i in range(12)]
        max_counts = np.max([np.max(_hist_counts(signal)) for signal in monthly_signals])
        for i, signal in enumerate(monthly_signals):
            ax_month = fig.add_subplot(month_grid[i], sharex=ax_year, sharey=ax_year)
            month_number = i + 1
            month_name = datetime(1, month_number, 1).strftime("%B")
            ax_month.set_title(month_name)

            if signal is not None:
                handles[month_number] = _draw_histogram(signal, ax_month, color_min_value=1, color_max_value=max_counts)

            # Adjust axes and tick labels
            if not ax_month.is_last_row():
                plt.setp(ax_month.get_xticklabels(), visible=False)
            if not ax_month.is_first_col():
                plt.setp(ax_month.get_yticklabels(), visible=False)

            axes[month_number] = ax_month

        ax_year.set_xlim(x_lim)
        ax_year.set_ylim(y_lim)

        ax_year.set(xlabel="Time of the day / hour")

        set_axis_properties(ax_year, Coordinate.Y, unit=self.unit, label=self.textual_name)

        for ax in axes:
            ax.grid(linewidth=0.5, alpha=0.5)

        not_nan_handles = handles[np.where(handles)]
        fig.colorbar(not_nan_handles[0][3], ax=axes[0])
        fig.colorbar(not_nan_handles[1][3], ax=axes[[4, 8, 12]])

        return fig, tuple(axes)  # type:ignore[return-value]

    def _draw_data(self, target, args, kwargs):
        if "label" not in kwargs:
            kwargs["label"] = self.name
        target(self.time.to_pydatetime(), self.values, *args, **kwargs)

    @staticmethod
    def plot_signals(signals: List[Signal]) -> Tuple[plt.Figure, plt.Axes]:
        fig, axes = plt.subplots(len(signals), sharex="col")
        for ax, signal in zip(axes, signals):
            signal.plot(ax)
            ax.legend()
            set_datetime_formatter(ax)
            set_axis_properties(ax, Coordinate.Y)
        return fig, axes

    def __hash__(self):
        return hash((type(self), self.get_uuid()))


_ALLOWED_SIGNAL_TYPES = Union[Quantity, Signal, UUID]


class SignalAttribute(Attribute):

    @staticmethod
    def _validate_value(obj, field, value, signal_type: AbstractSignalDomain, criterion: str):
        LOGGER.debug("Validating value of type {} of field {} of class {}.", value.__class__.__name__, field.name,
                     obj.__class__.__name__)
        if isinstance(value, Quantity):
            validators = [isarray, lambda x: signal_type.check_compatibility(x)]
            if criterion:
                validators.append(validation.criterion(criterion))
            validate(f"Value of field {field.name}", value, custom=validators)

        elif isinstance(value, Signal):
            value_of_signal: Quantity = value.values.quantity
            SignalAttribute._validate_value(obj, field, value_of_signal, signal_type, criterion)
            value.domain.validate_requirement(signal_type, field.name)

        elif not isinstance(value, UUID):
            raise TypeError(f"The value has type {type(value).__name__}, which is not supported.")

    def __init__(self, domain: AbstractSignalDomain, criterion: str = ""):
        # Initialize basic Attribute
        validator = partial(self._validate_value, signal_type=domain, criterion=criterion)
        super().__init__(read_only=True, validators=validator)
        self.type_hint = _ALLOWED_SIGNAL_TYPES
        self.serialize_as = UUID

        # Add custom instance members
        self.domain = domain


X = TypeVar("X", bound=_ALLOWED_SIGNAL_TYPES)
G = TypeVar("G", bound="SignalGroup")


@serializable(only_subclasses=True)
class SignalGroup(BinaryConvertible):

    @classmethod
    def __init_subclass__(cls, **kwargs):
        for field in Attribute.reveal(cls):
            if not isinstance(field, SignalAttribute):
                raise ValueError(f"Not all attributes of {cls.__name__!r} are signal attributes, "
                                 f"e.g. {field.name!r} is a {field.__class__.__name__!r}.")

    def check_types(self, expected: Type[_ALLOWED_SIGNAL_TYPES]):
        for field in Attribute.reveal(self):
            value = field.get_value(self)
            if not isinstance(value, expected):
                raise ValueError(
                    f"Expected type {expected}, but attribute named {field.name} has type {type(value).__name__}.")

    def check_dimensions(self, length: int):
        signals = self.get_values(Quantity)
        signal_dimensions = {k: len(v) for (k, v) in signals.items()}
        lengths = list(signal_dimensions.values())
        if signals and len(np.unique(lengths)) > 1:
            raise ValueError(f"Not all signals have the same length, but {signal_dimensions}.")
        if signals and lengths[0] != length:
            raise ValueError(f"The signal lengths are not as required, but {lengths[0]} != {length}.")

    def get_values(self, type: Type[X]) -> Dict[str, X]:
        self.check_types(type)
        return {field.name: field.get_value(self) for field in Attribute.reveal(self)}

    def load_signals(self: G, server: DataServer) -> G:
        uuids = self.get_values(UUID)
        signals = {k: server.get_signal(uuid=v) for k, v in uuids.items()}
        # noinspection PyArgumentList
        return self.__class__(**signals)

    def interpolate_signals(self: G, horizon: Horizon) -> G:
        signals = self.get_values(Signal)
        quantities = {k: v.interpolate(horizon)[:-1] for k, v in signals.items()}
        # noinspection PyArgumentList
        return self.__class__(**quantities)

    def resample_signals(self: G, horizon: Horizon) -> G:
        signals = self.get_values(Signal)
        signals = {k: v.resample(horizon) for k, v in signals.items()}
        # noinspection PyArgumentList
        return self.__class__(**signals)

    def create_signals(self: G, horizon: Horizon, source: str) -> G:
        self.check_types(Quantity)
        fields: Tuple[SignalAttribute] = Attribute.reveal(self)  # type:ignore
        signal_specs = {field.name: (field.get_value(self), field.domain) for field in fields}

        time = horizon.time
        signals = {k: Signal(k, v[1], source, *self._fix_time_value(time, v[0])) for k, v in signal_specs.items()}
        # noinspection PyArgumentList
        return self.__class__(**signals)

    @staticmethod
    def _fix_time_value(time: DatetimeIndex, value: Quantity):
        if len(value) == len(time):
            return time, QuantitySeries(value)
        if len(value) == len(time) - 1:
            return time[:-1], QuantitySeries(value)
        else:
            raise ValueError(f"The array of time indices must either be equally long than the array of values, "
                             f"or one element longer, which indicates that the signal is a piecewise constant signal. "
                             f"However, the time array has {len(time)} elements, while the value array has "
                             f"{len(value)} elements.")


class SignalContainer(ABC):

    def get_groups(self) -> Dict[str, G]:
        return {field.name: field.get_value(self) for field in Attribute.reveal(self)}

    def check_types(self, expected: Type[_ALLOWED_SIGNAL_TYPES]):
        [group.check_types(expected) for group in self.get_groups().values()]  # type:ignore


R = TypeVar("R", bound="InputSignalContainer")
S = TypeVar("S", bound="OutputSignalContainer")


@serializable(only_subclasses=True)
class InputSignalContainer(SignalContainer):

    @classmethod
    def __init_subclass__(cls, **kwargs):
        for field in Attribute.reveal(cls):
            if not issubclass(field.type_hint, SignalGroup):
                raise ValueError(f"Not all attributes of {cls.__name__!r} are signal groups, "
                                 f"e.g. {field.name!r} has type {field.type_hint!r}.")

    def load_signals(self: R, server: DataServer) -> R:
        signal_groups = {k: v.load_signals(server) for k, v in self.get_groups().items()}  # type:ignore
        # noinspection PyArgumentList
        return self.__class__(**signal_groups)

    def interpolate_signals(self: R, horizon: Horizon) -> R:
        signal_groups = {k: v.interpolate_signals(horizon) for k, v in self.get_groups().items()}  # type:ignore
        # noinspection PyArgumentList
        return self.__class__(**signal_groups)

    def resample_signals(self: R, horizon: Horizon) -> R:
        signal_groups = {k: v.resample_signals(horizon) for k, v in self.get_groups().items()}  # type:ignore
        # noinspection PyArgumentList
        return self.__class__(**signal_groups)


@serializable(only_subclasses=True)
class OutputSignalContainer(SignalContainer):

    def create_signals(self: S, horizon: Horizon, source: str) -> S:
        signal_groups = {k: v.create_signals(horizon, source) for k, v in self.get_groups().items()}  # type:ignore
        # noinspection PyArgumentList
        return self.__class__(**signal_groups)
