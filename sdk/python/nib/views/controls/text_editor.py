"""TextEditor view for multi-line text editing.

Provides a multi-line text input control, similar to a textarea in HTML.
"""

from typing import TYPE_CHECKING, Callable, Optional, Union
from ..base import View

if TYPE_CHECKING:
    from ...types import Color, Font, TextEditorStyle


class TextEditor(View):
    """A view that displays a multi-line text editor.

    TextEditor is suitable for editing longer text content like notes,
    descriptions, or any multi-line input.

    Args:
        text: Initial text content.
        placeholder: Placeholder text when empty (macOS 14+).
        on_change: Callback when text changes, receives new text.
        style: TextEditorStyle for comprehensive styling.
        font: Text font (alternative to style).
        foreground_color: Text color (alternative to style).
        line_limit: Maximum number of lines (deprecated, use style).
        scrolls_disabled: Disable scrolling (deprecated, use style).
        content_background: Background color (deprecated, use style).
        **kwargs: Additional view modifiers.

    Example:
        Simple text editor::

            notes = nib.TextEditor(
                text="",
                placeholder="Enter your notes...",
                on_change=lambda text: print(f"Text: {text}"),
            )

        Using TextEditorStyle::

            nib.TextEditor(
                text=content,
                style=nib.TextEditorStyle(
                    font=nib.Font.custom("Iosevka", size=14),
                    foreground_color=nib.Color.PRIMARY,
                    background_color=nib.Color(hex="#1E1E1E"),
                    line_spacing=6,
                    text_alignment=nib.Alignment.LEADING,
                    editor_style=nib.EditorStyle.PLAIN,
                ),
            )
    """

    _type = "TextEditor"

    def __init__(
        self,
        text: str = "",
        placeholder: Optional[str] = None,
        on_change: Optional[Callable[[str], None]] = None,
        style: Optional["TextEditorStyle"] = None,
        font: Optional["Font"] = None,
        foreground_color: Optional[Union[str, "Color"]] = None,
        # Legacy params (deprecated — use style instead)
        line_limit: Optional[int] = None,
        scrolls_disabled: bool = False,
        content_background: Optional[Union[str, "Color", bool]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._text = text
        self._placeholder = placeholder
        self._on_change = on_change
        self._style = style
        self._font = font
        self._foreground_color = foreground_color

        # Legacy params
        self._legacy_line_limit = line_limit
        self._legacy_scrolls_disabled = scrolls_disabled
        self._legacy_content_background = content_background

    @property
    def text(self) -> str:
        """Current text content."""
        return self._text

    @text.setter
    def text(self, val: str) -> None:
        self._text = val
        self._trigger_update()

    @property
    def placeholder(self) -> Optional[str]:
        """Placeholder text."""
        return self._placeholder

    @placeholder.setter
    def placeholder(self, val: Optional[str]) -> None:
        self._placeholder = val
        self._trigger_update()

    @property
    def on_change(self) -> Optional[Callable[[str], None]]:
        """Text change callback."""
        return self._on_change

    @on_change.setter
    def on_change(self, val: Optional[Callable[[str], None]]) -> None:
        self._on_change = val

    @property
    def style(self) -> Optional["TextEditorStyle"]:
        """Text editor style configuration."""
        return self._style

    @style.setter
    def style(self, val: Optional["TextEditorStyle"]) -> None:
        self._style = val
        self._trigger_update()

    def _get_props(self) -> dict:
        from ...types import Color, Font

        props = {
            "text": self._text,
        }
        if self._placeholder is not None:
            props["placeholder"] = self._placeholder

        # Build textEditorStyles from style + standalone params + legacy params
        editor_styles = {}

        # Style object takes highest precedence
        if self._style is not None:
            editor_styles = self._style.to_dict()

        # Standalone font/foreground_color (lower priority than style)
        if self._font is not None and "font" not in editor_styles:
            if isinstance(self._font, Font):
                editor_styles["font"] = self._font.to_dict()
            else:
                editor_styles["font"] = {"fontName": self._font}

        if self._foreground_color is not None and "foregroundColor" not in editor_styles:
            if isinstance(self._foreground_color, Color):
                editor_styles["foregroundColor"] = self._foreground_color.to_dict()
            else:
                editor_styles["foregroundColor"] = self._foreground_color

        # Legacy params (lowest priority)
        if self._legacy_line_limit is not None and "lineLimit" not in editor_styles:
            editor_styles["lineLimit"] = self._legacy_line_limit
        if self._legacy_scrolls_disabled and "scrollsDisabled" not in editor_styles:
            editor_styles["scrollsDisabled"] = True
        if self._legacy_content_background is not None and "backgroundColor" not in editor_styles:
            if self._legacy_content_background is False or self._legacy_content_background == "hidden":
                editor_styles["contentBackgroundHidden"] = True
            elif isinstance(self._legacy_content_background, Color):
                editor_styles["backgroundColor"] = self._legacy_content_background.to_dict()
            else:
                editor_styles["backgroundColor"] = self._legacy_content_background

        if editor_styles:
            props["textEditorStyles"] = editor_styles

        return props

    def _handle_event(self, event: str) -> None:
        if event.startswith("change:") and self._on_change:
            new_text = event[7:]  # Remove "change:" prefix
            self._text = new_text
            self._on_change(new_text)
