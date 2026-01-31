"""Screen service for display information and control.

Provides access to screen brightness, resolution, dark mode, and multi-display info.

Example:
    Get screen info::

        info = app.screen.get_info()
        print(f"Brightness: {info.brightness * 100}%")
        print(f"Resolution: {info.width}x{info.height}")
        print(f"Refresh rate: {info.refresh_rate}Hz")

    Toggle dark mode::

        dark_info = app.screen.get_dark_mode()
        app.screen.set_dark_mode(not dark_info.is_dark_mode)

    List all displays::

        displays = app.screen.list_displays()
        for d in displays:
            print(f"{d['name']}: {d['width']}x{d['height']}")
"""

import json
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from .base import Service

if TYPE_CHECKING:
    from ..core.app import App


@dataclass
class ScreenInfo:
    """Screen information.

    Attributes:
        brightness: Current brightness level (0.0 to 1.0), None if unavailable.
        is_builtin: Whether this is the built-in display.
        width: Screen width in points.
        height: Screen height in points.
        scale: Display scale factor (e.g., 2.0 for Retina).
        visible_width: Visible width (excluding dock/menu bar).
        visible_height: Visible height (excluding dock/menu bar).
        display_id: System display identifier.
        name: Display name (e.g., "Built-in Retina Display").
        refresh_rate: Display refresh rate in Hz.
        native_width: Native pixel width.
        native_height: Native pixel height.
        color_space: Color space name.
        color_depth: Bits per pixel.
        available_resolutions: List of available display modes.
    """
    brightness: Optional[float]
    is_builtin: bool
    width: float
    height: float
    scale: float
    visible_width: Optional[float] = None
    visible_height: Optional[float] = None
    display_id: Optional[int] = None
    name: Optional[str] = None
    refresh_rate: Optional[float] = None
    native_width: Optional[int] = None
    native_height: Optional[int] = None
    color_space: Optional[str] = None
    color_depth: Optional[int] = None
    available_resolutions: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "ScreenInfo":
        """Create ScreenInfo from dictionary response."""
        # Parse JSON-encoded resolutions if present
        resolutions = []
        if "availableResolutionsJson" in data and data["availableResolutionsJson"]:
            try:
                resolutions = json.loads(data["availableResolutionsJson"])
            except json.JSONDecodeError:
                pass

        return cls(
            brightness=data.get("brightness"),
            is_builtin=data.get("isBuiltin", True),
            width=data.get("width", 0),
            height=data.get("height", 0),
            scale=data.get("scale", 1.0),
            visible_width=data.get("visibleWidth"),
            visible_height=data.get("visibleHeight"),
            display_id=data.get("displayID"),
            name=data.get("name"),
            refresh_rate=data.get("refreshRate"),
            native_width=data.get("nativeWidth"),
            native_height=data.get("nativeHeight"),
            color_space=data.get("colorSpace"),
            color_depth=data.get("colorDepth"),
            available_resolutions=resolutions,
        )


@dataclass
class DarkModeInfo:
    """Dark mode information.

    Attributes:
        is_dark_mode: Whether dark mode is enabled.
        appearance_name: Full appearance name (e.g., "NSAppearanceNameDarkAqua").
    """
    is_dark_mode: bool
    appearance_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "DarkModeInfo":
        """Create DarkModeInfo from dictionary response."""
        return cls(
            is_dark_mode=data.get("isDarkMode", False),
            appearance_name=data.get("appearanceName"),
        )


@dataclass
class ColorProfileInfo:
    """Color profile information.

    Attributes:
        color_space_name: Color space name.
        color_component_count: Number of color components.
        icc_profile_size: Size of ICC profile in bytes.
    """
    color_space_name: Optional[str] = None
    color_component_count: Optional[int] = None
    icc_profile_size: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ColorProfileInfo":
        """Create ColorProfileInfo from dictionary response."""
        return cls(
            color_space_name=data.get("colorSpaceName"),
            color_component_count=data.get("colorComponentCount"),
            icc_profile_size=data.get("iccProfileSize"),
        )


@dataclass
class ScreenshotResult:
    """Screenshot result.

    Attributes:
        success: Whether the screenshot was captured successfully.
        image_data: Raw PNG image data (bytes).
        width: Image width in pixels.
        height: Image height in pixels.
    """
    success: bool
    image_data: Optional[bytes] = None
    width: Optional[int] = None
    height: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ScreenshotResult":
        """Create ScreenshotResult from dictionary response."""
        image_data = data.get("imageData")
        if isinstance(image_data, bytes):
            pass  # Already bytes
        elif image_data is not None:
            image_data = bytes(image_data)  # Convert from list

        return cls(
            success=data.get("success", False),
            image_data=image_data,
            width=data.get("imageWidth"),
            height=data.get("imageHeight"),
        )

    def save(self, path: str) -> bool:
        """Save screenshot to file.

        Args:
            path: File path to save to (should end in .png).

        Returns:
            True if saved successfully.
        """
        if not self.success or not self.image_data:
            return False
        try:
            with open(path, "wb") as f:
                f.write(self.image_data)
            return True
        except IOError:
            return False


class Screen(Service):
    """Service for accessing and controlling screen/display settings.

    Access via app.screen property.

    Features:
        - Get display info (brightness, resolution, refresh rate)
        - Set brightness
        - List all connected displays
        - Get/set dark mode
        - Take screenshots
        - Change resolution

    Note:
        Some operations may require accessibility or screen recording permissions.

    Example:
        Get screen info::

            info = app.screen.get_info()
            print(f"Display: {info.name}")
            print(f"Resolution: {info.width}x{info.height} @{info.scale}x")
            print(f"Refresh rate: {info.refresh_rate}Hz")
    """

    def get_info(self) -> ScreenInfo:
        """Get current screen information.

        Returns:
            ScreenInfo with brightness, dimensions, refresh rate, and more.

        Example:
            Get detailed screen info::

                info = app.screen.get_info()
                print(f"Display: {info.name}")
                print(f"Brightness: {info.brightness * 100:.0f}%")
                print(f"Native: {info.native_width}x{info.native_height}")
        """
        data = self._request("screen", "info")
        return ScreenInfo.from_dict(data)

    def list_displays(self) -> List[Dict[str, Any]]:
        """List all connected displays.

        Returns:
            List of display info dictionaries with keys:
            - index: Display index
            - displayID: System display ID
            - name: Display name
            - width, height: Resolution in points
            - scale: Scale factor
            - isMain: Whether this is the main display
            - isBuiltin: Whether this is built-in
            - refreshRate: Refresh rate in Hz
            - colorSpace: Color space name

        Example:
            List all monitors::

                for display in app.screen.list_displays():
                    print(f"{display['name']}: {display['width']}x{display['height']}")
        """
        data = self._request("screen", "list")
        # Parse JSON-encoded displays
        if "displaysJson" in data and data["displaysJson"]:
            try:
                return json.loads(data["displaysJson"])
            except json.JSONDecodeError:
                return []
        return []

    def set_brightness(self, brightness: float) -> bool:
        """Set screen brightness.

        Args:
            brightness: Brightness level from 0.0 (darkest) to 1.0 (brightest).

        Returns:
            True if brightness was set successfully.

        Note:
            Only works on built-in displays.

        Example:
            Set brightness to 50%::

                success = app.screen.set_brightness(0.5)
        """
        brightness = max(0.0, min(1.0, brightness))
        data = self._request("screen", "setBrightness", {"brightness": brightness})
        return data.get("success", False)

    def set_resolution(self, width: int, height: int) -> bool:
        """Set screen resolution.

        Args:
            width: Target width in points.
            height: Target height in points.

        Returns:
            True if resolution was changed successfully.

        Note:
            Resolution must be one of the available modes from get_info().

        Example:
            Change to 1920x1080::

                success = app.screen.set_resolution(1920, 1080)
        """
        data = self._request("screen", "setResolution", {"width": width, "height": height})
        return data.get("success", False)

    def get_dark_mode(self) -> DarkModeInfo:
        """Get current dark mode status.

        Returns:
            DarkModeInfo with is_dark_mode and appearance_name.

        Example:
            Check if dark mode is enabled::

                info = app.screen.get_dark_mode()
                if info.is_dark_mode:
                    print("Dark mode is on")
        """
        data = self._request("screen", "getDarkMode")
        return DarkModeInfo.from_dict(data)

    def set_dark_mode(self, enabled: bool) -> bool:
        """Set system dark mode.

        Args:
            enabled: True for dark mode, False for light mode.

        Returns:
            True if dark mode was changed successfully.

        Note:
            Requires automation permission for System Events.

        Example:
            Enable dark mode::

                success = app.screen.set_dark_mode(True)
        """
        data = self._request("screen", "setDarkMode", {"enabled": enabled})
        return data.get("success", False)

    def get_color_profile(self) -> ColorProfileInfo:
        """Get current color profile information.

        Returns:
            ColorProfileInfo with color space details.

        Example:
            Get color profile::

                profile = app.screen.get_color_profile()
                print(f"Color space: {profile.color_space_name}")
        """
        data = self._request("screen", "getColorProfile")
        return ColorProfileInfo.from_dict(data)

    def screenshot(
        self,
        display_id: Optional[int] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
    ) -> ScreenshotResult:
        """Take a screenshot.

        Args:
            display_id: Specific display ID (default: main display).
            x, y, width, height: Optional region to capture.

        Returns:
            ScreenshotResult with image data.

        Note:
            Requires screen recording permission.

        Example:
            Capture full screen::

                result = app.screen.screenshot()
                if result.success:
                    result.save("/tmp/screenshot.png")

            Capture region::

                result = app.screen.screenshot(x=0, y=0, width=500, height=500)
        """
        params = {}
        if display_id is not None:
            params["displayID"] = display_id
        if all(v is not None for v in [x, y, width, height]):
            params["x"] = x
            params["y"] = y
            params["width"] = width
            params["height"] = height

        data = self._request("screen", "screenshot", params if params else None)
        return ScreenshotResult.from_dict(data)
