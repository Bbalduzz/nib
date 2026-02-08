# Notifications

Nib provides full access to macOS system notifications, including instant push, scheduled delivery, custom sounds, action buttons, and text input.

---

## Quick Notification

The simplest way to send a notification is `app.notify()`:

```python
import nib

def main(app: nib.App):
    app.title = "Notify"
    app.icon = nib.SFSymbol("bell")
    app.width = 200
    app.height = 100

    app.build(
        nib.Button("Send Notification", action=lambda: app.notify("Hello!", "World"))
    )

nib.run(main)
```

### app.notify() parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | `str` | required | Main notification title |
| `body` | `str` | `None` | Body text |
| `subtitle` | `str` | `None` | Secondary line below the title |
| `sound` | `bool` | `True` | Play the default notification sound |
| `identifier` | `str` | `None` | Unique ID (for updating or canceling) |

```python
app.notify(
    "Download Complete",
    body="report.pdf has been saved to Downloads",
    subtitle="File Manager",
    sound=True,
)
```

---

## Requesting Permission

macOS requires user permission before delivering notifications. Request it early:

```python
def on_permission(granted):
    if granted:
        print("Notifications enabled")
    else:
        print("Notifications denied")

app.notifications.request_permission(callback=on_permission)
```

!!! note
    The first call shows the system permission dialog. Subsequent calls return the cached result. If the user denied permission, they must re-enable it in System Settings.

---

## Notification Objects

For full control, create `Notification` objects and push them through the notification manager:

```python
from nib import Notification

notification = Notification(
    title="New Message",
    body="You have a new message from Alice",
    subtitle="Messages",
)

app.notifications.push(notification)
```

### Custom sounds

Use `NotificationSound` to configure the notification sound:

```python
from nib import Notification, NotificationSound, NotificationSoundName

# Default sound
notification = Notification(
    title="Alert",
    body="Something happened",
    sound=NotificationSound(name=NotificationSoundName.DEFAULT),
)

# Built-in macOS sound by name
notification = Notification(
    title="Alert",
    body="Something happened",
    sound=NotificationSound(name=NotificationSoundName.custom("Glass")),
)

# Other built-in sounds: "Frog", "Ping", "Pop", "Purr", "Sosumi", "Tink"
```

---

## Scheduling Notifications

### Schedule at a specific time

```python
from datetime import datetime, timedelta
from nib import Notification

reminder = Notification(
    title="Break Time",
    body="You have been working for 2 hours. Take a break!",
)

# Schedule for 1 hour from now
notification_id = app.notifications.schedule(
    reminder,
    at=datetime.now() + timedelta(hours=1),
)
```

### Schedule daily recurring

```python
from nib import Notification

daily_reminder = Notification(
    title="Daily Standup",
    body="Time for the morning standup meeting",
)

# Every day at 9:00 AM
app.notifications.schedule_daily(
    daily_reminder,
    from_time="09:00",
)

# Multiple times per day between 8 AM and 6 PM
app.notifications.schedule_daily(
    daily_reminder,
    from_time="08:00",
    to_time="18:00",
    count=3,
)

# Daily for one week
from datetime import date, timedelta

app.notifications.schedule_daily(
    daily_reminder,
    from_time="09:00",
    from_date=date.today(),
    to_date=date.today() + timedelta(days=7),
)
```

### Reschedule

Cancel and reschedule an existing notification:

```python
app.notifications.reschedule(
    reminder,
    at=datetime.now() + timedelta(hours=2),
)
```

---

## Notification Actions

Actions appear as buttons on the notification. Users can tap them to trigger callbacks without opening the app.

```python
from nib import Notification, NotificationAction, TextInputNotificationAction

notification = Notification(
    title="New Message",
    body="Alice: Hey, are you free for lunch?",
    actions=[
        NotificationAction(
            id="reply",
            title="Reply",
            text_input=TextInputNotificationAction(
                button_title="Send",
                placeholder="Type your reply...",
            ),
        ),
        NotificationAction(
            id="mark_read",
            title="Mark as Read",
        ),
    ],
)

app.notifications.push(notification)
```

### Handling action callbacks

Register a handler to receive action events:

```python
def handle_action(notification_id, action_id, user_text):
    if action_id == "reply" and user_text:
        print(f"User replied: {user_text}")
    elif action_id == "mark_read":
        print("Marked as read")

unsubscribe = app.notifications.on_action(handle_action)

# Later, to stop receiving callbacks:
# unsubscribe()
```

The callback receives three arguments:

| Argument | Type | Description |
|----------|------|-------------|
| `notification_id` | `str` | ID of the notification that was acted on |
| `action_id` | `str` | ID of the action button that was tapped |
| `user_text` | `str` or `None` | Text entered if the action has `text_input` |

### Action options

```python
from nib import NotificationAction, NotificationActionOption

NotificationAction(
    id="delete",
    title="Delete",
    options=[
        NotificationActionOption.DESTRUCTIVE,            # Red button
        NotificationActionOption.AUTHENTICATION_REQUIRED, # Requires unlock
    ],
)

NotificationAction(
    id="open",
    title="Open App",
    options=[NotificationActionOption.FOREGROUND],  # Brings app to front
)
```

---

## Canceling Notifications

```python
# Cancel a specific notification by ID
app.notifications.cancel_notification(notification_id)

# Cancel all scheduled and delivered notifications
app.notifications.cancel_all_notifications()
```

---

## Querying Notifications

Retrieve notifications that are currently scheduled or displayed in Notification Center:

```python
# Get all scheduled (pending) notifications
def on_scheduled(notifications):
    for n in notifications:
        print(f"Scheduled: {n.title} (id: {n.id})")

app.notifications.get_all_scheduled_notifications(on_scheduled)

# Get all delivered (visible in Notification Center) notifications
def on_delivered(notifications):
    print(f"{len(notifications)} notifications showing")

app.notifications.get_all_delivered_notifications(on_delivered)

# Get a specific notification by ID
app.notifications.get_scheduled_notification(
    "some-id",
    callback=lambda n: print(f"Found: {n.title}") if n else print("Not found"),
)
```

---

## Full Example

A complete notification demo app:

```python
import nib
from datetime import datetime, timedelta
from nib import Notification, NotificationAction, NotificationSound, NotificationSoundName, TextInputNotificationAction

def main(app: nib.App):
    app.title = "Notifications"
    app.icon = nib.SFSymbol("bell.badge")
    app.width = 300
    app.height = 350

    # Request permission on startup
    app.notifications.request_permission()

    # Handle action callbacks
    response_label = nib.Text("No response yet",
                               foreground_color=nib.Color.SECONDARY,
                               font=nib.Font.CAPTION)

    def on_action(notif_id, action_id, user_text):
        if action_id == "reply" and user_text:
            response_label.content = f"Reply: {user_text}"
        elif action_id == "dismiss":
            response_label.content = "Dismissed"

    app.notifications.on_action(on_action)

    def send_simple():
        app.notify("Hello!", body="This is a simple notification.")

    def send_with_actions():
        notification = Notification(
            title="Message from Alice",
            body="Want to grab coffee?",
            sound=NotificationSound(name=NotificationSoundName.custom("Glass")),
            actions=[
                NotificationAction(
                    id="reply",
                    title="Reply",
                    text_input=TextInputNotificationAction(
                        button_title="Send",
                        placeholder="Type reply...",
                    ),
                ),
                NotificationAction(id="dismiss", title="Dismiss"),
            ],
        )
        app.notifications.push(notification)

    def schedule_reminder():
        reminder = Notification(
            title="Reminder",
            body="This was scheduled 10 seconds ago.",
        )
        app.notifications.schedule(reminder, at=datetime.now() + timedelta(seconds=10))
        response_label.content = "Reminder scheduled in 10s"

    def cancel_all():
        app.notifications.cancel_all_notifications()
        response_label.content = "All notifications canceled"

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Notification Demo", font=nib.Font.HEADLINE),
                nib.Divider(),
                nib.Button("Simple Notification", action=send_simple),
                nib.Button("With Actions", action=send_with_actions),
                nib.Button("Schedule (10s)", action=schedule_reminder),
                nib.Button("Cancel All", action=cancel_all),
                nib.Divider(),
                nib.Text("Last response:", font=nib.Font.CAPTION),
                response_label,
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```
