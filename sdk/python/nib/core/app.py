"""Main application class and entry point for Nib applications.

This module provides the core :class:`App` class that manages the lifecycle
of a Nib menu bar application, including window management, event handling,
notifications, hotkeys, and communication with the Swift runtime.

It also provides helper classes for menu items (:class:`MenuItem`,
:class:`MenuDivider`) and SF Symbols (:class:`SFSymbol`).

Example:
    Function-based approach (recommended)::

        import nib

        def main(app: nib.App):
            app.title = "My App"
            app.icon = nib.SFSymbol("star.fill")
            app.width = 300
            app.height = 200

            counter = nib.Text("0")

            def increment():
                counter.content = str(int(counter.content) + 1)

            app.build(
                nib.VStack(
                    controls=[counter, nib.Button("Add", action=increment)],
                    spacing=8,
                    padding=16,
                )
            )

        nib.run(main)

    Class-based approach::

        import nib

        class MyApp(nib.App):
            def body(self) -> nib.View:
                return nib.Text("Hello, World!")

        MyApp(icon="star.fill").run()
"""

import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union
import uuid

from .connection import Connection
from .diff import diff_trees  # noqa: F401 (kept for backward compatibility)
from .logging import logger
from .settings import Settings
from ..views import View
from ..views.settings_page import SettingsPage, SettingsTab
from ..types import SymbolRenderingMode, resolve_enum


class App:
    """Main application class for Nib menu bar applications.

    The App class manages the entire lifecycle of a Nib application, including:

    - Window configuration (size, title, icon)
    - View tree rendering and updates
    - Event handling (taps, changes, hotkeys)
    - System integration (notifications, clipboard, file dialogs)
    - Communication with the Swift runtime

    Attributes:
        title: The title displayed in the menu bar (optional).
        icon: The menu bar icon as string or :class:`SFSymbol`.
        width: The popover window width in points.
        height: The popover window height in points.
        menu: List of :class:`MenuItem` for right-click context menu.
        fonts: Dictionary mapping font names to file paths/URLs.
        on_appear: Callback invoked when the popover opens.

    Example:
        Function-based (recommended)::

            def main(app: nib.App):
                app.title = "My App"
                app.icon = nib.SFSymbol("star.fill")
                app.width = 300
                app.height = 200

                app.build(nib.Text("Hello!"))

            nib.run(main)

        Class-based::

            class MyApp(nib.App):
                def body(self) -> nib.View:
                    return nib.Text("Hello!")

            MyApp(icon="star.fill").run()
    """

    # Class-level assets directory (shared across all instances)
    _assets_dir: Optional[Path] = None
    _assets_dir_initialized: bool = False

    @classmethod
    def set_assets_dir(cls, path: Union[str, Path, None]) -> None:
        """Set the assets directory for the application.

        Args:
            path: Path to assets directory, or None to auto-detect.
        """
        if path is not None:
            p = Path(path)
            # Resolve relative paths to absolute (relative to script dir or CWD)
            if not p.is_absolute():
                main_module = sys.modules.get("__main__")
                if main_module and hasattr(main_module, "__file__") and main_module.__file__:
                    p = Path(main_module.__file__).parent / p
                else:
                    p = p.resolve()
            cls._assets_dir = p
        else:
            cls._assets_dir = None
        cls._assets_dir_initialized = True

    @classmethod
    def _auto_detect_assets_dir(cls) -> Optional[Path]:
        """Auto-detect the assets directory based on execution mode."""
        # Check for bundled mode via NIB_SOCKET environment variable
        # This is set by Swift when launching embedded Python
        if os.environ.get("NIB_SOCKET"):
            # Bundled mode with python-build-standalone
            # Try multiple detection methods

            # Method 1: Use PYTHONHOME (Contents/MacOS/python -> Contents/Resources/assets)
            python_home = os.environ.get("PYTHONHOME", "")
            if python_home:
                bundle_contents = Path(python_home).parent.parent
                assets_path = bundle_contents / "Resources" / "assets"
                if assets_path.exists():
                    return assets_path

            # Method 2: Use __file__ of this module to find bundle
            # nib is in Contents/Resources/app/vendor/nib/core/app.py
            # -> Contents/Resources/assets
            try:
                module_path = Path(__file__).resolve()
                # Go up from nib/core/app.py -> vendor -> app -> Resources
                resources_dir = module_path.parent.parent.parent.parent.parent
                assets_path = resources_dir / "assets"
                if assets_path.exists():
                    return assets_path
            except Exception:
                pass

            # Method 3: Use __main__.__file__ which is Contents/Resources/app/main.py
            main_module = sys.modules.get("__main__")
            if main_module and hasattr(main_module, "__file__") and main_module.__file__:
                main_path = Path(main_module.__file__).resolve()
                # main.py is in Contents/Resources/app/ -> Contents/Resources/assets
                resources_dir = main_path.parent.parent
                assets_path = resources_dir / "assets"
                if assets_path.exists():
                    return assets_path

        # Legacy py2app bundled mode (sys.frozen)
        if getattr(sys, "frozen", False):
            # Bundled mode - assets are in Contents/Resources/assets
            bundle_dir = Path(sys.executable).parent.parent
            return bundle_dir / "Resources" / "assets"

        # Development mode - find assets relative to main script
        main_module = sys.modules.get("__main__")
        if main_module and hasattr(main_module, "__file__") and main_module.__file__:
            script_dir = Path(main_module.__file__).parent
            # Check common locations
            for assets_path in [
                script_dir / "assets",           # Same dir as script
                script_dir.parent / "assets",    # Parent dir (if script is in src/)
                script_dir / "src" / "assets",   # src/assets from project root
            ]:
                if assets_path.exists():
                    return assets_path
        return None

    @classmethod
    def resolve_asset(cls, relative_path: str) -> str:
        """Resolve an asset path to an absolute path.

        Args:
            relative_path: Path relative to assets directory, or absolute/URL.

        Returns:
            Resolved absolute path. Returns empty string if asset not found
            (allows Swift to show placeholder).
        """
        # Don't resolve absolute paths or URLs
        if relative_path.startswith("/") or relative_path.startswith(("http://", "https://")):
            return relative_path

        # Initialize assets dir if not done yet
        if not cls._assets_dir_initialized:
            cls._assets_dir = cls._auto_detect_assets_dir()
            cls._assets_dir_initialized = True
            if cls._assets_dir:
                logger.debug(f"Assets directory: {cls._assets_dir}")

        # Resolve relative to assets dir
        if cls._assets_dir and cls._assets_dir.exists():
            asset_path = cls._assets_dir / relative_path
            if asset_path.exists():
                return str(asset_path)
            else:
                # Asset not found - log warning
                logger.warn(f"Asset not found: {relative_path}", path=str(cls._assets_dir))
                return ""  # Return empty string so Swift shows placeholder

        # No assets directory configured
        logger.warn(f"No assets directory configured, cannot resolve: {relative_path}")
        return ""

    def __init__(
        self,
        title: Optional[str] = None,
        icon: Optional[Union[str, "SFSymbol"]] = None,
        identifier: Optional[str] = None,
    ):
        self._title = title
        self._icon: Optional[Union[str, "SFSymbol"]] = icon  # Keep full object for serialization
        self._identifier = identifier  # Bundle identifier for UserDefaults
        self._root_view: Optional[View] = None
        self._show_quit_item = False
        self._width: Optional[float] = None
        self._height: Optional[float] = None
        self._connection: Optional[Connection] = None
        self._runtime_process: Optional[subprocess.Popen] = None
        self._socket_path: Optional[str] = None
        self._action_map: Dict[str, Callable] = {}
        self._change_map: Dict[str, Callable] = {}
        self._view_event_map: Dict[str, Callable] = {}
        self._submit_map: Dict[str, Callable] = {}
        self._running = False
        self._previous_tree: Optional[dict] = None  # For diffing
        # Render loop (single thread, event-based)
        self._render_lock = threading.Lock()
        self._render_requested = threading.Event()
        self._render_thread: Optional[threading.Thread] = None
        # Menu bar right-click menu
        self._menu: List["MenuItem"] = []
        self._menu_action_map: Dict[str, Callable] = {}
        # Hotkeys
        self._hotkey_map: Dict[str, Callable] = {}
        # Clipboard read callbacks
        self._clipboard_callbacks: Dict[str, Callable] = {}
        # Drop handlers
        self._drop_map: Dict[str, Callable] = {}
        # Canvas pan/hover handlers
        self._pan_start_map: Dict[str, Callable] = {}
        self._pan_update_map: Dict[str, Callable] = {}
        self._pan_end_map: Dict[str, Callable] = {}
        self._hover_map: Dict[str, Callable] = {}
        # Click handlers
        self._click_map: Dict[str, Callable] = {}
        # Custom fonts
        self._fonts: Dict[str, str] = {}
        # App lifecycle callbacks
        self._on_appear: Optional[Callable[[], None]] = None
        self._on_disappear: Optional[Callable[[], None]] = None
        self._on_quit: Optional[Callable[[], None]] = None
        self._quit_callback: Optional[Callable[[], None]] = None
        # Settings
        self._settings_page: Optional[SettingsPage] = None
        self._settings: Optional[Settings] = None
        # Notifications
        from ..notifications import NotificationManager
        self._notifications = NotificationManager()

    @property
    def notifications(self) -> "NotificationManager":
        """Access the notification manager.

        Returns:
            NotificationManager instance for pushing, scheduling, and managing notifications.

        Example:
            from nib import Notification

            notification = Notification(title="Hello", body="World")
            app.notifications.push(notification)
        """
        return self._notifications

    @property
    def fonts(self) -> Dict[str, str]:
        """
        Get the registered custom fonts.

        Returns:
            Dictionary mapping font names to their paths/URLs.
        """
        return self._fonts

    @fonts.setter
    def fonts(self, value: Dict[str, str]) -> None:
        """
        Register custom fonts for use in the app.

        Fonts can be loaded from:
        - Local file paths (absolute): "/Users/me/fonts/MyFont.ttf"
        - URLs: "https://example.com/fonts/MyFont.ttf"
        - System fonts are available by name without registration

        Note: Fonts in the assets directory (assets/fonts/) are automatically
        registered and don't need to be added here.

        Args:
            value: Dictionary mapping font names to paths or URLs.

        Example:
            app.fonts = {
                "CustomFont": "/path/to/CustomFont.ttf",
                "WebFont": "https://example.com/fonts/WebFont.otf",
            }

            # Then use in views:
            nib.Text("Hello", font=nib.Font.custom("CustomFont", size=16))
        """
        self._fonts = value

    @classmethod
    def _detect_fonts_in_assets(cls) -> Dict[str, str]:
        """Auto-detect font files in the assets directory.

        Scans the assets directory for font files (.ttf, .otf, .ttc, .woff, .woff2)
        and returns a dictionary mapping font names to absolute paths.

        The font name is derived from the filename without extension.
        For example, "Geist-Regular.ttf" becomes "Geist-Regular".

        Returns:
            Dictionary mapping font names to absolute file paths.
        """
        # Initialize assets dir if not done
        if not cls._assets_dir_initialized:
            cls._assets_dir = cls._auto_detect_assets_dir()
            cls._assets_dir_initialized = True

        if not cls._assets_dir or not cls._assets_dir.exists():
            return {}

        font_extensions = {".ttf", ".otf", ".ttc", ".woff", ".woff2"}
        fonts = {}

        for font_file in cls._assets_dir.rglob("*"):
            if font_file.is_file() and font_file.suffix.lower() in font_extensions:
                # Use filename without extension as font name
                font_name = font_file.stem
                fonts[font_name] = str(font_file)

        if fonts:
            logger.info(f"Auto-detected {len(fonts)} font(s) in assets")

        return fonts

    def _get_all_fonts(self) -> Optional[Dict[str, str]]:
        """Get all fonts (auto-detected + user-specified).

        Auto-detected fonts from assets are merged with user-specified fonts.
        User-specified fonts take precedence in case of name conflicts.

        Returns:
            Combined fonts dictionary, or None if no fonts.
        """
        # Start with auto-detected fonts
        all_fonts = self._detect_fonts_in_assets()

        # Merge user-specified fonts (they override auto-detected)
        # Resolve relative paths to absolute so Swift can find them
        if self._fonts:
            for name, source in self._fonts.items():
                if source.startswith(("/", "http://", "https://")):
                    all_fonts[name] = source
                else:
                    resolved = self.resolve_asset(source)
                    if resolved:
                        all_fonts[name] = resolved
                    else:
                        # Fallback: resolve relative to script directory
                        main_module = sys.modules.get("__main__")
                        if main_module and hasattr(main_module, "__file__") and main_module.__file__:
                            script_path = Path(main_module.__file__).parent / source
                            if script_path.exists():
                                all_fonts[name] = str(script_path.resolve())
                                continue
                        all_fonts[name] = source

        return all_fonts if all_fonts else None

    @property
    def on_appear(self) -> Optional[Callable[[], None]]:
        """Get the on_appear callback."""
        return self._on_appear

    @on_appear.setter
    def on_appear(self, callback: Callable[[], None]) -> None:
        """
        Set a callback to be called when the popover appears.

        The callback is fired every time the user clicks on the menu bar
        icon and the popover opens.

        Args:
            callback: A function with no arguments to call on appear.

        Example:
            def on_open():
                print("Popover opened!")
                # Refresh data, update UI, etc.

            app.on_appear = on_open
        """
        self._on_appear = callback

    @property
    def on_disappear(self) -> Optional[Callable[[], None]]:
        """Get the on_disappear callback."""
        return self._on_disappear

    @on_disappear.setter
    def on_disappear(self, callback: Callable[[], None]) -> None:
        """
        Set a callback to be called when the popover disappears.

        The callback is fired every time the popover closes (user clicks
        outside, presses escape, or clicks the menu bar icon again).

        Args:
            callback: A function with no arguments to call on disappear.

        Example:
            def on_close():
                print("Popover closed!")
                # Save state, pause updates, etc.

            app.on_disappear = on_close
        """
        self._on_disappear = callback

    @property
    def on_quit(self) -> Optional[Callable[[], None]]:
        """Get the on_quit callback."""
        return self._on_quit

    @on_quit.setter
    def on_quit(self, callback: Callable[[], None]) -> None:
        """
        Set a callback to be called when the app is quitting.

        The callback is fired once when the app is shutting down,
        before cleanup. Use this for saving state, closing connections, etc.

        Args:
            callback: A function with no arguments to call on quit.

        Example:
            def cleanup():
                print("App quitting!")
                save_settings()
                close_database()

            app.on_quit = cleanup
        """
        self._on_quit = callback

    # --- Settings ---

    @property
    def settings(self) -> Optional[SettingsPage]:
        """Get the settings page configuration."""
        return self._settings_page

    @settings.setter
    def settings(self, value: SettingsPage) -> None:
        """
        Set the settings page for the application.

        When a settings page is set, it becomes accessible via:
        - Cmd+, keyboard shortcut (standard macOS)
        - App menu -> Settings item (if menu is configured)

        Args:
            value: A SettingsPage instance defining the preferences UI.

        Example:
            app.settings = nib.SettingsPage(
                tabs=[
                    nib.SettingsTab(
                        "General",
                        icon="gear",
                        content=nib.VStack([
                            nib.Toggle("Dark Mode", is_on=False),
                        ])
                    ),
                ]
            )
        """
        self._settings_page = value
        if value:
            value._app = self
        if self._connection and value:
            self._send_settings_render()

    def register_settings(self, settings: Settings) -> None:
        """
        Register a Settings object for persistence.

        The Settings object provides sync cache + async persist behavior,
        allowing instant reads and background writes to UserDefaults.

        Args:
            settings: A Settings instance with defined defaults.

        Example:
            settings = nib.Settings({
                "dark_mode": False,
                "font_size": 14,
            })
            app.register_settings(settings)

            # Now settings.dark_mode reads instantly from cache
            # and settings.dark_mode = True persists in background
        """
        self._settings = settings
        if self._connection:
            settings._set_connection(self._connection)
            # Wait for settings to load from UserDefaults before returning
            # This ensures persisted values are available when user code reads settings
            settings.wait_for_load(timeout=2.0)

    def open_settings(self) -> None:
        """Open the settings window.

        Prefer using app.settings.open() instead.

        Example:
            nib.Button("Preferences", action=app.settings.open)
        """
        if self._settings_page:
            self._settings_page.open()

    def close_settings(self) -> None:
        """Close the settings window.

        Prefer using app.settings.close() instead.

        Example:
            nib.Button("Done", action=app.settings.close)
        """
        if self._settings_page:
            self._settings_page.close()

    def _send_settings_render(self) -> None:
        """Send settings page configuration to Swift runtime."""
        if self._settings_page and self._connection:
            self._connection.send_settings_render(self._settings_page._to_dict())

    # --- Service Properties ---

    @property
    def battery(self) -> "Battery":
        """Access the battery service.

        Example:
            status = app.battery.get_status()
            print(f"Battery: {status.level}%")
        """
        if not hasattr(self, "_battery"):
            from ..services.battery import Battery
            self._battery = Battery(self)
        return self._battery

    @property
    def connectivity(self) -> "Connectivity":
        """Access the connectivity service.

        Example:
            status = app.connectivity.get_status()
            print(f"Connected: {status.is_connected}")
        """
        if not hasattr(self, "_connectivity"):
            from ..services.connectivity import Connectivity
            self._connectivity = Connectivity(self)
        return self._connectivity

    @property
    def screen(self) -> "Screen":
        """Access the screen service.

        Example:
            info = app.screen.get_info()
            app.screen.set_brightness(0.5)
        """
        if not hasattr(self, "_screen"):
            from ..services.screen import Screen
            self._screen = Screen(self)
        return self._screen

    @property
    def keychain(self) -> "Keychain":
        """Access the keychain service for secure storage.

        Example:
            app.keychain.set("MyApp", "user", "password123")
            pwd = app.keychain.get("MyApp", "user")
        """
        if not hasattr(self, "_keychain"):
            from ..services.keychain import Keychain
            self._keychain = Keychain(self)
        return self._keychain

    @property
    def camera(self) -> "Camera":
        """Access the camera service.

        Example:
            devices = app.camera.list_devices()
            frame = app.camera.capture_photo()
            frame.save("/tmp/photo.jpg")
        """
        if not hasattr(self, "_camera"):
            from ..services.camera import Camera
            self._camera = Camera(self)
        return self._camera

    @property
    def launch_at_login(self) -> "LaunchAtLogin":
        """Access the launch at login service.

        Per Mac App Store guidelines, launch at login should only be
        enabled in response to a user action.

        Example:
            # Check if enabled
            if app.launch_at_login.is_enabled:
                print("App launches at login")

            # Toggle in response to user action
            def toggle_login():
                app.launch_at_login.set(not app.launch_at_login.is_enabled)

            nib.Button("Toggle Login", action=toggle_login)
        """
        if not hasattr(self, "_launch_at_login"):
            from ..services.launch_at_login import LaunchAtLogin
            self._launch_at_login = LaunchAtLogin(self)
        return self._launch_at_login

    @property
    def permissions(self) -> "Permissions":
        """Access the permissions service.

        Provides a unified API to check and request Camera, Microphone,
        and Notification permissions.

        Example:
            status = app.permissions.check(nib.Permission.CAMERA)
            if status == nib.PermissionStatus.NOT_DETERMINED:
                granted = app.permissions.request(nib.Permission.CAMERA)
        """
        if not hasattr(self, "_permissions"):
            from ..services.permissions import Permissions
            self._permissions = Permissions(self)
        return self._permissions

    @property
    def title(self) -> Optional[str]:
        """Get the app title."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Set the app title."""
        self._title = value

    @property
    def icon(self) -> Optional[Union[str, "SFSymbol"]]:
        """Get the app icon."""
        return self._icon

    @icon.setter
    def icon(self, value: Union[str, "SFSymbol", View]) -> None:
        """Set the app icon (SF Symbol name, SFSymbol instance, or View)."""
        self._icon = value
        # Set app reference on icon if it's a View
        if hasattr(value, "_set_app"):
            value._set_app(self)

    @property
    def identifier(self) -> str:
        """Get the app bundle identifier (used for UserDefaults storage).

        If not explicitly set, defaults to 'com.nib.<normalized_title>'.
        """
        if self._identifier:
            return self._identifier
        # Derive from title
        if self._title:
            normalized = self._title.lower().replace(" ", "-").replace("_", "-")
            return f"com.nib.{normalized}"
        return "com.nib.app"

    @identifier.setter
    def identifier(self, value: str) -> None:
        """Set the app bundle identifier."""
        self._identifier = value

    def _serialize_icon(self) -> Optional[Union[str, dict]]:
        """Serialize app icon to string or config dict for Swift."""
        if self._icon is None:
            return None
        if isinstance(self._icon, str):
            return self._icon
        # SFSymbol instance - serialize configuration
        if isinstance(self._icon, SFSymbol):
            config = {"name": self._icon.name}
            if self._icon._weight:
                config["weight"] = self._icon._weight
            if self._icon._scale:
                config["scale"] = self._icon._scale
            if self._icon._rendering_mode:
                config["renderingMode"] = resolve_enum(self._icon._rendering_mode)
            if self._icon._foreground_color:
                from ..types import Color, resolve_color
                color = self._icon._foreground_color
                if isinstance(color, Color):
                    config["color"] = resolve_color(color)
                else:
                    config["color"] = color
            return config
        # View instance - serialize as view tree
        if hasattr(self._icon, "to_dict"):
            return {"view": self._icon.to_dict()}
        return None

    @property
    def show_quit_item(self) -> bool:
        """Get whether the quit item is shown."""
        return self._show_quit_item

    @show_quit_item.setter
    def show_quit_item(self, value: bool) -> None:
        """Set whether to show a quit item at the bottom of the app."""
        self._show_quit_item = value

    @property
    def width(self) -> Optional[float]:
        """Get the app window width."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        """Set the app window width."""
        self._width = value

    @property
    def height(self) -> Optional[float]:
        """Get the app window height."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        """Set the app window height."""
        self._height = value

    @property
    def menu(self) -> List["MenuItem"]:
        """Get the right-click menu items."""
        return self._menu

    @menu.setter
    def menu(self, items: List["MenuItem"]) -> None:
        """Set the right-click menu items."""
        self._menu = items
        # Build action map for menu items (recursively)
        self._menu_action_map.clear()
        self._register_menu_actions(items)

    def _register_menu_actions(self, items: List["MenuItem"]) -> None:
        """Recursively register actions from menu items and their submenus."""
        for item in items:
            if isinstance(item, MenuItem):
                if item.action:
                    self._menu_action_map[item._id] = item.action
                if item.menu:
                    self._register_menu_actions(item.menu)

    @property
    def clipboard(self) -> str:
        """
        Get clipboard content (blocking).
        Note: For async usage, use get_clipboard() with a callback.
        """
        # For simple sync access, we can't easily block for response
        # So this returns empty - use get_clipboard() instead
        return ""

    @clipboard.setter
    def clipboard(self, value: str) -> None:
        """Set clipboard content."""
        if self._connection:
            self._connection.send_clipboard_write(value)

    def get_clipboard(self, callback: Callable[[str], None]) -> None:
        """
        Get clipboard content asynchronously.

        Args:
            callback: Function called with the clipboard content.
        """
        if self._connection:
            request_id = str(uuid.uuid4())
            self._clipboard_callbacks[request_id] = callback
            self._connection.send_clipboard_read(request_id)

    def set_clipboard(self, content: str) -> None:
        """Set clipboard content."""
        self.clipboard = content

    def on_hotkey(self, shortcut: str, callback: Callable[[], None]) -> None:
        """
        Register a global keyboard shortcut.

        Args:
            shortcut: Key combination like "cmd+shift+n", "cmd+k"
            callback: Function to call when hotkey is pressed.

        Example:
            app.on_hotkey("cmd+shift+n", show_window)
        """
        self._hotkey_map[shortcut.lower()] = callback

    def hotkey(self, shortcut: str) -> Callable:
        """
        Decorator to register a global keyboard shortcut.

        Example:
            @app.hotkey("cmd+shift+n")
            def show_window():
                pass
        """
        def decorator(func: Callable[[], None]) -> Callable[[], None]:
            self.on_hotkey(shortcut, func)
            return func
        return decorator

    def quit(self) -> None:
        """Quit the application."""
        self._running = False
        if self._quit_callback:
            self._quit_callback()

    def notify(
        self,
        title: str,
        body: Optional[str] = None,
        subtitle: Optional[str] = None,
        sound: bool = True,
        identifier: Optional[str] = None,
    ) -> None:
        """
        Send a macOS system notification.

        Args:
            title: The notification title (required).
            body: The notification body text.
            subtitle: A subtitle shown below the title.
            sound: Whether to play the default notification sound (default: True).
            identifier: A unique identifier for this notification. Can be used to
                       update or remove the notification later.

        Example:
            app.notify("Download Complete", "Your file has been saved")

            app.notify(
                title="New Message",
                body="You have a new message from John",
                subtitle="Messages",
                sound=True,
            )
        """
        if self._connection:
            self._connection.send_notify(
                title=title,
                body=body,
                subtitle=subtitle,
                sound=sound,
                identifier=identifier,
            )

    def update(self) -> None:
        """
        Manually trigger a UI re-render.

        Use this to force an update when you've made changes that the
        automatic reactivity system might not detect, or when you want
        to batch multiple changes and update once.

        Example:
            # Batch multiple changes
            label1.content = "New text 1"
            label2.content = "New text 2"
            app.update()  # Single re-render for both changes
        """
        self._trigger_rerender()

    def _send_action(
        self,
        node_id: str,
        action: str,
        params: Optional[dict] = None,
    ) -> None:
        """Send an action to a specific view node.

        Used internally by views like WebView to trigger actions
        (reload, goBack, goForward, evaluateJS, etc.).

        Args:
            node_id: The ID of the target view node.
            action: The action to perform.
            params: Optional parameters for the action.
        """
        if self._connection:
            self._connection.send_action(node_id, action, params)

    def build(self, view: View) -> None:
        """
        Set the root view of the app and trigger a rerender if running.

        Args:
            view: The root view to display.
        """
        self._root_view = view
        # Set app reference on all views for reactive updates
        view._set_app(self)
        # Also set app reference on icon if it's a View
        if hasattr(self._icon, "_set_app"):
            self._icon._set_app(self)
        # Trigger rerender if app is already running
        if self._running:
            self._trigger_rerender()

    def body(self) -> View:
        """
        Define the UI of your app. Override this method in subclass,
        or use build() in function-based style.

        Returns:
            The root view of your application.
        """
        if self._root_view is not None:
            root = self._root_view
        else:
            raise NotImplementedError("Use build() or override body()")

        # Wrap with quit item if enabled
        if self._show_quit_item:
            root = self._wrap_with_quit_item(root)

        return root

    def _wrap_with_quit_item(self, content: View) -> View:
        """Wrap the content with a quit item footer."""
        from ..views import VStack, Divider, Button, HStack, Text

        return VStack(
            controls=[
                content,
                Divider(),
                Button(
                    content=HStack(
                        controls=[
                            SFSymbol("power", foreground_color="#FF6B6B"),
                            Text("Quit"),
                        ],
                        spacing=6,
                    ),
                    action=self.quit,
                ),
            ],
            spacing=8,
        )

    def run(self) -> None:
        """Run the application."""
        try:
            self._setup()
            self._running = True
            self._start_render_loop()
            self._render()  # Initial render
            self._main_loop()
        except KeyboardInterrupt:
            pass
        finally:
            self._teardown()

    def _trigger_rerender(self) -> None:
        """Trigger a re-render of the UI."""
        if not self._running or not self._connection:
            return
        self._render_requested.set()

    def _start_render_loop(self) -> None:
        """Start the background render loop (single thread, event-based)."""
        def render_loop():
            min_interval = 0.002  # ~500fps max
            while self._running:
                # Wait for a render request (with timeout to check _running)
                if not self._render_requested.wait(timeout=0.1):
                    continue

                # Clear and render (coalesces rapid requests)
                self._render_requested.clear()
                if self._running and self._connection:
                    self._render()

                # Throttle to prevent CPU spinning
                time.sleep(min_interval)

        self._render_thread = threading.Thread(target=render_loop, daemon=True)
        self._render_thread.start()

    def _setup(self) -> None:
        """Set up the application."""
        # Check if we're launched by Swift (bundled mode)
        # In bundled mode, Swift passes NIB_SOCKET env var
        socket_from_env = os.environ.get("NIB_SOCKET")

        if socket_from_env:
            # Bundled mode: Swift launched us, socket already exists
            self._socket_path = socket_from_env
            self._runtime_process = None  # We don't own the runtime process
            logger.info(f"Running in bundled mode", socket=self._socket_path)
        else:
            # Development mode: We launch Swift runtime
            self._socket_path = f"/tmp/nib-{os.getpid()}.sock"

            # Find and launch the Swift runtime
            runtime_path = self._find_runtime()
            if not runtime_path:
                raise RuntimeError(
                    "Could not find nib-runtime. "
                    "Please build the Swift runtime first:\n"
                    "  cd swift && swift build -c release"
                )

            # Launch runtime with socket path and bundle ID
            env = os.environ.copy()
            env["NIB_SOCKET"] = self._socket_path
            env["NIB_BUNDLE_ID"] = self.identifier  # For UserDefaults storage

            self._runtime_process = subprocess.Popen(
                [str(runtime_path)],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        # Connect to runtime
        self._connection = Connection(self._socket_path)
        if not self._connection.connect():
            raise RuntimeError("Failed to connect to nib-runtime")

        # Set up event handler
        self._connection.set_event_handler(self._handle_event)

        # Set up notification manager
        self._notifications._set_connection(self._connection)
        self._connection.set_notification_manager(self._notifications)

        # Register settings if already set
        if self._settings:
            self._settings._set_connection(self._connection)
            # Wait for settings to load from UserDefaults
            self._settings.wait_for_load(timeout=2.0)

        # Handle signals
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _find_runtime(self) -> Optional[Path]:
        """Find the nib-runtime executable.

        Searches in the following order:
        1. NIB_RUNTIME environment variable
        2. Bundled binary in package (pip install)
        3. System PATH
        4. Common installation locations
        5. Relative to nib package (for development)
        6. Relative to current working directory
        """
        import shutil

        # 1. Check environment variable first
        env_runtime = os.environ.get("NIB_RUNTIME")
        if env_runtime:
            path = Path(env_runtime)
            if path.exists() and path.is_file():
                return path

        # 2. Check bundled binary in package (installed via pip)
        bundled_runtime = Path(__file__).resolve().parent.parent / "bin" / "nib-runtime"
        if bundled_runtime.exists() and bundled_runtime.is_file():
            return bundled_runtime

        # 3. Check PATH (most portable)
        path_runtime = shutil.which("nib-runtime")
        if path_runtime:
            return Path(path_runtime)

        # 4. Check common installation locations
        common_locations = [
            Path.home() / ".local" / "bin" / "nib-runtime",
            Path.home() / ".nib" / "bin" / "nib-runtime",
            Path("/usr/local/bin/nib-runtime"),
            Path("/opt/homebrew/bin/nib-runtime"),
        ]

        for path in common_locations:
            if path.exists() and path.is_file():
                return path

        # 5. Check relative to nib package (editable install during development)
        try:
            current = Path(__file__).resolve().parent
            for _ in range(6):
                package_build = current / "package" / ".build"
                if package_build.exists():
                    for build_type in ["release", "debug"]:
                        runtime = package_build / build_type / "nib-runtime"
                        if runtime.exists() and runtime.is_file():
                            return runtime
                current = current.parent
        except Exception:
            pass

        # 6. Check relative to current working directory
        cwd_locations = [
            Path.cwd() / "package" / ".build" / "release" / "nib-runtime",
            Path.cwd() / "package" / ".build" / "debug" / "nib-runtime",
        ]

        for path in cwd_locations:
            if path.exists() and path.is_file():
                return path

        return None

    def _render(self) -> None:
        """Render the current UI state."""
        if not self._connection:
            return

        # Use lock to prevent concurrent renders (race between main thread and render loop)
        with self._render_lock:
            self._render_internal()

    def _render_internal(self) -> None:
        """Internal render implementation (must be called with _render_lock held)."""
        # Clear action maps
        self._action_map.clear()
        self._change_map.clear()
        self._view_event_map.clear()
        self._submit_map.clear()
        self._drop_map.clear()
        self._pan_start_map.clear()
        self._pan_update_map.clear()
        self._pan_end_map.clear()
        self._hover_map.clear()
        self._click_map.clear()

        # Build view tree
        root = self.body()

        # Collect actions (also assigns IDs)
        self._collect_actions(root)

        # Collect actions from icon view if it's a View
        if hasattr(self._icon, "to_dict"):
            self._collect_actions(self._icon, "_icon")

        # Collect actions from settings page views (must do on every render
        # since action maps are cleared)
        if self._settings_page:
            for i, tab in enumerate(self._settings_page.tabs):
                if tab.content:
                    self._collect_actions(tab.content, f"settings.{i}")

        # Serialize as flat list (iterative, prevents Swift stack overflow)
        nodes, root_id = root.to_flat_list()

        # Debug output
        if self._previous_tree is None:
            logger.info(f"Initial render (root_type={root._type})")

        # Build menu config
        menu_config = None
        if self._menu:
            menu_config = [item.to_dict() for item in self._menu]

        # Get hotkey list
        hotkeys = list(self._hotkey_map.keys()) if self._hotkey_map else None

        # Send flat render (decoded iteratively on Swift side)
        self._connection.send_flat_render(
            nodes=nodes,
            root_id=root_id,
            icon=self._serialize_icon(),
            title=self._title,
            width=self._width,
            height=self._height,
            menu=menu_config,
            hotkeys=hotkeys,
            fonts=self._get_all_fonts(),
        )

        # Send settings page if configured (only on first render)
        is_full_render = self._previous_tree is None

        # Mark that we've done the first render
        self._previous_tree = True

        # Send settings on first render
        if is_full_render and self._settings_page:
            self._send_settings_render()

    def _collect_actions(self, view: View, path: str = "0") -> None:
        """Recursively collect actions and change handlers from the view tree.

        Also assigns position-based IDs to views for stable identity.
        """
        # Assign position-based ID
        view._id = path

        # Collect tap actions
        if hasattr(view, "_action") and view._action is not None:
            self._action_map[view._id] = view._action

        # Collect change handlers (TextField, Toggle, Slider, Picker)
        if hasattr(view, "_on_change") and view._on_change is not None:
            self._change_map[view._id] = view._on_change

        # Store view._handle_event for views that need internal event routing
        # (e.g. TextEditor syncs _text before calling _on_change,
        #  Table routes selection/sort events)
        if hasattr(view, "_handle_event") and callable(view._handle_event):
            self._view_event_map[view._id] = view._handle_event

        # Collect submit handlers (TextField, SecureField)
        if hasattr(view, "_on_submit") and view._on_submit is not None:
            self._submit_map[view._id] = view._on_submit

        # Collect drop handlers
        if hasattr(view, "_on_drop") and view._on_drop is not None:
            self._drop_map[view._id] = view._on_drop

        # Collect canvas pan/hover handlers
        if hasattr(view, "_on_pan_start") and view._on_pan_start is not None:
            self._pan_start_map[view._id] = view._on_pan_start
        if hasattr(view, "_on_pan_update") and view._on_pan_update is not None:
            self._pan_update_map[view._id] = view._on_pan_update
        if hasattr(view, "_on_pan_end") and view._on_pan_end is not None:
            self._pan_end_map[view._id] = view._on_pan_end
        if hasattr(view, "_on_hover") and view._on_hover is not None:
            self._hover_map[view._id] = view._on_hover
        if hasattr(view, "_on_click") and view._on_click is not None:
            self._click_map[view._id] = view._on_click

        # Recurse into children with indexed paths
        if hasattr(view, "_children") and view._children:
            for i, child in enumerate(view._children):
                self._collect_actions(child, f"{path}.{i}")

        # Handle single-child content (Button, Toggle, Link) - only if it's a View
        if hasattr(view, "_content") and view._content is not None:
            if isinstance(view._content, View):
                self._collect_actions(view._content, f"{path}.0")

        # Handle Label's special children
        if hasattr(view, "_title_view") and view._title_view is not None:
            self._collect_actions(view._title_view, f"{path}.title")
        if hasattr(view, "_icon_view") and view._icon_view is not None:
            self._collect_actions(view._icon_view, f"{path}.icon")

        # Handle NavigationLink destination
        if hasattr(view, "_destination") and view._destination:
            for i, child in enumerate(view._destination):
                if isinstance(child, View):
                    self._collect_actions(child, f"{path}.{i}")

        # Handle context menu views
        if hasattr(view, "_context_menu_views") and view._context_menu_views:
            for i, child in enumerate(view._context_menu_views):
                self._collect_actions(child, f"{path}.ctx.{i}")

    def _handle_event(self, node_id: str, event: str) -> None:
        """Handle an event from the Swift runtime."""
        # Handle app lifecycle events
        if node_id == "_app":
            if event == "appear":
                if self._on_appear:
                    try:
                        self._on_appear()
                    except Exception as e:
                        logger.error("Error in on_appear handler", exc=e)
                return
            elif event == "disappear":
                if self._on_disappear:
                    try:
                        self._on_disappear()
                    except Exception as e:
                        logger.error("Error in on_disappear handler", exc=e)
                return

        # Handle tap events
        if event == "tap" and node_id in self._action_map:
            action = self._action_map[node_id]
            try:
                action()
            except Exception as e:
                logger.error("Error in action handler", exc=e, node_id=node_id)

        # Handle menu tap events
        elif event == "menu:tap":
            logger.info("menu:tap received", node_id=node_id, registered_ids=list(self._menu_action_map.keys()))
            if node_id in self._menu_action_map:
                logger.info("Found menu action, calling it")
                action = self._menu_action_map[node_id]
                try:
                    action()
                    logger.info("Menu action completed")
                except Exception as e:
                    logger.error("Error in menu action handler", exc=e)
            else:
                logger.warn("Menu action not found", node_id=node_id)

        # Handle hotkey events
        elif event.startswith("hotkey:"):
            shortcut = event[7:]  # Remove "hotkey:" prefix
            if shortcut in self._hotkey_map:
                try:
                    self._hotkey_map[shortcut]()
                except Exception as e:
                    logger.error("Error in hotkey handler", exc=e, shortcut=shortcut)

        # Handle clipboard read response
        elif event.startswith("clipboard:"):
            content = event[10:]  # Remove "clipboard:" prefix
            if node_id in self._clipboard_callbacks:
                callback = self._clipboard_callbacks.pop(node_id)
                try:
                    callback(content)
                except Exception as e:
                    logger.error("Error in clipboard callback", exc=e)

        # Handle userDefaults response
        elif event.startswith("userDefaults:"):
            # Parse the response: "userDefaults:action:value"
            parts = event.split(":", 2)  # Split into at most 3 parts
            if len(parts) >= 3:
                response_action = parts[1]
                response_value = parts[2]
                from .user_defaults import _handle_user_defaults_response
                _handle_user_defaults_response(node_id, response_action, response_value)

        # Handle drop events
        elif event.startswith("drop:") and node_id in self._drop_map:
            paths_str = event[5:]  # Remove "drop:" prefix
            paths = [p for p in paths_str.split("\n") if p] if paths_str else []
            handler = self._drop_map[node_id]
            try:
                handler(paths)
            except Exception as e:
                logger.error("Error in drop handler", exc=e)

        # Handle canvas pan events
        elif event.startswith("pan:"):
            self._handle_pan_event(node_id, event)

        # Handle hover events (both canvas x,y and general true/false)
        elif event.startswith("hover:") and node_id in self._hover_map:
            value = event[6:]  # Remove "hover:" prefix
            try:
                # Check if it's a boolean (general hover) or coordinates (canvas hover)
                if value in ("true", "false"):
                    # General hover: callback receives bool
                    self._hover_map[node_id](value == "true")
                else:
                    # Canvas hover: callback receives PanEvent with coordinates
                    x, y = map(float, value.split(","))
                    from ..views.canvas import PanEvent
                    self._hover_map[node_id](PanEvent(x=x, y=y))
            except Exception as e:
                logger.error("Error in hover handler", exc=e, node_id=node_id)

        # Handle click events
        elif event == "click" and node_id in self._click_map:
            try:
                self._click_map[node_id]()
            except Exception as e:
                logger.error("Error in click handler", exc=e, node_id=node_id)

        # Handle change events (change:value)
        elif event.startswith("change:") and node_id in self._change_map:
            # If the view has _handle_event, delegate to it so internal state
            # (e.g. TextEditor._text) is synced. _handle_event calls _on_change
            # internally, so we skip the normal parsing flow.
            if node_id in self._view_event_map:
                try:
                    self._view_event_map[node_id](event)
                except Exception as e:
                    logger.error("Error in view event handler", exc=e, node_id=node_id)
            else:
                value_str = event[7:]  # Remove "change:" prefix
                handler = self._change_map[node_id]
                try:
                    # Try to parse as appropriate type
                    if value_str.lower() in ("true", "false"):
                        value = value_str.lower() == "true"
                    else:
                        try:
                            value = float(value_str)
                            # Keep as int if it's a whole number
                            if value.is_integer():
                                value = int(value)
                        except ValueError:
                            value = value_str
                    handler(value)
                except Exception as e:
                    logger.error("Error in change handler", exc=e, node_id=node_id)

        # Handle submit events (submit:value) - TextField, SecureField
        elif event.startswith("submit:") and node_id in self._submit_map:
            value_str = event[7:]  # Remove "submit:" prefix
            handler = self._submit_map[node_id]
            try:
                handler(value_str)
            except Exception as e:
                logger.error("Error in submit handler", exc=e, node_id=node_id)

        # Fallback: delegate to view's _handle_event for custom event types
        # (e.g. Table selection/sort/doubleClick events)
        elif node_id in self._view_event_map:
            try:
                self._view_event_map[node_id](event)
            except Exception as e:
                logger.error("Error in view event handler", exc=e, node_id=node_id)

    def _handle_pan_event(self, node_id: str, event: str) -> None:
        """Handle canvas pan events (pan:start, pan:update, pan:end)."""
        # Parse event: "pan:type:x,y"
        parts = event.split(":", 2)
        if len(parts) < 3:
            return

        event_type = parts[1]  # start, update, or end
        coords = parts[2]

        try:
            x, y = map(float, coords.split(","))
            from ..views.canvas import PanEvent
            pan_event = PanEvent(x=x, y=y)

            if event_type == "start" and node_id in self._pan_start_map:
                self._pan_start_map[node_id](pan_event)
            elif event_type == "update" and node_id in self._pan_update_map:
                self._pan_update_map[node_id](pan_event)
            elif event_type == "end" and node_id in self._pan_end_map:
                self._pan_end_map[node_id](pan_event)
        except Exception as e:
            logger.error("Error in pan handler", exc=e, node_id=node_id, event=event)

    def _main_loop(self) -> None:
        """Main event loop."""
        while self._running:
            try:
                time.sleep(0.1)
                # Check if runtime is still running
                if self._runtime_process and self._runtime_process.poll() is not None:
                    self._running = False
            except KeyboardInterrupt:
                break

    def _signal_handler(self, signum, frame) -> None:
        """Handle termination signals."""
        self._running = False

    def _teardown(self) -> None:
        """Clean up resources."""
        # Call on_quit callback before cleanup
        if self._on_quit:
            try:
                self._on_quit()
            except Exception as e:
                logger.error("Error in on_quit handler", exc=e)

        self._running = False
        # Wake up render thread so it exits promptly
        self._render_requested.set()

        if self._connection:
            self._connection.send_quit()
            self._connection.disconnect()

        if self._runtime_process:
            self._runtime_process.terminate()
            try:
                self._runtime_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self._runtime_process.kill()

        # Clean up socket file
        if self._socket_path and os.path.exists(self._socket_path):
            try:
                os.unlink(self._socket_path)
            except Exception:
                pass


class SFSymbol(View):
    """
    A view that displays an SF Symbol (Apple system icon).

    Usage:
        app.icon = nib.SFSymbol("pencil.and.outline")

        nib.Button(content=nib.SFSymbol("star.fill"), action=on_click)

        nib.HStack(controls=[
            nib.SFSymbol("star", foreground_color=nib.Color.yellow),
            nib.Text("Favorites"),
        ])

        # With symbol configuration
        nib.SFSymbol(
            "heart.fill",
            weight="bold",
            scale="large",
            rendering_mode="hierarchical",
            foreground_color=nib.Color.red,
        )
    """

    _type = "Image"

    def __init__(
        self,
        name: str,
        # SF Symbol-specific styling
        weight: Optional[str] = None,
        scale: Optional[str] = None,
        rendering_mode: Optional[Union[SymbolRenderingMode, str]] = None,
        # View modifiers
        width: Optional[float] = None,
        height: Optional[float] = None,
        padding: Optional[Union[float, dict]] = None,
        foreground_color: Optional[str] = None,
        background: Optional[str] = None,
        opacity: Optional[float] = None,
        font: Optional[str] = None,
        font_weight: Optional[str] = None,
        **kwargs,
    ):
        """
        Create an SF Symbol view.

        Args:
            name: The SF Symbol name (e.g., "star.fill", "gear")
            weight: Symbol weight ("ultralight", "thin", "light", "regular",
                    "medium", "semibold", "bold", "heavy", "black")
            scale: Symbol scale ("small", "medium", "large")
            rendering_mode: Rendering mode (SymbolRenderingMode enum or string:
                           "monochrome", "hierarchical", "palette", "multicolor")
        """
        super().__init__(
            width=width,
            height=height,
            padding=padding,
            foreground_color=foreground_color,
            background=background,
            opacity=opacity,
            font=font,
            font_weight=font_weight,
            **kwargs,
        )
        self.name = name
        self._weight = weight
        self._scale = scale
        self._rendering_mode = rendering_mode
        self._foreground_color = foreground_color  # Store for menu icon serialization

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"SFSymbol({self.name!r})"

    def _get_props(self) -> dict:
        props = {"systemName": self.name}

        # Build symbol styles
        styles = {}
        if self._weight is not None:
            styles["symbolWeight"] = self._weight
        if self._scale is not None:
            styles["symbolScale"] = self._scale
        if self._rendering_mode is not None:
            styles["symbolRenderingMode"] = resolve_enum(self._rendering_mode)

        if styles:
            props["imageStyles"] = styles

        return props


def _resolve_icon(icon: Optional[Union[str, SFSymbol]]) -> Optional[str]:
    """Resolve an icon to its string name."""
    if icon is None:
        return None
    if isinstance(icon, SFSymbol):
        return icon.name
    return icon


def run(main: Callable[[App], None], assets_dir: Optional[Union[str, Path]] = None) -> None:
    """
    Run a Nib application with a function-based entry point.

    This is the recommended way to create Nib apps:

        import nib

        def main(app: nib.App):
            app.title = "My App"
            app.icon = nib.SFSymbol("star.fill")

            counter = nib.TextField(value="0")

            def increment(e):
                counter.value = str(int(counter.value) + 1)

            app.build(
                nib.HStack(controls=[
                    counter,
                    nib.Button(content=nib.Text("+"), action=increment),
                ])
            )

        nib.run(main)

        # Or with custom assets directory:
        nib.run(main, assets_dir="my_assets")

    Args:
        main: A function that receives an App instance and configures it.
        assets_dir: Path to assets directory (default: auto-detect "assets" folder).
    """
    from .user_defaults import _set_current_app

    # Set assets directory before creating app
    if assets_dir is not None:
        App.set_assets_dir(assets_dir)

    app = App()
    _set_current_app(app)  # Set as current app for UserDefaults
    try:
        main(app)
        app.run()
    finally:
        _set_current_app(None)  # Clear on exit


class MenuItem:
    """
    A menu item for the right-click context menu.

    Supports nested submenus, keyboard shortcuts, badges, state indicators,
    and custom views for rich menu content.

    Args:
        title: The menu item text (optional if content is provided).
        action: Callback when item is clicked.
        icon: SF Symbol name (str) or SFSymbol view with configuration.
        content: Custom View for rich menu item content (replaces title/icon).
        menu: List of child MenuItems for submenus.
        shortcut: Keyboard shortcut (e.g., "cmd+q", "cmd+shift+n", "opt+x").
        state: Checkmark state - "on" (checkmark), "off" (none), or "mixed" (dash).
        badge: Badge text shown on the right (macOS 14+).
        enabled: Whether the item is clickable (default True).
        height: Custom height for content-based items (default: auto).

    Usage:
        app.menu = [
            # Simple text item
            nib.MenuItem("Settings", action=open_settings, icon="gear", shortcut="cmd+,"),

            # Custom view content
            nib.MenuItem(
                content=nib.HStack(
                    controls=[
                        nib.SFSymbol("star.fill", foreground_color=nib.Color.YELLOW),
                        nib.VStack(
                            controls=[
                                nib.Text("Premium", font=nib.Font.HEADLINE),
                                nib.Text("Upgrade now", font=nib.Font.CAPTION),
                            ],
                            alignment=nib.HorizontalAlignment.LEADING,
                            spacing=2,
                        ),
                    ],
                    spacing=8,
                ),
                action=upgrade,
                height=50,
            ),

            # Submenus
            nib.MenuItem(
                "More Options",
                icon="ellipsis.circle",
                menu=[
                    nib.MenuItem("Option A", action=option_a),
                    nib.MenuItem("Option B", action=option_b),
                ],
            ),
            nib.MenuDivider(),
            nib.MenuItem("Quit", action=app.quit, shortcut="cmd+q"),
        ]
    """

    def __init__(
        self,
        title: Optional[str] = None,
        action: Optional[Callable[[], None]] = None,
        icon: Optional[Union[str, "SFSymbol"]] = None,
        content: Optional[View] = None,
        menu: Optional[List["MenuItem"]] = None,
        shortcut: Optional[str] = None,
        state: Optional[str] = None,
        badge: Optional[str] = None,
        enabled: bool = True,
        height: Optional[float] = None,
    ):
        self._id = str(uuid.uuid4())
        self.title = title
        self.action = action
        self.icon = icon
        self.content = content
        self.menu = menu or []
        self.shortcut = shortcut
        self.state = state
        self.badge = badge
        self.enabled = enabled
        self.height = height

    def _serialize_icon(self) -> Optional[Union[str, dict]]:
        """Serialize icon to string or config dict."""
        if self.icon is None:
            return None
        if isinstance(self.icon, str):
            return self.icon
        # SFSymbol instance - serialize configuration
        if isinstance(self.icon, SFSymbol):
            config = {"name": self.icon.name}
            if self.icon._weight:
                config["weight"] = self.icon._weight
            if self.icon._scale:
                config["scale"] = self.icon._scale
            if self.icon._rendering_mode:
                config["renderingMode"] = resolve_enum(self.icon._rendering_mode)
            if self.icon._foreground_color:
                # Handle both Color objects and strings
                from ..types import Color, resolve_color
                color = self.icon._foreground_color
                if isinstance(color, Color):
                    config["color"] = resolve_color(color)
                else:
                    config["color"] = color
            return config
        return None

    def to_dict(self) -> dict:
        result = {
            "id": self._id,
            "title": self.title,
            "icon": self._serialize_icon(),
            "divider": False,
        }
        # Add custom content view if provided
        if self.content is not None:
            result["content"] = self.content.to_dict()
        if self.height is not None:
            result["height"] = float(self.height)
        if self.menu:
            result["children"] = [item.to_dict() for item in self.menu]
        if self.shortcut:
            result["shortcut"] = self.shortcut
        if self.state:
            result["state"] = self.state
        if self.badge:
            result["badge"] = self.badge
        if not self.enabled:
            result["enabled"] = False
        return result


class MenuDivider:
    """A separator line in the right-click context menu."""

    def __init__(self):
        self._id = str(uuid.uuid4())

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "divider": True,
        }
