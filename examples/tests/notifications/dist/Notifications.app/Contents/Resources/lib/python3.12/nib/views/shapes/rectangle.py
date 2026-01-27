"""Rectangle - Rectangle shape with declarative parameter-based API."""

from typing import Any, Optional
from ..base import View
from ...types import ColorLike


class Rectangle(View):
    """
    A rectangular shape aligned inside the frame of the view containing it.

        Rectangle(fill=Color.blue)

        Rectangle(
            fill=Color.gray,
            stroke_color=Color.black,
            stroke_width=1,
            width=100,
            height=50,
        )
    """

    _type = "Rectangle"

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
