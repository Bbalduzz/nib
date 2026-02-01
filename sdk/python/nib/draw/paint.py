"""Paint and gradient classes for Canvas drawing.

This module provides Paint styling and gradient fills for Canvas primitives.

All color values accept either:
- Hex strings: "#FF0000", "#ff0000", "FF0000"
- nib.Color objects: nib.Color.RED, nib.Color(hex="#FF0000")

Example:
    Using gradients with nib.Color::

        import nib

        # Linear gradient with nib.Color
        canvas.draw([
            nib.draw.Rect(
                x=10, y=10, width=100, height=100,
                fill=nib.draw.LinearGradient(
                    start=(0, 0),
                    end=(100, 100),
                    colors=[nib.Color.RED, nib.Color.BLUE],
                ),
            ),
        ])

        # Radial gradient with hex colors
        canvas.draw([
            nib.draw.Circle(
                cx=100, cy=100, radius=50,
                fill=nib.draw.RadialGradient(
                    center=(100, 100),
                    radius=50,
                    colors=["#FFFF00", "#FF0000"],
                ),
            ),
        ])
"""

from dataclasses import dataclass
from typing import Optional, List, Tuple, Union
from enum import Enum

# Import nib types for integration
from ..types import Color, ColorLike, resolve_color, BlendMode


class PaintStyle(Enum):
    """Paint style enumeration."""
    FILL = "fill"
    STROKE = "stroke"


class StrokeCap(Enum):
    """Stroke cap style."""
    BUTT = "butt"
    ROUND = "round"
    SQUARE = "square"


class StrokeJoin(Enum):
    """Stroke join style."""
    MITER = "miter"
    ROUND = "round"
    BEVEL = "bevel"


class PointMode(Enum):
    """Point drawing mode."""
    POINTS = "points"      # Draw each point as a dot
    LINES = "lines"        # Draw lines between pairs of points
    POLYGON = "polygon"    # Draw connected line segments


def _resolve_color_to_hex(color: ColorLike) -> str:
    """Convert a ColorLike value to a hex string for Core Graphics.

    Args:
        color: A Color instance, hex string, or named color string.

    Returns:
        A string suitable for Core Graphics (hex or named color).
    """
    if isinstance(color, Color):
        # Color.to_dict() returns the value, possibly with opacity
        return color.to_dict()
    return color


@dataclass
class LinearGradient:
    """A linear gradient fill.

    Args:
        start: Starting point (x, y) of the gradient in pixels.
        end: Ending point (x, y) of the gradient in pixels.
        colors: List of colors (hex strings or nib.Color objects).
        stops: Optional list of stop positions (0.0 to 1.0).

    Example:
        Using nib.Color::

            nib.draw.LinearGradient(
                start=(0, 0),
                end=(100, 100),
                colors=[nib.Color.RED, nib.Color.BLUE],
            )
    """
    start: Tuple[float, float]
    end: Tuple[float, float]
    colors: List[ColorLike]
    stops: Optional[List[float]] = None

    def to_dict(self) -> dict:
        result = {
            "type": "linear",
            "start": list(self.start),
            "end": list(self.end),
            "colors": [_resolve_color_to_hex(c) for c in self.colors],
        }
        if self.stops:
            result["stops"] = self.stops
        return result


@dataclass
class RadialGradient:
    """A radial gradient fill.

    Args:
        center: Center point (x, y) of the gradient in pixels.
        radius: Radius of the gradient in pixels.
        colors: List of colors (hex strings or nib.Color objects).
        stops: Optional list of stop positions (0.0 to 1.0).
        focus: Optional focus point (x, y) for off-center gradients.

    Example:
        Using nib.Color::

            nib.draw.RadialGradient(
                center=(100, 100),
                radius=50,
                colors=[nib.Color.YELLOW, nib.Color.RED],
            )
    """
    center: Tuple[float, float]
    radius: float
    colors: List[ColorLike]
    stops: Optional[List[float]] = None
    focus: Optional[Tuple[float, float]] = None

    def to_dict(self) -> dict:
        result = {
            "type": "radial",
            "center": list(self.center),
            "radius": self.radius,
            "colors": [_resolve_color_to_hex(c) for c in self.colors],
        }
        if self.stops:
            result["stops"] = self.stops
        if self.focus:
            result["focus"] = list(self.focus)
        return result


@dataclass
class SweepGradient:
    """A sweep (conic/angular) gradient fill.

    Args:
        center: Center point (x, y) of the gradient in pixels.
        colors: List of colors (hex strings or nib.Color objects).
        stops: Optional list of stop positions (0.0 to 1.0).
        start_angle: Starting angle in radians (default 0).
        end_angle: Ending angle in radians (default 2*pi).

    Example:
        Color wheel::

            nib.draw.SweepGradient(
                center=(100, 100),
                colors=[nib.Color.RED, nib.Color.GREEN, nib.Color.BLUE, nib.Color.RED],
            )
    """
    center: Tuple[float, float]
    colors: List[ColorLike]
    stops: Optional[List[float]] = None
    start_angle: float = 0
    end_angle: float = 6.283185307  # 2 * pi

    def to_dict(self) -> dict:
        result = {
            "type": "sweep",
            "center": list(self.center),
            "colors": [_resolve_color_to_hex(c) for c in self.colors],
            "startAngle": self.start_angle,
            "endAngle": self.end_angle,
        }
        if self.stops:
            result["stops"] = self.stops
        return result


@dataclass
class Blur:
    """Blur effect for paint.

    Args:
        sigma_x: Horizontal blur radius.
        sigma_y: Vertical blur radius (defaults to sigma_x).
        style: Blur style ("normal", "solid", "outer", "inner").
    """
    sigma_x: float
    sigma_y: Optional[float] = None
    style: str = "normal"

    def to_dict(self) -> dict:
        return {
            "sigmaX": self.sigma_x,
            "sigmaY": self.sigma_y if self.sigma_y is not None else self.sigma_x,
            "style": self.style,
        }


# Type alias for gradient or color (accepts nib.Color or hex strings)
GradientOrColor = Union[ColorLike, LinearGradient, RadialGradient, SweepGradient]


def serialize_fill(fill: Optional[GradientOrColor]) -> Optional[Union[str, dict]]:
    """Serialize a fill value (color or gradient) for transmission.

    Args:
        fill: A color (hex string or nib.Color) or gradient object.

    Returns:
        Serialized fill for transmission to Swift.
    """
    if fill is None:
        return None
    if isinstance(fill, Color):
        return fill.to_dict()
    if isinstance(fill, str):
        return fill
    if hasattr(fill, "to_dict"):
        return {"gradient": fill.to_dict()}
    return None


@dataclass
class Paint:
    """Paint defines the style for drawing shapes.

    This is the equivalent of a "paintbrush" that determines color,
    stroke width, fill style, gradients, and more.

    Args:
        color: Color to use (hex string or nib.Color).
        style: FILL or STROKE.
        stroke_width: Width of strokes.
        stroke_cap: Shape at line ends (BUTT, ROUND, SQUARE).
        stroke_join: Shape at corners (MITER, ROUND, BEVEL).
        stroke_miter_limit: Limit for miter joins.
        opacity: Opacity from 0.0 to 1.0.
        blend_mode: Blend mode for compositing (nib.BlendMode).
        gradient: Gradient fill (overrides color for fill).
        blur: Blur effect.
        anti_alias: Whether to apply anti-aliasing.

    Example:
        Creating a paint with gradient and nib.Color::

            paint = nib.draw.Paint(
                gradient=nib.draw.LinearGradient(
                    start=(0, 0),
                    end=(100, 100),
                    colors=[nib.Color.RED, nib.Color.BLUE],
                ),
                style=nib.draw.PaintStyle.FILL,
            )

        Using nib.BlendMode::

            paint = nib.draw.Paint(
                color=nib.Color.RED,
                blend_mode=nib.BlendMode.MULTIPLY,
            )
    """
    color: Optional[ColorLike] = None
    style: PaintStyle = PaintStyle.FILL
    stroke_width: float = 1.0
    stroke_cap: StrokeCap = StrokeCap.BUTT
    stroke_join: StrokeJoin = StrokeJoin.MITER
    stroke_miter_limit: float = 4.0
    opacity: float = 1.0
    blend_mode: Optional[BlendMode] = None
    gradient: Optional[Union[LinearGradient, RadialGradient, SweepGradient]] = None
    blur: Optional[Blur] = None
    anti_alias: bool = True

    def to_dict(self) -> dict:
        result = {
            "style": self.style.value,
            "strokeWidth": self.stroke_width,
            "strokeCap": self.stroke_cap.value,
            "strokeJoin": self.stroke_join.value,
            "strokeMiterLimit": self.stroke_miter_limit,
            "opacity": self.opacity,
            "antiAlias": self.anti_alias,
        }
        if self.color:
            result["color"] = _resolve_color_to_hex(self.color)
        if self.blend_mode:
            result["blendMode"] = self.blend_mode.value
        if self.gradient:
            result["gradient"] = self.gradient.to_dict()
        if self.blur:
            result["blur"] = self.blur.to_dict()
        return result
