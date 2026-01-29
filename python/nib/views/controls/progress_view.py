"""ProgressView control for displaying task progress indicators.

The ProgressView displays the progress of an ongoing task, either as a
determinate progress bar (when the completion percentage is known) or as
an indeterminate spinner (when the completion time is unknown).

Example:
    Indeterminate spinner::

        nib.ProgressView()  # Shows spinning indicator

    Determinate progress bar::

        nib.ProgressView(value=0.7, total=1.0)  # Shows 70% complete

    Styled progress with label::

        nib.ProgressView(
            value=50,
            total=100,
            label="Downloading...",
            tint=nib.Color.blue,
            style=nib.ProgressStyle.linear,
        )
"""

from typing import Any, Optional, Union
from ..base import View, _float
from ...types import (
    ColorLike,
    ProgressStyle,
    resolve_color,
    resolve_enum,
)


class ProgressView(View):
    """A view that shows the progress of an ongoing task.

    ProgressView can display either determinate progress (when you know
    the completion percentage) or indeterminate progress (a spinning
    indicator for unknown duration tasks).

    When value is None, an indeterminate spinner is shown. When value is
    provided, a progress bar showing the completion percentage is displayed.

    Attributes:
        _value: Current progress value, or None for indeterminate.
        _total: Maximum value representing 100% completion.
        _label: Optional text label describing the task.

    Example:
        Indeterminate loading indicator::

            nib.ProgressView()

        File download progress::

            nib.ProgressView(
                value=bytes_downloaded,
                total=total_bytes,
                label="Downloading file...",
                tint=nib.Color.green,
            )

        Task progress with percentage::

            nib.ProgressView(
                value=0.75,
                total=1.0,
                style=nib.ProgressStyle.linear,
            )

        Circular progress indicator::

            nib.ProgressView(
                value=3,
                total=10,
                style=nib.ProgressStyle.circular,
                tint=nib.Color.blue,
            )
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
        """Initialize a ProgressView.

        Args:
            value: Current progress value. When None, displays an indeterminate
                spinner. When provided, shows a progress bar filled to
                (value / total) percent. Must be between 0 and total.
            total: Maximum value representing 100% completion. Defaults to 1.0,
                which means value should be between 0.0 and 1.0. Set to 100
                for percentage values, or the actual total for counts.
            label: Optional text label displayed alongside the progress
                indicator. Useful for describing what task is in progress.
            style: Visual style of the progress indicator. Options:
                - ProgressStyle.automatic: System default
                - ProgressStyle.linear: Horizontal progress bar
                - ProgressStyle.circular: Circular/ring progress indicator
            tint: Tint color for the progress indicator fill.
                Accepts Color enum, hex string, or RGB tuple.
            **kwargs: Standard view modifiers including padding, background,
                opacity, width, height, etc.

        Example:
            Create a file upload progress indicator::

                nib.ProgressView(
                    value=uploaded_mb,
                    total=total_mb,
                    label=f"Uploading: {uploaded_mb}/{total_mb} MB",
                    style=nib.ProgressStyle.linear,
                    tint=nib.Color.blue,
                    width=200,
                )
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

    @property
    def value(self) -> Optional[float]:
        """Get the current progress value."""
        return self._value

    @value.setter
    def value(self, new_value: Optional[float]) -> None:
        """Set the progress value and trigger UI update.

        Args:
            new_value: Progress value (0 to total), or None for indeterminate.
        """
        if self._value != new_value:
            self._value = new_value
            self._trigger_update()

    @property
    def progress(self) -> Optional[float]:
        """Get the current progress as a fraction (0.0 to 1.0)."""
        if self._value is None:
            return None
        return self._value / self._total

    @progress.setter
    def progress(self, new_progress: Optional[float]) -> None:
        """Set the progress as a fraction and trigger UI update.

        Args:
            new_progress: Progress fraction (0.0 to 1.0), or None for indeterminate.
        """
        if new_progress is None:
            new_value = None
        else:
            new_value = new_progress * self._total
        if self._value != new_value:
            self._value = new_value
            self._trigger_update()

    @property
    def total(self) -> float:
        """Get the total value (100% completion)."""
        return self._total

    @total.setter
    def total(self, new_total: float) -> None:
        """Set the total value and trigger UI update."""
        if self._total != new_total:
            self._total = new_total
            self._trigger_update()

    @property
    def label(self) -> str:
        """Get the progress label."""
        return self._label

    @label.setter
    def label(self, new_label: str) -> None:
        """Set the progress label and trigger UI update."""
        if self._label != new_label:
            self._label = new_label
            self._trigger_update()

    def _get_props(self) -> dict:
        props = {}
        if self._value is not None:
            props["progress"] = _float(self._value / self._total)
        if self._label:
            props["label"] = self._label
        if self._progress_styles:
            props["progressStyles"] = self._progress_styles
        return props
