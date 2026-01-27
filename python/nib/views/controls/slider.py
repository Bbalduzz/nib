"""Slider control for selecting a value from a continuous range.

The Slider view provides a horizontal track with a draggable thumb that allows
users to select a value within a specified range. It supports continuous values
or discrete steps.

Example:
    Basic slider::

        nib.Slider(value=50, min_value=0, max_value=100, on_change=handle_change)

    Slider with steps::

        nib.Slider(
            value=3,
            min_value=1,
            max_value=5,
            step=1,
            on_change=set_rating,
        )

    Styled slider::

        nib.Slider(
            value=volume,
            min_value=0,
            max_value=100,
            on_change=set_volume,
            tint=nib.Color.blue,
        )
"""

from typing import Any, Callable, Optional
from ..base import View, _float
from ...types import (
    ColorLike,
    resolve_color,
)


class Slider(View):
    """A control for selecting a value from a continuous range.

    Slider displays a horizontal track with a draggable thumb that users can
    move to select a numeric value. The value can be continuous within the
    range or snapped to discrete steps.

    Attributes:
        _value: The current selected value.
        _min_value: The minimum value of the range.
        _max_value: The maximum value of the range.
        _step: Optional step increment for discrete values.
        _on_change: Callback function triggered when value changes.

    Example:
        Volume control slider::

            nib.Slider(
                value=current_volume,
                min_value=0,
                max_value=100,
                on_change=set_volume,
                tint=nib.Color.green,
            )

        Rating slider with discrete steps::

            nib.Slider(
                value=current_rating,
                min_value=1,
                max_value=5,
                step=1,
                label="Rating",
                on_change=set_rating,
            )

        Percentage slider::

            nib.Slider(
                value=0.5,
                min_value=0.0,
                max_value=1.0,
                on_change=lambda v: print(f"{v * 100:.0f}%"),
            )
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
        """Initialize a Slider view.

        Args:
            value: Initial value of the slider. Must be between min_value and
                max_value. Defaults to 0.
            min_value: Minimum value of the slider range. Defaults to 0.
            max_value: Maximum value of the slider range. Defaults to 1.
            step: Optional step increment. When specified, the slider snaps to
                discrete values at this interval. For example, step=0.5 allows
                values 0.0, 0.5, 1.0, etc. When None, values are continuous.
            label: Optional text label displayed with the slider.
            on_change: Callback function called when the slider value changes.
                Receives the new float value as an argument. Called continuously
                while dragging.
            tint: Tint color for the slider track (the filled portion).
                Accepts Color enum, hex string, or RGB tuple.
            disabled: Whether the slider is disabled and non-interactive.
            **kwargs: Standard view modifiers including padding, background,
                opacity, width, etc.

        Example:
            Create a brightness slider::

                nib.Slider(
                    value=brightness,
                    min_value=0,
                    max_value=100,
                    step=5,
                    label="Brightness",
                    on_change=set_brightness,
                    tint=nib.Color.yellow,
                    width=200,
                )
        """
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
