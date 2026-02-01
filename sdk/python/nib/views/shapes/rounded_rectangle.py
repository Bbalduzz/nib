"""Rounded rectangle shape view.

This module provides the :class:`RoundedRectangle` shape, a rectangular shape
with configurable rounded corners. RoundedRectangle is one of the most commonly
used shapes in Nib for creating cards, buttons, containers, and other UI
elements with a modern, polished appearance.

Example:
    Basic rounded rectangle::

        nib.RoundedRectangle(corner_radius=10, fill=nib.Color.BLUE)

    Card-style container background::

        nib.VStack(
            controls=[
                nib.Text("Card Title", font=nib.Font.HEADLINE),
                nib.Text("Card content goes here."),
            ],
            spacing=8,
            background=nib.RoundedRectangle(
                corner_radius=12,
                fill="#262626",
                stroke_color="#383837",
                stroke_width=1,
            ),
            padding=16,
        )

    Rounded rectangle with dimensions::

        nib.RoundedRectangle(
            corner_radius=16,
            fill=nib.Color.BLUE,
            stroke_color=nib.Color.WHITE,
            stroke_width=2,
            width=200,
            height=100,
        )

See Also:
    - :class:`Rectangle`: Rectangle with sharp corners.
    - :class:`Capsule`: Fully rounded ends (pill shape).
    - :class:`Circle`: Circular shape.
"""

from typing import Any, Optional
from ..base import View
from ...types import ColorLike, resolve_color


class RoundedRectangle(View):
    """A rectangular shape with rounded corners.

    RoundedRectangle draws a rectangle with configurable corner rounding.
    It is commonly used for card backgrounds, button shapes, and container
    styling. The corner radius can be set to any positive value, where
    larger values create more pronounced rounding.

    When used as a ``clip_shape`` for other views, RoundedRectangle clips
    the content to the rounded rectangle bounds.

    Attributes:
        _type: The SwiftUI view type identifier ("RoundedRectangle").
        _corner_radius: The corner radius in points.
        _stroke_color: The stroke color if set.
        _stroke_width: The stroke width if set.

    Args:
        corner_radius: The radius of the rounded corners in points.
            Defaults to 10. Larger values create more rounded corners.
        fill: The fill color for the rectangle interior. Can be a
            :class:`Color` instance, a named color string (e.g., "red"),
            or a hex color string (e.g., "#FF5733").
        stroke_color: The stroke color for the rectangle border. Uses
            the same color format as ``fill``.
        stroke_width: The width of the stroke in points. Defaults to 1
            if ``stroke_color`` is set but ``stroke_width`` is not.
        **kwargs: Additional view modifiers passed to the base :class:`View`
            class (e.g., ``width``, ``height``, ``padding``, ``opacity``).

    Example:
        Simple rounded rectangle::

            nib.RoundedRectangle(corner_radius=10, fill=nib.Color.BLUE)

        Card with border::

            nib.RoundedRectangle(
                corner_radius=16,
                fill=nib.Color.BLUE,
                stroke_color=nib.Color.WHITE,
                stroke_width=2,
                width=200,
                height=100,
            )

        As a clip shape for an image::

            nib.Image(
                source="avatar.jpg",
                clip_shape=nib.RoundedRectangle(corner_radius=8),
                width=64,
                height=64,
            )

    See Also:
        :class:`Rectangle`: For sharp-cornered rectangles.
        :class:`Capsule`: For fully rounded ends (pill shape).
    """

    _type = "RoundedRectangle"

    def __init__(
        self,
        corner_radius: float = 10,
        fill: Optional[ColorLike] = None,
        stroke_color: Optional[ColorLike] = None,
        stroke_width: Optional[float] = None,
        **kwargs: Any,
    ):
        """Initialize a RoundedRectangle shape.

        Args:
            corner_radius: The radius of the rounded corners in points.
                Defaults to 10 points.
            fill: The fill color for the rectangle interior. Accepts a
                :class:`Color` instance, named color string, or hex string.
            stroke_color: The stroke color for the rectangle border.
            stroke_width: The width of the stroke in points. Defaults to 1
                if stroke_color is provided.
            **kwargs: Additional view modifiers (width, height, padding,
                opacity, etc.) passed to the base View class.
        """
        super().__init__(fill=fill, **kwargs)
        self._corner_radius = corner_radius
        self._stroke_color = stroke_color
        self._stroke_width = stroke_width

        # Add stroke as border modifier with shape info
        if stroke_color is not None:
            self._add_modifier(
                "border",
                borderColor=resolve_color(stroke_color),
                borderWidth=float(stroke_width) if stroke_width else 1,
                shape="roundedRectangle",
                cornerRadius=float(corner_radius),
            )

    def _get_props(self) -> dict:
        """Get view-specific properties for serialization.

        Returns:
            Dictionary containing the corner radius for the Swift runtime.
        """
        return {"cornerRadius": float(self._corner_radius)}
