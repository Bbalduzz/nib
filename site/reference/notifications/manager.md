# NotificationManager

The `NotificationManager` handles all notification operations: pushing, scheduling, querying, canceling, and responding to user actions. Access it via `app.notifications`.

```python
app.notifications.push(nib.Notification(title="Hello", body="World"))
```

## Methods

### Permission

#### `request_permission(callback)`

Request notification permission from the user. On the first call, macOS shows a system permission dialog. Subsequent calls return the cached status.

```python
app.notifications.request_permission(callback: Callable[[bool], None] | None = None) -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `callback` | `Callable[[bool], None] \| None` | `None` | Optional function called with `True` if permission was granted, `False` otherwise |

### Push

#### `push(notification)`

Push a notification for immediate delivery.

```python
app.notifications.push(notification: Notification) -> str
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `notification` | `Notification` | The notification to deliver immediately |

Returns the notification ID.

### Schedule

#### `schedule(notification, at)`

Schedule a notification for delivery at a specific date and time. If the target time is in the past, the notification is pushed immediately.

```python
app.notifications.schedule(notification: Notification, at: datetime) -> str
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `notification` | `Notification` | The notification to schedule |
| `at` | `datetime` | The date and time when the notification should be delivered |

Returns the notification ID.

#### `reschedule(notification, at)`

Cancel an existing notification and schedule it for a new time.

```python
app.notifications.reschedule(notification: Notification, at: datetime) -> str
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `notification` | `Notification` | The notification to reschedule (must have the same `id` as the original) |
| `at` | `datetime` | The new delivery time |

Returns the notification ID.

#### `schedule_daily(notification, from_time, to_time, count, from_date, to_date, interval)`

Schedule a notification that recurs daily. Supports time windows, multiple notifications per day, and date ranges.

```python
app.notifications.schedule_daily(
    notification: Notification,
    from_time: str,
    to_time: str | None = None,
    count: int = 1,
    from_date: date | None = None,
    to_date: date | None = None,
    interval: timedelta | None = None,
) -> str
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `notification` | `Notification` | -- | The notification to schedule |
| `from_time` | `str` | -- | Start time in `"HH:MM"` format (e.g., `"08:00"`) |
| `to_time` | `str \| None` | `None` | Optional end time in `"HH:MM"` format |
| `count` | `int` | `1` | Number of notifications per day |
| `from_date` | `date \| None` | `None` | Optional start date for the schedule |
| `to_date` | `date \| None` | `None` | Optional end date for the schedule |
| `interval` | `timedelta \| None` | `None` | Optional interval between notifications |

Returns the notification ID.

### Cancel

#### `cancel_notification(id)`

Cancel a specific notification by its ID. Works for both scheduled (pending) and delivered notifications.

```python
app.notifications.cancel_notification(id: str) -> None
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | `str` | The notification ID to cancel |

#### `cancel_all_notifications()`

Cancel all scheduled notifications and remove all delivered notifications from Notification Center.

```python
app.notifications.cancel_all_notifications() -> None
```

### Query

#### `get_all_scheduled_notifications(callback)`

Get all pending (scheduled but not yet delivered) notifications.

```python
app.notifications.get_all_scheduled_notifications(
    callback: Callable[[list[Notification]], None]
) -> None
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `callback` | `Callable[[list[Notification]], None]` | Function called with the list of scheduled notifications |

#### `get_all_delivered_notifications(callback)`

Get all delivered notifications still visible in Notification Center.

```python
app.notifications.get_all_delivered_notifications(
    callback: Callable[[list[Notification]], None]
) -> None
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `callback` | `Callable[[list[Notification]], None]` | Function called with the list of delivered notifications |

#### `get_scheduled_notification(id, callback)`

Get a specific scheduled notification by ID.

```python
app.notifications.get_scheduled_notification(
    id: str,
    callback: Callable[[Notification | None], None]
) -> None
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | `str` | The notification ID to look up |
| `callback` | `Callable[[Notification \| None], None]` | Function called with the notification, or `None` if not found |

#### `get_delivered_notification(id, callback)`

Get a specific delivered notification by ID.

```python
app.notifications.get_delivered_notification(
    id: str,
    callback: Callable[[Notification | None], None]
) -> None
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | `str` | The notification ID to look up |
| `callback` | `Callable[[Notification \| None], None]` | Function called with the notification, or `None` if not found |

### Action Handling

#### `on_action(callback)`

Register a handler for notification action callbacks. Called when the user interacts with a notification (taps an action button, types a reply, or clicks the notification itself).

```python
app.notifications.on_action(
    callback: Callable[[str, str, str | None], None]
) -> Callable[[], None]
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `callback` | `Callable[[str, str, str \| None], None]` | Function called with `(notification_id, action_id, user_text)`. `user_text` is the text entered if the action has a `text_input` field, otherwise `None` |

Returns an unsubscribe function. Call it to stop receiving callbacks.

**Built-in action IDs:**

| Action ID | When |
|-----------|------|
| `"default"` | User clicked the notification body |
| `"dismiss"` | User dismissed the notification |
| Custom ID | User tapped a custom action button |

---

## Examples

### Push and schedule notifications

```python
import nib
from datetime import datetime, timedelta

def main(app: nib.App):
    app.title = "Reminders"
    app.icon = nib.SFSymbol("bell.fill")
    app.width = 320
    app.height = 200

    status = nib.Text("Ready", foreground_color=nib.Color.SECONDARY)

    # Request permission on startup
    app.notifications.request_permission(
        callback=lambda granted: setattr(status, "content",
            "Permission granted" if granted else "Permission denied")
    )

    def push_now():
        app.notifications.push(
            nib.Notification(title="Instant", body="Delivered right now!")
        )
        status.content = "Notification pushed"

    def schedule_later():
        n = nib.Notification(title="Reminder", body="Time to take a break!")
        app.notifications.schedule(n, at=datetime.now() + timedelta(seconds=30))
        status.content = f"Scheduled for 30s (ID: {n.id[:8]}...)"

    def cancel_all():
        app.notifications.cancel_all_notifications()
        status.content = "All notifications cancelled"

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Reminders", font=nib.Font.HEADLINE),
                nib.HStack(
                    controls=[
                        nib.Button("Push Now", action=push_now),
                        nib.Button("In 30s", action=schedule_later),
                    ],
                    spacing=8,
                ),
                nib.Button("Cancel All", action=cancel_all, role=nib.ButtonRole.DESTRUCTIVE),
                status,
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

### Handle action callbacks

```python
import nib

def main(app: nib.App):
    app.title = "Chat"
    app.icon = nib.SFSymbol("message.fill")
    app.width = 320
    app.height = 180

    last_reply = nib.Text("No replies yet", foreground_color=nib.Color.SECONDARY)

    def on_action(notification_id, action_id, user_text):
        if action_id == "reply" and user_text:
            last_reply.content = f"You replied: {user_text}"
        elif action_id == "mark_read":
            last_reply.content = "Marked as read"
        elif action_id == "default":
            last_reply.content = "Notification clicked"

    app.notifications.on_action(on_action)
    app.notifications.request_permission()

    def send_message():
        app.notifications.push(
            nib.Notification(
                title="New Message",
                body="Alice: Want to grab lunch?",
                sound=nib.NotificationSound(),
                actions=[
                    nib.NotificationAction(
                        id="reply",
                        title="Reply",
                        text_input=nib.TextInputNotificationAction(
                            button_title="Send",
                            placeholder="Type reply...",
                        ),
                    ),
                    nib.NotificationAction(id="mark_read", title="Mark as Read"),
                ],
            )
        )

    app.build(
        nib.VStack(
            controls=[
                nib.Button("Simulate Message", action=send_message,
                           style=nib.ButtonStyle.BORDERED_PROMINENT),
                last_reply,
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

### Daily recurring notification

```python
import nib
from datetime import date, timedelta

def main(app: nib.App):
    app.notifications.request_permission()

    # Daily reminder at 9 AM
    app.notifications.schedule_daily(
        nib.Notification(
            title="Good Morning",
            body="Time to start your day!",
            sound=nib.NotificationSound(),
        ),
        from_time="09:00",
    )

    # Three reminders between 8 AM and 6 PM for one week
    app.notifications.schedule_daily(
        nib.Notification(title="Hydration", body="Drink some water!"),
        from_time="08:00",
        to_time="18:00",
        count=3,
        from_date=date.today(),
        to_date=date.today() + timedelta(days=7),
    )

nib.run(main)
```

### Query scheduled notifications

```python
import nib

def main(app: nib.App):
    app.title = "Scheduled"
    app.icon = nib.SFSymbol("clock")
    app.width = 320
    app.height = 200

    count_text = nib.Text("--", font=nib.Font.TITLE)
    list_text = nib.Text("", foreground_color=nib.Color.SECONDARY)

    def check():
        def on_result(notifications):
            count_text.content = f"{len(notifications)} scheduled"
            titles = [n.title for n in notifications[:5]]
            list_text.content = "\n".join(titles) if titles else "None"

        app.notifications.get_all_scheduled_notifications(on_result)

    app.on_appear = check

    app.build(
        nib.VStack(
            controls=[count_text, list_text,
                nib.Button("Refresh", action=check)],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

## Related

- [Notification](notification.md) -- Notification dataclass
- [Sound & Actions](types.md) -- Sound and action button types
