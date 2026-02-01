"""Rectangle shape view.

This module provides the :class:`Rectangle` shape, a rectangular shape that
supports configurable corner radii. Rectangle can have sharp corners (default),
uniform rounded corners, or per-corner control using :class:`CornerRadius`.

Example:
    Basic filled rectangle::

        nib.Rectangle(fill=nib.Color.BLUE, width=100, height=50)

    Rectangle with uniform rounded corners::

        nib.Rectangle(
            fill=nib.Color.GRAY,
            corner_radius=10,
            width=200,
            height=100,
        )

    Rectangle with per-corner radii::

        nib.Rectangle(
            fill=nib.Color.BLUE,
            corner_radius=nib.CornerRadius(
                top_left=20,
                top_right=20,
                bottom_left=0,
                bottom_right=0,
            ),
            width=200,
            height=100,
        )

    Rectangle as background::

        nib.VStack(
            controls=[nib.Text("Content")],
            background=nib.Rectangle(fill="#333333", corner_radius=12),
            padding=16,
        )

See Also:
    - :class:`CornerRadius`: Per-corner radius configuration.
    - :class:`Circle`: Circular shape.
    - :class:`Capsule`: Pill-shaped rectangle.
"""

from typing import Any, Optional, Union

from ...types import ColorLike, CornerRadius, resolve_color
from ..base import View


class Rectangle(View):
    """A rectangular shape with configurable corner radii.

    Rectangle draws a rectangular shape that fills its frame. It supports
    sharp corners (default), uniform rounded corners via a single float,
    or per-corner control using :class:`CornerRadius`.

    When used as a ``clip_shape`` for other views, Rectangle clips the
    content to the rectangle bounds (with optional rounding).

    Attributes:
        _type: The SwiftUI view type identifier ("Rectangle").
        _corner_radius: The corner radius configuration.
        _stroke_color: The stroke color if set.
        _stroke_width: The stroke width if set.

    Args:
        fill: The fill color for the rectangle interior. Can be a
            :class:`Color` instance, a named color string (e.g., "red"),
            or a hex color string (e.g., "#FF5733").
        corner_radius: The corner radius configuration. Can be:
            - None: Sharp corners (default)
            - float: Uniform radius for all corners
            - :class:`CornerRadius`: Per-corner radius control
        stroke_color: The stroke color for the rectangle border. Uses
            the same color format as ``fill``.
        stroke_width: The width of the stroke in points.
        **kwargs: Additional view modifiers passed to the base :class:`View`
            class (e.g., ``width``, ``height``, ``padding``, ``opacity``).

    Example:
        Sharp corners (default)::

            nib.Rectangle(fill=nib.Color.BLUE)

        Uniform rounded corners::

            nib.Rectangle(fill=nib.Color.BLUE, corner_radius=10)

        Per-corner control::

            nib.Rectangle(
                fill=nib.Color.BLUE,
                corner_radius=nib.CornerRadius(
                    top_left=20,
                    top_right=20,
                    bottom_left=0,
                    bottom_right=0,
                ),
            )

        Using factory methods::

            nib.Rectangle(
                fill=nib.Color.BLUE,
                corner_radius=nib.CornerRadius.vertical(top=15, bottom=0),
            )

        With stroke::

            nib.Rectangle(
                fill=nib.Color.GRAY,
                corner_radius=12,
                stroke_color=nib.Color.WHITE,
                stroke_width=2,
                width=200,
                height=100,
            )

    See Also:
        :class:`CornerRadius`: For per-corner radius configuration.
    """

    _type = "Rectangle"

    def __init__(
        self,
        fill: Optional[ColorLike] = None,
        corner_radius: Optional[Union[float, CornerRadius]] = None,
        stroke_color: Optional[ColorLike] = None,
        stroke_width: Optional[float] = None,
        **kwargs: Any,
    ):
        """Initialize a Rectangle shape.

        Args:
            fill: The fill color for the rectangle interior. Accepts a
                :class:`Color` instance, named color string, or hex string.
            corner_radius: The corner radius. Can be a float for uniform
                corners or a :class:`CornerRadius` for per-corner control.
            stroke_color: The stroke color for the rectangle border.
            stroke_width: The width of the stroke in points.
            **kwargs: Additional view modifiers (width, height, padding,
                opacity, etc.) passed to the base View class.
        """
        super().__init__(fill=fill, **kwargs)
        self._corner_radius = corner_radius
        self._stroke_color = stroke_color
        self._stroke_width = stroke_width

    def _get_props(self) -> dict:
        """Get view-specific properties for serialization.

        Returns:
            Dictionary containing the corner radius and stroke configuration
            for the Swift runtime.
        """
        props = {}

        if self._corner_radius is not None:
            if isinstance(self._corner_radius, CornerRadius):
                # Per-corner radius - serialize as object
                props["cornerRadii"] = self._corner_radius.to_dict()
            else:
                # Uniform radius - serialize as single value
                props["cornerRadius"] = float(self._corner_radius)

        # Pass stroke as props (not modifier) so it respects the shape
        if self._stroke_color is not None:
            props["stroke"] = resolve_color(self._stroke_color)
        if self._stroke_width is not None:
            props["strokeWidth"] = float(self._stroke_width)

        return props
