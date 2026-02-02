"""Notification class for the Nib notification system.

This module provides the main Notification class used to create and configure
macOS notifications.
"""

import uuid
from dataclasses import dataclass, field
from typing import List, Optional

from .types import NotificationAction, NotificationSound


@dataclass
class Notification:
    """A macOS notification.

    Represents a notification that can be pushed immediately or scheduled
    for future delivery. Supports rich features like custom sounds, action
    buttons, and text input.

    Attributes:
        title: The main title of the notification (required).
        body: The body text of the notification.
        subtitle: A secondary line of text below the title.
        sound: Sound configuration for the notification.
        actions: List of action buttons to display.
        id: Unique identifier for this notification (auto-generated if not provided).

    Example:
        Simple notification::

            notification = Notification(
                title="Download Complete",
                body="Your file has been saved"
            )
            app.notifications.push(notification)

        Notification with sound::

            notification = Notification(
                title="New Message",
                body="You have a new message from John",
                sound=NotificationSound(name=NotificationSoundName.DEFAULT)
            )

        Notification with actions::

            notification = Notification(
                title="New Message",
                body="John: Hey, are you there?",
                actions=[
                    NotificationAction(
                        id="reply",
                        title="Reply",
                        text_input=TextInputNotificationAction(
                            button_title="Send",
                            placeholder="Type reply..."
                        )
                    ),
                    NotificationAction(
                        id="mark_read",
                        title="Mark as Read"
                    )
                ]
            )

        Scheduled notification::

            from datetime import datetime, timedelta

            notification = Notification(
                title="Reminder",
                body="Time to take a break!"
            )
            app.notifications.schedule(
                notification,
                at=datetime.now() + timedelta(hours=1)
            )
    """

    title: str
    body: str = ""
    subtitle: str = ""
    sound: Optional[NotificationSound] = None
    actions: List[NotificationAction] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # trigger configuration set by manager scheduling methods
    _trigger: Optional[dict] = field(default=None, repr=False)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization.

        Returns:
            Dictionary representation suitable for sending to Swift runtime.
        """
        result = {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "subtitle": self.subtitle,
        }

        if self.sound is not None:
            result["sound"] = self.sound.to_dict()

        if self.actions:
            result["actions"] = [action.to_dict() for action in self.actions]

        return result

    @classmethod
    def from_dict(cls, data: dict) -> "Notification":
        """Create a Notification from a dictionary.

        Used when receiving notification data from Swift runtime.

        Args:
            data: Dictionary containing notification data.

        Returns:
            A Notification instance.
        """
        from .types import (
            CustomNotificationSoundName,
            NotificationActionOption,
            NotificationSoundName,
            TextInputNotificationAction,
        )

        # Parse sound
        sound = None
        if "sound" in data and data["sound"]:
            sound_data = data["sound"]
            if sound_data.get("custom"):
                sound_name = CustomNotificationSoundName(sound_data["name"])
            else:
                sound_name = NotificationSoundName(sound_data["name"])
            sound = NotificationSound(
                name=sound_name,
                volume=sound_data.get("volume", 1.0),
            )

        # Parse actions
        actions = []
        for action_data in data.get("actions", []):
            text_input = None
            if "textInput" in action_data:
                ti_data = action_data["textInput"]
                text_input = TextInputNotificationAction(
                    button_title=ti_data.get("buttonTitle", "Send"),
                    placeholder=ti_data.get("placeholder", "Type message..."),
                )

            actions.append(
                NotificationAction(
                    id=action_data["id"],
                    title=action_data["title"],
                    options=[
                        NotificationActionOption(opt)
                        for opt in action_data.get("options", [])
                    ],
                    text_input=text_input,
                )
            )

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            title=data["title"],
            body=data.get("body", ""),
            subtitle=data.get("subtitle", ""),
            sound=sound,
            actions=actions,
        )
