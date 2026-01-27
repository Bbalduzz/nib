"""Label - A view combining an icon and text with declarative parameter-based API."""

from typing import Any, List, Optional, Union
from ..base import View
from ...types import LabelStyle, resolve_enum


class Label(View):
    """
    A view that combines a title and an icon.

        Label("Settings", icon="gear")

        Label(
            "Favorites",
            icon="star.fill",
            style=LabelStyle.titleAndIcon,
            foreground_color=Color.yellow,
        )

        # Custom content
        Label(
            title_view=Text("Custom Title", bold=True),
            icon_view=Image(system_name="star.fill", foreground_color=Color.yellow),
        )
    """

    _type = "Label"

    def __init__(
        self,
        title: Optional[str] = None,
        icon: Optional[str] = None,
        title_view: Optional[View] = None,
        icon_view: Optional[View] = None,
        # Label-specific styling
        style: Optional[Union[LabelStyle, str]] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """
        Create a label.

        Args:
            title: The label's text (simple string)
            icon: SF Symbol name (e.g., "gear", "star.fill")
            title_view: Custom View for the title (alternative to title string)
            icon_view: Custom View for the icon (alternative to icon string)
            style: Label display style (LabelStyle enum)
        """
        super().__init__(**kwargs)
        self._title = title
        self._icon = icon
        self._title_view = title_view
        self._icon_view = icon_view

        # Build label-specific styles
        self._label_styles: dict = {}
        if style is not None:
            self._label_styles["labelStyle"] = resolve_enum(style)

    def _get_props(self) -> dict:
        props = {}
        if self._title:
            props["label"] = self._title
        if self._icon:
            props["icon"] = self._icon
        if self._label_styles:
            props["labelStyles"] = self._label_styles
        return props

    def _get_children(self, parent_path: str) -> Optional[List[dict]]:
        """Return custom content as children if provided."""
        children = []
        if self._title_view:
            children.append({"role": "title", **self._title_view.to_dict(f"{parent_path}.title")})
        if self._icon_view:
            children.append({"role": "icon", **self._icon_view.to_dict(f"{parent_path}.icon")})
        return children if children else None
