"""ProgressView - A view showing progress of a task with declarative parameter-based API."""

from typing import Any, Optional, Union
from ..base import View, _float
from ...types import (
    ColorLike,
    ProgressStyle,
    resolve_color,
    resolve_enum,
)


class ProgressView(View):
    """
    A view that shows the progress of a task.

        # Indeterminate progress (spinning)
        ProgressView()

        # Determinate progress (0.0 to 1.0)
        ProgressView(value=0.7, tint=Color.green)

        # With label
        ProgressView(value=0.5, label="Downloading...", style=ProgressStyle.linear)
    """

    _type = "ProgressView"

    def __init__(
        self,
        value: Optional[float] = None,
        total: float = 1.0,
        label: str = "",
        # ProgressView-specific styling
        style: Optional[Union[ProgressStyle, str]] = None,
        tint: Optional[ColorLike] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """
        Create a progress view.

        Args:
            value: Current progress (0.0 to total). None for indeterminate.
            total: Maximum value (default 1.0)
            label: Optional label text
            style: Progress view style (ProgressStyle enum)
            tint: Tint color for the progress indicator
        """
        super().__init__(**kwargs)
        self._value = value
        self._total = total
        self._label = label

        # Build progress-specific styles
        self._progress_styles: dict = {}
        if style is not None:
            self._progress_styles["style"] = resolve_enum(style)
        if tint is not None:
            self._progress_styles["tint"] = resolve_color(tint)

    def _get_props(self) -> dict:
        props = {}
        if self._value is not None:
            props["progress"] = _float(self._value / self._total)
        if self._label:
            props["label"] = self._label
        if self._progress_styles:
            props["progressStyles"] = self._progress_styles
        return props
