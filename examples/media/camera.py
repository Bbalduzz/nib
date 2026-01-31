import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

import nib
from nib.services.camera import CameraDevice


def main(app: nib.App):
    app.title = "Camera"
    app.width = 640
    app.height = 520
    app.menu = [nib.MenuItem("Quit", action=app.quit)]

    camera_devices: list[CameraDevice] = []
    preview = nib.CameraPreview()
    status = nib.Text("Loading cameras...")
    picker = nib.Picker(
        label="Camera",
        selection="",
        options=[],
    )

    def on_camera_change(value: str):
        """Change camera for CameraPreview."""
        preview.device_id = value if value else None
        for d in camera_devices:
            if d.id == value:
                status.content = f"Using: {d.name}"
                break

    def load_cameras():
        """Load camera list using sync API."""
        devices = app.camera.list_devices()
        camera_devices.clear()
        camera_devices.extend(devices)

        if devices:
            options = [{"value": d.id, "label": d.name} for d in devices]
            picker.options = options
            picker.selection = devices[0].id
            preview.device_id = devices[0].id
            status.content = f"Using: {devices[0].name}"
        else:
            status.content = "No cameras found"

    def take_photo():
        """Capture a photo from current camera."""
        status.content = "Capturing..."
        frame = app.camera.capture_photo(
            device_id=preview.device_id,
            format="jpeg",
            quality=0.9,
        )
        path = "/tmp/nib_photo.jpg"
        frame.save(path)
        status.content = f"Saved: {frame.width}x{frame.height} to {path}"
        print(f"Photo saved to {path}")

    picker.on_change = on_camera_change

    # Load cameras on app appear
    app.on_appear = load_cameras

    app.build(
        nib.VStack(
            controls=[
                preview,
                nib.HStack(
                    controls=[
                        picker,
                        nib.Spacer(),
                        nib.Button("Take Photo", action=take_photo),
                    ],
                    padding={"horizontal": 12, "vertical": 8},
                ),
                status,
            ],
        )
    )


nib.run(main)
