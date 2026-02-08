# Camera

The Camera service provides access to camera devices for listing, photo capture, and video frame streaming. Access it via `app.camera`.

```python
devices = app.camera.list_devices()
for d in devices:
    print(f"Found camera: {d.name}")

frame = app.camera.capture_photo()
frame.save("/tmp/photo.jpg")
```

!!! note "Permission Required"
    Camera access requires the user to grant the Camera permission. Use `app.permissions.check(nib.Permission.CAMERA)` and `app.permissions.request(nib.Permission.CAMERA)` before accessing the camera.

## Methods

### `list_devices()`

List all available camera devices on the system.

```python
app.camera.list_devices() -> list[CameraDevice]
```

Returns a list of `CameraDevice` dataclass instances.

### `capture_photo(device_id, format, quality)`

Capture a single photo from a camera.

```python
app.camera.capture_photo(
    device_id: str | None = None,
    format: str = "jpeg",
    quality: float = 0.9,
) -> CameraFrame
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `device_id` | `str \| None` | `None` | Camera device ID from `list_devices()`. Uses the default camera if `None` |
| `format` | `str` | `"jpeg"` | Image format: `"jpeg"` or `"png"` |
| `quality` | `float` | `0.9` | JPEG compression quality from `0.0` to `1.0`. Ignored for PNG |

Returns a `CameraFrame` dataclass with the captured image data.

### `start_stream(callback, device_id, fps)`

Start streaming video frames from a camera. Frames are delivered to the callback function at approximately the specified frame rate. Only one stream can be active at a time.

```python
app.camera.start_stream(
    callback: Callable[[CameraFrame], None],
    device_id: str | None = None,
    fps: int = 30,
) -> bool
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `callback` | `Callable[[CameraFrame], None]` | -- | Function called with each frame |
| `device_id` | `str \| None` | `None` | Camera device ID. Uses the default camera if `None` |
| `fps` | `int` | `30` | Target frames per second (1--60) |

Returns `True` if streaming started successfully.

### `stop_stream()`

Stop the active video frame stream.

```python
app.camera.stop_stream() -> bool
```

Returns `True` if streaming stopped successfully.

---

## Data Classes

### `CameraDevice`

Information about an available camera device.

| Property | Type | Description |
|----------|------|-------------|
| `id` | `str` | Unique device identifier, used in `capture_photo()` and `start_stream()` |
| `name` | `str` | Human-readable device name (e.g., `"FaceTime HD Camera"`) |
| `position` | `CameraPosition` | Physical position of the camera |
| `is_built_in` | `bool` | Whether the camera is built into the device |

### `CameraFrame`

A captured camera frame, either from a photo or a video stream.

| Property | Type | Description |
|----------|------|-------------|
| `data` | `bytes` | Raw image data |
| `width` | `int` | Image width in pixels |
| `height` | `int` | Image height in pixels |
| `format` | `str` | Image format (`"jpeg"` or `"png"`) |

#### `CameraFrame.save(path)`

Save the frame to a file.

```python
frame.save(path: str) -> None
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | `str` | File path to save the image (e.g., `"/tmp/photo.jpg"`) |

---

## Enums

### `CameraPosition`

```python
from nib.services.camera import CameraPosition
```

| Value | Description |
|-------|-------------|
| `CameraPosition.FRONT` | Front-facing camera (e.g., FaceTime camera) |
| `CameraPosition.BACK` | Rear-facing camera (not typical on Macs) |
| `CameraPosition.EXTERNAL` | External USB or Thunderbolt camera |

---

## Examples

### List cameras and capture a photo

```python
import nib

def main(app: nib.App):
    app.title = "Camera"
    app.icon = nib.SFSymbol("camera")
    app.width = 320
    app.height = 200

    status = nib.Text("Ready", foreground_color=nib.Color.SECONDARY)
    device_list = nib.Text("", foreground_color=nib.Color.SECONDARY)

    def list_cameras():
        devices = app.camera.list_devices()
        if devices:
            names = [f"{d.name} ({d.position.value})" for d in devices]
            device_list.content = "\n".join(names)
        else:
            device_list.content = "No cameras found"

    def take_photo():
        status.content = "Capturing..."
        frame = app.camera.capture_photo(format="jpeg", quality=0.9)
        frame.save("/tmp/nib_photo.jpg")
        status.content = f"Saved {frame.width}x{frame.height} photo"

    app.on_appear = list_cameras

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Camera", font=nib.Font.HEADLINE),
                device_list,
                nib.HStack(
                    controls=[
                        nib.Button("List Cameras", action=list_cameras),
                        nib.Button("Take Photo", action=take_photo,
                                   style=nib.ButtonStyle.BORDERED_PROMINENT),
                    ],
                    spacing=8,
                ),
                status,
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

### Stream video frames for processing

```python
import nib

def main(app: nib.App):
    app.title = "Stream"
    app.icon = nib.SFSymbol("video")
    app.width = 300
    app.height = 150

    frame_count = nib.Text("Frames: 0")
    count = 0

    def on_frame(frame):
        nonlocal count
        count += 1
        if count % 30 == 0:  # Update display every 30 frames
            frame_count.content = f"Frames: {count} ({frame.width}x{frame.height})"

    def start():
        app.camera.start_stream(on_frame, fps=15)
        frame_count.content = "Streaming..."

    def stop():
        app.camera.stop_stream()
        frame_count.content = f"Stopped at {count} frames"

    app.build(
        nib.VStack(
            controls=[
                frame_count,
                nib.HStack(
                    controls=[
                        nib.Button("Start", action=start, style=nib.ButtonStyle.BORDERED_PROMINENT),
                        nib.Button("Stop", action=stop, role=nib.ButtonRole.DESTRUCTIVE),
                    ],
                    spacing=8,
                ),
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```
