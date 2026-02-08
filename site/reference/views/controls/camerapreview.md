# CameraPreview

A view that displays a live camera feed from a connected device. CameraPreview shows a real-time video preview, useful for camera-enabled applications, barcode scanning, or video conferencing interfaces.

## Constructor

```python
nib.CameraPreview(
    device_id=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `device_id` | `str` | `None` | Camera device ID. When `None`, the system default camera is used. Obtain device IDs from `Camera.list_devices()`. |
| `**modifiers` | | | Common view modifiers: `width`, `height`, `corner_radius`, `opacity`, `padding`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `device_id` | `str` | Get or set the camera device ID. |

## Examples

### Default camera preview

```python
import nib

def main(app: nib.App):
    app.build(
        nib.CameraPreview(
            width=320,
            height=240,
            corner_radius=12,
            padding=16,
        )
    )

nib.run(main)
```

### Camera preview with device selection

```python
import nib
from nib.services import Camera

def main(app: nib.App):
    preview = nib.CameraPreview(
        width=320,
        height=240,
        corner_radius=8,
    )

    devices = Camera.list_devices()
    options = [(d["id"], d["name"]) for d in devices]

    app.build(
        nib.VStack(controls=[
            nib.Picker(
                "Camera",
                selection=options[0][0] if options else "",
                options=options,
                on_change=lambda device_id: setattr(
                    preview, "device_id", device_id
                ),
            ),
            preview,
        ], spacing=12, padding=16)
    )

nib.run(main)
```

### Camera feed with overlay

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ZStack(controls=[
            nib.CameraPreview(
                width=400,
                height=300,
                corner_radius=12,
            ),
            nib.VStack(controls=[
                nib.Spacer(),
                nib.Text(
                    "Live",
                    foreground_color=nib.Color.WHITE,
                    font=nib.Font.CAPTION,
                    padding={"horizontal": 8, "vertical": 4},
                    background=nib.Color.RED,
                    corner_radius=4,
                ),
            ], padding=12),
        ], padding=16)
    )

nib.run(main)
```
