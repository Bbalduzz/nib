"""Link control that opens a URL in the default browser.

The Link view creates a tappable element that opens a URL when clicked.
It can display simple text or custom content views, and opens the URL
in the system's default web browser.

Example:
    Simple text link::

        nib.Link("Visit Website", url="https://example.com")

    Link with custom content::

        nib.Link(
            url="https://github.com/user/repo",
            content=nib.HStack(controls=[
                nib.Image(system_name="link"),
                nib.Text("View on GitHub"),
            ]),
        )

    Styled link::

        nib.Link(
            "Documentation",
            url="https://docs.example.com",
            foreground_color=nib.Color.blue,
        )
"""

from typing import Any, List, Optional
from ..base import View


class Link(View):
    """A control that opens a URL in the default browser when tapped.

    Link provides a clickable element that navigates to a URL. It can display
    a simple text title or custom content views. When tapped, the URL opens
    in the system's default web browser.

    Attributes:
        _title: The text string to display as the link.
        _url: The URL to open when tapped.
        _content: Custom view content (alternative to title).

    Example:
        Basic website link::

            nib.Link("Visit our website", url="https://example.com")

        Styled documentation link::

            nib.Link(
                "Read the docs",
                url="https://docs.example.com",
                foreground_color=nib.Color.blue,
                font=nib.Font.body,
            )

        Link with icon and text::

            nib.Link(
                url="https://github.com/user/repo",
                content=nib.HStack(controls=[
                    nib.Image(system_name="globe"),
                    nib.Text("Open in Browser", bold=True),
                ], spacing=4),
                foreground_color=nib.Color.blue,
            )

        Email link::

            nib.Link(
                "Contact Support",
                url="mailto:support@example.com",
            )
    """

    _type = "Link"

    def __init__(
        self,
        title: Optional[str] = None,
        url: str = "",
        content: Optional[View] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a Link view.

        Args:
            title: Text to display as the link. Use this for simple text links.
                For more complex content, use the content parameter instead.
            url: The URL to open when the link is tapped. Supports http://,
                https://, mailto:, tel:, and other URL schemes supported
                by the system.
            content: Custom View to display as the link content. This is an
                alternative to the title parameter and provides full control
                over the link's appearance. Cannot be used together with title.
            **kwargs: Standard view modifiers including foreground_color,
                font, padding, opacity, etc.

        Example:
            Create a help link::

                nib.Link(
                    "Need help?",
                    url="https://help.example.com",
                    foreground_color=nib.Color.blue,
                    font=nib.Font.footnote,
                )
        """
        super().__init__(**kwargs)
        self._title = title
        self._url = url
        self._content = content

    def _get_props(self) -> dict:
        props = {"url": self._url}
        if self._title:
            props["label"] = self._title
        return props

    def _get_children(self, parent_path: str, depth: int = 0) -> Optional[List[dict]]:
        """Return custom content as children if provided."""
        if self._content and self._content._visible:
            return [self._content.to_dict(f"{parent_path}.0", depth + 1)]
        return None
