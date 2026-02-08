# Permissions

The Permissions service provides a unified API for checking and requesting macOS permissions for Camera, Microphone, and Notifications. Access it via `app.permissions`.

```python
status = app.permissions.check(nib.Permission.CAMERA)
if status == nib.PermissionStatus.NOT_DETERMINED:
    granted = app.permissions.request(nib.Permission.CAMERA)
```

## Methods

### `check(permission)`

Check the current authorization status of a permission without prompting the user.

```python
app.permissions.check(permission: Permission) -> PermissionStatus
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `permission` | `Permission` | The permission to check |

Returns a `PermissionStatus` enum value.

### `request(permission)`

Request authorization for a permission. If the permission status is `NOT_DETERMINED`, the system will display a permission dialog. If the permission has already been authorized or denied, the current state is returned without showing a dialog.

```python
app.permissions.request(permission: Permission) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `permission` | `Permission` | The permission to request |

Returns `True` if the permission was granted, `False` otherwise.

---

## Enums

### `Permission`

```python
import nib
# or: from nib.services.permissions import Permission
```

| Value | Description |
|-------|-------------|
| `nib.Permission.CAMERA` | Camera access |
| `nib.Permission.MICROPHONE` | Microphone access |
| `nib.Permission.NOTIFICATIONS` | Notification delivery |

### `PermissionStatus`

```python
import nib
# or: from nib.services.permissions import PermissionStatus
```

| Value | Description |
|-------|-------------|
| `nib.PermissionStatus.AUTHORIZED` | Permission has been granted |
| `nib.PermissionStatus.DENIED` | Permission has been denied by the user |
| `nib.PermissionStatus.NOT_DETERMINED` | Permission has not been requested yet |
| `nib.PermissionStatus.RESTRICTED` | Permission is restricted by system policy (e.g., parental controls) |

---

## Examples

### Check and request camera permission

```python
import nib

def main(app: nib.App):
    app.title = "Permissions"
    app.icon = nib.SFSymbol("lock.shield")
    app.width = 320
    app.height = 200

    camera_status = nib.Text("--", foreground_color=nib.Color.SECONDARY)
    mic_status = nib.Text("--", foreground_color=nib.Color.SECONDARY)
    notif_status = nib.Text("--", foreground_color=nib.Color.SECONDARY)

    def refresh():
        cam = app.permissions.check(nib.Permission.CAMERA)
        mic = app.permissions.check(nib.Permission.MICROPHONE)
        notif = app.permissions.check(nib.Permission.NOTIFICATIONS)

        camera_status.content = f"Camera: {cam.value}"
        mic_status.content = f"Microphone: {mic.value}"
        notif_status.content = f"Notifications: {notif.value}"

    def request_camera():
        granted = app.permissions.request(nib.Permission.CAMERA)
        camera_status.content = f"Camera: {'authorized' if granted else 'denied'}"

    def request_mic():
        granted = app.permissions.request(nib.Permission.MICROPHONE)
        mic_status.content = f"Microphone: {'authorized' if granted else 'denied'}"

    def request_notif():
        granted = app.permissions.request(nib.Permission.NOTIFICATIONS)
        notif_status.content = f"Notifications: {'authorized' if granted else 'denied'}"

    app.on_appear = refresh

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Permissions", font=nib.Font.HEADLINE),
                nib.HStack(controls=[camera_status, nib.Spacer(),
                    nib.Button("Request", action=request_camera)], spacing=8),
                nib.HStack(controls=[mic_status, nib.Spacer(),
                    nib.Button("Request", action=request_mic)], spacing=8),
                nib.HStack(controls=[notif_status, nib.Spacer(),
                    nib.Button("Request", action=request_notif)], spacing=8),
            ],
            spacing=10,
            padding=20,
        )
    )

nib.run(main)
```

### Gate a feature behind permission

```python
import nib

def main(app: nib.App):
    app.title = "Photo App"
    app.icon = nib.SFSymbol("camera")
    app.width = 300
    app.height = 150

    status = nib.Text("Checking camera access...", foreground_color=nib.Color.SECONDARY)

    def check_and_capture():
        perm = app.permissions.check(nib.Permission.CAMERA)

        if perm == nib.PermissionStatus.AUTHORIZED:
            frame = app.camera.capture_photo()
            frame.save("/tmp/photo.jpg")
            status.content = f"Photo saved ({frame.width}x{frame.height})"

        elif perm == nib.PermissionStatus.NOT_DETERMINED:
            granted = app.permissions.request(nib.Permission.CAMERA)
            if granted:
                status.content = "Permission granted. Tap again to capture."
            else:
                status.content = "Camera access denied."

        elif perm == nib.PermissionStatus.DENIED:
            status.content = "Camera access denied. Enable in System Settings."

        else:
            status.content = "Camera access restricted."

    app.build(
        nib.VStack(
            controls=[
                nib.Button("Take Photo", action=check_and_capture,
                           style=nib.ButtonStyle.BORDERED_PROMINENT),
                status,
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```
