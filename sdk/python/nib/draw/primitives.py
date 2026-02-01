"""Drawing primitives for Canvas.

This module provides shape primitives that can be drawn on a Canvas view
using Core Graphics on the Swift side.

All color values accept either:
- Hex strings: "#FF0000", "#ff0000", "FF0000"
- nib.Color objects: nib.Color.RED, nib.Color(hex="#FF0000")

Example:
    Basic shapes with nib.Color::

        import nib

        canvas.draw([
            nib.draw.Rect(x=10, y=10, width=100, height=50, fill=nib.Color.RED),
            nib.draw.Circle(cx=100, cy=100, radius=30, stroke=nib.Color.GREEN),
            nib.draw.Line(x1=0, y1=0, x2=200, y2=200, stroke=nib.Color.BLUE),
        ])

    With gradients::

        canvas.draw([
            nib.draw.Rect(
                x=10, y=10, width=100, height=100,
                fill=nib.draw.LinearGradient(
                    start=(10, 10), end=(110, 110),
                    colors=[nib.Color.RED, nib.Color.BLUE],
                ),
            ),
        ])
"""

from dataclasses import dataclass
from typing import Optional, List, Tuple, Union, Any, TYPE_CHECKING

from .paint import (
    LinearGradient,
    RadialGradient,
    SweepGradient,
    PointMode,
    serialize_fill,
    GradientOrColor,
    _resolve_color_to_hex,
)
from ..types import BlendMode, ColorLike

if TYPE_CHECKING:
    from .path import PathElement


@dataclass
class DrawCommand:
    """Base class for all drawing commands."""

    def to_dict(self) -> dict:
        """Convert command to dictionary for serialization."""
        raise NotImplementedError

    def _serialize_fill(self, fill: Optional[GradientOrColor]) -> Optional[Union[str, dict]]:
        """Serialize fill value (color or gradient)."""
        return serialize_fill(fill)


@dataclass
class Rect(DrawCommand):
    """A rectangle drawing command.

    Args:
        x: X coordinate of top-left corner.
        y: Y coordinate of top-left corner.
        width: Width of the rectangle.
        height: Height of the rectangle.
        corner_radius: Radius for rounded corners (0 for sharp corners).
        fill: Fill color (hex string or nib.Color) or gradient.
        stroke: Stroke color (hex string or nib.Color or None).
        stroke_width: Width of the stroke.
        opacity: Opacity from 0.0 to 1.0.
        blend_mode: Blend mode for compositing (nib.BlendMode).
    """

    x: float
    y: float
    width: float
    height: float
    corner_radius: float = 0
    fill: Optional[GradientOrColor] = None
    stroke: Optional[ColorLike] = None
    stroke_width: float = 1
    opacity: float = 1.0
    blend_mode: Optional[BlendMode] = None

    def to_dict(self) -> dict:
        result = {
            "type": "rect",
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "cornerRadius": self.corner_radius,
            "fill": self._serialize_fill(self.fill),
            "stroke": _resolve_color_to_hex(self.stroke) if self.stroke else None,
            "strokeWidth": self.stroke_width,
            "opacity": self.opacity,
        }
        if self.blend_mode:
            result["blendMode"] = self.blend_mode.value
        return result


@dataclass
class Circle(DrawCommand):
    """A circle drawing command.

    Args:
        cx: X coordinate of center.
        cy: Y coordinate of center.
        radius: Radius of the circle.
        fill: Fill color (hex string or nib.Color) or gradient.
        stroke: Stroke color (hex string or nib.Color or None).
        stroke_width: Width of the stroke.
        opacity: Opacity from 0.0 to 1.0.
        blend_mode: Blend mode for compositing (nib.BlendMode).
    """

    cx: float
    cy: float
    radius: float
    fill: Optional[GradientOrColor] = None
    stroke: Optional[ColorLike] = None
    stroke_width: float = 1
    opacity: float = 1.0
    blend_mode: Optional[BlendMode] = None

    def to_dict(self) -> dict:
        result = {
            "type": "circle",
            "cx": self.cx,
            "cy": self.cy,
            "radius": self.radius,
            "fill": self._serialize_fill(self.fill),
            "stroke": _resolve_color_to_hex(self.stroke) if self.stroke else None,
            "strokeWidth": self.stroke_width,
            "opacity": self.opacity,
        }
        if self.blend_mode:
            result["blendMode"] = self.blend_mode.value
        return result


@dataclass
class Ellipse(DrawCommand):
    """An ellipse drawing command.

    Args:
        cx: X coordinate of center.
        cy: Y coordinate of center.
        rx: Horizontal radius.
        ry: Vertical radius.
        fill: Fill color (hex string or nib.Color) or gradient.
        stroke: Stroke color (hex string or nib.Color or None).
        stroke_width: Width of the stroke.
        opacity: Opacity from 0.0 to 1.0.
        blend_mode: Blend mode for compositing (nib.BlendMode).
    """

    cx: float
    cy: float
    rx: float
    ry: float
    fill: Optional[GradientOrColor] = None
    stroke: Optional[ColorLike] = None
    stroke_width: float = 1
    opacity: float = 1.0
    blend_mode: Optional[BlendMode] = None

    def to_dict(self) -> dict:
        result = {
            "type": "ellipse",
            "cx": self.cx,
            "cy": self.cy,
            "rx": self.rx,
            "ry": self.ry,
            "fill": self._serialize_fill(self.fill),
            "stroke": _resolve_color_to_hex(self.stroke) if self.stroke else None,
            "strokeWidth": self.stroke_width,
            "opacity": self.opacity,
        }
        if self.blend_mode:
            result["blendMode"] = self.blend_mode.value
        return result


@dataclass
class Line(DrawCommand):
    """A line drawing command.

    Args:
        x1: X coordinate of start point.
        y1: Y coordinate of start point.
        x2: X coordinate of end point.
        y2: Y coordinate of end point.
        stroke: Stroke color (hex string or nib.Color).
        stroke_width: Width of the stroke.
        line_cap: Line cap style ("butt", "round", "square").
        opacity: Opacity from 0.0 to 1.0.
    """

    x1: float
    y1: float
    x2: float
    y2: float
    stroke: ColorLike = "#000000"
    stroke_width: float = 1
    line_cap: str = "butt"
    opacity: float = 1.0

    def to_dict(self) -> dict:
        return {
            "type": "line",
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2,
            "stroke": _resolve_color_to_hex(self.stroke),
            "strokeWidth": self.stroke_width,
            "lineCap": self.line_cap,
            "opacity": self.opacity,
        }


@dataclass
class Arc(DrawCommand):
    """An arc drawing command.

    Args:
        cx: X coordinate of center.
        cy: Y coordinate of center.
        radius: Radius of the arc.
        start_angle: Start angle in radians.
        end_angle: End angle in radians.
        clockwise: Draw clockwise direction.
        fill: Fill color (hex string or nib.Color or None).
        stroke: Stroke color (hex string or nib.Color or None).
        stroke_width: Width of the stroke.
        opacity: Opacity from 0.0 to 1.0.
    """

    cx: float
    cy: float
    radius: float
    start_angle: float
    end_angle: float
    clockwise: bool = True
    fill: Optional[ColorLike] = None
    stroke: Optional[ColorLike] = None
    stroke_width: float = 1
    opacity: float = 1.0

    def to_dict(self) -> dict:
        return {
            "type": "arc",
            "cx": self.cx,
            "cy": self.cy,
            "radius": self.radius,
            "startAngle": self.start_angle,
            "endAngle": self.end_angle,
            "clockwise": self.clockwise,
            "fill": _resolve_color_to_hex(self.fill) if self.fill else None,
            "stroke": _resolve_color_to_hex(self.stroke) if self.stroke else None,
            "strokeWidth": self.stroke_width,
            "opacity": self.opacity,
        }


@dataclass
class Path(DrawCommand):
    """A path drawing command from a list of points.

    Args:
        points: List of (x, y) coordinate tuples.
        closed: Whether to close the path back to the first point.
        fill: Fill color (hex string or nib.Color or None).
        stroke: Stroke color (hex string or nib.Color or None).
        stroke_width: Width of the stroke.
        line_join: Line join style ("miter", "round", "bevel").
        opacity: Opacity from 0.0 to 1.0.
    """

    points: List[Tuple[float, float]]
    closed: bool = False
    fill: Optional[ColorLike] = None
    stroke: Optional[ColorLike] = None
    stroke_width: float = 1
    line_join: str = "miter"
    opacity: float = 1.0

    def to_dict(self) -> dict:
        return {
            "type": "path",
            "points": [[p[0], p[1]] for p in self.points],
            "closed": self.closed,
            "fill": _resolve_color_to_hex(self.fill) if self.fill else None,
            "stroke": _resolve_color_to_hex(self.stroke) if self.stroke else None,
            "strokeWidth": self.stroke_width,
            "lineJoin": self.line_join,
            "opacity": self.opacity,
        }


@dataclass
class Polygon(DrawCommand):
    """A closed polygon drawing command.

    Convenience wrapper around Path with closed=True.

    Args:
        points: List of (x, y) coordinate tuples.
        fill: Fill color (hex string or nib.Color or None).
        stroke: Stroke color (hex string or nib.Color or None).
        stroke_width: Width of the stroke.
        opacity: Opacity from 0.0 to 1.0.
    """

    points: List[Tuple[float, float]]
    fill: Optional[ColorLike] = None
    stroke: Optional[ColorLike] = None
    stroke_width: float = 1
    opacity: float = 1.0

    def to_dict(self) -> dict:
        return {
            "type": "path",
            "points": [[p[0], p[1]] for p in self.points],
            "closed": True,
            "fill": _resolve_color_to_hex(self.fill) if self.fill else None,
            "stroke": _resolve_color_to_hex(self.stroke) if self.stroke else None,
            "strokeWidth": self.stroke_width,
            "opacity": self.opacity,
        }


@dataclass
class BezierPath(DrawCommand):
    """A bezier path drawing command with curves.

    Accepts either typed PathElement objects (recommended) or legacy dict format.

    Args:
        elements: List of PathElement objects (MoveTo, LineTo, CubicTo, etc.)
        commands: Legacy format - list of dicts (deprecated, use elements instead)
        fill: Fill color (hex string or nib.Color) or gradient.
        stroke: Stroke color (hex string or nib.Color or None).
        stroke_width: Width of the stroke.
        opacity: Opacity from 0.0 to 1.0.

    Example:
        Using typed elements (recommended)::

            from nib.draw import BezierPath, MoveTo, QuadraticTo, Close

            BezierPath(
                elements=[
                    MoveTo(25, 125),
                    QuadraticTo(cp1x=50, cp1y=25, x=135, y=35),
                    QuadraticTo(cp1x=75, cp1y=115, x=135, y=215),
                    Close(),
                ],
                fill="#F06292",
            )

        Using legacy dict format (deprecated)::

            BezierPath(
                commands=[
                    {"move": [25, 125]},
                    {"quad": [50, 25, 135, 35]},
                    {"close": True},
                ],
                fill="#F06292",
            )
    """

    elements: Optional[List["PathElement"]] = None
    commands: Optional[List[dict]] = None  # Legacy format
    fill: Optional[GradientOrColor] = None
    stroke: Optional[ColorLike] = None
    stroke_width: float = 1
    opacity: float = 1.0

    def to_dict(self) -> dict:
        # Serialize elements to the new format
        if self.elements is not None:
            serialized_elements = [el.to_dict() for el in self.elements]
        elif self.commands is not None:
            # Convert legacy format to new format
            serialized_elements = self._convert_legacy_commands()
        else:
            serialized_elements = []

        return {
            "type": "bezierPath",
            "elements": serialized_elements,
            "fill": self._serialize_fill(self.fill),
            "stroke": _resolve_color_to_hex(self.stroke) if self.stroke else None,
            "strokeWidth": self.stroke_width,
            "opacity": self.opacity,
        }

    def _convert_legacy_commands(self) -> List[dict]:
        """Convert legacy dict commands to new element format."""
        result = []
        for cmd in self.commands or []:
            if "move" in cmd:
                vals = cmd["move"]
                result.append({"type": "moveTo", "x": vals[0], "y": vals[1]})
            elif "line" in cmd:
                vals = cmd["line"]
                result.append({"type": "lineTo", "x": vals[0], "y": vals[1]})
            elif "curve" in cmd:
                vals = cmd["curve"]
                result.append({
                    "type": "cubicTo",
                    "cp1x": vals[0], "cp1y": vals[1],
                    "cp2x": vals[2], "cp2y": vals[3],
                    "x": vals[4], "y": vals[5],
                })
            elif "quad" in cmd:
                vals = cmd["quad"]
                result.append({
                    "type": "quadraticTo",
                    "cp1x": vals[0], "cp1y": vals[1],
                    "x": vals[2], "y": vals[3],
                    "w": 1.0,
                })
            elif "close" in cmd:
                result.append({"type": "close"})
        return result


@dataclass
class Points(DrawCommand):
    """A points drawing command for drawing multiple points.

    Args:
        points: List of (x, y) coordinate tuples.
        point_mode: How to interpret points (POINTS, LINES, POLYGON).
        stroke: Stroke color (hex string or nib.Color).
        stroke_width: Width of the stroke/point size.
        stroke_cap: Cap style for points/lines.
        opacity: Opacity from 0.0 to 1.0.

    Example:
        Drawing scatter points with nib.Color::

            nib.draw.Points(
                points=[(10, 10), (50, 50), (100, 30)],
                point_mode=nib.draw.PointMode.POINTS,
                stroke=nib.Color.RED,
                stroke_width=5,
            )
    """

    points: List[Tuple[float, float]]
    point_mode: PointMode = PointMode.POINTS
    stroke: ColorLike = "#000000"
    stroke_width: float = 2
    stroke_cap: str = "round"
    opacity: float = 1.0

    def to_dict(self) -> dict:
        return {
            "type": "points",
            "points": [[p[0], p[1]] for p in self.points],
            "pointMode": self.point_mode.value,
            "stroke": _resolve_color_to_hex(self.stroke),
            "strokeWidth": self.stroke_width,
            "strokeCap": self.stroke_cap,
            "opacity": self.opacity,
        }


@dataclass
class Shadow(DrawCommand):
    """A shadow drawing command for material elevation shadows.

    Args:
        path: List of (x, y) points defining the shadow shape.
        elevation: Shadow elevation (material design elevation).
        color: Shadow color (hex string or nib.Color).
        opacity: Opacity from 0.0 to 1.0.

    Example:
        Drawing a shadow for a rectangle::

            nib.draw.Shadow(
                path=[(10, 10), (110, 10), (110, 110), (10, 110)],
                elevation=10,
                color=nib.Color.BLACK,
            )
    """

    path: List[Tuple[float, float]]
    elevation: float = 5
    color: ColorLike = "#000000"
    opacity: float = 0.3

    def to_dict(self) -> dict:
        return {
            "type": "shadow",
            "path": [[p[0], p[1]] for p in self.path],
            "elevation": self.elevation,
            "color": _resolve_color_to_hex(self.color),
            "opacity": self.opacity,
        }


@dataclass
class Fill(DrawCommand):
    """Fill the entire canvas with a color or gradient.

    Args:
        fill: Fill color (hex string or nib.Color) or gradient.
        blend_mode: Blend mode for compositing (nib.BlendMode).

    Example:
        Fill canvas with white::

            nib.draw.Fill(fill=nib.Color.WHITE)

        Fill with gradient::

            nib.draw.Fill(
                fill=nib.draw.LinearGradient(
                    start=(0, 0), end=(400, 300),
                    colors=[nib.Color.RED, nib.Color.BLUE],
                )
            )
    """

    fill: GradientOrColor = "#FFFFFF"
    blend_mode: Optional[BlendMode] = None

    def to_dict(self) -> dict:
        result = {
            "type": "fill",
            "fill": self._serialize_fill(self.fill),
        }
        if self.blend_mode:
            result["blendMode"] = self.blend_mode.value
        return result


@dataclass
class ColorFill(DrawCommand):
    """Fill canvas with a color and blend mode (like Flet's Color shape).

    Args:
        color: Color to paint (hex string or nib.Color).
        blend_mode: Blend mode to apply (nib.BlendMode).

    Example:
        Tint the canvas red::

            nib.draw.ColorFill(
                color=nib.Color.RED,
                blend_mode=nib.BlendMode.MULTIPLY,
            )
    """

    color: ColorLike = "#000000"
    blend_mode: BlendMode = BlendMode.NORMAL

    def to_dict(self) -> dict:
        return {
            "type": "colorFill",
            "color": _resolve_color_to_hex(self.color),
            "blendMode": self.blend_mode.value,
        }
