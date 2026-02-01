"""Markdown view for displaying rich formatted text.

The Markdown view renders CommonMark/GitHub Flavored Markdown content
using SwiftUI's MarkdownUI library.

Supported elements:
    - Headings (# through ######)
    - Paragraphs and line breaks
    - Bold (**text**) and italic (*text*)
    - Strikethrough (~~text~~)
    - Code (inline `code` and code blocks)
    - Links [text](url)
    - Lists (bulleted and numbered)
    - Blockquotes (> quote)
    - Task lists (- [ ] / - [x])
    - Tables
    - Images

Example:
    Basic markdown::

        nib.Markdown('''
        # Hello World

        This is **bold** and *italic* text.

        - Item 1
        - Item 2
        ''')

    Markdown with theme::

        nib.Markdown(
            content="# Title",
            theme="gitHub",  # or "docC" or "basic"
        )
"""

from typing import Any, Optional
from ..base import View


class Markdown(View):
    """A view that renders Markdown formatted text.

    Markdown provides rich text formatting using CommonMark syntax.
    It supports headings, lists, code blocks, links, images, and more.

    The content property is reactive - changing it triggers a UI update.

    Attributes:
        content: The Markdown string to render.

    Example:
        Basic markdown::

            md = nib.Markdown('''
            # Welcome

            This is a **bold** statement.

            ```python
            print("Hello!")
            ```
            ''')

        Reactive updates::

            md = nib.Markdown("# Counter: 0")

            def update():
                md.content = f"# Counter: {count}"

        With a theme::

            nib.Markdown(
                "# Styled",
                theme="gitHub",
            )
    """

    _type = "Markdown"

    def __init__(
        self,
        content: str,
        theme: Optional[str] = None,
        **kwargs: Any,
    ):
        """Initialize a Markdown view.

        Args:
            content: The Markdown string to render.
            theme: Optional theme name. Options: "basic" (default), "gitHub", "docC".
            **kwargs: Standard view modifiers including padding, background, etc.

        Example:
            Simple markdown::

                nib.Markdown("# Hello **World**")

            With GitHub theme::

                nib.Markdown(
                    "# README\\n\\nContent here...",
                    theme="gitHub",
                )
        """
        super().__init__(**kwargs)
        self._content = content
        self._theme = theme

    @property
    def content(self) -> str:
        """Get the Markdown content.

        Returns:
            The current Markdown string being rendered.
        """
        return self._content

    @content.setter
    def content(self, new_content: str) -> None:
        """Set the Markdown content and trigger UI update.

        Args:
            new_content: The new Markdown string to render.

        Note:
            Only triggers a UI update if the content actually changed.
        """
        if self._content != new_content:
            self._content = new_content
            self._trigger_update()

    @property
    def theme(self) -> Optional[str]:
        """Get the current theme."""
        return self._theme

    @theme.setter
    def theme(self, new_theme: Optional[str]) -> None:
        """Set the theme and trigger UI update."""
        if self._theme != new_theme:
            self._theme = new_theme
            self._trigger_update()

    def _get_props(self) -> dict:
        props = {"content": str(self._content)}
        if self._theme is not None:
            props["theme"] = self._theme
        return props
