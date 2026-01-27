"""Capsule - Capsule shape with declarative parameter-based API."""

from typing import Any, Optional
from ..base import View
from ...types import ColorLike


class Capsule(View):
    """
    A capsule shape aligned inside the frame of the view containing it.

    A capsule is a rounded rectangle where the shorter dimension is
    completely rounded (like a pill shape).

        Capsule(fill=Color.green, width=100, height=40)

        Capsule(
            fill=Color.blue,
            stroke_color=Color.white,
            stroke_width=2,
            width=150,
            height=50,
        )
    """

    _type = "Capsule"

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
