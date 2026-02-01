"""Path elements for BezierPath drawing.

This module provides typed path elements for constructing bezier paths,
similar to Flet's Canvas Path API.

Example:
    Drawing a heart shape::

        import nib
        from nib.draw import BezierPath, MoveTo, CubicTo, Close

        canvas.draw([
            BezierPath(
                elements=[
                    MoveTo(100, 50),
                    CubicTo(cp1x=100, cp1y=0, cp2x=50, cp2y=0, x=50, y=50),
                    CubicTo(cp1x=50, cp1y=80, cp2x=100, cp2y=120, x=100, y=150),
                    CubicTo(cp1x=100, cp1y=120, cp2x=150, cp2y=80, x=150, y=50),
                    CubicTo(cp1x=150, cp1y=0, cp2x=100, cp2y=0, x=100, y=50),
                    Close(),
                ],
                fill="#FF0000",
            ),
        ])
"""

from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class PathElement:
    """Base class for path elements."""

    def to_dict(self) -> dict:
        """Convert element to dictionary for serialization."""
        raise NotImplementedError


@dataclass
class MoveTo(PathElement):
    """Starts a new sub-path at the given point (x, y).

    Args:
        x: X coordinate of the point.
        y: Y coordinate of the point.
    """

    x: float
    y: float

    def to_dict(self) -> dict:
        return {"type": "moveTo", "x": self.x, "y": self.y}


@dataclass
class LineTo(PathElement):
    """Adds a straight line segment from the current point to the given point (x, y).

    Args:
        x: X coordinate of the endpoint.
        y: Y coordinate of the endpoint.
    """

    x: float
    y: float

    def to_dict(self) -> dict:
        return {"type": "lineTo", "x": self.x, "y": self.y}


@dataclass
class Close(PathElement):
    """Closes the last sub-path.

    Draws a straight line from the current point to the first point of the sub-path.
    """

    def to_dict(self) -> dict:
        return {"type": "close"}


@dataclass
class CubicTo(PathElement):
    """Adds a cubic bezier segment from the current point to (x, y).

    Uses control points (cp1x, cp1y) and (cp2x, cp2y).

    Args:
        cp1x: First control point X coordinate.
        cp1y: First control point Y coordinate.
        cp2x: Second control point X coordinate.
        cp2y: Second control point Y coordinate.
        x: Endpoint X coordinate.
        y: Endpoint Y coordinate.
    """

    cp1x: float
    cp1y: float
    cp2x: float
    cp2y: float
    x: float
    y: float

    def to_dict(self) -> dict:
        return {
            "type": "cubicTo",
            "cp1x": self.cp1x,
            "cp1y": self.cp1y,
            "cp2x": self.cp2x,
            "cp2y": self.cp2y,
            "x": self.x,
            "y": self.y,
        }


@dataclass
class QuadraticTo(PathElement):
    """Adds a quadratic bezier segment from the current point to (x, y).

    Uses control point (cp1x, cp1y) and optional weight w for conic sections.

    Args:
        cp1x: Control point X coordinate.
        cp1y: Control point Y coordinate.
        x: Endpoint X coordinate.
        y: Endpoint Y coordinate.
        w: Weight for conic sections. If w > 1: hyperbola, w == 1: parabola,
           w < 1: ellipse. Default is 1.0 (standard quadratic bezier).
    """

    cp1x: float
    cp1y: float
    x: float
    y: float
    w: float = 1.0

    def to_dict(self) -> dict:
        return {
            "type": "quadraticTo",
            "cp1x": self.cp1x,
            "cp1y": self.cp1y,
            "x": self.x,
            "y": self.y,
            "w": self.w,
        }


@dataclass
class Arc(PathElement):
    """Adds an arc segment following the edge of an oval.

    The arc follows the oval bounded by the rectangle at (x, y) with the given
    width and height, from start_angle to start_angle + sweep_angle.

    Zero radians is at the right side of the oval (3 o'clock position).
    Positive angles go clockwise.

    Args:
        x: Top-left X of the bounding rectangle.
        y: Top-left Y of the bounding rectangle.
        width: Width of the bounding rectangle.
        height: Height of the bounding rectangle.
        start_angle: Starting angle in radians.
        sweep_angle: Sweep angle in radians from start_angle.
    """

    x: float
    y: float
    width: float
    height: float
    start_angle: float
    sweep_angle: float

    def to_dict(self) -> dict:
        return {
            "type": "arc",
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "startAngle": self.start_angle,
            "sweepAngle": self.sweep_angle,
        }


@dataclass
class ArcTo(PathElement):
    """Adds an arc from the current point to (x, y).

    Appends up to four conic curves to describe an arc with the given radius,
    rotated by rotation degrees.

    Args:
        x: Endpoint X coordinate.
        y: Endpoint Y coordinate.
        radius: Radius of the arc.
        rotation: Rotation of the arc in degrees. Default 0.
        large_arc: Whether to use the large arc sweep. Default False.
        clockwise: Whether the arc should be drawn clockwise. Default True.
    """

    x: float
    y: float
    radius: float = 0
    rotation: float = 0
    large_arc: bool = False
    clockwise: bool = True

    def to_dict(self) -> dict:
        return {
            "type": "arcTo",
            "x": self.x,
            "y": self.y,
            "radius": self.radius,
            "rotation": self.rotation,
            "largeArc": self.large_arc,
            "clockwise": self.clockwise,
        }


@dataclass
class Oval(PathElement):
    """Adds an ellipse that fills the given rectangle.

    Args:
        x: Top-left X of the bounding rectangle.
        y: Top-left Y of the bounding rectangle.
        width: Width of the bounding rectangle.
        height: Height of the bounding rectangle.
    """

    x: float
    y: float
    width: float
    height: float

    def to_dict(self) -> dict:
        return {
            "type": "oval",
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }


@dataclass
class Rect(PathElement):
    """Adds a rectangle as a new sub-path.

    Args:
        x: Top-left X of the rectangle.
        y: Top-left Y of the rectangle.
        width: Width of the rectangle.
        height: Height of the rectangle.
        border_radius: Optional corner radius for rounded rectangles.
    """

    x: float
    y: float
    width: float
    height: float
    border_radius: Optional[float] = None

    def to_dict(self) -> dict:
        result = {
            "type": "rect",
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }
        if self.border_radius is not None:
            result["borderRadius"] = self.border_radius
        return result


@dataclass
class SubPath(PathElement):
    """Adds the sub-path described by elements at (x, y).

    The sub-path is translated to start at the given point.

    Args:
        x: X offset for the sub-path.
        y: Y offset for the sub-path.
        elements: List of path elements in the sub-path.
    """

    x: float
    y: float
    elements: List[PathElement]

    def to_dict(self) -> dict:
        return {
            "type": "subPath",
            "x": self.x,
            "y": self.y,
            "elements": [el.to_dict() for el in self.elements],
        }
