"""Rectangle shape view.

This module provides the :class:`Rectangle` shape, a basic rectangular shape
that can be used as content, backgrounds, overlays, or clip shapes in Nib
applications. Rectangles have sharp corners and support fill colors, strokes,
and all standard view modifiers.

Example:
    Basic filled rectangle::

        nib.Rectangle(fill=nib.Color.BLUE, width=100, height=50)

    Rectangle with stroke::

        nib.Rectangle(
            fill=nib.Color.GRAY,
            stroke_color=nib.Color.BLACK,
            stroke_width=2,
            width=200,
            height=100,
        )

    Rectangle as background::

        nib.VStack(
            controls=[nib.Text("Content")],
            background=nib.Rectangle(fill="#333333"),
            padding=16,
        )

See Also:
    - :class:`RoundedRectangle`: Rectangle with rounded corners.
    - :class:`Circle`: Circular shape.
    - :class:`Capsule`: Pill-shaped rectangle.
"""

from typing import Any, Optional
from ..base import View
from ...types import ColorLike


class Rectangle(View):
    """A rectangular shape aligned inside the frame of the view containing it.

    Rectangle draws a sharp-cornered rectangular shape that fills its frame.
    It can be used as standalone content, as a background for other views,
    or as a clip shape. Supports fill colors, strokes, and all standard
    view modifiers.

    Attributes:
        _type: The SwiftUI view type identifier ("Rectangle").

    Args:
        fill: The fill color for the rectangle interior. Can be a
            :class:`Color` instance, a named color string (e.g., "red"),
            or a hex color string (e.g., "#FF5733").
        stroke_color: The stroke color for the rectangle border. Uses
            the same color format as ``fill``.
        stroke_width: The width of the stroke in points. Only applies
            if ``stroke_color`` is set.
        **kwargs: Additional view modifiers passed to the base :class:`View`
            class (e.g., ``width``, ``height``, ``padding``, ``opacity``).

    Example:
        Simple filled rectangle::

            nib.Rectangle(fill=nib.Color.BLUE)

        Rectangle with specific dimensions and stroke::

            nib.Rectangle(
                fill=nib.Color.GRAY,
                stroke_color=nib.Color.BLACK,
                stroke_width=1,
                width=100,
                height=50,
            )

        Semi-transparent rectangle overlay::

            nib.Rectangle(
                fill=nib.Color.BLACK.with_opacity(0.5),
                width=200,
                height=200,
            )

    See Also:
        :class:`RoundedRectangle`: For rectangles with rounded corners.
    """

    _type = "Rectangle"

    def __init__(
        self,
        fill: Optional[ColorLike] = None,
        stroke_color: Optional[ColorLike] = None,
        stroke_width: Optional[float] = None,
        **kwargs: Any,
    ):
        """Initialize a Rectangle shape.

        Args:
            fill: The fill color for the rectangle interior. Accepts a
                :class:`Color` instance, named color string, or hex string.
            stroke_color: The stroke color for the rectangle border.
            stroke_width: The width of the stroke in points.
            **kwargs: Additional view modifiers (width, height, padding,
                opacity, etc.) passed to the base View class.
        """
        super().__init__(
            fill=fill,
            border_color=stroke_color,
            border_width=stroke_width,
            **kwargs,
        )
