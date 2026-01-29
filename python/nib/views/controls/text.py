"""Text view for displaying static or dynamic text content.

The Text view displays a string of text with optional styling via TextStyle,
which groups font, decorations (bold, italic, underline, strikethrough),
and spacing options into a single configuration object.

Example:
    Basic text::

        nib.Text("Hello, World!")

    Using a preset style::

        nib.Text("Title", style=nib.TextStyle.TITLE)

    Using a custom style::

        nib.Text(
            "Custom styled text",
            style=nib.TextStyle(
                font=nib.Font.system(18),
                bold=True,
                underline=True,
                color="#FF5733",
            ),
        )

    Text with truncation::

        nib.Text(
            "Long text content...",
            style=nib.TextStyle.BODY,
            line_limit=2,
            truncation_mode=nib.TruncationMode.TAIL,
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
    Styling is configured via TextStyle, which groups font, decorations,
    and spacing into a single object.

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

        Using preset styles::

            nib.Text("Title", style=nib.TextStyle.TITLE)
            nib.Text("Body text", style=nib.TextStyle.BODY)

        Custom styled text::

            nib.Text(
                "Important Notice",
                style=nib.TextStyle(
                    font=nib.Font.TITLE,
                    color=nib.Color.RED,
                    bold=True,
                    underline=True,
                ),
            )
    """

    _type = "Text"

    def __init__(
        self,
        content: str,
        # TextStyle (includes font, decorations, spacing)
        style: Optional[TextStyle] = None,
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
            style: A TextStyle that configures font, decorations, and spacing.
                Can be a preset (TextStyle.TITLE) or custom TextStyle instance.
            line_limit: Maximum number of lines to display.
            truncation_mode: How to truncate text that exceeds line_limit.
                Options: TruncationMode.HEAD, TruncationMode.MIDDLE, TruncationMode.TAIL.
            minimum_scale_factor: Minimum scale factor for text shrinking (0.0-1.0).
            allows_tightening: Whether to allow tightening character spacing.
            text_case: Text case transformation. Options: TextCase.UPPERCASE,
                TextCase.LOWERCASE.
            **kwargs: Standard view modifiers including font, foreground_color,
                padding, background, opacity, etc.

        Example:
            Using a preset style::

                nib.Text("Title", style=nib.TextStyle.TITLE)

            Using a custom style::

                nib.Text(
                    "Custom styled text",
                    style=nib.TextStyle(
                        font=nib.Font.system(18),
                        bold=True,
                        underline=True,
                        color="#FF5733",
                    ),
                )

            With layout options::

                nib.Text(
                    "Long text...",
                    style=nib.TextStyle.BODY,
                    line_limit=2,
                    truncation_mode=nib.TruncationMode.TAIL,
                )
        """
        # Apply style settings to kwargs (style.font -> kwargs["font"], etc.)
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

        # Build text-specific styles from TextStyle
        self._text_styles: dict = {}

        if style is not None:
            # Extract text decorations and spacing from style
            style_dict = style.to_dict()
            # Copy relevant keys (excluding font/color/weight which are handled above)
            for key in ["bold", "italic", "strikethrough", "strikethroughColor",
                        "underline", "underlineColor", "monospaced", "monospacedDigit",
                        "kerning", "tracking", "baselineOffset"]:
                if key in style_dict:
                    self._text_styles[key] = style_dict[key]

        # Layout options
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
