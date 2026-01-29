"""ShareLink view for native share sheet integration.

Provides a button that opens the system share sheet.
"""

from typing import TYPE_CHECKING, List, Optional, Union
from ..base import View

if TYPE_CHECKING:
    from ...types import Color


class ShareLink(View):
    """A view that presents a share sheet for sharing content.

    ShareLink provides native macOS share sheet integration, allowing
    users to share text, URLs, images, or files through system services.

    Args:
        items: Items to share (strings, URLs, or file paths).
        content: Optional view to use as the button label.
        label: Button label text (used if content is not provided).
        icon: Optional SF Symbol name for the button.
        **kwargs: Additional view modifiers.

    Example:
        Share with text label::

            nib.ShareLink(
                items=["Check out this cool app!"],
                label="Share",
            )

        Share with custom view label::

            nib.ShareLink(
                items=["https://example.com"],
                content=nib.HStack(
                    controls=[
                        nib.Image(system_name="square.and.arrow.up"),
                        nib.Text("Share Link"),
                    ],
                    spacing=4,
                ),
            )

        Share with icon and text::

            nib.ShareLink(
                items=["https://example.com"],
                label="Share Link",
                icon="square.and.arrow.up",
            )

        Share file::

            nib.ShareLink(
                items=["/path/to/file.pdf"],
                label="Share File",
            )
    """

    _type = "ShareLink"

    def __init__(
        self,
        items: List[str],
        content: Optional[View] = None,
        label: Optional[str] = None,
        icon: Optional[str] = None,
        subject: Optional[str] = None,
        message: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._items = items
        self._content = content
        self._label = label
        self._icon = icon
        self._subject = subject  # For email shares
        self._message = message  # For social shares

        if self._content is not None:
            self._content._parent = self

    @property
    def items(self) -> List[str]:
        """Items to share."""
        return self._items

    @items.setter
    def items(self, val: List[str]) -> None:
        self._items = val
        self._mark_dirty()

    @property
    def content(self) -> Optional[View]:
        """Custom view label."""
        return self._content

    @content.setter
    def content(self, val: Optional[View]) -> None:
        if self._content is not None:
            self._content._parent = None
        self._content = val
        if self._content is not None:
            self._content._parent = self
        self._mark_dirty()

    @property
    def label(self) -> Optional[str]:
        """Button label."""
        return self._label

    @label.setter
    def label(self, val: Optional[str]) -> None:
        self._label = val
        self._mark_dirty()

    @property
    def icon(self) -> Optional[str]:
        """SF Symbol icon name."""
        return self._icon

    @icon.setter
    def icon(self, val: Optional[str]) -> None:
        self._icon = val
        self._mark_dirty()

    def _get_props(self) -> dict:
        props = {
            "items": self._items,
        }
        if self._label is not None:
            props["label"] = self._label
        if self._icon is not None:
            props["icon"] = self._icon
        if self._subject is not None:
            props["subject"] = self._subject
        if self._message is not None:
            props["message"] = self._message
        return props

    def _get_children(self, parent_path: str = "") -> list:
        if self._content is not None and self._content._visible:
            return [self._content.to_dict(f"{parent_path}.0")]
        return []
