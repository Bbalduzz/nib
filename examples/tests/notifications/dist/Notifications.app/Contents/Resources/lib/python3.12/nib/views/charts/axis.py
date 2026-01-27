"""Chart axis configuration for Nib Charts."""

from typing import List, Optional, Union

from .types import AxisPosition


class ChartAxis:
    """Configuration for chart axes."""

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
        """
        Create a chart axis configuration.

        Args:
            position: Axis position ("bottom", "top", "leading", "trailing")
            label: Axis label text
            grid_lines: Whether to show grid lines
            hidden: Whether to hide the axis
            format: Value format ("number", "currency", "percent")
            values: Explicit axis values/ticks
            label_color: Color for axis labels
            grid_color: Color for grid lines
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
        """Convert to dictionary for serialization."""
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
    """Configuration for chart legend."""

    def __init__(
        self,
        position: Optional[str] = None,
        hidden: Optional[bool] = None,
        title: Optional[str] = None,
    ):
        """
        Create a chart legend configuration.

        Args:
            position: Legend position ("top", "bottom", "leading", "trailing", "automatic")
            hidden: Whether to hide the legend
            title: Legend title
        """
        self._position = position
        self._hidden = hidden
        self._title = title

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        result = {}
        if self._position is not None:
            result["position"] = self._position
        if self._hidden is not None:
            result["hidden"] = self._hidden
        if self._title is not None:
            result["title"] = self._title
        return result
