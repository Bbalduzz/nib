"""Nib Charts - Swift Charts integration for Nib."""

from .axis import ChartAxis, ChartLegend
from .chart import Chart
from .marks import (
    AreaMark,
    BarMark,
    BaseMark,
    LineMark,
    PointMark,
    RectMark,
    RuleMark,
    SectorMark,
)
from .types import (
    AxisPosition,
    InterpolationMethod,
    LegendPosition,
    PlottableField,
    PlottableType,
    PlottableValue,
    StackingMethod,
    SymbolShape,
)

__all__ = [
    # Main container
    "Chart",
    # Marks
    "BaseMark",
    "LineMark",
    "BarMark",
    "AreaMark",
    "PointMark",
    "RuleMark",
    "RectMark",
    "SectorMark",
    # Axis and legend
    "ChartAxis",
    "ChartLegend",
    # Types
    "InterpolationMethod",
    "StackingMethod",
    "SymbolShape",
    "AxisPosition",
    "LegendPosition",
    "PlottableType",
    "PlottableField",
    "PlottableValue",
]
