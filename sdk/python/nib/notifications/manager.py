"""Notification manager for the Nib notification system.

This module provides the NotificationManager class that handles all
notification operations including pushing, scheduling, querying, and canceling.
"""

import uuid
from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING, Callable, Dict, List, Optional

from .notification import Notification

if TYPE_CHECKING:
    from ..core.connection import Connection


class NotificationManager:
    """Manager for macOS notifications.

    Provides methods for pushing, scheduling, querying, and canceling
    notifications. Access via `app.notifications`.

    Example:
        Request permission::

            app.notifications.request_permission(
                callback=lambda granted: print(f"Permission: {granted}")
            )

        Push notification::

            notification = Notification(
                title="Hello",
                body="World"
            )
            app.notifications.push(notification)

        Schedule notification::

            from datetime import datetime, timedelta

            notification = Notification(title="Reminder", body="Time!")
            app.notifications.schedule(
                notification,
                at=datetime.now() + timedelta(hours=1)
            )

        Handle action callbacks::

            def on_notification_action(notification_id, action_id, user_text):
                print(f"Action {action_id} on {notification_id}")
                if user_text:
                    print(f"User typed: {user_text}")

            app.notifications.on_action(on_notification_action)
    """

    def __init__(self):
        self._connection: Optional["Connection"] = None
        self._action_handlers: List[Callable[[str, str, Optional[str]], None]] = []
        self._pending_callbacks: Dict[str, Callable] = {}

    def _set_connection(self, connection: "Connection") -> None:
        """Set the connection (called internally by App)."""
        self._connection = connection

    # MARK: - Permission

    def request_permission(
        self, callback: Optional[Callable[[bool], None]] = None
    ) -> None:
        """Request notification permission from the user.

        On first call, the system will show a permission dialog. Subsequent
        calls return the cached permission status.

        Args:
            callback: Optional callback receiving True if granted, False otherwise.

        Example:
            def on_permission(granted):
                if granted:
                    print("Notifications enabled!")
                else:
                    print("Notifications denied")

            app.notifications.request_permission(on_permission)
        """
        if not self._connection:
            if callback:
                callback(False)
            return

        request_id = str(uuid.uuid4())
        if callback:
            self._pending_callbacks[request_id] = callback

        self._connection.send_notification_action(
            action="requestPermission",
            request_id=request_id,
        )

    # MARK: - Query

    def get_all_scheduled_notifications(
        self, callback: Callable[[List[Notification]], None]
    ) -> None:
        """Get all scheduled (pending) notifications.

        Args:
            callback: Callback receiving list of scheduled notifications.

        Example:
            def on_scheduled(notifications):
                for n in notifications:
                    print(f"Scheduled: {n.title}")

            app.notifications.get_all_scheduled_notifications(on_scheduled)
        """
        if not self._connection:
            callback([])
            return

        request_id = str(uuid.uuid4())
        self._pending_callbacks[request_id] = lambda data: callback(
            [Notification.from_dict(n) for n in data.get("notifications", [])]
        )

        self._connection.send_notification_action(
            action="getScheduled",
            request_id=request_id,
        )

    def get_all_delivered_notifications(
        self, callback: Callable[[List[Notification]], None]
    ) -> None:
        """Get all delivered notifications still visible in Notification Center.

        Args:
            callback: Callback receiving list of delivered notifications.

        Example:
            def on_delivered(notifications):
                print(f"Currently showing {len(notifications)} notifications")

            app.notifications.get_all_delivered_notifications(on_delivered)
        """
        if not self._connection:
            callback([])
            return

        request_id = str(uuid.uuid4())
        self._pending_callbacks[request_id] = lambda data: callback(
            [Notification.from_dict(n) for n in data.get("notifications", [])]
        )

        self._connection.send_notification_action(
            action="getDelivered",
            request_id=request_id,
        )

    def get_scheduled_notification(
        self, id: str, callback: Callable[[Optional[Notification]], None]
    ) -> None:
        """Get a specific scheduled notification by ID.

        Args:
            id: The notification ID.
            callback: Callback receiving the notification or None if not found.
        """
        if not self._connection:
            callback(None)
            return

        request_id = str(uuid.uuid4())
        self._pending_callbacks[request_id] = lambda data: callback(
            Notification.from_dict(data["notification"])
            if data.get("notification")
            else None
        )

        self._connection.send_notification_action(
            action="getScheduledById",
            request_id=request_id,
            notification_id=id,
        )

    def get_delivered_notification(
        self, id: str, callback: Callable[[Optional[Notification]], None]
    ) -> None:
        """Get a specific delivered notification by ID.

        Args:
            id: The notification ID.
            callback: Callback receiving the notification or None if not found.
        """
        if not self._connection:
            callback(None)
            return

        request_id = str(uuid.uuid4())
        self._pending_callbacks[request_id] = lambda data: callback(
            Notification.from_dict(data["notification"])
            if data.get("notification")
            else None
        )

        self._connection.send_notification_action(
            action="getDeliveredById",
            request_id=request_id,
            notification_id=id,
        )

    # MARK: - Cancel

    def cancel_all_notifications(self) -> None:
        """Cancel all scheduled and remove all delivered notifications.

        Example:
            app.notifications.cancel_all_notifications()
        """
        if not self._connection:
            return

        self._connection.send_notification_action(action="cancelAll")

    def cancel_notification(self, id: str) -> None:
        """Cancel a specific notification by ID.

        Works for both scheduled and delivered notifications.

        Args:
            id: The notification ID to cancel.

        Example:
            app.notifications.cancel_notification(notification.id)
        """
        if not self._connection:
            return

        self._connection.send_notification_action(
            action="cancel",
            notification_id=id,
        )

    # MARK: - Schedule

    def schedule(self, notification: Notification, at: datetime) -> str:
        """Schedule a notification for a specific date/time.

        Args:
            notification: The notification to schedule.
            at: The datetime when the notification should be delivered.

        Returns:
            The notification ID.

        Example:
            from datetime import datetime, timedelta

            notification = Notification(
                title="Reminder",
                body="Time to take a break!"
            )
            id = app.notifications.schedule(
                notification,
                at=datetime.now() + timedelta(hours=1)
            )
        """
        if not self._connection:
            return notification.id

        interval = (at - datetime.now()).total_seconds()
        if interval <= 0:
            return self.push(notification)

        self._connection.send_notification_action(
            action="schedule",
            notification=notification.to_dict(),
            trigger={
                "type": "interval",
                "interval": interval,
            },
        )

        return notification.id

    def reschedule(self, notification: Notification, at: datetime) -> str:
        """Reschedule an existing notification.

        Cancels the existing notification and schedules it for a new time.

        Args:
            notification: The notification to reschedule.
            at: The new datetime for delivery.

        Returns:
            The notification ID.
        """
        self.cancel_notification(notification.id)
        return self.schedule(notification, at)

    def schedule_daily(
        self,
        notification: Notification,
        from_time: str,
        to_time: Optional[str] = None,
        count: int = 1,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        interval: Optional[timedelta] = None,
    ) -> str:
        """Schedule a daily recurring notification.

        Args:
            notification: The notification to schedule.
            from_time: Start time in "HH:MM" format (e.g., "08:00").
            to_time: Optional end time in "HH:MM" format.
            count: Number of notifications per day (default: 1).
            from_date: Optional start date for the schedule.
            to_date: Optional end date for the schedule.
            interval: Optional interval between notifications.

        Returns:
            The notification ID.

        Example:
            # Daily reminder at 8 AM
            app.notifications.schedule_daily(
                notification,
                from_time="08:00"
            )

            # Multiple reminders between 8 AM and 6 PM
            app.notifications.schedule_daily(
                notification,
                from_time="08:00",
                to_time="18:00",
                count=3
            )

            # Daily for one week
            from datetime import date, timedelta

            app.notifications.schedule_daily(
                notification,
                from_time="09:00",
                from_date=date.today(),
                to_date=date.today() + timedelta(days=7)
            )
        """
        if not self._connection:
            return notification.id

        trigger = {
            "type": "calendar",
            "fromTime": from_time,
            "repeats": True,
        }

        if to_time:
            trigger["toTime"] = to_time
        if count > 1:
            trigger["count"] = count
        if from_date:
            trigger["fromDate"] = from_date.isoformat()
        if to_date:
            trigger["toDate"] = to_date.isoformat()
        if interval:
            trigger["interval"] = interval.total_seconds()

        self._connection.send_notification_action(
            action="schedule",
            notification=notification.to_dict(),
            trigger=trigger,
        )

        return notification.id

    def push(self, notification: Notification) -> str:
        """Push a notification immediately.

        Args:
            notification: The notification to push.

        Returns:
            The notification ID.

        Example:
            notification = Notification(
                title="Download Complete",
                body="Your file has been saved"
            )
            app.notifications.push(notification)
        """
        if not self._connection:
            return notification.id

        self._connection.send_notification_action(
            action="push",
            notification=notification.to_dict(),
        )

        return notification.id

    def on_action(
        self, callback: Callable[[str, str, Optional[str]], None]
    ) -> Callable[[], None]:
        """Register a handler for notification action callbacks.

        Args:
            callback: Function called when user interacts with a notification.
                     Receives (notification_id, action_id, user_text).
                     user_text is the text entered if action has text_input.

        Returns:
            A function to unregister the handler.

        Example:
            def handle_action(notification_id, action_id, user_text):
                if action_id == "reply" and user_text:
                    print(f"User replied: {user_text}")
                elif action_id == "mark_read":
                    print("Marked as read")

            unsubscribe = app.notifications.on_action(handle_action)

            # Later, to stop receiving callbacks:
            unsubscribe()
        """
        self._action_handlers.append(callback)

        def unsubscribe():
            if callback in self._action_handlers:
                self._action_handlers.remove(callback)

        return unsubscribe

    def _handle_action_event(
        self, notification_id: str, action_id: str, user_text: Optional[str]
    ) -> None:
        """Handle an action event from Swift (called internally)."""
        for handler in self._action_handlers:
            try:
                handler(notification_id, action_id, user_text)
            except Exception:
                pass  # Don't let one handler break others

    def _handle_response(self, request_id: str, data: dict) -> None:
        """Handle a response from Swift (called internally)."""
        callback = self._pending_callbacks.pop(request_id, None)
        if callback:
            # Check if it's a permission response
            if "granted" in data:
                callback(data["granted"])
            else:
                callback(data)
