"""Chart-specific types and enums for Nib Charts.

This module defines the type system for chart data encoding, including
enumerations for visual properties and classes for referencing data fields.

The types in this module are used to configure how data maps to visual
properties in chart marks. They provide type safety and clear semantics
for chart configuration.

Enumerations:
    - InterpolationMethod: Curve types for lines and areas
    - StackingMethod: How overlapping bars/areas are stacked
    - SymbolShape: Point marker shapes
    - AxisPosition: Axis placement options
    - LegendPosition: Legend placement options
    - PlottableType: Data type hints for proper scale selection

Classes:
    - PlottableField: Reference to a data column with optional type hint
    - PlottableValue: Static value for marks like RuleMark

Example:
    Using enums for mark configuration::

        LineMark(
            x="date",
            y="value",
            interpolation=InterpolationMethod.MONOTONE,
            symbol=SymbolShape.CIRCLE,
        )

    Using PlottableField for typed data::

        LineMark(
            x=PlottableField("date", type=PlottableType.TEMPORAL),
            y=PlottableField("temperature", type=PlottableType.QUANTITATIVE),
        )

    Using PlottableValue for reference lines::

        RuleMark(y=PlottableValue(100, label="Target"))
"""

from enum import Enum
from typing import Optional, Union


class InterpolationMethod(Enum):
    """Interpolation methods for line and area charts.

    Determines how the curve is drawn between data points. Different
    interpolation methods create different visual effects and are suitable
    for different types of data.

    Attributes:
        LINEAR: Straight lines between points. Best for showing exact data
            without smoothing. Default for most charts.
        MONOTONE: Smooth curve that preserves monotonicity (no artificial
            peaks/valleys between points). Best for continuous data where
            smoothness matters but overshooting would be misleading.
        CATMULL_ROM: Smooth cubic spline that passes through all points.
            Creates visually pleasing curves but may overshoot.
        CARDINAL: Smooth curve with adjustable tension. Similar to Catmull-Rom
            but with different mathematical properties.
        STEP_START: Horizontal step at each point's y-value, stepping at the
            start of each interval. Good for discrete state changes.
        STEP_CENTER: Horizontal step with the transition at the midpoint
            between data points. Centered visual appearance.
        STEP_END: Horizontal step at each point's y-value, stepping at the
            end of each interval. Good for cumulative or trailing values.

    Example:
        Smooth monotonic curve::

            LineMark(x="date", y="temp", interpolation=InterpolationMethod.MONOTONE)

        Step chart for discrete events::

            AreaMark(x="time", y="state", interpolation=InterpolationMethod.STEP_END)
    """

    LINEAR = "linear"
    MONOTONE = "monotone"
    CATMULL_ROM = "catmullRom"
    CARDINAL = "cardinal"
    STEP_START = "stepStart"
    STEP_CENTER = "stepCenter"
    STEP_END = "stepEnd"


class StackingMethod(Enum):
    """Stacking methods for bar and area charts.

    Controls how multiple series are stacked when they share the same
    x-axis position. Stacking is commonly used with BarMark and AreaMark
    to show part-to-whole relationships or compare totals.

    Attributes:
        STANDARD: Values are stacked on top of each other, showing both
            individual values and cumulative total. The y-axis scale
            reflects the sum of all series. Best for comparing totals
            while seeing individual contributions.
        NORMALIZED: Values are scaled to sum to 100% at each x position.
            Shows relative proportions rather than absolute values.
            Best for comparing composition across categories when
            totals vary significantly.
        CENTER: Values are centered around the middle axis, creating a
            streamgraph effect. The baseline varies to minimize overall
            wiggle. Best for showing flow and patterns in time series
            with many categories.

    Example:
        Stacked bar chart::

            BarMark(
                x="quarter",
                y="revenue",
                foreground_style=PlottableField("region"),
                stacking=StackingMethod.STANDARD,
            )

        100% stacked area chart::

            AreaMark(
                x="date",
                y="value",
                foreground_style=PlottableField("category"),
                stacking=StackingMethod.NORMALIZED,
            )
    """

    STANDARD = "standard"
    NORMALIZED = "normalized"
    CENTER = "center"


class SymbolShape(Enum):
    """Symbol shapes for point marks.

    Defines the geometric shape used for data point markers in PointMark
    and as optional symbols on LineMark. Different shapes can help
    distinguish series in multi-line charts or add visual interest to
    scatter plots.

    Attributes:
        CIRCLE: Filled circle. The default and most common choice.
            Works well at all sizes and densities.
        SQUARE: Filled square. Good contrast with circles for
            distinguishing series.
        TRIANGLE: Filled upward-pointing triangle. Distinctive shape
            that stands out in mixed-symbol charts.
        DIAMOND: Filled diamond (rotated square). Elegant appearance,
            good for highlighting special points.
        CROSS: X-shaped cross. Lighter visual weight, good for dense
            scatter plots where filled shapes would overlap.
        PLUS: Plus sign shape. Similar to cross but axis-aligned.
            Good for grid-aligned data.
        PENTAGON: Filled five-sided polygon. Distinctive but less
            common, useful when many series need differentiation.
        HEXAGON: Filled six-sided polygon. Works well in dense
            visualizations and hexbin plots.

    Example:
        Scatter plot with custom symbols::

            PointMark(
                x="x",
                y="y",
                symbol=SymbolShape.DIAMOND,
                symbol_size=100,
            )

        Line chart with circle markers::

            LineMark(
                x="date",
                y="value",
                symbol=SymbolShape.CIRCLE,
            )
    """

    CIRCLE = "circle"
    SQUARE = "square"
    TRIANGLE = "triangle"
    DIAMOND = "diamond"
    CROSS = "cross"
    PLUS = "plus"
    PENTAGON = "pentagon"
    HEXAGON = "hexagon"


class AxisPosition(Enum):
    """Axis position relative to the plot area.

    Specifies where an axis should be rendered in the chart. The appropriate
    values depend on whether you are configuring an x-axis or y-axis.

    Attributes:
        BOTTOM: Below the plot area. Default position for x-axis.
        TOP: Above the plot area. Alternative x-axis position for
            charts that need axis at top or dual axes.
        LEADING: Left side in left-to-right layouts. Default position
            for y-axis.
        TRAILING: Right side in left-to-right layouts. Alternative
            y-axis position for dual-axis charts.

    Example:
        X-axis at top::

            ChartAxis(position=AxisPosition.TOP, label="Date")

        Y-axis on right side::

            ChartAxis(position=AxisPosition.TRAILING, label="Value")
    """

    BOTTOM = "bottom"
    TOP = "top"
    LEADING = "leading"
    TRAILING = "trailing"


class LegendPosition(Enum):
    """Legend position relative to the chart.

    Specifies where the legend should be placed around the chart.
    Used with ChartLegend configuration.

    Attributes:
        TOP: Legend appears above the chart.
        BOTTOM: Legend appears below the chart. Common default position.
        LEADING: Legend appears on the left side (in LTR layouts).
            Useful for charts with many legend items.
        TRAILING: Legend appears on the right side (in LTR layouts).
            Traditional position for legends.
        AUTOMATIC: System determines optimal position based on
            available space and chart content.
        HIDDEN: Legend is not displayed. Equivalent to setting
            hidden=True on ChartLegend.

    Example:
        Position legend at bottom::

            ChartLegend(position=LegendPosition.BOTTOM)

        Or using string value::

            ChartLegend(position="bottom")
    """

    TOP = "top"
    BOTTOM = "bottom"
    LEADING = "leading"
    TRAILING = "trailing"
    AUTOMATIC = "automatic"
    HIDDEN = "hidden"


class PlottableType(Enum):
    """Data type hints for plottable values.

    Specifies the semantic type of data in a field, which affects how
    Swift Charts interprets and scales the data. In most cases, the
    type is inferred automatically from the data, but explicit type
    hints can be useful when the automatic inference is incorrect.

    Attributes:
        QUANTITATIVE: Numeric data on a continuous scale. Values are
            treated as measurements that can be compared, added, or
            averaged. Examples: temperature, revenue, count.
            Uses a linear numeric scale.
        NOMINAL: Categorical data with no inherent order. Values are
            treated as discrete categories. Examples: country names,
            product types, colors.
            Uses a discrete band scale.
        TEMPORAL: Date or time data. Values are treated as points in
            time and displayed on a time-aware scale with appropriate
            tick marks (days, months, years, etc.).
            Uses a time scale with intelligent tick formatting.

    Example:
        Explicitly typed temporal field::

            PlottableField("date", type=PlottableType.TEMPORAL)

        Force numeric treatment of string IDs::

            PlottableField("year", type=PlottableType.NOMINAL)
    """

    QUANTITATIVE = "quantitative"  # Numbers (continuous scale)
    NOMINAL = "nominal"            # Categories (discrete scale)
    TEMPORAL = "temporal"          # Dates/times (time scale)


class PlottableField:
    """Reference to a data column for chart encoding.

    PlottableField provides a way to reference a column in your chart data
    with optional type information. While you can usually pass field names
    as simple strings, PlottableField is useful when you need to:

    1. Specify an explicit data type (quantitative, nominal, temporal)
    2. Create more self-documenting code
    3. Enable IDE autocompletion for field types

    Attributes:
        field: The name of the data column to reference.

    Example:
        Basic field reference (equivalent to just using "sales")::

            PlottableField("sales")

        Typed temporal field::

            PlottableField("date", type=PlottableType.TEMPORAL)

        Using with marks::

            LineMark(
                x=PlottableField("timestamp", type="temporal"),
                y=PlottableField("temperature", type="quantitative"),
            )

        For color encoding by category::

            LineMark(
                x="date",
                y="value",
                foreground_style=PlottableField("category"),  # Colors by category
            )
    """

    def __init__(
        self,
        field: str,
        type: Optional[Union[PlottableType, str]] = None,
    ):
        """Initialize a PlottableField.

        Args:
            field: Name of the data column to reference. Must match a key
                in your chart's data dictionaries.
            type: Optional data type hint. Can be a PlottableType enum value
                or a string ("quantitative", "nominal", "temporal"). If not
                specified, the type is inferred from the data values.
        """
        self.field = field
        if type is None:
            self._type = None
        elif isinstance(type, PlottableType):
            self._type = type.value
        else:
            self._type = type

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization.

        Returns:
            Dictionary with "field" key and optional "type" key.
        """
        result = {"field": self.field}
        if self._type:
            result["type"] = self._type
        return result


class PlottableValue:
    """Static value for chart encoding.

    PlottableValue represents a fixed value rather than a reference to a
    data field. It is primarily used with RuleMark to create reference
    lines at specific positions, with an optional label for annotation.

    Unlike PlottableField which pulls values from your data, PlottableValue
    specifies a constant that applies to all data points or stands alone.

    Attributes:
        value: The static value (number or string).
        label: Optional label to display with the value.

    Example:
        Reference line at a fixed value::

            RuleMark(y=PlottableValue(100, label="Target"))

        Threshold line::

            RuleMark(
                y=PlottableValue(0, label="Baseline"),
                foreground_style="#666666",
                line_width=1,
            )

        Note that for simple numeric values without labels, you can
        just pass the number directly::

            RuleMark(y=100)  # Equivalent to PlottableValue(100)
    """

    def __init__(
        self,
        value: Union[int, float, str],
        label: Optional[str] = None,
    ):
        """Initialize a PlottableValue.

        Args:
            value: The static value. Can be a number (int or float) for
                quantitative axes, or a string for categorical axes.
            label: Optional label text to display alongside the value.
                Useful for annotating reference lines with descriptive
                text like "Target" or "Average".
        """
        self.value = value
        self.label = label

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization.

        Returns:
            Dictionary with "value" key and optional "label" key.
        """
        result = {"value": self.value}
        if self.label:
            result["label"] = self.label
        return result
