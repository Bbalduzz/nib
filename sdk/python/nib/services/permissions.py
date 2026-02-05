"""Unified permission checking and requesting for Camera, Microphone, and Notifications.

Services are accessed via the app property:

Example:
    Checking and requesting permissions::

        def main(app: nib.App):
            status = app.permissions.check(nib.Permission.CAMERA)
            if status == nib.PermissionStatus.NOT_DETERMINED:
                granted = app.permissions.request(nib.Permission.CAMERA)
"""

from enum import Enum

from .base import Service


class Permission(Enum):
    """Permission types that can be checked and requested."""

    CAMERA = "camera"
    MICROPHONE = "microphone"
    NOTIFICATIONS = "notifications"


class PermissionStatus(Enum):
    """Status of a permission."""

    AUTHORIZED = "authorized"
    DENIED = "denied"
    NOT_DETERMINED = "notDetermined"
    RESTRICTED = "restricted"


class Permissions(Service):
    """Service for checking and requesting app permissions.

    Provides a unified API to check the current status of a permission
    and to request authorization from the user.
    """

    def check(self, permission: Permission) -> PermissionStatus:
        """Check the current status of a permission.

        Args:
            permission: The permission to check.

        Returns:
            The current status of the permission.
        """
        data = self._request(
            "permissions",
            "check",
            params={"permission": permission.value},
        )
        status_str = data.get("permissionStatus", "notDetermined")
        try:
            return PermissionStatus(status_str)
        except ValueError:
            return PermissionStatus.NOT_DETERMINED

    def request(self, permission: Permission) -> bool:
        """Request authorization for a permission.

        Shows the system permission dialog if the permission has not
        been determined yet. If already authorized or denied, returns
        the current state without showing a dialog.

        Args:
            permission: The permission to request.

        Returns:
            True if the permission was granted, False otherwise.
        """
        data = self._request(
            "permissions",
            "request",
            params={"permission": permission.value},
        )
        return data.get("success", False)
