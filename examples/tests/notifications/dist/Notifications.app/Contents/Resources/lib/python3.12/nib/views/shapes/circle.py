"""Circle - Circle shape with declarative parameter-based API."""

from typing import Any, Optional
from ..base import View
from ...types import ColorLike


class Circle(View):
    """
    A circle centered in the frame of the view containing it.

        Circle(fill=Color.blue)

        Circle(
            fill=Color.red,
            stroke_color=Color.white,
            stroke_width=2,
            width=50,
            height=50,
        )

        # Progress ring (arc from 0% to 75%)
        Circle(
            stroke_color=Color.blue,
            stroke_width=8,
            trim_from=0.0,
            trim_to=0.75,
            width=200,
            height=200,
        )
    """

    _type = "Circle"

    def __init__(
        self,
        # Shape-specific styling
        fill: Optional[ColorLike] = None,
        stroke_color: Optional[ColorLike] = None,
        stroke_width: Optional[float] = None,
        trim_from: Optional[float] = None,  # 0.0 to 1.0
        trim_to: Optional[float] = None,    # 0.0 to 1.0
        rotation: Optional[float] = None,  # Rotation in degrees
        # View modifiers passed through
        **kwargs: Any,
    ):
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
        props = {}
        if self._trim_from is not None:
            props["trimFrom"] = float(self._trim_from)
        if self._trim_to is not None:
            props["trimTo"] = float(self._trim_to)
        if self._rotation is not None:
            props["rotation"] = float(self._rotation)
        return props
