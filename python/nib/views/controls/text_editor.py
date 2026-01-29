"""TextEditor view for multi-line text editing.

Provides a multi-line text input control, similar to a textarea in HTML.
"""

from typing import TYPE_CHECKING, Callable, Optional, Union
from ..base import View

if TYPE_CHECKING:
    from ...types import Color, Font, TextStyle


class TextEditor(View):
    """A view that displays a multi-line text editor.

    TextEditor is suitable for editing longer text content like notes,
    descriptions, or any multi-line input.

    Args:
        text: Initial text content.
        placeholder: Placeholder text when empty (macOS 14+).
        on_change: Callback when text changes, receives new text.
        style: TextStyle for font, color, and text decorations.
        font: Text font (alternative to style).
        foreground_color: Text color (alternative to style).
        line_limit: Maximum number of lines (None for unlimited).
        scrolls_disabled: Disable scrolling within the editor.
        **kwargs: Additional view modifiers.

    Example:
        Simple text editor::

            notes = nib.TextEditor(
                text="",
                placeholder="Enter your notes...",
                on_change=lambda text: print(f"Text: {text}"),
            )

        Using TextStyle::

            nib.TextEditor(
                text=content,
                style=nib.TextStyle(
                    font=nib.Font.system(14),
                    color=nib.Color.PRIMARY,
                    monospaced=True,
                ),
            )

        Using preset style::

            nib.TextEditor(
                text=content,
                style=nib.TextStyle.BODY,
            )
    """

    _type = "TextEditor"

    def __init__(
        self,
        text: str = "",
        placeholder: Optional[str] = None,
        on_change: Optional[Callable[[str], None]] = None,
        style: Optional["TextStyle"] = None,
        font: Optional["Font"] = None,
        foreground_color: Optional[Union[str, "Color"]] = None,
        line_limit: Optional[int] = None,
        scrolls_disabled: bool = False,
        content_background: Optional[Union[str, "Color", bool]] = None,
        **kwargs,
    ):
        """Initialize a TextEditor.

        Args:
            text: Initial text content.
            placeholder: Placeholder text when empty (macOS 14+).
            on_change: Callback when text changes.
            style: TextStyle for font, color, and formatting.
            font: Text font (alternative to style).
            foreground_color: Text color (alternative to style).
            line_limit: Maximum number of lines.
            scrolls_disabled: Disable scrolling.
            content_background: Background color for the text area.
                - None: Use system default background
                - False or "hidden": Hide the default background (transparent)
                - Color/string: Use specified color as background
            **kwargs: Additional view modifiers (including background for outer view).
        """
        super().__init__(**kwargs)
        self._text = text
        self._placeholder = placeholder
        self._on_change = on_change
        self._style = style
        self._line_limit = line_limit
        self._scrolls_disabled = scrolls_disabled
        self._content_background = content_background

        # Style takes precedence, then individual font/color params
        if style is not None:
            self._font = style.font if style.font else font
            self._foreground_color = style.color if style.color else foreground_color
        else:
            self._font = font
            self._foreground_color = foreground_color

    @property
    def text(self) -> str:
        """Current text content."""
        return self._text

    @text.setter
    def text(self, val: str) -> None:
        self._text = val
        self._mark_dirty()

    @property
    def placeholder(self) -> Optional[str]:
        """Placeholder text."""
        return self._placeholder

    @placeholder.setter
    def placeholder(self, val: Optional[str]) -> None:
        self._placeholder = val
        self._mark_dirty()

    @property
    def on_change(self) -> Optional[Callable[[str], None]]:
        """Text change callback."""
        return self._on_change

    @on_change.setter
    def on_change(self, val: Optional[Callable[[str], None]]) -> None:
        self._on_change = val

    @property
    def style(self) -> Optional["TextStyle"]:
        """Text style configuration."""
        return self._style

    @style.setter
    def style(self, val: Optional["TextStyle"]) -> None:
        self._style = val
        if val is not None:
            if val.font:
                self._font = val.font
            if val.color:
                self._foreground_color = val.color
        self._mark_dirty()

    @property
    def line_limit(self) -> Optional[int]:
        """Maximum number of lines."""
        return self._line_limit

    @line_limit.setter
    def line_limit(self, val: Optional[int]) -> None:
        self._line_limit = val
        self._mark_dirty()

    @property
    def content_background(self) -> Optional[Union[str, "Color", bool]]:
        """Content background color."""
        return self._content_background

    @content_background.setter
    def content_background(self, val: Optional[Union[str, "Color", bool]]) -> None:
        self._content_background = val
        self._mark_dirty()

    def _get_props(self) -> dict:
        from ...types import Color

        props = {
            "text": self._text,
        }
        if self._placeholder is not None:
            props["placeholder"] = self._placeholder
        if self._line_limit is not None:
            props["lineLimit"] = self._line_limit
        if self._scrolls_disabled:
            props["scrollsDisabled"] = True

        # Handle content background
        if self._content_background is not None:
            if self._content_background is False or self._content_background == "hidden":
                props["contentBackgroundHidden"] = True
            elif isinstance(self._content_background, Color):
                props["contentBackground"] = self._content_background.to_dict()
            else:
                props["contentBackground"] = self._content_background

        # Include text styles from TextStyle
        if self._style is not None:
            text_styles = {}
            style_dict = self._style.to_dict()
            # Copy relevant text style keys
            for key in ["bold", "italic", "strikethrough", "strikethroughColor",
                        "underline", "underlineColor", "monospaced", "monospacedDigit",
                        "kerning", "tracking", "baselineOffset"]:
                if key in style_dict:
                    text_styles[key] = style_dict[key]
            if text_styles:
                props["textStyles"] = text_styles

        return props

    def _apply_modifiers(self) -> list:
        from ...types import Color, Font

        modifiers = super()._apply_modifiers()

        if self._font is not None:
            modifiers.append({
                "type": "font",
                "args": self._font._to_dict() if isinstance(self._font, Font) else {"fontName": self._font},
            })

        if self._foreground_color is not None:
            color_str = self._foreground_color.to_dict() if isinstance(self._foreground_color, Color) else self._foreground_color
            modifiers.append({
                "type": "foregroundColor",
                "args": {"color": color_str},
            })

        return modifiers

    def _handle_event(self, event: str) -> None:
        if event.startswith("change:") and self._on_change:
            new_text = event[7:]  # Remove "change:" prefix
            self._text = new_text
            self._on_change(new_text)
