"""Ellipse - Ellipse shape with declarative parameter-based API."""

from typing import Any, Optional
from ..base import View
from ...types import ColorLike


class Ellipse(View):
    """
    An ellipse aligned inside the frame of the view containing it.

        Ellipse(fill=Color.blue, width=100, height=50)

        Ellipse(
            fill=Color.purple,
            stroke_color=Color.white,
            stroke_width=2,
            width=200,
            height=100,
        )
    """

    _type = "Ellipse"

    def __init__(
        self,
        # Shape-specific styling
        fill: Optional[ColorLike] = None,
        stroke_color: Optional[ColorLike] = None,
        stroke_width: Optional[float] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        super().__init__(
            fill=fill,
            border_color=stroke_color,
            border_width=stroke_width,
            **kwargs,
        )
