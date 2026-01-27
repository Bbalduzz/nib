"""Text view for displaying static or dynamic text content.

The Text view displays a string of text with optional styling including
font, color, truncation, text transformations, and various text decorations
like bold, italic, underline, and strikethrough.

Example:
    Basic text::

        nib.Text("Hello, World!")

    Styled text::

        nib.Text(
            "Title",
            font=nib.Font.title,
            foreground_color=nib.Color.blue,
            bold=True,
        )

    Text with truncation::

        nib.Text(
            "Long text content...",
            line_limit=2,
            truncation_mode=nib.TruncationMode.tail,
        )
"""

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
    """A view that displays one or more lines of text.

    Text is the fundamental view for displaying read-only text in the UI.
    It supports rich styling options including fonts, colors, text decorations,
    and layout controls like line limits and truncation.

    The content property is reactive - changing it triggers a UI update.

    Attributes:
        content: The text string to display.

    Example:
        Basic text display::

            label = nib.Text("Hello, World!")

        Reactive text updates::

            counter = nib.Text("0")

            def increment():
                counter.content = str(int(counter.content) + 1)

        Styled text with decorations::

            nib.Text(
                "Important Notice",
                font=nib.Font.title,
                foreground_color=nib.Color.red,
                bold=True,
                underline=True,
            )

        Text with style preset::

            nib.Text(
                "Heading",
                style=nib.TextStyle.headline,
            )
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
        """Initialize a Text view.

        Args:
            content: The text string to display.
            style: A TextStyle preset that sets font, color, and weight together.
                Individual font/color/weight parameters override style settings.
            bold: Whether to render the text in bold.
            italic: Whether to render the text in italic.
            strikethrough: Whether to add a strikethrough line.
            strikethrough_color: Color of the strikethrough line (hex string).
            underline: Whether to add an underline.
            underline_color: Color of the underline (hex string).
            monospaced: Whether to use a monospaced font.
            monospaced_digit: Whether to use monospaced digits for numbers.
            kerning: Character spacing adjustment in points.
            tracking: Additional spacing between characters.
            baseline_offset: Vertical offset from the baseline in points.
            line_limit: Maximum number of lines to display.
            truncation_mode: How to truncate text that exceeds line_limit.
                Options: TruncationMode.head, TruncationMode.middle, TruncationMode.tail.
            minimum_scale_factor: Minimum scale factor for text shrinking (0.0-1.0).
            allows_tightening: Whether to allow tightening character spacing.
            text_case: Text case transformation. Options: TextCase.uppercase,
                TextCase.lowercase.
            **kwargs: Standard view modifiers including font, foreground_color,
                padding, background, opacity, etc.

        Example:
            Create styled text with truncation::

                nib.Text(
                    "This is a very long text that might get truncated",
                    font=nib.Font.body,
                    foreground_color=nib.Color.gray,
                    line_limit=1,
                    truncation_mode=nib.TruncationMode.tail,
                )
        """
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
        """Get the text content.

        Returns:
            The current text string being displayed.
        """
        return self._content

    @content.setter
    def content(self, new_content: str) -> None:
        """Set the text content and trigger UI update.

        Args:
            new_content: The new text string to display.

        Note:
            Only triggers a UI update if the content actually changed.
        """
        if self._content != new_content:
            self._content = new_content
            self._trigger_update()

    def _get_props(self) -> dict:
        props = {"content": str(self._content)}
        if self._text_styles:
            props["textStyles"] = self._text_styles
        return props
