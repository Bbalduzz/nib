"""Nib notification system.

This module provides a comprehensive API for macOS notifications using
the UserNotifications framework.

Example:
    Basic notification::

        import nib

        notification = nib.Notification(
            title="Hello",
            body="World"
        )
        app.notifications.push(notification)

    Notification with sound::

        notification = nib.Notification(
            title="Alert",
            body="Something happened",
            sound=nib.NotificationSound(
                name=nib.NotificationSoundName.DEFAULT
            )
        )

    Notification with actions::

        notification = nib.Notification(
            title="New Message",
            body="John: Hey!",
            actions=[
                nib.NotificationAction(
                    id="reply",
                    title="Reply",
                    text_input=nib.TextInputNotificationAction(
                        button_title="Send",
                        placeholder="Type reply..."
                    )
                ),
                nib.NotificationAction(
                    id="dismiss",
                    title="Dismiss"
                )
            ]
        )

    Scheduled notification::

        from datetime import datetime, timedelta

        notification = nib.Notification(title="Reminder", body="Time!")
        app.notifications.schedule(notification, at=datetime.now() + timedelta(hours=1))

Note:
    Critical alerts require a special entitlement from Apple:
    https://developer.apple.com/contact/request/notifications-critical-alerts-entitlement/
"""

from .manager import NotificationManager
from .notification import Notification
from .types import (
    CustomNotificationSoundName,
    NotificationAction,
    NotificationActionOption,
    NotificationSound,
    NotificationSoundName,
    TextInputNotificationAction,
)

__all__ = [
    # Main classes
    "Notification",
    "NotificationManager",
    # Sound types
    "NotificationSound",
    "NotificationSoundName",
    "CustomNotificationSoundName",
    # Action types
    "NotificationAction",
    "NotificationActionOption",
    "TextInputNotificationAction",
]
