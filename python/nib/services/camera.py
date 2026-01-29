"""Camera service for capturing photos and streaming video frames.

Example:
    List cameras and capture a photo::

        devices = app.camera.list_devices()
        for d in devices:
            print(f"Found: {d.name}")

        frame = app.camera.capture_photo()
        frame.save("/tmp/photo.jpg")
"""

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Callable, List, Optional

from .base import Service

if TYPE_CHECKING:
    from ..core.app import App


class CameraPosition(Enum):
    """Camera position/type."""
    FRONT = "front"
    BACK = "back"
    EXTERNAL = "external"


@dataclass
class CameraDevice:
    """Information about a camera device."""
    id: str
    name: str
    position: CameraPosition
    is_built_in: bool

    @classmethod
    def from_dict(cls, data: dict) -> "CameraDevice":
        """Create CameraDevice from response dictionary."""
        position_str = data.get("position", "external")
        try:
            position = CameraPosition(position_str)
        except ValueError:
            position = CameraPosition.EXTERNAL

        return cls(
            id=data.get("id", ""),
            name=data.get("name", "Unknown"),
            position=position,
            is_built_in=data.get("isBuiltIn", False),
        )


@dataclass
class CameraFrame:
    """A captured camera frame (photo or video frame)."""
    data: bytes
    width: int
    height: int
    format: str  # "jpeg" or "png"

    def save(self, path: str) -> None:
        """Save frame to a file."""
        with open(path, "wb") as f:
            f.write(self.data)

    @classmethod
    def from_dict(cls, data: dict) -> "CameraFrame":
        """Create CameraFrame from response dictionary."""
        image_data = data.get("imageData")
        if image_data is None:
            image_data = b""
        elif isinstance(image_data, str):
            import base64
            image_data = base64.b64decode(image_data)

        return cls(
            data=image_data,
            width=data.get("imageWidth", 0),
            height=data.get("imageHeight", 0),
            format=data.get("imageFormat", "jpeg"),
        )


class Camera(Service):
    """Service for camera capture and streaming.

    Access via app.camera property.

    Example:
        List cameras and capture photo::

            # List available cameras
            devices = app.camera.list_devices()
            for d in devices:
                print(f"Found camera: {d.name}")

            # Capture a photo
            frame = app.camera.capture_photo()
            frame.save("/tmp/photo.jpg")
            print(f"Saved {frame.width}x{frame.height} photo")

        Stream video frames::

            def on_frame(frame: CameraFrame):
                # Process frame for ML/CV
                pass

            app.camera.start_stream(on_frame, fps=15)
            # Later: app.camera.stop_stream()
    """

    _stream_callback: Optional[Callable[["CameraFrame"], None]] = None

    def list_devices(self) -> List[CameraDevice]:
        """List available camera devices.

        Returns:
            List of CameraDevice objects.
        """
        data = self._request("camera", "listDevices")
        return [CameraDevice.from_dict(d) for d in data.get("devices", [])]

    def capture_photo(
        self,
        device_id: Optional[str] = None,
        format: str = "jpeg",
        quality: float = 0.9,
    ) -> CameraFrame:
        """Capture a single photo.

        Args:
            device_id: Optional camera device ID. Uses default camera if None.
            format: Image format, either "jpeg" or "png".
            quality: JPEG quality from 0.0 to 1.0 (ignored for PNG).

        Returns:
            CameraFrame with the captured image.
        """
        data = self._request(
            "camera", "capturePhoto",
            params={
                "deviceId": device_id,
                "format": format,
                "quality": quality,
            },
        )
        return CameraFrame.from_dict(data)

    def start_stream(
        self,
        callback: Callable[["CameraFrame"], None],
        device_id: Optional[str] = None,
        fps: int = 30,
    ) -> bool:
        """Start streaming video frames.

        Frames are delivered to the callback at approximately the specified FPS.
        Only one stream can be active at a time.

        Note: Streaming uses callbacks since it's continuous.

        Args:
            callback: Function called with each CameraFrame.
            device_id: Optional camera device ID. Uses default camera if None.
            fps: Target frames per second (1-60).

        Returns:
            True if streaming started successfully.
        """
        Camera._stream_callback = callback
        data = self._request(
            "camera", "startStream",
            params={
                "deviceId": device_id,
                "fps": max(1, min(60, fps)),
            },
        )
        return data.get("success", False)

    def stop_stream(self) -> bool:
        """Stop streaming video frames.

        Returns:
            True if streaming stopped successfully.
        """
        Camera._stream_callback = None
        data = self._request("camera", "stopStream")
        return data.get("success", False)

    @classmethod
    def _handle_stream_frame(cls, data: dict) -> None:
        """Handle incoming stream frame (called by connection)."""
        if cls._stream_callback:
            frame = CameraFrame.from_dict(data)
            cls._stream_callback(frame)
