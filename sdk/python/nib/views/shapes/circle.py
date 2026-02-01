"""Circle shape view.

This module provides the :class:`Circle` shape, a circular shape that can be
used as content, backgrounds, overlays, clip shapes, or for creating progress
rings and indicators. Circles support fill colors, strokes, trimming for
partial arcs, and rotation.

Example:
    Basic filled circle::

        nib.Circle(fill=nib.Color.BLUE, width=50, height=50)

    Circle as clip shape::

        nib.Image(source="photo.jpg", clip_shape=nib.Circle())

    Progress ring indicator::

        nib.Circle(
            stroke_color=nib.Color.BLUE,
            stroke_width=8,
            trim_from=0.0,
            trim_to=0.75,
            width=100,
            height=100,
        )

    Rotated progress ring (starting from top)::

        nib.Circle(
            stroke_color=nib.Color.GREEN,
            stroke_width=6,
            trim_from=0.0,
            trim_to=0.5,
            rotation=-90,
            width=80,
            height=80,
        )

See Also:
    - :class:`Ellipse`: Oval shape with independent width/height.
    - :class:`Capsule`: Pill-shaped rectangle.
    - :class:`RoundedRectangle`: Rectangle with rounded corners.
"""

from typing import Any, Optional
from ..base import View
from ...types import ColorLike


class Circle(View):
    """A circle centered in the frame of the view containing it.

    Circle draws a circular shape that fills the smaller dimension of its
    frame (always maintaining a 1:1 aspect ratio). It can be used as
    standalone content, as a clip shape for images, or with trim properties
    to create progress rings and arc indicators.

    The trim properties (``trim_from`` and ``trim_to``) allow drawing partial
    circles, useful for progress indicators. Values range from 0.0 to 1.0,
    where 0.0 is the start of the circle (3 o'clock position by default)
    and 1.0 is a complete circle. Use ``rotation`` to change the starting
    position (e.g., -90 to start from the top).

    Attributes:
        _type: The SwiftUI view type identifier ("Circle").
        _trim_from: The starting point for trimmed circles (0.0-1.0).
        _trim_to: The ending point for trimmed circles (0.0-1.0).
        _rotation: The rotation angle in degrees.

    Args:
        fill: The fill color for the circle interior. Can be a
            :class:`Color` instance, a named color string (e.g., "red"),
            or a hex color string (e.g., "#FF5733").
        stroke_color: The stroke color for the circle border. Uses
            the same color format as ``fill``.
        stroke_width: The width of the stroke in points. Only applies
            if ``stroke_color`` is set.
        trim_from: The fractional starting point for the circle arc,
            from 0.0 to 1.0. Used with ``trim_to`` for progress rings.
        trim_to: The fractional ending point for the circle arc,
            from 0.0 to 1.0. Used with ``trim_from`` for progress rings.
        rotation: The rotation angle in degrees. Useful for positioning
            the start point of trimmed circles (e.g., -90 for top).
        **kwargs: Additional view modifiers passed to the base :class:`View`
            class (e.g., ``width``, ``height``, ``padding``, ``opacity``).

    Example:
        Simple filled circle::

            nib.Circle(fill=nib.Color.BLUE)

        Circle with stroke and dimensions::

            nib.Circle(
                fill=nib.Color.RED,
                stroke_color=nib.Color.WHITE,
                stroke_width=2,
                width=50,
                height=50,
            )

        Progress ring (75% complete)::

            nib.Circle(
                stroke_color=nib.Color.BLUE,
                stroke_width=8,
                trim_from=0.0,
                trim_to=0.75,
                width=200,
                height=200,
            )

        Progress ring starting from top::

            nib.Circle(
                stroke_color=nib.Color.GREEN,
                stroke_width=6,
                trim_from=0.0,
                trim_to=progress,  # 0.0 to 1.0
                rotation=-90,
                width=100,
                height=100,
            )

    See Also:
        :class:`Ellipse`: For oval shapes with different width and height.
    """

    _type = "Circle"

    def __init__(
        self,
        fill: Optional[ColorLike] = None,
        stroke_color: Optional[ColorLike] = None,
        stroke_width: Optional[float] = None,
        trim_from: Optional[float] = None,
        trim_to: Optional[float] = None,
        rotation: Optional[float] = None,
        **kwargs: Any,
    ):
        """Initialize a Circle shape.

        Args:
            fill: The fill color for the circle interior. Accepts a
                :class:`Color` instance, named color string, or hex string.
            stroke_color: The stroke color for the circle border.
            stroke_width: The width of the stroke in points.
            trim_from: The fractional starting point (0.0-1.0) for partial
                circle arcs. Defaults to None (full circle).
            trim_to: The fractional ending point (0.0-1.0) for partial
                circle arcs. Defaults to None (full circle).
            rotation: The rotation angle in degrees. Use -90 to start
                trimmed circles from the top instead of the right.
            **kwargs: Additional view modifiers (width, height, padding,
                opacity, etc.) passed to the base View class.
        """
        super().__init__(
            fill=fill,
            border_color=stroke_color,
            border_width=stroke_width,
            **kwargs,
        )
        self._trim_from = trim_from
        self._trim_to = trim_to
        self._rotation = rotation

    def _get_props(self) -> dict:
        """Get view-specific properties for serialization.

        Returns:
            Dictionary containing trim and rotation properties for
            the Swift runtime.
        """
        props = {}
        if self._trim_from is not None:
            props["trimFrom"] = float(self._trim_from)
        if self._trim_to is not None:
            props["trimTo"] = float(self._trim_to)
        if self._rotation is not None:
            props["rotation"] = float(self._rotation)
        return props
