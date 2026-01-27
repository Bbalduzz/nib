"""Text - Text display view with declarative parameter-based API."""

from typing import Any, Optional, Union
from ..base import View, _float
from ...types import (
    Font,
    FontWeightLike,
    TextStyle,
    TruncationMode,
    TextCase,
    resolve_enum,
)


# Type aliases
TruncationModeLike = Union[TruncationMode, str]
TextCaseLike = Union[TextCase, str]


class Text(View):
    """
    A view that displays one or more lines of text.

    The content property can be read and written directly:

        label = nib.Text("0")

        def increment(e):
            label.content = str(int(label.content) + 1)

    All styling is done via constructor parameters:

        Text(
            "Hello World",
            font=Font.title,
            foreground_color=Color.blue,
            bold=True,
        )

    Supports all View modifiers (padding, background, overlay, etc.) via **kwargs.
    """

    _type = "Text"

    def __init__(
        self,
        content: str,
        # TextStyle preset
        style: Optional[TextStyle] = None,
        # Text-specific styling
        bold: bool = False,
        italic: bool = False,
        strikethrough: bool = False,
        strikethrough_color: Optional[str] = None,
        underline: bool = False,
        underline_color: Optional[str] = None,
        monospaced: bool = False,
        monospaced_digit: bool = False,
        kerning: Optional[float] = None,
        tracking: Optional[float] = None,
        baseline_offset: Optional[float] = None,
        # Text layout
        line_limit: Optional[int] = None,
        truncation_mode: Optional[TruncationModeLike] = None,
        minimum_scale_factor: Optional[float] = None,
        allows_tightening: bool = False,
        # Text case
        text_case: Optional[TextCaseLike] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        # Apply style preset first if provided
        if style is not None:
            if style.font and "font" not in kwargs:
                kwargs["font"] = style.font
            if style.color and "foreground_color" not in kwargs:
                kwargs["foreground_color"] = style.color
            if style.weight and "font_weight" not in kwargs:
                kwargs["font_weight"] = style.weight

        # Initialize base View with modifiers
        super().__init__(**kwargs)

        self._content = content

        # Build text-specific styles
        self._text_styles: dict = {}

        if bold:
            self._text_styles["bold"] = True
        if italic:
            self._text_styles["italic"] = True
        if strikethrough:
            self._text_styles["strikethrough"] = True
            if strikethrough_color:
                self._text_styles["strikethroughColor"] = strikethrough_color
        if underline:
            self._text_styles["underline"] = True
            if underline_color:
                self._text_styles["underlineColor"] = underline_color
        if monospaced:
            self._text_styles["monospaced"] = True
        if monospaced_digit:
            self._text_styles["monospacedDigit"] = True
        if kerning is not None:
            self._text_styles["kerning"] = _float(kerning)
        if tracking is not None:
            self._text_styles["tracking"] = _float(tracking)
        if baseline_offset is not None:
            self._text_styles["baselineOffset"] = _float(baseline_offset)
        if line_limit is not None:
            self._text_styles["lineLimit"] = line_limit
        if truncation_mode is not None:
            self._text_styles["truncationMode"] = resolve_enum(truncation_mode)
        if minimum_scale_factor is not None:
            self._text_styles["minimumScaleFactor"] = _float(minimum_scale_factor)
        if allows_tightening:
            self._text_styles["allowsTightening"] = True
        if text_case is not None:
            self._text_styles["textCase"] = resolve_enum(text_case)

    @property
    def content(self) -> str:
        """Get the text content."""
        return self._content

    @content.setter
    def content(self, new_content: str) -> None:
        """Set the text content and trigger UI update."""
        if self._content != new_content:
            self._content = new_content
            self._trigger_update()

    def _get_props(self) -> dict:
        props = {"content": str(self._content)}
        if self._text_styles:
            props["textStyles"] = self._text_styles
        return props
