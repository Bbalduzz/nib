"""Navigation views - NavigationStack, NavigationLink, DisclosureGroup."""

from typing import Any, Callable, List as ListType, Optional
from ..base import View


class NavigationStack(View):
    """
    A view that displays a root view and enables you to present additional views.

    Example:
        NavigationStack(controls=[
            NavigationLink("Go to Detail", destination=[
                Text("Detail View")
            ]),
        ])
    """

    _type = "NavigationStack"

    def __init__(
        self,
        controls: ListType[View] = None,
        # Alias for backwards compatibility
        children: ListType[View] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """
        Create a navigation stack.

        Args:
            controls: Root content views
        """
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])

    def _get_props(self) -> dict:
        return {}

    def _get_children(self, parent_path: str) -> ListType[dict]:
        return [child.to_dict(f"{parent_path}.{i}") for i, child in enumerate(self._children)]


class NavigationLink(View):
    """
    A view that controls a navigation presentation.

    Example:
        NavigationLink("Settings", destination=[
            Text("Settings Page"),
            Toggle("Enable notifications", is_on=True),
        ])
    """

    _type = "NavigationLink"

    def __init__(
        self,
        label: str,
        destination: Optional[ListType[View]] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """
        Create a navigation link.

        Args:
            label: The label text for the link
            destination: Views to display when navigated to
        """
        super().__init__(**kwargs)
        self._label = label
        self._destination = destination or []

    def _get_props(self) -> dict:
        return {"label": self._label}

    def _get_children(self, parent_path: str) -> ListType[dict]:
        return [child.to_dict(f"{parent_path}.{i}") for i, child in enumerate(self._destination)]


class DisclosureGroup(View):
    """
    A view that shows or hides another content view based on disclosure state.

    Example:
        DisclosureGroup("Advanced Options", controls=[
            Toggle("Enable feature A"),
            Toggle("Enable feature B"),
        ])

        # Initially expanded
        DisclosureGroup("Settings", controls=[...], is_expanded=True)
    """

    _type = "DisclosureGroup"

    def __init__(
        self,
        label: str,
        controls: ListType[View] = None,
        # Alias for backwards compatibility
        children: ListType[View] = None,
        is_expanded: bool = False,
        on_expand: Optional[Callable[[bool], None]] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """
        Create a disclosure group.

        Args:
            label: The label for the disclosure group
            controls: Content to show when expanded
            is_expanded: Initial expansion state
            on_expand: Callback when expansion state changes
        """
        super().__init__(**kwargs)
        self._label = label
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])
        self._is_expanded = is_expanded
        self._on_expand = on_expand

    def _get_props(self) -> dict:
        return {
            "label": self._label,
            "isExpanded": self._is_expanded,
        }

    def _get_children(self, parent_path: str) -> ListType[dict]:
        return [child.to_dict(f"{parent_path}.{i}") for i, child in enumerate(self._children)]

    def _handle_event(self, event: str) -> None:
        if event.startswith("expand:") and self._on_expand:
            value = event.split(":", 1)[1] == "true"
            self._on_expand(value)
