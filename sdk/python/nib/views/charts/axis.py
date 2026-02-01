"""Chart axis and legend configuration for Nib Charts.

This module provides classes for configuring chart axes and legends. Axes
control how data values are mapped to visual positions and how tick marks,
labels, and grid lines are displayed. Legends explain the meaning of colors,
shapes, or other visual encodings.

Both ChartAxis and ChartLegend are configuration objects that are passed to
the Chart constructor. They do not render anything on their own.

Example:
    Configure axes for a chart::

        chart = Chart(
            data=sales_data,
            marks=[BarMark(x="month", y="revenue")],
            x_axis=ChartAxis(
                label="Month",
                position="bottom",
            ),
            y_axis=ChartAxis(
                label="Revenue ($)",
                grid_lines=True,
                format="currency",
            ),
        )

    Configure legend::

        chart = Chart(
            data=data,
            marks=[LineMark(x="date", y="value", foreground_style="category")],
            legend=ChartLegend(
                position="bottom",
                title="Category",
            ),
        )

    Hide axis or legend::

        chart = Chart(
            data=data,
            marks=[...],
            x_axis=ChartAxis(hidden=True),
            legend=False,  # Shorthand to hide legend
        )
"""

from typing import List, Optional, Union

from .types import AxisPosition


class ChartAxis:
    """Configuration for chart axes.

    ChartAxis controls the appearance and behavior of an axis in a chart.
    This includes the axis position, label text, grid lines, value formatting,
    and colors. All properties are optional - unspecified properties use
    sensible defaults determined by Swift Charts.

    ChartAxis is used with the x_axis and y_axis parameters of the Chart
    constructor.

    Example:
        Basic axis with label::

            ChartAxis(label="Revenue ($)")

        Axis with grid lines and formatting::

            ChartAxis(
                label="Sales",
                grid_lines=True,
                format="currency",
                label_color="#666666",
                grid_color="#333333",
            )

        Custom tick values::

            ChartAxis(
                label="Rating",
                values=[1, 2, 3, 4, 5],
            )

        Hidden axis::

            ChartAxis(hidden=True)
    """

    def __init__(
        self,
        position: Optional[Union[str, AxisPosition]] = None,
        label: Optional[str] = None,
        grid_lines: Optional[bool] = None,
        hidden: Optional[bool] = None,
        format: Optional[str] = None,
        values: Optional[List] = None,
        label_color: Optional[str] = None,
        grid_color: Optional[str] = None,
    ):
        """Initialize a ChartAxis configuration.

        All parameters are optional. Omitted parameters use Swift Charts
        defaults, which adapt based on the data and chart type.

        Args:
            position: Position of the axis relative to the plot area.
                For x-axis: "bottom" (default) or "top".
                For y-axis: "leading" (default, left in LTR) or "trailing".
                Can also use AxisPosition enum values.
            label: Text label for the axis, displayed alongside the axis
                to describe what the values represent (e.g., "Temperature (F)").
            grid_lines: Whether to display grid lines extending from tick
                marks across the plot area. Defaults to False. Grid lines
                help readers trace values but can add visual clutter.
            hidden: Whether to completely hide the axis, including tick marks
                and labels. Useful for minimalist charts or small sparklines.
                Defaults to False.
            format: Format string for axis values. Supported formats include:
                - "number": Standard numeric formatting
                - "currency": Currency formatting with symbol
                - "percent": Percentage formatting
                Defaults to automatic formatting based on data type.
            values: Explicit list of values to show as tick marks. When
                specified, only these values appear on the axis. Useful for
                categorical data or when you want specific tick positions.
            label_color: Color for axis labels and tick text. Accepts hex
                color strings (e.g., "#666666") or named colors.
            grid_color: Color for grid lines when grid_lines is True.
                Accepts hex color strings or named colors.
        """
        if isinstance(position, AxisPosition):
            self._position = position.value
        else:
            self._position = position
        self._label = label
        self._grid_lines = grid_lines
        self._hidden = hidden
        self._format = format
        self._values = values
        self._label_color = label_color
        self._grid_color = grid_color

    def to_dict(self) -> dict:
        """Convert axis configuration to dictionary for serialization.

        Produces a dictionary representation suitable for sending to the
        Swift runtime. Only includes properties that were explicitly set.

        Returns:
            Dictionary containing axis configuration properties with camelCase
            keys matching the Swift protocol expectations.
        """
        result = {}
        if self._position is not None:
            result["position"] = self._position
        if self._label is not None:
            result["label"] = self._label
        if self._grid_lines is not None:
            result["gridLines"] = self._grid_lines
        if self._hidden is not None:
            result["hidden"] = self._hidden
        if self._format is not None:
            result["format"] = self._format
        if self._values is not None:
            result["values"] = self._values
        if self._label_color is not None:
            result["labelColor"] = self._label_color
        if self._grid_color is not None:
            result["gridColor"] = self._grid_color
        return result


class ChartLegend:
    """Configuration for chart legend.

    ChartLegend controls the appearance and position of the chart legend,
    which explains the meaning of colors, shapes, or other visual encodings
    used in the chart marks.

    The legend is automatically generated based on the foreground_style
    mappings in your marks. For example, if you use
    ``foreground_style=PlottableField("category")``, the legend will show
    each category with its assigned color.

    Example:
        Bottom-positioned legend with title::

            ChartLegend(
                position="bottom",
                title="Product Category",
            )

        Hidden legend::

            ChartLegend(hidden=True)

        Or simply pass False to Chart::

            Chart(data=data, marks=[...], legend=False)
    """

    def __init__(
        self,
        position: Optional[str] = None,
        hidden: Optional[bool] = None,
        title: Optional[str] = None,
    ):
        """Initialize a ChartLegend configuration.

        Args:
            position: Position of the legend relative to the chart. Options:
                - "top": Above the chart
                - "bottom": Below the chart
                - "leading": Left side (in LTR layouts)
                - "trailing": Right side (in LTR layouts)
                - "automatic": System chooses based on available space
                Defaults to "automatic" if not specified.
            hidden: Whether to hide the legend entirely. Set to True for
                charts where the legend is not needed or adds clutter.
                Defaults to False.
            title: Optional title text displayed above the legend items.
                Useful for clarifying what the legend represents (e.g.,
                "Region" or "Product Type").
        """
        self._position = position
        self._hidden = hidden
        self._title = title

    def to_dict(self) -> dict:
        """Convert legend configuration to dictionary for serialization.

        Produces a dictionary representation suitable for sending to the
        Swift runtime. Only includes properties that were explicitly set.

        Returns:
            Dictionary containing legend configuration properties with keys
            matching the Swift protocol expectations.
        """
        result = {}
        if self._position is not None:
            result["position"] = self._position
        if self._hidden is not None:
            result["hidden"] = self._hidden
        if self._title is not None:
            result["title"] = self._title
        return result
