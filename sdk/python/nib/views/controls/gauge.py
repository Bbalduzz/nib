"""Gauge view for displaying values within a range.

Provides various gauge styles for visualizing numeric values like
battery level, CPU usage, progress, etc.
"""

from typing import TYPE_CHECKING, Optional, Union
from ..base import View

if TYPE_CHECKING:
    from ...types import Color


class GaugeStyle:
    """Gauge display styles."""
    AUTOMATIC = "automatic"
    LINEAR_CAPACITY = "linearCapacity"
    CIRCULAR_CAPACITY = "circularCapacity"
    ACCESSORY_LINEAR = "accessoryLinear"
    ACCESSORY_LINEAR_CAPACITY = "accessoryLinearCapacity"
    ACCESSORY_CIRCULAR = "accessoryCircular"
    ACCESSORY_CIRCULAR_CAPACITY = "accessoryCircularCapacity"


class Gauge(View):
    """A view that shows a value within a range.

    Gauges are ideal for displaying values like battery level, CPU usage,
    memory consumption, or any other bounded numeric value.

    All label parameters accept either a string or a View for full customization.

    Args:
        value: Current value (0.0 to 1.0 by default).
        min_value: Minimum value of the range (default 0.0).
        max_value: Maximum value of the range (default 1.0).
        label: Label describing the gauge (string or View).
        current_value_label: Label showing the current value (string or View).
        min_value_label: Label for the minimum value (string or View).
        max_value_label: Label for the maximum value (string or View).
        style: Gauge style (see GaugeStyle).
        tint: Color tint for the gauge.
        **kwargs: Additional view modifiers.

    Example:
        Simple gauge with string labels::

            nib.Gauge(value=0.75, label="Battery")

        Gauge with custom view labels::

            nib.Gauge(
                value=cpu_usage / 100,
                label=nib.Label("CPU", system_image="cpu"),
                current_value_label=nib.Text(f"{cpu_usage}%", font=nib.Font.headline),
                min_value_label=nib.Image(system_name="tortoise"),
                max_value_label=nib.Image(system_name="hare"),
                style=nib.GaugeStyle.ACCESSORY_CIRCULAR,
                tint=nib.Color.BLUE,
            )

        Linear gauge::

            nib.Gauge(
                value=progress,
                label="Download",
                current_value_label=f"{int(progress * 100)}%",
                min_value_label="0%",
                max_value_label="100%",
                style=nib.GaugeStyle.LINEAR_CAPACITY,
            )
    """

    _type = "Gauge"

    def __init__(
        self,
        value: float = 0.0,
        min_value: float = 0.0,
        max_value: float = 1.0,
        label: Optional[Union[str, View]] = None,
        current_value_label: Optional[Union[str, View]] = None,
        min_value_label: Optional[Union[str, View]] = None,
        max_value_label: Optional[Union[str, View]] = None,
        style: str = GaugeStyle.AUTOMATIC,
        tint: Optional[Union[str, "Color"]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._value = value
        self._min_value = min_value
        self._max_value = max_value
        self._label = label
        self._current_value_label = current_value_label
        self._min_value_label = min_value_label
        self._max_value_label = max_value_label
        self._style = style
        self._tint = tint

        # Set parent for view labels
        for lbl in [label, current_value_label, min_value_label, max_value_label]:
            if isinstance(lbl, View):
                lbl._parent = self

    @property
    def value(self) -> float:
        """Current gauge value."""
        return self._value

    @value.setter
    def value(self, val: float) -> None:
        self._value = val
        self._mark_dirty()

    @property
    def label(self) -> Optional[Union[str, View]]:
        """Gauge label (string or View)."""
        return self._label

    @label.setter
    def label(self, val: Optional[Union[str, View]]) -> None:
        if isinstance(self._label, View):
            self._label._parent = None
        self._label = val
        if isinstance(val, View):
            val._parent = self
        self._mark_dirty()

    @property
    def current_value_label(self) -> Optional[Union[str, View]]:
        """Current value label (string or View)."""
        return self._current_value_label

    @current_value_label.setter
    def current_value_label(self, val: Optional[Union[str, View]]) -> None:
        if isinstance(self._current_value_label, View):
            self._current_value_label._parent = None
        self._current_value_label = val
        if isinstance(val, View):
            val._parent = self
        self._mark_dirty()

    @property
    def min_value_label(self) -> Optional[Union[str, View]]:
        """Minimum value label (string or View)."""
        return self._min_value_label

    @min_value_label.setter
    def min_value_label(self, val: Optional[Union[str, View]]) -> None:
        if isinstance(self._min_value_label, View):
            self._min_value_label._parent = None
        self._min_value_label = val
        if isinstance(val, View):
            val._parent = self
        self._mark_dirty()

    @property
    def max_value_label(self) -> Optional[Union[str, View]]:
        """Maximum value label (string or View)."""
        return self._max_value_label

    @max_value_label.setter
    def max_value_label(self, val: Optional[Union[str, View]]) -> None:
        if isinstance(self._max_value_label, View):
            self._max_value_label._parent = None
        self._max_value_label = val
        if isinstance(val, View):
            val._parent = self
        self._mark_dirty()

    @property
    def style(self) -> str:
        """Gauge style."""
        return self._style

    @style.setter
    def style(self, val: str) -> None:
        self._style = val
        self._mark_dirty()

    @property
    def tint(self) -> Optional[Union[str, "Color"]]:
        """Gauge tint color."""
        return self._tint

    @tint.setter
    def tint(self, val: Optional[Union[str, "Color"]]) -> None:
        self._tint = val
        self._mark_dirty()

    def _get_props(self) -> dict:
        from ...types import Color

        props = {
            "value": self._value,
            "minValue": self._min_value,
            "maxValue": self._max_value,
            "gaugeStyle": self._style,
        }
        # Only include string labels in props; view labels go in children
        if isinstance(self._label, str):
            props["label"] = self._label
        if isinstance(self._current_value_label, str):
            props["currentValueLabel"] = self._current_value_label
        if isinstance(self._min_value_label, str):
            props["minValueLabel"] = self._min_value_label
        if isinstance(self._max_value_label, str):
            props["maxValueLabel"] = self._max_value_label
        if self._tint is not None:
            props["tint"] = self._tint.to_dict() if isinstance(self._tint, Color) else self._tint
        return props

    def _get_children(self, parent_path: str = "") -> list:
        """Serialize view labels as children with slot identifiers."""
        children = []
        slot_map = [
            ("label", self._label),
            ("currentValue", self._current_value_label),
            ("minValue", self._min_value_label),
            ("maxValue", self._max_value_label),
        ]
        for i, (slot, lbl) in enumerate(slot_map):
            if isinstance(lbl, View) and lbl._visible:
                child_dict = lbl.to_dict(f"{parent_path}.{i}")
                child_dict["slot"] = slot  # Mark which slot this child belongs to
                children.append(child_dict)
        return children if children else None
