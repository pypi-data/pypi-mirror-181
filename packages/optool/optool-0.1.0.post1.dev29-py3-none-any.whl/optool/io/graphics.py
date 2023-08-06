from enum import Enum
from typing import Iterator, List, Optional

from matplotlib import pyplot as plt
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.text import Text
from pint import Unit

from optool.logging import LOGGER


def _get_style(line: Line2D) -> List[str]:
    style = [
        line.get_color(),
        line.get_linestyle(),
        line.get_linewidth(),
        line.get_marker(),
        line.get_markeredgecolor(),
        line.get_markerfacecolor()
    ]
    style = ['' if val == 'None' else val for val in style]
    return style


def _find_element_with_matching_style(legend_line, plot_elements: list):
    legend_style = _get_style(legend_line)
    plot_styles = [_get_style(val) for val in plot_elements]

    matches = [element for (style, element) in zip(plot_styles, plot_elements) if legend_style == style]

    if len(matches) != 1:
        LOGGER.warning("Not exactly one plot elements found with the same style and the same name ({}), but {}.",
                       legend_line.get_label(), len(matches))
        return None
    return matches[0]


def _find_matching_plot_element(legend_line, ax):
    [plot_elements, plot_element_labels] = ax.get_legend_handles_labels()
    for (handle, label) in zip(plot_elements, plot_element_labels):
        if handle.get_label() != label:
            raise ValueError("The label of the handle and the corresponding label are not identical.")

    label_text = legend_line.get_label()
    matches = [element for (element, label) in zip(plot_elements, plot_element_labels) if label == label_text]
    if not matches:
        LOGGER.warning("No plot element found labeled {!r}.", label_text)
        return None

    if len(matches) > 1:
        return _find_element_with_matching_style(legend_line, matches)

    return matches[0]


def make_interactive(leg: Legend, recompute_axes_limits: bool = True) -> None:
    """
    Adds interactivity to legend entries.

    When clicking on a legend entry (text or icon), the visibility of corresponding plot element is toggled.

    Args:
        leg (Legend): The legend to which interactivity should be added.
        recompute_axes_limits (bool): Set to `False` to disable the automatic scaling of the axes limits.
    """

    leg.set_draggable(state=True)
    leg.set_clip_on(False)

    ax = leg.axes
    fig = ax.figure

    legend_entry_map = {}  # Will map legend lines to legend texts and vice versa
    for this_legend_line, this_legend_text in zip(leg.get_lines(), leg.get_texts()):
        this_legend_line.set_picker(True)  # Enable picking on the legend line.
        this_legend_text.set_picker(True)  # Enable picking on the legend text.
        this_legend_line.set_pickradius(10)

        plot_element = _find_matching_plot_element(this_legend_line, ax)
        legend_entry_map[this_legend_line] = (plot_element, this_legend_text)
        legend_entry_map[this_legend_text] = (plot_element, this_legend_line)

    # noinspection PyShadowingNames
    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        if event.artist not in legend_entry_map:
            LOGGER.warning("The clicked element {!r} is not part of the known elements.", event.artist)
            return
        if isinstance(event.artist, Text):
            legend_text = event.artist
            (plot_element, legend_line) = legend_entry_map[legend_text]
        else:
            legend_line = event.artist
            (plot_element, legend_text) = legend_entry_map[legend_line]

        if plot_element is None:
            return

        visible = not plot_element.get_visible()
        LOGGER.debug("Changing visibility to {} of {} labeled {!r}.", visible, plot_element, legend_text.get_text())

        plot_element.set_visible(visible)
        legend_text.set_alpha(1.0 if visible else 0.2)
        legend_line.set_alpha(1.0 if visible else 0.2)

        if recompute_axes_limits:
            ax.relim(visible_only=True)  # recompute the ax.dataLim
            ax.autoscale_view()  # update ax.viewLim using the new dataLim
        plt.draw()  # Update visualization

    fig.canvas.mpl_connect('pick_event', on_pick)


def get_color_cycle() -> Iterator[str]:
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors: List[str] = prop_cycle.by_key()['color']
    return iter(colors)


def set_datetime_formatter(ax):
    # activate the new datetime formatter
    # https://matplotlib.org/stable/api/dates_api.html#matplotlib.dates.ConciseDateFormatter
    locator = AutoDateLocator()
    formatter = ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)


class Coordinate(Enum):
    X = 1
    Y = 2
    Z = 3

    def set_label_and_unit(self, ax, unit: Optional[Unit] = None, label: Optional[str] = None, **kwargs):
        label_setter = getattr(ax, f"set_{self.name.lower()}label")
        ax_subplot = getattr(ax, f"{self.name.lower()}axis")

        if unit is None:
            unit = ax_subplot.units
        elif len(ax.containers) > 0 and unit != ax_subplot.units:
            raise ValueError(f"There are already {len(ax.containers)} elements in the axis, i.e., {ax.containers}."
                             f"Cannot reset the unit.")

        if unit is None:
            if label is not None:
                label_setter(f"{label}", **kwargs)
        else:
            ax_subplot.set_units(unit)
            if label is None:
                label_setter(f"{ax_subplot.units:~P}", **kwargs)
            else:
                label_setter(f"{label} / {ax_subplot.units:~P}", **kwargs)


def set_axis_properties(ax,
                        coordinate: Coordinate,
                        *,
                        unit: Optional[Unit] = None,
                        label: Optional[str] = None,
                        **kwargs):
    coordinate.set_label_and_unit(ax, unit, label, **kwargs)
