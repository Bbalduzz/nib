"""Chart container view for Nib Charts."""

from typing import Any, Dict, List, Optional, Union

from ..base import View
from .axis import ChartAxis, ChartLegend
from .marks import BaseMark


class Chart(View):
    """
    Chart container for displaying data visualizations.

    Uses columnar data format for efficient MessagePack serialization.

    Example:
        chart = Chart(
            data=[
                {"month": "Jan", "sales": 100},
                {"month": "Feb", "sales": 150},
            ],
            marks=[
                LineMark(x="month", y="sales"),
            ],
            x_axis=ChartAxis(label="Month"),
            y_axis=ChartAxis(label="Sales", grid_lines=True),
        )
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
        """
        Create a chart.

        Args:
            data: List of data rows as dicts (e.g., [{"x": 1, "y": 2}, ...])
            marks: List of mark objects (LineMark, BarMark, etc.)
            x_axis: X-axis configuration
            y_axis: Y-axis configuration
            legend: Legend configuration or False to hide
            chart_background: Background color for entire chart
            plot_background: Background color for plot area
            **kwargs: Standard view modifiers (width, height, padding, etc.)
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
        """
        Convert row-based data to columnar format for efficient serialization.

        Input: [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}]
        Output: {"columnsJson": '{"a": [1, 2], "b": ["x", "y"]}', "rowCount": 2}

        Note: Columns are encoded as JSON string to work around MessagePack
        decoder limitations with heterogeneous arrays.
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
        """Get chart properties."""
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
        """Get mark children."""
        if not self._marks:
            return None
        return [
            mark.to_dict(f"{parent_path}.{i}")
            for i, mark in enumerate(self._marks)
        ]

    @property
    def data(self) -> List[Dict[str, Any]]:
        """Get chart data."""
        return self._data

    @data.setter
    def data(self, value: List[Dict[str, Any]]):
        """Set chart data and trigger re-render."""
        self._data = value
        self._trigger_update()

    def append_data(self, row: Dict[str, Any]):
        """Append a single data row and trigger re-render."""
        self._data.append(row)
        self._trigger_update()

    def update_data(self, index: int, row: Dict[str, Any]):
        """Update a data row at the given index and trigger re-render."""
        if 0 <= index < len(self._data):
            self._data[index] = row
            self._trigger_update()

    def clear_data(self):
        """Clear all data and trigger re-render."""
        self._data = []
        self._trigger_update()
