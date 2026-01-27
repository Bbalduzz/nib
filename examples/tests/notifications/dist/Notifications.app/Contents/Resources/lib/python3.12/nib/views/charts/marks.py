"""Chart mark classes for Nib Charts."""

from typing import Optional, Union

from .types import (
    InterpolationMethod,
    PlottableField,
    PlottableValue,
    StackingMethod,
    SymbolShape,
)
from ...types import resolve_enum


def _resolve_field(
    value: Optional[Union[str, PlottableField, PlottableValue]]
) -> Optional[dict]:
    """Convert a field reference to dict format."""
    if value is None:
        return None
    if isinstance(value, str):
        return {"field": value}
    if isinstance(value, (PlottableField, PlottableValue)):
        return value.to_dict()
    return value


class BaseMark:
    """Base class for all chart marks."""

    _type: str = "Mark"

    def __init__(
        self,
        foreground_style: Optional[Union[str, PlottableField]] = None,
        opacity: Optional[float] = None,
    ):
        self._foreground_style = foreground_style
        self._opacity = opacity

    def _get_base_props(self) -> dict:
        """Get common mark properties."""
        props = {}
        if self._foreground_style:
            props["foregroundStyle"] = _resolve_field(self._foreground_style)
        if self._opacity is not None:
            props["opacity"] = float(self._opacity)
        return props

    def to_dict(self, path: str = "0") -> dict:
        """Convert mark to dictionary for serialization."""
        return {
            "id": path,
            "type": self._type,
            "props": self._get_props(),
        }

    def _get_props(self) -> dict:
        """Get mark-specific properties. Override in subclasses."""
        return self._get_base_props()


class LineMark(BaseMark):
    """Line mark for line charts."""

    _type = "LineMark"

    def __init__(
        self,
        x: Union[str, PlottableField],
        y: Union[str, PlottableField],
        foreground_style: Optional[Union[str, PlottableField]] = None,
        symbol: Optional[Union[str, SymbolShape, PlottableField]] = None,
        interpolation: Optional[Union[str, InterpolationMethod]] = None,
        line_width: Optional[float] = None,
        opacity: Optional[float] = None,
    ):
        super().__init__(foreground_style=foreground_style, opacity=opacity)
        self._x = x
        self._y = y
        self._symbol = symbol
        self._interpolation = interpolation
        self._line_width = line_width

    def _get_props(self) -> dict:
        props = self._get_base_props()
        props["x"] = _resolve_field(self._x)
        props["y"] = _resolve_field(self._y)
        if self._symbol:
            if isinstance(self._symbol, (str, SymbolShape)):
                props["symbol"] = resolve_enum(self._symbol)
            else:
                props["symbolField"] = _resolve_field(self._symbol)
        if self._interpolation:
            props["interpolation"] = resolve_enum(self._interpolation)
        if self._line_width is not None:
            props["lineWidth"] = float(self._line_width)
        return props


class BarMark(BaseMark):
    """Bar mark for bar charts."""

    _type = "BarMark"

    def __init__(
        self,
        x: Optional[Union[str, PlottableField]] = None,
        y: Optional[Union[str, PlottableField]] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
        foreground_style: Optional[Union[str, PlottableField]] = None,
        stacking: Optional[Union[str, StackingMethod]] = None,
        corner_radius: Optional[float] = None,
        opacity: Optional[float] = None,
    ):
        super().__init__(foreground_style=foreground_style, opacity=opacity)
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._stacking = stacking
        self._corner_radius = corner_radius

    def _get_props(self) -> dict:
        props = self._get_base_props()
        if self._x:
            props["x"] = _resolve_field(self._x)
        if self._y:
            props["y"] = _resolve_field(self._y)
        if self._width is not None:
            props["barWidth"] = float(self._width)
        if self._height is not None:
            props["barHeight"] = float(self._height)
        if self._stacking:
            props["stacking"] = resolve_enum(self._stacking)
        if self._corner_radius is not None:
            props["cornerRadius"] = float(self._corner_radius)
        return props


class AreaMark(BaseMark):
    """Area mark for area charts."""

    _type = "AreaMark"

    def __init__(
        self,
        x: Union[str, PlottableField],
        y: Union[str, PlottableField],
        y_start: Optional[Union[str, PlottableField]] = None,
        foreground_style: Optional[Union[str, PlottableField]] = None,
        interpolation: Optional[Union[str, InterpolationMethod]] = None,
        stacking: Optional[Union[str, StackingMethod]] = None,
        opacity: Optional[float] = None,
    ):
        super().__init__(foreground_style=foreground_style, opacity=opacity)
        self._x = x
        self._y = y
        self._y_start = y_start
        self._interpolation = interpolation
        self._stacking = stacking

    def _get_props(self) -> dict:
        props = self._get_base_props()
        props["x"] = _resolve_field(self._x)
        props["y"] = _resolve_field(self._y)
        if self._y_start:
            props["yStart"] = _resolve_field(self._y_start)
        if self._interpolation:
            props["interpolation"] = resolve_enum(self._interpolation)
        if self._stacking:
            props["stacking"] = resolve_enum(self._stacking)
        return props


class PointMark(BaseMark):
    """Point mark for scatter plots."""

    _type = "PointMark"

    def __init__(
        self,
        x: Union[str, PlottableField],
        y: Union[str, PlottableField],
        foreground_style: Optional[Union[str, PlottableField]] = None,
        symbol: Optional[Union[str, SymbolShape, PlottableField]] = None,
        symbol_size: Optional[float] = None,
        opacity: Optional[float] = None,
    ):
        super().__init__(foreground_style=foreground_style, opacity=opacity)
        self._x = x
        self._y = y
        self._symbol = symbol
        self._symbol_size = symbol_size

    def _get_props(self) -> dict:
        props = self._get_base_props()
        props["x"] = _resolve_field(self._x)
        props["y"] = _resolve_field(self._y)
        if self._symbol:
            if isinstance(self._symbol, (str, SymbolShape)):
                props["symbol"] = resolve_enum(self._symbol)
            else:
                props["symbolField"] = _resolve_field(self._symbol)
        if self._symbol_size is not None:
            props["symbolSize"] = float(self._symbol_size)
        return props


class RuleMark(BaseMark):
    """Rule mark for reference lines (horizontal or vertical)."""

    _type = "RuleMark"

    def __init__(
        self,
        x: Optional[Union[str, float, PlottableField, PlottableValue]] = None,
        x_start: Optional[Union[str, float, PlottableField, PlottableValue]] = None,
        x_end: Optional[Union[str, float, PlottableField, PlottableValue]] = None,
        y: Optional[Union[str, float, PlottableField, PlottableValue]] = None,
        y_start: Optional[Union[str, float, PlottableField, PlottableValue]] = None,
        y_end: Optional[Union[str, float, PlottableField, PlottableValue]] = None,
        foreground_style: Optional[Union[str, PlottableField]] = None,
        line_width: Optional[float] = None,
        opacity: Optional[float] = None,
    ):
        super().__init__(foreground_style=foreground_style, opacity=opacity)
        self._x = x
        self._x_start = x_start
        self._x_end = x_end
        self._y = y
        self._y_start = y_start
        self._y_end = y_end
        self._line_width = line_width

    def _resolve_value(
        self, value: Optional[Union[str, float, PlottableField, PlottableValue]]
    ) -> Optional[dict]:
        """Resolve a value that could be a field reference or static value."""
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return {"value": float(value)}
        if isinstance(value, str):
            return {"field": value}
        if isinstance(value, (PlottableField, PlottableValue)):
            return value.to_dict()
        return value

    def _get_props(self) -> dict:
        props = self._get_base_props()
        if self._x is not None:
            props["x"] = self._resolve_value(self._x)
        if self._x_start is not None:
            props["xStart"] = self._resolve_value(self._x_start)
        if self._x_end is not None:
            props["xEnd"] = self._resolve_value(self._x_end)
        if self._y is not None:
            props["y"] = self._resolve_value(self._y)
        if self._y_start is not None:
            props["yStart"] = self._resolve_value(self._y_start)
        if self._y_end is not None:
            props["yEnd"] = self._resolve_value(self._y_end)
        if self._line_width is not None:
            props["lineWidth"] = float(self._line_width)
        return props


class RectMark(BaseMark):
    """Rectangle mark for heatmaps and range visualizations."""

    _type = "RectMark"

    def __init__(
        self,
        x: Optional[Union[str, PlottableField]] = None,
        x_start: Optional[Union[str, PlottableField]] = None,
        x_end: Optional[Union[str, PlottableField]] = None,
        y: Optional[Union[str, PlottableField]] = None,
        y_start: Optional[Union[str, PlottableField]] = None,
        y_end: Optional[Union[str, PlottableField]] = None,
        foreground_style: Optional[Union[str, PlottableField]] = None,
        corner_radius: Optional[float] = None,
        opacity: Optional[float] = None,
    ):
        super().__init__(foreground_style=foreground_style, opacity=opacity)
        self._x = x
        self._x_start = x_start
        self._x_end = x_end
        self._y = y
        self._y_start = y_start
        self._y_end = y_end
        self._corner_radius = corner_radius

    def _get_props(self) -> dict:
        props = self._get_base_props()
        if self._x:
            props["x"] = _resolve_field(self._x)
        if self._x_start:
            props["xStart"] = _resolve_field(self._x_start)
        if self._x_end:
            props["xEnd"] = _resolve_field(self._x_end)
        if self._y:
            props["y"] = _resolve_field(self._y)
        if self._y_start:
            props["yStart"] = _resolve_field(self._y_start)
        if self._y_end:
            props["yEnd"] = _resolve_field(self._y_end)
        if self._corner_radius is not None:
            props["cornerRadius"] = float(self._corner_radius)
        return props


class SectorMark(BaseMark):
    """Sector mark for pie and donut charts."""

    _type = "SectorMark"

    def __init__(
        self,
        angle: Union[str, PlottableField],
        foreground_style: Optional[Union[str, PlottableField]] = None,
        inner_radius: Optional[float] = None,
        outer_radius: Optional[float] = None,
        angle_start: Optional[Union[str, PlottableField]] = None,
        corner_radius: Optional[float] = None,
        opacity: Optional[float] = None,
    ):
        super().__init__(foreground_style=foreground_style, opacity=opacity)
        self._angle = angle
        self._inner_radius = inner_radius
        self._outer_radius = outer_radius
        self._angle_start = angle_start
        self._corner_radius = corner_radius

    def _get_props(self) -> dict:
        props = self._get_base_props()
        props["angle"] = _resolve_field(self._angle)
        if self._inner_radius is not None:
            props["innerRadius"] = float(self._inner_radius)
        if self._outer_radius is not None:
            props["outerRadius"] = float(self._outer_radius)
        if self._angle_start:
            props["angleStart"] = _resolve_field(self._angle_start)
        if self._corner_radius is not None:
            props["cornerRadius"] = float(self._corner_radius)
        return props
