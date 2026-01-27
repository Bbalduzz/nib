"""Group - A transparent container for grouping views."""

from typing import Any, List as ListType
from ..base import View


class Group(View):
    """
    A transparent container that groups views without adding visual structure.

    Useful for applying modifiers to multiple views at once or for
    returning multiple views from a conditional.

    Example:
        Group(controls=[
            Text("Line 1"),
            Text("Line 2"),
        ])
    """

    _type = "Group"

    def __init__(
        self,
        controls: ListType[View] = None,
        # Alias for backwards compatibility
        children: ListType[View] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """
        Create a group.

        Args:
            controls: Child views to group
        """
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])

    def _get_props(self) -> dict:
        return {}

    def _get_children(self, parent_path: str) -> ListType[dict]:
        return [child.to_dict(f"{parent_path}.{i}") for i, child in enumerate(self._children)]
