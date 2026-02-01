"""Capsule shape view.

This module provides the :class:`Capsule` shape, a pill-shaped rectangle
where the shorter dimension is completely rounded. Capsules are commonly
used for buttons, tags, badges, and other UI elements that need a smooth,
rounded appearance.

Example:
    Basic capsule::

        nib.Capsule(fill=nib.Color.GREEN, width=100, height=40)

    Capsule button background::

        nib.Button(
            "Click Me",
            background=nib.Capsule(fill=nib.Color.BLUE),
            padding={"horizontal": 20, "vertical": 10},
        )

    Capsule with stroke::

        nib.Capsule(
            fill=nib.Color.BLUE,
            stroke_color=nib.Color.WHITE,
            stroke_width=2,
            width=150,
            height=50,
        )

    Tag/badge with capsule shape::

        nib.Text(
            "NEW",
            font=nib.Font.CAPTION,
            foreground_color=nib.Color.WHITE,
            background=nib.Capsule(fill=nib.Color.RED),
            padding={"horizontal": 8, "vertical": 4},
        )

See Also:
    - :class:`RoundedRectangle`: Rectangle with configurable corner radius.
    - :class:`Circle`: Circular shape.
    - :class:`Ellipse`: Oval shape.
"""

from typing import Any, Optional
from ..base import View
from ...types import ColorLike


class Capsule(View):
    """A capsule shape aligned inside the frame of the view containing it.

    Capsule draws a pill-shaped rectangle where the shorter dimension
    (width or height) determines the corner radius, creating fully
    rounded ends. This is different from :class:`RoundedRectangle` which
    has a fixed corner radius regardless of dimensions.

    For horizontal capsules (width > height), the ends are semicircles
    with radius equal to half the height. For vertical capsules
    (height > width), the ends are semicircles with radius equal to
    half the width.

    Attributes:
        _type: The SwiftUI view type identifier ("Capsule").

    Args:
        fill: The fill color for the capsule interior. Can be a
            :class:`Color` instance, a named color string (e.g., "red"),
            or a hex color string (e.g., "#FF5733").
        stroke_color: The stroke color for the capsule border. Uses
            the same color format as ``fill``.
        stroke_width: The width of the stroke in points. Only applies
            if ``stroke_color`` is set.
        **kwargs: Additional view modifiers passed to the base :class:`View`
            class (e.g., ``width``, ``height``, ``padding``, ``opacity``).

    Example:
        Simple capsule::

            nib.Capsule(fill=nib.Color.GREEN, width=100, height=40)

        Capsule with border::

            nib.Capsule(
                fill=nib.Color.BLUE,
                stroke_color=nib.Color.WHITE,
                stroke_width=2,
                width=150,
                height=50,
            )

        Vertical capsule::

            nib.Capsule(
                fill=nib.Color.ORANGE,
                width=30,
                height=100,
            )

        As a clip shape::

            nib.Image(
                source="banner.jpg",
                clip_shape=nib.Capsule(),
                width=200,
                height=60,
            )

    See Also:
        :class:`RoundedRectangle`: For rectangles with a fixed corner radius.
    """

    _type = "Capsule"

    def __init__(
        self,
        fill: Optional[ColorLike] = None,
        stroke_color: Optional[ColorLike] = None,
        stroke_width: Optional[float] = None,
        **kwargs: Any,
    ):
        """Initialize a Capsule shape.

        Args:
            fill: The fill color for the capsule interior. Accepts a
                :class:`Color` instance, named color string, or hex string.
            stroke_color: The stroke color for the capsule border.
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
