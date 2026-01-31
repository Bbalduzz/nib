"""Chart mark classes for Nib Charts.

This module provides mark classes that define how data is visually represented
in charts. Marks are the visual elements of a chart - lines, bars, areas,
points, and other shapes that encode data values.

Each mark type maps data fields to visual properties. For example, a LineMark
maps x and y data fields to positions along a line, while a BarMark maps
fields to bar heights and positions.

Marks support visual customization through properties like foreground_style
(color), opacity, and mark-specific options like line_width or corner_radius.

Available Marks:
    - LineMark: Line charts with optional symbols and interpolation
    - BarMark: Vertical or horizontal bar charts with stacking support
    - AreaMark: Filled area charts with stacking and interpolation
    - PointMark: Scatter plots with customizable symbols
    - RuleMark: Reference lines (horizontal or vertical)
    - RectMark: Rectangle marks for heatmaps and range visualizations
    - SectorMark: Pie and donut chart segments

Coordinate system:
    (0,0)-----(1,0)
        |         |
        |  (0.5,0.5)
        |         |
    (0,1)-----(1,1)

Example:
    Simple line chart mark::

        mark = LineMark(x="date", y="value")

    Styled bar chart mark::

        mark = BarMark(
            x="category",
            y="sales",
            foreground_style="blue",
            corner_radius=4,
        )

    Multi-series with color encoding::

        mark = LineMark(
            x="date",
            y="value",
            foreground_style=PlottableField("series"),  # Color by series
        )
"""

from typing import Optional, Union

from ...types import resolve_enum
from .types import (
    InterpolationMethod,
    PlottableField,
    PlottableValue,
    StackingMethod,
    SymbolShape,
)

GRADIENT_TYPES = (
    "LinearGradient",
    "RadialGradient",
    "AngularGradient",
    "EllipticalGradient",
)


def _is_color_string(value: str) -> bool:
    """Check if a string looks like a color value rather than a field name."""
    # Hex colors: #RGB, #RRGGBB, #RRGGBBAA
    if value.startswith("#"):
        return True
    # RGB/RGBA: rgb(...) or rgba(...)
    if value.startswith("rgb"):
        return True
    # Named CSS colors (common ones)
    named_colors = {
        "white",
        "black",
        "red",
        "green",
        "blue",
        "yellow",
        "orange",
        "purple",
        "pink",
        "cyan",
        "magenta",
        "gray",
        "grey",
        "brown",
        "clear",
        "transparent",
    }
    if value.lower() in named_colors:
        return True
    return False


def _resolve_field(
    value: Optional[Union[str, PlottableField, PlottableValue]],
) -> Optional[dict]:
    """Convert a field reference to dictionary format for serialization.

    This helper function normalizes different ways of specifying data field
    references into a consistent dictionary format that the Swift runtime
    expects.

    Args:
        value: The field reference to resolve. Can be:
            - None: Returns None
            - str: If it looks like a color (hex, rgb, named), returns {"color": value}
                   Otherwise interpreted as a field name, returns {"field": value}
            - PlottableField: Calls its to_dict() method
            - PlottableValue: Calls its to_dict() method
            - Gradient View: Returns gradient data with gradientType

    Returns:
        Dictionary representation of the field reference, or None if the
        input was None.

    Example:
        >>> _resolve_field("sales")
        {"field": "sales"}
        >>> _resolve_field("#ffffff")
        {"color": "#ffffff"}
        >>> _resolve_field(PlottableField("date", type="temporal"))
        {"field": "date", "type": "temporal"}
        >>> _resolve_field(LinearGradient(colors=["red", "blue"]))
        {"gradientType": "LinearGradient", "colors": [...], ...}
    """
    if value is None:
        return None
    # Check for gradient Views
    if hasattr(value, "_type") and value._type in GRADIENT_TYPES:
        result = {"gradientType": value._type}
        result.update(value._get_props())
        return result
    if isinstance(value, str):
        if _is_color_string(value):
            return {"color": value}
        return {"field": value}
    if isinstance(value, (PlottableField, PlottableValue)):
        return value.to_dict()
    return value


class BaseMark:
    """Base class for all chart marks.

    BaseMark provides the common interface and functionality shared by all
    mark types. It handles common visual properties like foreground_style
    and opacity, and defines the serialization interface.

    Subclasses should override _get_props() to add mark-specific properties
    while calling _get_base_props() to include the common properties.

    This class is not meant to be instantiated directly. Use one of the
    concrete mark classes like LineMark, BarMark, etc.

    Attributes:
        _type: String identifier for the mark type, used in serialization.
    """

    _type: str = "Mark"

    def __init__(
        self,
        foreground_style: Optional[Union[str, PlottableField]] = None,
        opacity: Optional[float] = None,
    ):
        """Initialize common mark properties.

        Args:
            foreground_style: Color or data field for the mark's fill/stroke.
                Can be a hex color string (e.g., "#FF5733"), a named color
                (e.g., "blue"), or a PlottableField to encode color based
                on data values (for automatic color assignment per category).
            opacity: Opacity of the mark from 0.0 (transparent) to 1.0 (opaque).
                Defaults to None (uses system default, typically 1.0).
        """
        self._foreground_style = foreground_style
        self._opacity = opacity

    def _get_base_props(self) -> dict:
        """Get common mark properties shared by all mark types.

        Returns:
            Dictionary containing foregroundStyle and opacity if set.
        """
        props = {}
        if self._foreground_style:
            props["foregroundStyle"] = _resolve_field(self._foreground_style)
        if self._opacity is not None:
            props["opacity"] = float(self._opacity)
        return props

    def to_dict(self, path: str = "0") -> dict:
        """Convert mark to dictionary for serialization.

        Produces a dictionary representation suitable for sending to the
        Swift runtime via MessagePack.

        Args:
            path: The path identifier for this mark in the view tree.
                Defaults to "0".

        Returns:
            Dictionary containing the mark's id, type, and properties.
        """
        return {
            "id": path,
            "type": self._type,
            "props": self._get_props(),
        }

    def _get_props(self) -> dict:
        """Get mark-specific properties for serialization.

        Override this method in subclasses to add mark-specific properties.
        Always call _get_base_props() to include common properties.

        Returns:
            Dictionary containing all mark properties.
        """
        return self._get_base_props()


class LineMark(BaseMark):
    """Line mark for creating line charts.

    LineMark connects data points with a continuous line, ideal for showing
    trends over time or continuous relationships between variables. Lines
    can be styled with different colors, widths, and interpolation methods.

    Optionally, symbols (markers) can be added at each data point for better
    visibility of individual values.

    Example:
        Basic line chart::

            LineMark(x="date", y="temperature")

        Styled line with symbols::

            LineMark(
                x="month",
                y="sales",
                foreground_style="#3B82F6",
                symbol=SymbolShape.CIRCLE,
                line_width=2.0,
                interpolation=InterpolationMethod.MONOTONE,
            )

        Multi-series line chart (color by category)::

            LineMark(
                x="date",
                y="value",
                foreground_style=PlottableField("series"),
            )
    """

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
        """Initialize a LineMark.

        Args:
            x: Data field for the x-axis position. Can be a string field name
                or a PlottableField for additional type information.
            y: Data field for the y-axis position. Can be a string field name
                or a PlottableField for additional type information.
            foreground_style: Line color. Can be a hex color string, named
                color, or PlottableField to color lines by a data category.
            symbol: Shape for data point markers. Can be a SymbolShape enum
                value (CIRCLE, SQUARE, TRIANGLE, etc.), a string, or a
                PlottableField to vary symbols by data category.
            interpolation: Method for interpolating between points. Options
                include LINEAR, MONOTONE, CATMULL_ROM, CARDINAL, STEP_START,
                STEP_CENTER, and STEP_END. Defaults to LINEAR.
            line_width: Width of the line in points. Defaults to system default.
            opacity: Opacity from 0.0 to 1.0. Defaults to 1.0.
        """
        super().__init__(foreground_style=foreground_style, opacity=opacity)
        self._x = x
        self._y = y
        self._symbol = symbol
        self._interpolation = interpolation
        self._line_width = line_width

    def _get_props(self) -> dict:
        """Get LineMark properties for serialization.

        Returns:
            Dictionary containing x, y, and optional symbol, interpolation,
            and line_width properties.
        """
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
    """Bar mark for creating bar charts.

    BarMark displays data as rectangular bars, ideal for comparing discrete
    categories or showing distribution of values. Bars can be oriented
    vertically (default) or horizontally, and support stacking for
    multi-series comparisons.

    The orientation is determined by which fields are categorical vs.
    quantitative. For vertical bars, x is typically categorical and y is
    quantitative. For horizontal bars, swap the fields.

    Example:
        Simple vertical bar chart::

            BarMark(x="category", y="value")

        Horizontal bar chart::

            BarMark(x="value", y="category")

        Stacked bar chart::

            BarMark(
                x="month",
                y="sales",
                foreground_style=PlottableField("region"),
                stacking=StackingMethod.STANDARD,
            )

        Styled bars::

            BarMark(
                x="product",
                y="revenue",
                foreground_style="#10B981",
                corner_radius=4,
            )
    """

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
        """Initialize a BarMark.

        Args:
            x: Data field for the x-axis. For vertical bars, this is typically
                the categorical field. Can be None for single-value charts.
            y: Data field for the y-axis. For vertical bars, this is typically
                the quantitative field (bar height). Can be None for
                single-value charts.
            width: Fixed width for bars in points. If not specified, bars
                are sized automatically based on available space.
            height: Fixed height for bars in points. If not specified, bars
                are sized based on the y data values.
            foreground_style: Bar fill color. Can be a hex color, named color,
                or PlottableField to color bars by category (creates grouped
                or stacked bars).
            stacking: How to stack bars when multiple series overlap. Options:
                STANDARD (stacked), NORMALIZED (100% stacked), CENTER (centered).
                Defaults to None (no stacking, bars are grouped).
            corner_radius: Radius for rounded bar corners in points.
            opacity: Opacity from 0.0 to 1.0. Defaults to 1.0.
        """
        super().__init__(foreground_style=foreground_style, opacity=opacity)
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._stacking = stacking
        self._corner_radius = corner_radius

    def _get_props(self) -> dict:
        """Get BarMark properties for serialization.

        Returns:
            Dictionary containing bar configuration including position fields,
            dimensions, stacking mode, and corner radius.
        """
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
    """Area mark for creating filled area charts.

    AreaMark fills the region between a line and a baseline (typically zero
    or another line), creating a visual representation of cumulative values
    or ranges. Area charts are effective for showing magnitude over time
    and support stacking for multi-series data.

    By default, the area extends from zero to the y value. Use y_start to
    create range areas or band charts.

    Example:
        Basic area chart::

            AreaMark(x="date", y="revenue")

        Stacked area chart::

            AreaMark(
                x="month",
                y="sales",
                foreground_style=PlottableField("category"),
                stacking=StackingMethod.STANDARD,
            )

        Range/band area::

            AreaMark(
                x="date",
                y="high",
                y_start="low",
                foreground_style="#3B82F6",
                opacity=0.3,
            )

        Smooth area with custom interpolation::

            AreaMark(
                x="date",
                y="value",
                interpolation=InterpolationMethod.MONOTONE,
            )
    """

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
        """Initialize an AreaMark.

        Args:
            x: Data field for the x-axis position.
            y: Data field for the upper boundary of the area (y-axis).
            y_start: Data field for the lower boundary of the area. If not
                specified, the area extends from zero (or the axis minimum)
                to the y value. Use this for range or band visualizations.
            foreground_style: Fill color for the area. Can be a hex color,
                named color, or PlottableField for multi-series coloring.
            interpolation: Curve interpolation method. Options include LINEAR,
                MONOTONE, CATMULL_ROM, CARDINAL, and step variants.
            stacking: Stacking mode for multi-series areas. Options: STANDARD
                (stacked), NORMALIZED (100% stacked), CENTER (stream graph).
            opacity: Fill opacity from 0.0 to 1.0. Consider using lower
                opacity (0.3-0.7) for overlapping areas.
        """
        super().__init__(foreground_style=foreground_style, opacity=opacity)
        self._x = x
        self._y = y
        self._y_start = y_start
        self._interpolation = interpolation
        self._stacking = stacking

    def _get_props(self) -> dict:
        """Get AreaMark properties for serialization.

        Returns:
            Dictionary containing x, y, and optional y_start, interpolation,
            and stacking properties.
        """
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
    """Point mark for creating scatter plots.

    PointMark displays individual data points as symbols, ideal for showing
    relationships between two quantitative variables or highlighting
    specific data points. Each point can be customized with different
    shapes, sizes, and colors.

    PointMark is commonly used for scatter plots, bubble charts (with
    size encoding), and adding data point markers to other chart types.

    Example:
        Basic scatter plot::

            PointMark(x="height", y="weight")

        Colored by category::

            PointMark(
                x="sepal_length",
                y="sepal_width",
                foreground_style=PlottableField("species"),
            )

        Custom symbols and size::

            PointMark(
                x="x",
                y="y",
                symbol=SymbolShape.DIAMOND,
                symbol_size=100,
                foreground_style="#EF4444",
            )

        Symbols varying by data::

            PointMark(
                x="x",
                y="y",
                symbol=PlottableField("category"),  # Different symbol per category
            )
    """

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
        """Initialize a PointMark.

        Args:
            x: Data field for the x-axis position.
            y: Data field for the y-axis position.
            foreground_style: Point fill color. Can be a hex color, named
                color, or PlottableField to color points by category.
            symbol: Shape of the point marker. Can be a SymbolShape enum
                (CIRCLE, SQUARE, TRIANGLE, DIAMOND, CROSS, PLUS, PENTAGON,
                HEXAGON), a string, or a PlottableField to vary symbols
                by data category.
            symbol_size: Size of the symbol in square points. Larger values
                create bigger markers. Defaults to system default.
            opacity: Opacity from 0.0 to 1.0. Useful for dense scatter plots
                where points overlap.
        """
        super().__init__(foreground_style=foreground_style, opacity=opacity)
        self._x = x
        self._y = y
        self._symbol = symbol
        self._symbol_size = symbol_size

    def _get_props(self) -> dict:
        """Get PointMark properties for serialization.

        Returns:
            Dictionary containing x, y, and optional symbol and symbol_size
            properties.
        """
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
    """Rule mark for reference lines (horizontal or vertical).

    RuleMark draws straight lines across the chart, useful for showing
    thresholds, averages, targets, or other reference values. Rules can
    be horizontal (fixed y, spanning x) or vertical (fixed x, spanning y).

    Rules can also be bounded to create line segments between specific
    start and end points.

    Example:
        Horizontal reference line (e.g., target line)::

            RuleMark(y=100, foreground_style="#EF4444", line_width=2)

        Vertical reference line (e.g., event marker)::

            RuleMark(x="2024-06-15", foreground_style="#6366F1")

        Bounded horizontal segment::

            RuleMark(
                y=50,
                x_start="Jan",
                x_end="Jun",
                foreground_style="#10B981",
            )

        Data-driven rules (one rule per data point)::

            RuleMark(
                y="threshold",  # Field name - creates rule for each row
                foreground_style="#F59E0B",
            )
    """

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
        """Initialize a RuleMark.

        Specify either x (for vertical line) or y (for horizontal line),
        along with optional start/end bounds.

        Args:
            x: X-axis position for a vertical rule. Can be a static value
                (number), a field name (string), PlottableField, or
                PlottableValue.
            x_start: Starting x position when creating a bounded horizontal
                rule segment.
            x_end: Ending x position when creating a bounded horizontal
                rule segment.
            y: Y-axis position for a horizontal rule. Can be a static value
                (number), a field name (string), PlottableField, or
                PlottableValue.
            y_start: Starting y position when creating a bounded vertical
                rule segment.
            y_end: Ending y position when creating a bounded vertical
                rule segment.
            foreground_style: Line color. Can be a hex color, named color,
                or PlottableField.
            line_width: Width of the rule line in points.
            opacity: Opacity from 0.0 to 1.0.
        """
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
        """Resolve a value that could be a field reference or static value.

        Args:
            value: The value to resolve. Can be a number (static value),
                string (field name), or PlottableField/PlottableValue object.

        Returns:
            Dictionary with either a "value" key (for static values) or
            "field" key (for field references), or None if input is None.
        """
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
        """Get RuleMark properties for serialization.

        Returns:
            Dictionary containing position and bounds for the rule line.
        """
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
    """Rectangle mark for heatmaps and range visualizations.

    RectMark draws filled rectangles defined by their bounds in data space.
    It is ideal for creating heatmaps, Gantt charts, range visualizations,
    and other grid-based charts where each cell represents a data value.

    Rectangles can be positioned using either center points (x, y) or
    explicit bounds (x_start/x_end, y_start/y_end).

    Example:
        Heatmap cell (positioned by category)::

            RectMark(
                x="weekday",
                y="hour",
                foreground_style=PlottableField("intensity"),
            )

        Range/Gantt chart::

            RectMark(
                x_start="start_date",
                x_end="end_date",
                y="task",
                foreground_style=PlottableField("status"),
                corner_radius=4,
            )

        Calendar heatmap::

            RectMark(
                x="week",
                y="day_of_week",
                foreground_style=PlottableField("value"),
                corner_radius=2,
            )
    """

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
        """Initialize a RectMark.

        Use x/y for categorical positioning (cells sized automatically) or
        x_start/x_end and y_start/y_end for explicit bounds.

        Args:
            x: Data field for the x-axis center position. Used for
                categorical grids where cell width is automatic.
            x_start: Data field for the left edge of the rectangle.
            x_end: Data field for the right edge of the rectangle.
            y: Data field for the y-axis center position. Used for
                categorical grids where cell height is automatic.
            y_start: Data field for the bottom edge of the rectangle.
            y_end: Data field for the top edge of the rectangle.
            foreground_style: Fill color for the rectangle. Can be a hex
                color, named color, or PlottableField to encode values
                as colors (essential for heatmaps).
            corner_radius: Radius for rounded corners in points.
            opacity: Opacity from 0.0 to 1.0.
        """
        super().__init__(foreground_style=foreground_style, opacity=opacity)
        self._x = x
        self._x_start = x_start
        self._x_end = x_end
        self._y = y
        self._y_start = y_start
        self._y_end = y_end
        self._corner_radius = corner_radius

    def _get_props(self) -> dict:
        """Get RectMark properties for serialization.

        Returns:
            Dictionary containing position and bounds for the rectangle.
        """
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
    """Sector mark for pie and donut charts.

    SectorMark creates circular segments (wedges) based on angular data,
    perfect for showing proportional relationships and part-to-whole
    comparisons. By adjusting the inner radius, you can create donut
    charts instead of pie charts.

    The angle field determines the size of each sector proportionally.
    Use foreground_style with a PlottableField to automatically assign
    colors to each category.

    Example:
        Pie chart::

            SectorMark(
                angle="value",
                foreground_style=PlottableField("category"),
            )

        Donut chart::

            SectorMark(
                angle="percentage",
                foreground_style=PlottableField("segment"),
                inner_radius=50,
                outer_radius=100,
            )

        Styled donut with rounded segments::

            SectorMark(
                angle="sales",
                foreground_style=PlottableField("region"),
                inner_radius=40,
                outer_radius=80,
                corner_radius=4,
            )
    """

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
        """Initialize a SectorMark.

        Args:
            angle: Data field containing values that determine sector sizes.
                Values are treated proportionally - a sector with value 20
                will be twice as large as one with value 10.
            foreground_style: Fill color for sectors. Use a PlottableField
                with a categorical field (e.g., "category") to automatically
                assign different colors to each sector.
            inner_radius: Inner radius in points. Set to 0 for a pie chart,
                or a positive value for a donut chart. Defaults to 0.
            outer_radius: Outer radius in points. Defaults to automatic
                sizing based on available space.
            angle_start: Data field or value for the starting angle of
                sectors. Rarely needed; use for custom sector positioning.
            corner_radius: Radius for rounded sector corners in points.
                Creates a softer visual appearance.
            opacity: Opacity from 0.0 to 1.0.
        """
        super().__init__(foreground_style=foreground_style, opacity=opacity)
        self._angle = angle
        self._inner_radius = inner_radius
        self._outer_radius = outer_radius
        self._angle_start = angle_start
        self._corner_radius = corner_radius

    def _get_props(self) -> dict:
        """Get SectorMark properties for serialization.

        Returns:
            Dictionary containing angle field and optional radius and
            corner_radius properties.
        """
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
