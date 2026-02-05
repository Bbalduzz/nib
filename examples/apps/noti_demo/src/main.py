"""Demo of the Notification API.

Shows how to:
- Push immediate notifications
- Schedule notifications for later
- Use custom sounds
- Add action buttons with text input
- Handle action callbacks
"""

from datetime import datetime, timedelta

import nib


def main(app: nib.App):
    app.title = "Notifications"
    app.icon = nib.SFSymbol("bell.fill")
    app.width = 380
    app.height = 650
    app.menu = [nib.MenuItem("Quit", action=app.quit)]

    # Status display
    status_text = nib.Text(
        "Ready", font=nib.Font.CAPTION, foreground_color=nib.Color.SECONDARY
    )

    def update_status(msg: str):
        status_text.content = msg

    # Track notification IDs
    last_notification_id = None

    # Simple notification
    def push_simple():
        nonlocal last_notification_id
        notification = nib.Notification(
            title="Hello from Nib!",
            body="This is a simple notification.",
        )
        last_notification_id = app.notifications.push(notification)
        update_status(f"Pushed: {notification.id[:8]}...")

    # Notification with sound
    def push_with_sound():
        nonlocal last_notification_id
        notification = nib.Notification(
            title="Notification with Sound",
            body="You should hear the default sound.",
            sound=nib.NotificationSound(name=nib.NotificationSoundName.DEFAULT),
        )
        last_notification_id = app.notifications.push(notification)
        update_status(f"Pushed with sound: {notification.id[:8]}...")

    # Notification with custom sound
    def push_custom_sound():
        nonlocal last_notification_id
        notification = nib.Notification(
            title="Custom Sound",
            body="Using built-in macOS 'Glass' sound.",
            sound=nib.NotificationSound(
                name=nib.NotificationSoundName.custom("Glass")
            ),
        )
        last_notification_id = app.notifications.push(notification)
        update_status(f"Pushed with Glass sound: {notification.id[:8]}...")

    # Notification with actions
    def push_with_actions():
        nonlocal last_notification_id
        notification = nib.Notification(
            title="New Message",
            body="John: Hey, are you free for lunch?",
            sound=nib.NotificationSound(
                name=nib.NotificationSoundName.custom("Frog")
            ),
            actions=[
                nib.NotificationAction(
                    id="reply",
                    title="Reply",
                    options=[nib.NotificationActionOption.FOREGROUND],
                    text_input=nib.TextInputNotificationAction(
                        button_title="Send",
                        placeholder="Type your reply...",
                    ),
                ),
                nib.NotificationAction(
                    id="mark_read",
                    title="Mark as Read",
                ),
                nib.NotificationAction(
                    id="delete",
                    title="Delete",
                    options=[nib.NotificationActionOption.DESTRUCTIVE],
                ),
            ],
        )
        last_notification_id = app.notifications.push(notification)
        update_status(f"Pushed with actions: {notification.id[:8]}...")

    # Schedule notification
    def schedule_notification():
        nonlocal last_notification_id
        notification = nib.Notification(
            title="Scheduled Reminder",
            body="This notification was scheduled 10 seconds ago!",
            sound=nib.NotificationSound(),
        )
        delay = datetime.now() + timedelta(seconds=10)
        last_notification_id = app.notifications.schedule(notification, at=delay)
        update_status(f"Scheduled for 10s: {notification.id[:8]}...")

    # Cancel last notification
    def cancel_last():
        nonlocal last_notification_id
        if last_notification_id:
            app.notifications.cancel_notification(last_notification_id)
            update_status(f"Cancelled: {last_notification_id[:8]}...")
            last_notification_id = None
        else:
            update_status("No notification to cancel")

    # Cancel all
    def cancel_all():
        app.notifications.cancel_all_notifications()
        update_status("All notifications cancelled")

    # Get scheduled count
    def check_scheduled():
        def on_scheduled(notifications):
            count = len(notifications)
            if count == 0:
                update_status("No scheduled notifications")
            else:
                titles = [n.title for n in notifications[:3]]
                update_status(f"{count} scheduled: {', '.join(titles)}")

        app.notifications.get_all_scheduled_notifications(on_scheduled)

    # Handle action callbacks
    def on_action(notification_id: str, action_id: str, user_text: str | None):
        if action_id == "reply" and user_text:
            update_status(f"Reply: {user_text}")
        elif action_id == "mark_read":
            update_status("Marked as read")
        elif action_id == "delete":
            update_status("Message deleted")
        elif action_id == "default":
            update_status("Notification clicked")
        elif action_id == "dismiss":
            update_status("Notification dismissed")
        else:
            update_status(f"Action: {action_id}")

    app.notifications.on_action(on_action)

    # Request permission on start
    def on_permission(granted: bool):
        if granted:
            update_status("Notification permission granted")
        else:
            update_status("Notification permission denied")

    app.notifications.request_permission(on_permission)

    # --- Permissions demo ---
    perm_camera_text = nib.Text("Camera: ...", font=nib.Font.CAPTION)
    perm_mic_text = nib.Text("Microphone: ...", font=nib.Font.CAPTION)
    perm_notif_text = nib.Text("Notifications: ...", font=nib.Font.CAPTION)

    def refresh_permissions():
        cam = app.permissions.check(nib.Permission.CAMERA)
        mic = app.permissions.check(nib.Permission.MICROPHONE)
        notif = app.permissions.check(nib.Permission.NOTIFICATIONS)
        perm_camera_text.content = f"Camera: {cam.value}"
        perm_mic_text.content = f"Microphone: {mic.value}"
        perm_notif_text.content = f"Notifications: {notif.value}"

    def request_camera():
        granted = app.permissions.request(nib.Permission.CAMERA)
        update_status(f"Camera permission: {'granted' if granted else 'denied'}")
        refresh_permissions()

    def request_mic():
        granted = app.permissions.request(nib.Permission.MICROPHONE)
        update_status(f"Microphone permission: {'granted' if granted else 'denied'}")
        refresh_permissions()

    def request_notif():
        granted = app.permissions.request(nib.Permission.NOTIFICATIONS)
        update_status(f"Notification permission: {'granted' if granted else 'denied'}")
        refresh_permissions()

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Notifications Demo", font=nib.Font.TITLE),
                nib.Text(
                    "Test the new notification API",
                    font=nib.Font.CAPTION,
                    foreground_color=nib.Color.SECONDARY,
                ),
                nib.Divider(),
                # Basic notifications
                nib.VStack(
                    controls=[
                        nib.Text("Push Notifications", font=nib.Font.HEADLINE),
                        nib.HStack(
                            controls=[
                                nib.Button("Simple", action=push_simple),
                                nib.Button("With Sound", action=push_with_sound),
                            ],
                            spacing=8,
                        ),
                        nib.HStack(
                            controls=[
                                nib.Button("Custom Sound", action=push_custom_sound),
                                nib.Button("With Actions", action=push_with_actions),
                            ],
                            spacing=8,
                        ),
                    ],
                    spacing=8,
                    padding=12,
                    background=nib.Rectangle(
                        corner_radius=8,
                        fill=nib.Color.hex("#1a1a1a"),
                    ),
                ),
                nib.Spacer(min_length=8),
                # Scheduling
                nib.VStack(
                    controls=[
                        nib.Text("Scheduling", font=nib.Font.HEADLINE),
                        nib.HStack(
                            controls=[
                                nib.Button("Schedule (10s)", action=schedule_notification),
                                nib.Button("Check Scheduled", action=check_scheduled),
                            ],
                            spacing=8,
                        ),
                    ],
                    spacing=8,
                    padding=12,
                    background=nib.Rectangle(
                        corner_radius=8,
                        fill=nib.Color.hex("#1a1a1a"),
                    ),
                ),
                nib.Spacer(min_length=8),
                # Management
                nib.VStack(
                    controls=[
                        nib.Text("Management", font=nib.Font.HEADLINE),
                        nib.HStack(
                            controls=[
                                nib.Button("Cancel Last", action=cancel_last),
                                nib.Button(
                                    "Cancel All",
                                    action=cancel_all,
                                    role=nib.ButtonRole.DESTRUCTIVE,
                                ),
                            ],
                            spacing=8,
                        ),
                    ],
                    spacing=8,
                    padding=12,
                    background=nib.Rectangle(
                        corner_radius=8,
                        fill=nib.Color.hex("#1a1a1a"),
                    ),
                ),
                nib.Spacer(min_length=8),
                # Permissions
                nib.VStack(
                    controls=[
                        nib.Text("Permissions", font=nib.Font.HEADLINE),
                        perm_camera_text,
                        perm_mic_text,
                        perm_notif_text,
                        nib.HStack(
                            controls=[
                                nib.Button("Check All", action=refresh_permissions),
                            ],
                            spacing=8,
                        ),
                        nib.HStack(
                            controls=[
                                nib.Button("Req Camera", action=request_camera),
                                nib.Button("Req Mic", action=request_mic),
                                nib.Button("Req Notif", action=request_notif),
                            ],
                            spacing=8,
                        ),
                    ],
                    spacing=8,
                    padding=12,
                    background=nib.Rectangle(
                        corner_radius=8,
                        fill=nib.Color.hex("#1a1a1a"),
                    ),
                ),
                nib.Spacer(),
                # Status
                nib.VStack(
                    controls=[
                        nib.Text("Status", font=nib.Font.CAPTION),
                        status_text,
                    ],
                    spacing=4,
                ),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
