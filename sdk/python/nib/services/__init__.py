"""System services for accessing device information.

This module provides access to system services like battery status,
network connectivity, screen brightness, keychain, camera, and launch at login.

Services are accessed via app properties for a clean synchronous API:

Example:
    Using battery service::

        def main(app: nib.App):
            status = app.battery.get_status()
            print(f"Level: {status.level}%")

    Using connectivity service::

        def main(app: nib.App):
            info = app.connectivity.get_status()
            print(f"Connected: {info.is_connected}, Type: {info.type}")

    Using screen service::

        def main(app: nib.App):
            info = app.screen.get_info()
            app.screen.set_brightness(0.5)

    Using keychain service::

        def main(app: nib.App):
            app.keychain.set("MyApp", "api_token", "secret123")
            token = app.keychain.get("MyApp", "api_token")

    Using camera service::

        def main(app: nib.App):
            devices = app.camera.list_devices()
            frame = app.camera.capture_photo()
            frame.save("/tmp/photo.jpg")

    Using launch at login service::

        def main(app: nib.App):
            # Check if enabled
            if app.launch_at_login.is_enabled:
                print("App launches at login")

            # Toggle (in response to user action)
            app.launch_at_login.set(True)
"""

from .battery import Battery, BatteryInfo, BatteryState
from .connectivity import Connectivity, ConnectivityInfo, ConnectionType
from .screen import Screen, ScreenInfo
from .keychain import Keychain
from .camera import Camera, CameraDevice, CameraFrame, CameraPosition
from .launch_at_login import LaunchAtLogin

__all__ = [
    # Battery
    "Battery",
    "BatteryInfo",
    "BatteryState",
    # Connectivity
    "Connectivity",
    "ConnectivityInfo",
    "ConnectionType",
    # Screen
    "Screen",
    "ScreenInfo",
    # Keychain
    "Keychain",
    # Camera
    "Camera",
    "CameraDevice",
    "CameraFrame",
    "CameraPosition",
    # Launch at Login
    "LaunchAtLogin",
]
