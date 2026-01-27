"""Section - A container for grouping content with optional header and footer."""

from typing import Any, List as ListType, Optional
from ..base import View


class Section(View):
    """
    A container for grouping content with optional header and footer.

    Example:
        Section(controls=[
            Text("Item 1"),
            Text("Item 2"),
        ], header="My Section")

        # With header and footer
        Section(
            controls=[Text("Content")],
            header="Header Text",
            footer="Footer Text"
        )
    """

    _type = "Section"

    def __init__(
        self,
        controls: ListType[View] = None,
        # Alias for backwards compatibility
        children: ListType[View] = None,
        header: Optional[str] = None,
        footer: Optional[str] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """
        Create a section.

        Args:
            children: Child views in the section
            header: Optional header text
            footer: Optional footer text
        """
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])
        self._header = header
        self._footer = footer

    def _get_props(self) -> dict:
        props = {}
        if self._header:
            props["header"] = self._header
        if self._footer:
            props["footer"] = self._footer
        return props

    def _get_children(self, parent_path: str) -> ListType[dict]:
        return [child.to_dict(f"{parent_path}.{i}") for i, child in enumerate(self._children)]
