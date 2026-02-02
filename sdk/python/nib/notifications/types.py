"""Notification types for the Nib notification system.

This module provides types for configuring macOS notifications including
sounds, actions, and text input capabilities.

Note:
    Critical alerts require a special entitlement from Apple. Request at:
    https://developer.apple.com/contact/request/notifications-critical-alerts-entitlement/
    Without the entitlement, critical sounds will fall back to default.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class NotificationSoundName(Enum):
    """Sound names for notifications.

    Attributes:
        DEFAULT: The default notification sound.
        DEFAULT_CRITICAL: Critical alert sound (requires Apple entitlement).

    Example:
        Basic usage::

            sound = NotificationSound(name=NotificationSoundName.DEFAULT)

        Custom sound::

            # Must be .aiff, .wav, .caff, or .mp3
            # Must be < 30 seconds
            # Must be in app bundle or ~/Library/Sounds
            sound = NotificationSound(name=NotificationSoundName.custom("mysound.aiff"))

            # Built-in macOS sounds by name
            sound = NotificationSound(name=NotificationSoundName.custom("Frog"))
    """

    DEFAULT = "default"
    DEFAULT_CRITICAL = "defaultCritical"

    @staticmethod
    def custom(name: str) -> "CustomNotificationSoundName":
        """Create a custom sound name.

        Args:
            name: Sound file name (.aiff, .wav, .caff, .mp3) or built-in macOS sound name.
                  Custom files must be < 30 seconds and placed in:
                  - App bundle's sound resources
                  - ~/Library/Sounds folder

        Returns:
            A CustomNotificationSoundName instance.

        Example:
            # Custom sound file
            NotificationSoundName.custom("mysound.aiff")

            # Built-in macOS sound
            NotificationSoundName.custom("Frog")
            NotificationSoundName.custom("Glass")
            NotificationSoundName.custom("Ping")
        """
        return CustomNotificationSoundName(name)


class CustomNotificationSoundName:
    """Custom notification sound name wrapper.

    Created via NotificationSoundName.custom().
    """

    def __init__(self, name: str):
        self.name = name
        self.value = name

    def __repr__(self) -> str:
        return f"CustomNotificationSoundName({self.name!r})"


@dataclass
class NotificationSound:
    """Configuration for notification sound.

    Attributes:
        name: The sound to play (NotificationSoundName or CustomNotificationSoundName).
        volume: Volume level from 0.0 to 1.0. Only applies to critical alerts.

    Example:
        Default sound::

            sound = NotificationSound()

        Custom sound with volume::

            sound = NotificationSound(
                name=NotificationSoundName.custom("alert.aiff"),
                volume=0.8
            )

        Critical alert (requires entitlement)::

            sound = NotificationSound(
                name=NotificationSoundName.DEFAULT_CRITICAL,
                volume=1.0
            )
    """

    name: NotificationSoundName | CustomNotificationSoundName = NotificationSoundName.DEFAULT
    volume: float = 1.0

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        if isinstance(self.name, CustomNotificationSoundName):
            return {"name": self.name.value, "custom": True, "volume": self.volume}
        return {"name": self.name.value, "custom": False, "volume": self.volume}


class NotificationActionOption(Enum):
    """Options for notification action buttons.

    Attributes:
        FOREGROUND: Brings the app to the foreground when action is triggered.
        DESTRUCTIVE: Displays the action button in red (indicates destructive action).
        AUTHENTICATION_REQUIRED: Requires device unlock before executing action.

    Example:
        action = NotificationAction(
            id="delete",
            title="Delete",
            options=[
                NotificationActionOption.DESTRUCTIVE,
                NotificationActionOption.AUTHENTICATION_REQUIRED
            ]
        )
    """

    FOREGROUND = "foreground"
    DESTRUCTIVE = "destructive"
    AUTHENTICATION_REQUIRED = "authenticationRequired"


@dataclass
class TextInputNotificationAction:
    """Configuration for text input in notification actions.

    Allows users to type a response directly in the notification.

    Attributes:
        button_title: Title for the send button (default: "Send").
        placeholder: Placeholder text in the input field.

    Example:
        text_input = TextInputNotificationAction(
            button_title="Reply",
            placeholder="Type your reply..."
        )
    """

    button_title: str = "Send"
    placeholder: str = "Type message..."

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "buttonTitle": self.button_title,
            "placeholder": self.placeholder,
        }


@dataclass
class NotificationAction:
    """An action button for a notification.

    Actions appear as buttons on the notification that users can tap
    to perform quick actions without opening the app.

    Attributes:
        id: Unique identifier for this action (used in callbacks).
        title: Display title for the action button.
        options: List of NotificationActionOption flags. Empty list means
                 the action runs in background without bringing app forward.
        text_input: Optional text input configuration for reply-style actions.

    Example:
        Simple action::

            action = NotificationAction(
                id="mark_read",
                title="Mark as Read"
            )

        Reply action with text input::

            action = NotificationAction(
                id="reply",
                title="Reply",
                options=[NotificationActionOption.FOREGROUND],
                text_input=TextInputNotificationAction(
                    button_title="Send",
                    placeholder="Type your reply..."
                )
            )

        Destructive action::

            action = NotificationAction(
                id="delete",
                title="Delete",
                options=[
                    NotificationActionOption.DESTRUCTIVE,
                    NotificationActionOption.AUTHENTICATION_REQUIRED
                ]
            )
    """

    id: str
    title: str
    options: List[NotificationActionOption] = field(default_factory=list)
    text_input: Optional[TextInputNotificationAction] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        result = {
            "id": self.id,
            "title": self.title,
            "options": [opt.value for opt in self.options],
        }
        if self.text_input is not None:
            result["textInput"] = self.text_input.to_dict()
        return result
