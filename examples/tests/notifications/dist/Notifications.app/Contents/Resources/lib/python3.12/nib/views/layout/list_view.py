"""List - A container that displays rows of data arranged in a single column."""

from typing import Any, List as ListType
from ..base import View


class List(View):
    """
    A container that displays rows of data arranged in a single column.

    Example:
        List(controls=[
            Text("Item 1"),
            Text("Item 2"),
            Text("Item 3"),
        ])

        # With sections
        List(controls=[
            Section(controls=[Text("A Item")], header="Section A"),
            Section(controls=[Text("B Item")], header="Section B"),
        ])
    """

    _type = "List"

    def __init__(
        self,
        controls: ListType[View] = None,
        # Alias for backwards compatibility
        children: ListType[View] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """
        Create a list view.

        Args:
            children: Child views (typically rows or sections)
        """
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])

    def _get_props(self) -> dict:
        return {}

    def _get_children(self, parent_path: str) -> ListType[dict]:
        return [child.to_dict(f"{parent_path}.{i}") for i, child in enumerate(self._children)]
