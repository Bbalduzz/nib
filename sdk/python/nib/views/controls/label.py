"""Label view combining text and an SF Symbol icon.

The Label view displays a title alongside an icon, commonly used for menu items,
list rows, and descriptive UI elements. It supports both simple string-based
titles/icons and fully custom view content.

Example:
    Simple label with icon::

        nib.Label("Settings", icon="gear")

    Styled label::

        nib.Label(
            "Favorites",
            icon="star.fill",
            foreground_color=nib.Color.yellow,
        )

    Label with custom views::

        nib.Label(
            title_view=nib.Text("Custom Title", bold=True),
            icon_view=nib.Image(system_name="star.fill"),
        )
"""

from typing import Any, List, Optional, Union
from ..base import View
from ...types import LabelStyle, resolve_enum


class Label(View):
    """A view that combines a title and an icon.

    Label provides a standardized way to display an icon alongside text,
    following Apple's Human Interface Guidelines. It's commonly used in
    navigation items, list rows, and menu entries.

    Labels can be created with simple strings for the title and icon, or
    with custom views for more control over appearance.

    Attributes:
        _title: The text string for the label title.
        _icon: The SF Symbol name for the icon.
        _title_view: Custom view for the title (alternative to string).
        _icon_view: Custom view for the icon (alternative to SF Symbol).

    Example:
        Simple label for settings::

            nib.Label("Settings", icon="gear")

        Colored label for favorites::

            nib.Label(
                "Favorites",
                icon="star.fill",
                style=nib.LabelStyle.titleAndIcon,
                foreground_color=nib.Color.yellow,
            )

        Label showing icon only::

            nib.Label(
                "Hidden Title",
                icon="bell.fill",
                style=nib.LabelStyle.iconOnly,
            )

        Label with custom content views::

            nib.Label(
                title_view=nib.Text("Premium", bold=True, foreground_color=nib.Color.gold),
                icon_view=nib.Image(system_name="crown.fill", foreground_color=nib.Color.gold),
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
        """Initialize a Label view.

        Args:
            title: The text string to display as the label title. Use this
                for simple text labels. For more control, use title_view.
            icon: SF Symbol name for the icon (e.g., "gear", "star.fill",
                "bell.badge"). Use this for standard system icons. For
                custom icons, use icon_view.
            title_view: Custom View to use as the title. This is an alternative
                to the title parameter and allows full styling control.
                Cannot be used together with title parameter.
            icon_view: Custom View to use as the icon. This is an alternative
                to the icon parameter and allows using custom images or
                styled SF Symbols. Cannot be used together with icon parameter.
            style: Visual style determining which parts of the label are shown.
                Options:
                - LabelStyle.automatic: System default (usually title and icon)
                - LabelStyle.titleOnly: Show only the title text
                - LabelStyle.iconOnly: Show only the icon
                - LabelStyle.titleAndIcon: Show both title and icon
            **kwargs: Standard view modifiers including padding, background,
                foreground_color, font, opacity, etc.

        Example:
            Create a navigation label::

                nib.Label(
                    "Documents",
                    icon="folder.fill",
                    style=nib.LabelStyle.titleAndIcon,
                    foreground_color=nib.Color.blue,
                )
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
        if self._title_view and self._title_view._visible:
            children.append({"role": "title", **self._title_view.to_dict(f"{parent_path}.title")})
        if self._icon_view and self._icon_view._visible:
            children.append({"role": "icon", **self._icon_view.to_dict(f"{parent_path}.icon")})
        return children if children else None
