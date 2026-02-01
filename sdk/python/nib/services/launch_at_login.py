"""Launch at Login service for macOS apps.

Provides the ability to enable/disable launching the app at user login.
This is required for Mac App Store apps to implement "Launch at Login"
functionality in response to a user action.

Example:
    Toggle launch at login::

        def toggle_launch_login():
            if app.launch_at_login.is_enabled:
                app.launch_at_login.set(False)
            else:
                app.launch_at_login.set(True)

        nib.Button("Launch at Login", action=toggle_launch_login)
"""

from typing import TYPE_CHECKING

from .base import Service

if TYPE_CHECKING:
    from ..core.app import App


class LaunchAtLogin(Service):
    """Service for managing Launch at Login state.

    Access via app.launch_at_login property.

    This service uses SMAppService on macOS 13+ to register the app
    as a login item. Per Mac App Store guidelines, this should only
    be enabled in response to a user action.

    Example:
        Check and toggle launch at login::

            # Check current state
            if app.launch_at_login.is_enabled:
                print("App will launch at login")

            # Enable (call in response to user action)
            app.launch_at_login.set(True)

            # Disable
            app.launch_at_login.set(False)

        With a toggle button::

            toggle = nib.Toggle(
                is_on=app.launch_at_login.is_enabled,
                label="Launch at Login",
                on_change=lambda is_on: app.launch_at_login.set(is_on),
            )
    """

    @property
    def is_enabled(self) -> bool:
        """Check if the app is set to launch at login.

        Returns:
            True if launch at login is enabled, False otherwise.
        """
        data = self._request("launchAtLogin", "status")
        return data.get("enabled", False)

    def set(self, enabled: bool) -> bool:
        """Set the launch at login state.

        Per Mac App Store guidelines, this should only be called
        in response to a user action (e.g., button click, toggle change).

        Args:
            enabled: True to enable launch at login, False to disable.

        Returns:
            True if the operation was successful.
        """
        data = self._request(
            "launchAtLogin", "set",
            params={"enabled": enabled},
        )
        return data.get("success", False)
