"""Settings page components for Nib applications.

This module provides :class:`SettingsPage` and :class:`SettingsTab` for creating
tabbed preferences windows that follow macOS conventions.

Example:
    Creating a tabbed settings page::

        import nib

        def main(app: nib.App):
            app.settings = nib.SettingsPage(
                tabs=[
                    nib.SettingsTab(
                        "General",
                        icon="gear",
                        content=nib.VStack([
                            nib.Toggle("Dark Mode", is_on=False),
                            nib.Slider("Font Size", value=14),
                        ])
                    ),
                    nib.SettingsTab(
                        "Account",
                        icon="person",
                        content=nib.VStack([
                            nib.TextField("Username"),
                        ])
                    ),
                ]
            )

            app.build(nib.VStack([...]))

        nib.run(main)
"""

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .base import View


class SettingsTab:
    """A single tab in a settings page.

    Each tab has a title, optional icon, and content view that is displayed
    when the tab is selected.

    Args:
        title: The tab title displayed in the tab bar.
        icon: Optional SF Symbol name for the tab icon.
        content: The View to display when this tab is selected.

    Example:
        Creating a settings tab::

            nib.SettingsTab(
                "General",
                icon="gear",
                content=nib.VStack([
                    nib.Toggle("Enable Feature"),
                    nib.Slider("Volume", value=50),
                ], spacing=12)
            )
    """

    def __init__(
        self,
        title: str,
        icon: Optional[str] = None,
        content: Optional["View"] = None,
    ):
        """Initialize a settings tab.

        Args:
            title: The tab title.
            icon: Optional SF Symbol name.
            content: The content View for this tab.
        """
        self.title = title
        self.icon = icon
        self.content = content

    def _to_dict(self, id_prefix: str) -> dict:
        """Serialize the tab for the protocol.

        Args:
            id_prefix: ID prefix for the content view tree.

        Returns:
            Dictionary representation for Swift.
        """
        return {
            "title": self.title,
            "icon": self.icon,
            "content": self.content.to_dict(id_prefix) if self.content else None,
        }


class SettingsPage:
    """A settings page with optional tabs.

    Creates a preferences window that can contain either a single content view
    or multiple tabbed sections. Opens via Cmd+, or programmatically via open().

    Args:
        tabs: List of SettingsTab objects for a tabbed interface.
        content: Single View for a non-tabbed settings page.
            If provided without tabs, creates a single "General" tab.
        width: Window width in points (default: 450).
        height: Window height in points (default: 300).
        title: Window title (default: "Settings").

    Example:
        Tabbed settings::

            app.settings = nib.SettingsPage(
                width=500,
                height=400,
                tabs=[
                    nib.SettingsTab("General", icon="gear", content=...),
                    nib.SettingsTab("Advanced", icon="wrench", content=...),
                ]
            )

        Opening programmatically::

            nib.Button("Preferences", action=app.settings.open)
    """

    def __init__(
        self,
        tabs: Optional[List[SettingsTab]] = None,
        content: Optional["View"] = None,
        width: float = 450,
        height: float = 300,
        title: str = "Settings",
    ):
        """Initialize a settings page.

        Args:
            tabs: List of tabs for tabbed interface.
            content: Single content view (creates single tab).
            width: Window width.
            height: Window height.
            title: Window title.
        """
        self.tabs = tabs or []
        self.content = content
        self.width = width
        self.height = height
        self.title = title
        self._app = None  # Set by App when assigned to app.settings

        # If content provided without tabs, wrap in single tab
        if content and not tabs:
            self.tabs = [SettingsTab("General", icon="gear", content=content)]

    def open(self) -> None:
        """Open the settings window.

        Example:
            nib.Button("Preferences", action=app.settings.open)
        """
        if self._app and self._app._connection:
            self._app._connection.send_settings_open()

    def close(self) -> None:
        """Close the settings window."""
        if self._app and self._app._connection:
            self._app._connection.send_settings_close()

    def _to_dict(self, id_prefix: str = "settings") -> dict:
        """Serialize the settings page for the protocol.

        Args:
            id_prefix: ID prefix for view trees.

        Returns:
            Dictionary representation for Swift.
        """
        return {
            "width": self.width,
            "height": self.height,
            "title": self.title,
            "tabs": [
                tab._to_dict(f"{id_prefix}.{i}")
                for i, tab in enumerate(self.tabs)
            ],
        }
