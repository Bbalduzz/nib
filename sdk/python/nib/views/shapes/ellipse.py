"""Ellipse shape view.

This module provides the :class:`Ellipse` shape, an oval shape that stretches
to fill its frame with independent width and height dimensions. Ellipses are
useful for decorative elements, badges, and when you need an oval that is
not a perfect circle.

Example:
    Basic ellipse::

        nib.Ellipse(fill=nib.Color.BLUE, width=100, height=50)

    Ellipse with stroke::

        nib.Ellipse(
            fill=nib.Color.PURPLE,
            stroke_color=nib.Color.WHITE,
            stroke_width=2,
            width=200,
            height=100,
        )

    Ellipse as background::

        nib.Text(
            "Badge",
            background=nib.Ellipse(fill=nib.Color.RED),
            padding={"horizontal": 16, "vertical": 8},
        )

See Also:
    - :class:`Circle`: Circular shape (equal width and height).
    - :class:`Capsule`: Pill-shaped rectangle with fully rounded ends.
    - :class:`RoundedRectangle`: Rectangle with rounded corners.
"""

from typing import Any, Optional
from ..base import View
from ...types import ColorLike


class Ellipse(View):
    """An ellipse aligned inside the frame of the view containing it.

    Ellipse draws an oval shape that stretches to fill its frame. Unlike
    :class:`Circle` which maintains a 1:1 aspect ratio, Ellipse can have
    different width and height values, creating an oval shape.

    When width equals height, an Ellipse appears identical to a Circle.
    For asymmetric shapes, the ellipse stretches along the larger dimension.

    Attributes:
        _type: The SwiftUI view type identifier ("Ellipse").

    Args:
        fill: The fill color for the ellipse interior. Can be a
            :class:`Color` instance, a named color string (e.g., "red"),
            or a hex color string (e.g., "#FF5733").
        stroke_color: The stroke color for the ellipse border. Uses
            the same color format as ``fill``.
        stroke_width: The width of the stroke in points. Only applies
            if ``stroke_color`` is set.
        **kwargs: Additional view modifiers passed to the base :class:`View`
            class (e.g., ``width``, ``height``, ``padding``, ``opacity``).

    Example:
        Wide ellipse::

            nib.Ellipse(fill=nib.Color.BLUE, width=100, height=50)

        Ellipse with border::

            nib.Ellipse(
                fill=nib.Color.PURPLE,
                stroke_color=nib.Color.WHITE,
                stroke_width=2,
                width=200,
                height=100,
            )

        Semi-transparent ellipse overlay::

            nib.Ellipse(
                fill=nib.Color.BLACK.with_opacity(0.3),
                width=150,
                height=75,
            )

    See Also:
        :class:`Circle`: For circular shapes with equal width and height.
    """

    _type = "Ellipse"

    def __init__(
        self,
        fill: Optional[ColorLike] = None,
        stroke_color: Optional[ColorLike] = None,
        stroke_width: Optional[float] = None,
        **kwargs: Any,
    ):
        """Initialize an Ellipse shape.

        Args:
            fill: The fill color for the ellipse interior. Accepts a
                :class:`Color` instance, named color string, or hex string.
            stroke_color: The stroke color for the ellipse border.
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
