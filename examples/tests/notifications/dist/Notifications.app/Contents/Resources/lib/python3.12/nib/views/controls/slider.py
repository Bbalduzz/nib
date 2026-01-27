"""Slider - A control for selecting a value from a range with declarative parameter-based API."""

from typing import Any, Callable, Optional
from ..base import View, _float
from ...types import (
    ColorLike,
    resolve_color,
)


class Slider(View):
    """
    A control for selecting a value from a continuous range.

        Slider(
            value=self.volume,
            min_value=0,
            max_value=100,
            on_change=self.set_volume,
            tint=Color.blue,
        )

        Slider(value=self.rating, min_value=1, max_value=5, step=1)
    """

    _type = "Slider"

    def __init__(
        self,
        value: float = 0,
        min_value: float = 0,
        max_value: float = 1,
        step: Optional[float] = None,
        label: str = "",
        on_change: Optional[Callable[[float], None]] = None,
        # Slider-specific styling
        tint: Optional[ColorLike] = None,
        disabled: bool = False,
        # View modifiers passed through
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._value = value
        self._min_value = min_value
        self._max_value = max_value
        self._step = step
        self._label = label
        self._on_change = on_change

        # Build slider-specific styles
        self._slider_styles: dict = {}
        if tint is not None:
            self._slider_styles["tint"] = resolve_color(tint)
        if disabled:
            self._slider_styles["disabled"] = True

    def _get_props(self) -> dict:
        props = {
            "value": _float(self._value),
            "minValue": _float(self._min_value),
            "maxValue": _float(self._max_value),
        }
        if self._step is not None:
            props["step"] = _float(self._step)
        if self._label:
            props["label"] = self._label
        if self._slider_styles:
            props["sliderStyles"] = self._slider_styles
        return props
