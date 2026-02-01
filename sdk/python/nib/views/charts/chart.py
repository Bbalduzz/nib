"""Chart container view for Nib Charts.

This module provides the Chart class, which is the main container for displaying
data visualizations in Nib applications. Charts support various mark types
(lines, bars, areas, points, etc.) and can be customized with axes, legends,
and styling options.

The Chart class uses a columnar data format internally for efficient MessagePack
serialization when communicating with the Swift runtime. Data is provided in
row-based format (list of dictionaries) and automatically converted.

Example:
    Basic line chart::

        import nib

        chart = nib.Chart(
            data=[
                {"month": "Jan", "sales": 100},
                {"month": "Feb", "sales": 150},
                {"month": "Mar", "sales": 200},
            ],
            marks=[nib.LineMark(x="month", y="sales")],
            width=300,
            height=200,
        )

    Chart with axes and legend::

        chart = nib.Chart(
            data=sales_data,
            marks=[nib.BarMark(x="category", y="value")],
            x_axis=nib.ChartAxis(label="Category"),
            y_axis=nib.ChartAxis(label="Sales ($)", grid_lines=True),
            legend=nib.ChartLegend(position="bottom"),
        )

    Multi-series chart::

        chart = nib.Chart(
            data=time_series_data,
            marks=[
                nib.LineMark(x="date", y="revenue", foreground_style="blue"),
                nib.LineMark(x="date", y="expenses", foreground_style="red"),
            ],
        )
"""

from typing import Any, Dict, List, Optional, Union

from ..base import View
from .axis import ChartAxis, ChartLegend
from .marks import BaseMark


class Chart(View):
    """Chart container for displaying data visualizations.

    Chart is the primary container for rendering data visualizations using
    Swift Charts. It manages the data, marks, axes, and legend configuration,
    and handles the conversion of data to an efficient columnar format for
    communication with the Swift runtime.

    Charts support multiple mark types that can be combined to create complex
    visualizations. Data is reactive - updating the data property or using
    helper methods like append_data() will trigger automatic re-renders.

    Attributes:
        data: The chart's data as a list of dictionaries. Each dictionary
            represents a row with column names as keys.

    Example:
        Basic bar chart::

            chart = Chart(
                data=[
                    {"month": "Jan", "sales": 100},
                    {"month": "Feb", "sales": 150},
                ],
                marks=[BarMark(x="month", y="sales")],
            )

        Chart with full configuration::

            chart = Chart(
                data=monthly_data,
                marks=[LineMark(x="month", y="sales")],
                x_axis=ChartAxis(label="Month"),
                y_axis=ChartAxis(label="Sales ($)", grid_lines=True),
                legend=ChartLegend(position="bottom"),
                chart_background="#1a1a1a",
                plot_background="#262626",
                width=400,
                height=300,
                padding=16,
            )

        Updating data reactively::

            chart.data = new_data  # Full replacement
            chart.append_data({"month": "Mar", "sales": 200})  # Add row
            chart.update_data(0, {"month": "Jan", "sales": 120})  # Update row
    """

    _type = "Chart"

    def __init__(
        self,
        data: List[Dict[str, Any]],
        marks: List[BaseMark],
        x_axis: Optional[ChartAxis] = None,
        y_axis: Optional[ChartAxis] = None,
        legend: Optional[Union[ChartLegend, bool]] = None,
        chart_background: Optional[str] = None,
        plot_background: Optional[str] = None,
        # View modifiers
        **kwargs,
    ):
        """Initialize a new Chart instance.

        Args:
            data: List of data rows as dictionaries. Each dictionary represents
                a single data point with column names as keys. For example:
                ``[{"x": 1, "y": 10}, {"x": 2, "y": 20}]``. The keys should
                match the field names referenced in your marks.
            marks: List of mark objects that define how data is visualized.
                Supported marks include LineMark, BarMark, AreaMark, PointMark,
                RuleMark, RectMark, and SectorMark. Multiple marks can be
                combined to create layered visualizations.
            x_axis: Configuration for the X-axis. Use ChartAxis to customize
                the label, grid lines, position, formatting, and appearance.
                Defaults to None (automatic axis configuration).
            y_axis: Configuration for the Y-axis. Use ChartAxis to customize
                the label, grid lines, position, formatting, and appearance.
                Defaults to None (automatic axis configuration).
            legend: Legend configuration. Pass a ChartLegend instance for
                custom positioning and styling, False to hide the legend
                entirely, or None for automatic legend behavior.
            chart_background: Background color for the entire chart container,
                including axes and legend. Accepts hex color strings like
                "#1a1a1a" or named colors.
            plot_background: Background color for just the plot area (the
                region where data is rendered). Accepts hex color strings
                or named colors.
            **kwargs: Standard view modifiers inherited from View, including
                width, height, padding, opacity, corner_radius, border_color,
                border_width, shadow properties, and more.

        Raises:
            TypeError: If data is not a list or marks is not a list.

        Example:
            Create a simple line chart::

                chart = Chart(
                    data=[{"x": 1, "y": 10}, {"x": 2, "y": 20}],
                    marks=[LineMark(x="x", y="y")],
                    width=300,
                    height=200,
                )
        """
        super().__init__(**kwargs)
        self._data = data
        self._marks = marks
        self._x_axis = x_axis
        self._y_axis = y_axis
        self._legend = legend
        self._chart_background = chart_background
        self._plot_background = plot_background

    def _convert_to_columnar(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Convert row-based data to columnar format for efficient serialization.

        This internal method transforms the user-provided row-based data format
        into a columnar format that is more efficient for MessagePack serialization
        and Swift Charts consumption.

        The columnar format groups all values for each column together, which
        reduces serialization overhead and allows the Swift runtime to process
        data more efficiently.

        Args:
            data: List of dictionaries representing data rows. Each dictionary
                should have the same keys (column names), though missing keys
                are handled gracefully with None values.

        Returns:
            A dictionary containing:
                - columnsJson: JSON string encoding the columnar data structure.
                    Uses JSON encoding to work around MessagePack limitations
                    with heterogeneous arrays (arrays containing mixed types).
                - rowCount: The number of rows in the dataset.

        Example:
            Input::

                [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}]

            Output::

                {"columnsJson": '{"a": [1, 2], "b": ["x", "y"]}', "rowCount": 2}

        Note:
            Columns are encoded as a JSON string rather than a native MessagePack
            structure to work around decoder limitations with heterogeneous arrays
            in the Swift runtime.
        """
        import json

        if not data:
            return {"columnsJson": "{}", "rowCount": 0}

        # Get all unique keys
        all_keys = set()
        for row in data:
            all_keys.update(row.keys())

        # Build columnar structure
        columns = {key: [] for key in all_keys}
        for row in data:
            for key in all_keys:
                columns[key].append(row.get(key))

        # Encode columns as JSON string for reliable decoding
        return {
            "columnsJson": json.dumps(columns),
            "rowCount": len(data),
        }

    def _get_props(self) -> dict:
        """Get chart properties for serialization.

        Builds the properties dictionary that will be sent to the Swift runtime.
        This includes the columnar data, axis configurations, legend settings,
        and background colors.

        Returns:
            Dictionary containing all chart properties in the format expected
            by the Swift ViewNode protocol.
        """
        props = {}

        # Convert data to columnar format
        props["chartData"] = self._convert_to_columnar(self._data)

        # Axis configuration
        if self._x_axis:
            props["xAxis"] = self._x_axis.to_dict()
        if self._y_axis:
            props["yAxis"] = self._y_axis.to_dict()

        # Legend configuration
        if self._legend is False:
            props["legend"] = {"hidden": True}
        elif isinstance(self._legend, ChartLegend):
            props["legend"] = self._legend.to_dict()

        # Background colors
        if self._chart_background:
            props["chartBackground"] = self._chart_background
        if self._plot_background:
            props["plotBackground"] = self._plot_background

        return props

    def _get_children(self, parent_path: str) -> Optional[List[dict]]:
        """Get mark children for the view tree.

        Converts the list of mark objects into serializable dictionaries
        that represent the chart's visual elements in the view tree.

        Args:
            parent_path: The path identifier of this chart in the view tree.
                Used to generate unique IDs for child marks (e.g., "0.1", "0.2").

        Returns:
            List of dictionaries representing each mark, or None if there
            are no marks. Each dictionary contains the mark's id, type,
            and properties.
        """
        if not self._marks:
            return None
        return [
            mark.to_dict(f"{parent_path}.{i}")
            for i, mark in enumerate(self._marks)
        ]

    @property
    def data(self) -> List[Dict[str, Any]]:
        """Get the chart's current data.

        Returns:
            List of dictionaries representing the chart's data rows.
            Each dictionary contains column names as keys and data values.
        """
        return self._data

    @data.setter
    def data(self, value: List[Dict[str, Any]]):
        """Set the chart data and trigger a re-render.

        Replaces the entire dataset with new data. This triggers an automatic
        re-render of the chart to reflect the updated data.

        Args:
            value: New list of data rows as dictionaries.

        Example:
            Update chart with new data::

                chart.data = [
                    {"x": 1, "y": 100},
                    {"x": 2, "y": 200},
                ]
        """
        self._data = value
        self._trigger_update()

    def append_data(self, row: Dict[str, Any]):
        """Append a single data row and trigger a re-render.

        Adds a new data point to the end of the dataset. Useful for
        real-time charts that accumulate data over time.

        Args:
            row: Dictionary representing a single data row with column
                names as keys.

        Example:
            Add a new data point::

                chart.append_data({"timestamp": "12:00", "value": 42})
        """
        self._data.append(row)
        self._trigger_update()

    def update_data(self, index: int, row: Dict[str, Any]):
        """Update a data row at the given index and trigger a re-render.

        Replaces the data at a specific index with new values. If the
        index is out of bounds, the update is silently ignored.

        Args:
            index: Zero-based index of the row to update.
            row: New dictionary to replace the existing row.

        Example:
            Update the first data point::

                chart.update_data(0, {"month": "Jan", "sales": 150})
        """
        if 0 <= index < len(self._data):
            self._data[index] = row
            self._trigger_update()

    def clear_data(self):
        """Clear all data and trigger a re-render.

        Removes all data points from the chart, resulting in an empty
        visualization. Useful for resetting the chart before loading
        new data.

        Example:
            Reset the chart::

                chart.clear_data()
                chart.data = load_new_dataset()
        """
        self._data = []
        self._trigger_update()
