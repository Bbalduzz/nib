# Notifications

Nib provides a comprehensive API for macOS notifications using the UserNotifications framework. You can push notifications immediately, schedule them for future delivery, add interactive action buttons with text input, and handle user responses.

```python
import nib

def main(app: nib.App):
    # Request permission first
    app.notifications.request_permission()

    # Push a notification
    notification = nib.Notification(
        title="Hello",
        body="This is a notification from Nib"
    )
    app.notifications.push(notification)

nib.run(main)
```

## Overview

The notification system consists of three parts:

| Class | Description |
|-------|-------------|
| [Notification](notification.md) | Dataclass representing a single notification with title, body, sound, and actions |
| [NotificationManager](manager.md) | Manager accessed via `app.notifications` for pushing, scheduling, canceling, and querying notifications |
| [Sound & Actions](types.md) | Supporting types: `NotificationSound`, `NotificationSoundName`, `NotificationAction`, `NotificationActionOption`, `TextInputNotificationAction` |

## Quick Reference

```python
import nib
from datetime import datetime, timedelta

def main(app: nib.App):
    # Request permission
    app.notifications.request_permission(
        callback=lambda granted: print(f"Permission: {granted}")
    )

    # Push immediately
    app.notifications.push(nib.Notification(title="Hello", body="World"))

    # Schedule for later
    app.notifications.schedule(
        nib.Notification(title="Reminder", body="Time to stretch!"),
        at=datetime.now() + timedelta(minutes=30),
    )

    # Schedule daily
    app.notifications.schedule_daily(
        nib.Notification(title="Stand Up", body="Take a break"),
        from_time="09:00",
    )

    # Cancel by ID
    n = nib.Notification(title="Temp")
    app.notifications.push(n)
    app.notifications.cancel_notification(n.id)

    # Cancel all
    app.notifications.cancel_all_notifications()

    # Handle user actions
    def on_action(notification_id, action_id, user_text):
        print(f"User tapped {action_id} on {notification_id}")

    app.notifications.on_action(on_action)

nib.run(main)
```

!!! note "Permission"
    Notifications require user permission. Call `app.notifications.request_permission()` before pushing. On the first call, macOS shows a system dialog. Subsequent calls return the cached status.

!!! note "Critical Alerts"
    Critical alert sounds (`NotificationSoundName.DEFAULT_CRITICAL`) require a special entitlement from Apple. Without it, the sound falls back to the default. Request the entitlement at [developer.apple.com](https://developer.apple.com/contact/request/notifications-critical-alerts-entitlement/).
