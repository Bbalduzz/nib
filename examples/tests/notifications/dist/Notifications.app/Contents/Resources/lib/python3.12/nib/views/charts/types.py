"""Chart-specific types and enums for Nib Charts."""

from enum import Enum
from typing import Optional, Union


class InterpolationMethod(Enum):
    """Interpolation methods for line and area charts."""
    LINEAR = "linear"
    MONOTONE = "monotone"
    CATMULL_ROM = "catmullRom"
    CARDINAL = "cardinal"
    STEP_START = "stepStart"
    STEP_CENTER = "stepCenter"
    STEP_END = "stepEnd"


class StackingMethod(Enum):
    """Stacking methods for bar and area charts."""
    STANDARD = "standard"
    NORMALIZED = "normalized"
    CENTER = "center"


class SymbolShape(Enum):
    """Symbol shapes for point marks."""
    CIRCLE = "circle"
    SQUARE = "square"
    TRIANGLE = "triangle"
    DIAMOND = "diamond"
    CROSS = "cross"
    PLUS = "plus"
    PENTAGON = "pentagon"
    HEXAGON = "hexagon"


class AxisPosition(Enum):
    """Axis position."""
    BOTTOM = "bottom"
    TOP = "top"
    LEADING = "leading"
    TRAILING = "trailing"


class LegendPosition(Enum):
    """Legend position."""
    TOP = "top"
    BOTTOM = "bottom"
    LEADING = "leading"
    TRAILING = "trailing"
    AUTOMATIC = "automatic"
    HIDDEN = "hidden"


class PlottableType(Enum):
    """Data type for plottable values."""
    QUANTITATIVE = "quantitative"  # Numbers (continuous scale)
    NOMINAL = "nominal"            # Categories (discrete scale)
    TEMPORAL = "temporal"          # Dates/times (time scale)


class PlottableField:
    """Reference to a data column for chart encoding."""

    def __init__(
        self,
        field: str,
        type: Optional[Union[PlottableType, str]] = None,
    ):
        self.field = field
        if type is None:
            self._type = None
        elif isinstance(type, PlottableType):
            self._type = type.value
        else:
            self._type = type

    def to_dict(self) -> dict:
        result = {"field": self.field}
        if self._type:
            result["type"] = self._type
        return result


class PlottableValue:
    """Static value for chart encoding (e.g., for RuleMark reference lines)."""

    def __init__(
        self,
        value: Union[int, float, str],
        label: Optional[str] = None,
    ):
        self.value = value
        self.label = label

    def to_dict(self) -> dict:
        result = {"value": self.value}
        if self.label:
            result["label"] = self.label
        return result
