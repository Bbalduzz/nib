# Sound & Actions

Supporting types for configuring notification sounds and interactive action buttons.

## NotificationSound

Configuration for the sound played when a notification is delivered.

### Constructor

```python
nib.NotificationSound(
    name: NotificationSoundName | CustomNotificationSoundName = NotificationSoundName.DEFAULT,
    volume: float = 1.0,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `NotificationSoundName \| CustomNotificationSoundName` | `NotificationSoundName.DEFAULT` | The sound to play |
| `volume` | `float` | `1.0` | Volume level from `0.0` to `1.0`. Only applies to critical alerts |

### Examples

```python
# Default notification sound
sound = nib.NotificationSound()

# Explicit default
sound = nib.NotificationSound(name=nib.NotificationSoundName.DEFAULT)

# Custom macOS system sound
sound = nib.NotificationSound(name=nib.NotificationSoundName.custom("Glass"))

# Custom sound file (must be .aiff, .wav, .caff, or .mp3, under 30 seconds)
sound = nib.NotificationSound(name=nib.NotificationSoundName.custom("alert.aiff"))

# Critical alert (requires Apple entitlement)
sound = nib.NotificationSound(
    name=nib.NotificationSoundName.DEFAULT_CRITICAL,
    volume=1.0,
)
```

---

## NotificationSoundName

Enum of built-in notification sound names.

```python
import nib
# or: from nib.notifications.types import NotificationSoundName
```

| Value | Description |
|-------|-------------|
| `NotificationSoundName.DEFAULT` | The default notification sound |
| `NotificationSoundName.DEFAULT_CRITICAL` | Critical alert sound (requires Apple entitlement) |

### `NotificationSoundName.custom(name)`

Create a custom sound name from a file name or built-in macOS sound name.

```python
NotificationSoundName.custom(name: str) -> CustomNotificationSoundName
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Sound file name (`.aiff`, `.wav`, `.caff`, `.mp3`) or a built-in macOS sound name |

Custom sound files must be:

- Less than 30 seconds in duration
- Placed in the app bundle's sound resources, or in `~/Library/Sounds`

**Built-in macOS sound names** that can be used directly:

`Basso`, `Blow`, `Bottle`, `Frog`, `Funk`, `Glass`, `Hero`, `Morse`, `Ping`, `Pop`, `Purr`, `Sosumi`, `Submarine`, `Tink`

```python
# Using a built-in macOS sound
sound = nib.NotificationSound(name=nib.NotificationSoundName.custom("Frog"))

# Using a custom sound file in the app bundle
sound = nib.NotificationSound(name=nib.NotificationSoundName.custom("mysound.aiff"))
```

---

## CustomNotificationSoundName

Wrapper for custom sound names. Created via `NotificationSoundName.custom()`, not instantiated directly.

| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | The sound file name or built-in sound name |
| `value` | `str` | Same as `name`, used for serialization |

---

## NotificationAction

An action button displayed on a notification. Actions allow users to respond to notifications without opening the app.

### Constructor

```python
nib.NotificationAction(
    id: str,
    title: str,
    options: list[NotificationActionOption] = [],
    text_input: TextInputNotificationAction | None = None,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | `str` | -- | Unique identifier for this action, received in the `on_action` callback |
| `title` | `str` | -- | Display title for the action button |
| `options` | `list[NotificationActionOption]` | `[]` | Behavioral flags for the action. Empty list means the action runs in the background |
| `text_input` | `TextInputNotificationAction \| None` | `None` | Optional text input configuration for reply-style actions |

### Examples

```python
# Simple action button
action = nib.NotificationAction(
    id="mark_read",
    title="Mark as Read",
)

# Reply action with text input
action = nib.NotificationAction(
    id="reply",
    title="Reply",
    options=[nib.NotificationActionOption.FOREGROUND],
    text_input=nib.TextInputNotificationAction(
        button_title="Send",
        placeholder="Type your reply...",
    ),
)

# Destructive action requiring authentication
action = nib.NotificationAction(
    id="delete",
    title="Delete",
    options=[
        nib.NotificationActionOption.DESTRUCTIVE,
        nib.NotificationActionOption.AUTHENTICATION_REQUIRED,
    ],
)
```

---

## NotificationActionOption

Enum of behavioral flags for notification action buttons.

```python
import nib
# or: from nib.notifications.types import NotificationActionOption
```

| Value | Description |
|-------|-------------|
| `NotificationActionOption.FOREGROUND` | Brings the app to the foreground when the action is triggered |
| `NotificationActionOption.DESTRUCTIVE` | Displays the action button in red, indicating a destructive operation |
| `NotificationActionOption.AUTHENTICATION_REQUIRED` | Requires the device to be unlocked before executing the action |

---

## TextInputNotificationAction

Configuration for adding a text input field to a notification action. When attached to a `NotificationAction`, users can type a response directly in the notification banner.

### Constructor

```python
nib.TextInputNotificationAction(
    button_title: str = "Send",
    placeholder: str = "Type message...",
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `button_title` | `str` | `"Send"` | Title of the send/submit button |
| `placeholder` | `str` | `"Type message..."` | Placeholder text in the input field |

### Example

```python
text_input = nib.TextInputNotificationAction(
    button_title="Reply",
    placeholder="Type your reply...",
)

action = nib.NotificationAction(
    id="reply",
    title="Reply",
    text_input=text_input,
)
```

---

## Complete Example

A full notification with sound, multiple actions, and text input:

```python
import nib

def main(app: nib.App):
    app.title = "Chat"
    app.icon = nib.SFSymbol("message")
    app.width = 300
    app.height = 150

    app.notifications.request_permission()

    def on_action(notification_id, action_id, user_text):
        if action_id == "reply" and user_text:
            print(f"Reply: {user_text}")
        elif action_id == "like":
            print("Liked the message")
        elif action_id == "delete":
            print("Message deleted")

    app.notifications.on_action(on_action)

    def send():
        notification = nib.Notification(
            title="Alice",
            subtitle="iMessage",
            body="Hey, want to grab coffee tomorrow?",
            sound=nib.NotificationSound(
                name=nib.NotificationSoundName.custom("Glass"),
            ),
            actions=[
                nib.NotificationAction(
                    id="reply",
                    title="Reply",
                    options=[nib.NotificationActionOption.FOREGROUND],
                    text_input=nib.TextInputNotificationAction(
                        button_title="Send",
                        placeholder="iMessage",
                    ),
                ),
                nib.NotificationAction(
                    id="like",
                    title="Thumbs Up",
                ),
                nib.NotificationAction(
                    id="delete",
                    title="Delete",
                    options=[
                        nib.NotificationActionOption.DESTRUCTIVE,
                        nib.NotificationActionOption.AUTHENTICATION_REQUIRED,
                    ],
                ),
            ],
        )
        app.notifications.push(notification)

    app.build(
        nib.VStack(
            controls=[nib.Button("Send Message", action=send)],
            padding=20,
        )
    )

nib.run(main)
```

## Related

- [Notification](notification.md) -- The notification dataclass
- [NotificationManager](manager.md) -- Push, schedule, and manage notifications
