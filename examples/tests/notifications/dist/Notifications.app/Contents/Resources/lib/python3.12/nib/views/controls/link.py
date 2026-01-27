"""Link - A control that opens a URL with declarative parameter-based API."""

from typing import Any, List, Optional
from ..base import View


class Link(View):
    """
    A control that opens a URL when tapped.

        Link("Visit Website", url="https://example.com")

        Link(
            url="https://example.com",
            content=HStack([
                Image(system_name="globe"),
                Text("Visit Website", bold=True),
            ]),
            foreground_color=Color.blue,
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
        """
        Create a link.

        Args:
            title: The link's display text (use this OR content)
            url: The URL to open
            content: Custom View content for the link (alternative to title)
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

    def _get_children(self, parent_path: str) -> Optional[List[dict]]:
        """Return custom content as children if provided."""
        if self._content:
            return [self._content.to_dict(f"{parent_path}.0")]
        return None
