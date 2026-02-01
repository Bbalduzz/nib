"""Drawing primitives for nib Canvas.

This module provides shape and content primitives that can be drawn
on a Canvas view using Core Graphics.

Example:
    Basic drawing::

        import nib

        canvas = nib.Canvas(width=400, height=300)
        canvas.draw([
            nib.draw.Rect(x=10, y=10, width=100, height=50, fill="#3498db"),
            nib.draw.Circle(cx=200, cy=100, radius=40, fill="#e74c3c"),
            nib.draw.Line(x1=10, y1=200, x2=390, y2=200, stroke="#2ecc71"),
            nib.draw.Text("Hello Canvas!", x=10, y=280, fill="#ffffff"),
        ])

    With gradients::

        canvas.draw([
            nib.draw.Rect(
                x=10, y=10, width=100, height=100,
                fill=nib.draw.LinearGradient(
                    start=(10, 10), end=(110, 110),
                    colors=["#FF0000", "#0000FF"],
                ),
            ),
            nib.draw.Circle(
                cx=200, cy=100, radius=50,
                fill=nib.draw.RadialGradient(
                    center=(200, 100), radius=50,
                    colors=["#FFFF00", "#FF0000"],
                ),
            ),
        ])

    Drawing images from file::

        with open("photo.jpg", "rb") as f:
            canvas.draw([nib.draw.Image(data=f.read(), x=0, y=0)])
"""

from .primitives import (
    DrawCommand,
    Rect,
    Circle,
    Ellipse,
    Line,
    Arc,
    Path,
    Polygon,
    BezierPath,
    Points,
    Shadow,
    Fill,
    ColorFill,
)
from .image import Image
from .text import Text
from .paint import (
    Paint,
    PaintStyle,
    StrokeCap,
    StrokeJoin,
    PointMode,
    LinearGradient,
    RadialGradient,
    SweepGradient,
    Blur,
)
from .path import (
    PathElement,
    MoveTo,
    LineTo,
    Close,
    CubicTo,
    QuadraticTo,
    Arc as PathArc,  # Renamed to avoid conflict with Arc draw command
    ArcTo,
    Oval,
    Rect as PathRect,  # Renamed to avoid conflict with Rect draw command
    SubPath,
)
# Re-export BlendMode from nib.types for convenience
from ..types import BlendMode

__all__ = [
    # Base
    "DrawCommand",
    # Shapes
    "Rect",
    "Circle",
    "Ellipse",
    "Line",
    "Arc",
    "Path",
    "Polygon",
    "BezierPath",
    "Points",
    "Shadow",
    "Fill",
    "ColorFill",
    # Content
    "Image",
    "Text",
    # Paint & Styling
    "Paint",
    "PaintStyle",
    "StrokeCap",
    "StrokeJoin",
    "BlendMode",
    "PointMode",
    # Gradients
    "LinearGradient",
    "RadialGradient",
    "SweepGradient",
    # Effects
    "Blur",
    # Path Elements
    "PathElement",
    "MoveTo",
    "LineTo",
    "Close",
    "CubicTo",
    "QuadraticTo",
    "PathArc",
    "ArcTo",
    "Oval",
    "PathRect",
    "SubPath",
]
