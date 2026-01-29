"""Camera preview view for displaying live camera feed."""

from typing import Any, Optional

from ..base import View


class CameraPreview(View):
    """
    Live camera preview view.

    Displays a real-time preview from a camera device.

    Example::

        import nib

        # Use default camera
        preview = nib.CameraPreview()

        # Use specific camera by device ID
        preview = nib.CameraPreview(device_id="device-uuid")

    Args:
        device_id: Optional camera device ID. Uses default camera if None.
                   Get device IDs from Camera.list_devices().
        **kwargs: Standard view modifiers (width, height, padding, etc.)
    """

    _type = "CameraPreview"

    def __init__(
        self,
        device_id: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._device_id = device_id

    @property
    def device_id(self) -> Optional[str]:
        """The camera device ID."""
        return self._device_id

    @device_id.setter
    def device_id(self, value: Optional[str]) -> None:
        """Set the camera device ID."""
        self._device_id = value

    def _get_props(self) -> dict:
        """Get view properties for serialization."""
        props = {}
        if self._device_id is not None:
            props["deviceId"] = self._device_id
        return props
