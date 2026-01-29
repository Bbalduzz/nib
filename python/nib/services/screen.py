"""Screen brightness service.

Provides access to screen brightness information and control.

Example:
    Get screen info::

        info = app.screen.get_info()
        print(f"Brightness: {info.brightness * 100}%")

    Set screen brightness::

        app.screen.set_brightness(0.5)  # 50% brightness
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .base import Service

if TYPE_CHECKING:
    from ..core.app import App


@dataclass
class ScreenInfo:
    """Screen information.

    Attributes:
        brightness: Current brightness level (0.0 to 1.0).
        is_builtin: Whether this is the built-in display.
        width: Screen width in points.
        height: Screen height in points.
        scale: Display scale factor (e.g., 2.0 for Retina).
    """
    brightness: float
    is_builtin: bool
    width: float
    height: float
    scale: float

    @classmethod
    def from_dict(cls, data: dict) -> "ScreenInfo":
        """Create ScreenInfo from dictionary response."""
        return cls(
            brightness=data.get("brightness", 0.5),
            is_builtin=data.get("isBuiltin", True),
            width=data.get("width", 0),
            height=data.get("height", 0),
            scale=data.get("scale", 1.0),
        )


class Screen(Service):
    """Service for accessing and controlling screen brightness.

    Access via app.screen property.

    Note:
        Setting brightness may require accessibility permissions on macOS.

    Example:
        Dim screen at night::

            info = app.screen.get_info()
            if info.brightness > 0.3:
                app.screen.set_brightness(0.3)
    """

    def get_info(self) -> ScreenInfo:
        """Get current screen information.

        Returns:
            ScreenInfo with brightness, dimensions, and scale.

        Example:
            Get screen brightness::

                info = app.screen.get_info()
                print(f"Brightness: {info.brightness}")
        """
        data = self._request("screen", "info")
        return ScreenInfo.from_dict(data)

    def set_brightness(self, brightness: float) -> bool:
        """Set screen brightness.

        Args:
            brightness: Brightness level from 0.0 (darkest) to 1.0 (brightest).

        Returns:
            True if brightness was set successfully.

        Example:
            Set brightness to 50%::

                success = app.screen.set_brightness(0.5)
        """
        brightness = max(0.0, min(1.0, brightness))
        data = self._request("screen", "setBrightness", {"brightness": brightness})
        return data.get("success", False)
