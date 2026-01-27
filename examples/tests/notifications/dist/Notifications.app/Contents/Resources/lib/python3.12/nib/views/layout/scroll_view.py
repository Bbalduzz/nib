"""ScrollView - A scrollable container view."""

from typing import Any, List as ListType, Literal
from ..base import View


class ScrollView(View):
    """
    A scrollable container view.

    Example:
        ScrollView(controls=[
            Text("Item 1"),
            Text("Item 2"),
            Text("Item 3"),
        ])

        # Horizontal scrolling
        ScrollView(controls=[...], axes="horizontal")

        # Hide scroll indicators
        ScrollView(controls=[...], shows_indicators=False)
    """

    _type = "ScrollView"

    def __init__(
        self,
        controls: ListType[View] = None,
        # Alias for backwards compatibility
        children: ListType[View] = None,
        axes: Literal["vertical", "horizontal", "both"] = "vertical",
        shows_indicators: bool = True,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """
        Create a scrollable container.

        Args:
            children: Child views to display in the scroll view
            axes: Scroll direction - "vertical", "horizontal", or "both"
            shows_indicators: Whether to show scroll indicators
        """
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])
        self._axes = axes
        self._shows_indicators = shows_indicators

    def _get_props(self) -> dict:
        return {
            "axes": self._axes,
            "showsIndicators": self._shows_indicators,
        }

    def _get_children(self, parent_path: str) -> ListType[dict]:
        return [child.to_dict(f"{parent_path}.{i}") for i, child in enumerate(self._children)]
