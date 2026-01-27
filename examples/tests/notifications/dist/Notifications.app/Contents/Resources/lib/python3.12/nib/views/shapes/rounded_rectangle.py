"""RoundedRectangle - Rounded rectangle shape with declarative parameter-based API."""

from typing import Any, Optional
from ..base import View
from ...types import ColorLike, resolve_color


class RoundedRectangle(View):
    """
    A rectangular shape with rounded corners.

        RoundedRectangle(corner_radius=10, fill=Color.blue)

        RoundedRectangle(
            corner_radius=16,
            fill=Color.blue,
            stroke_color=Color.white,
            stroke_width=2,
            width=200,
            height=100,
        )
    """

    _type = "RoundedRectangle"

    def __init__(
        self,
        corner_radius: float = 10,
        # Shape-specific styling
        fill: Optional[ColorLike] = None,
        stroke_color: Optional[ColorLike] = None,
        stroke_width: Optional[float] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
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
        return {"cornerRadius": float(self._corner_radius)}
