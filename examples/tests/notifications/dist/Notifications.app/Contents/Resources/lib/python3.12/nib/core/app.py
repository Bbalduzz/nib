"""App class for Nib applications."""

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
from .diff import diff_trees
from ..views import View
from ..types import SymbolRenderingMode, resolve_enum


class App:
    """
    Base class for Nib applications.

    Usage (function-based - recommended):
        def main(app: nib.App):
            app.title = "My App"
            app.icon = nib.SFSymbol("star.fill")

            app.build(
                nib.VStack(controls=[
                    nib.Text("Hello, Nib!"),
                ])
            )

        nib.run(main)

    Usage (class-based):
        class MyApp(App):
            def body(self) -> View:
                return Text("Hello, Nib!")

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
            cls._assets_dir = Path(path)
        else:
            cls._assets_dir = None
        cls._assets_dir_initialized = True

    @classmethod
    def _auto_detect_assets_dir(cls) -> Optional[Path]:
        """Auto-detect the assets directory based on execution mode."""
        if getattr(sys, "frozen", False):
            # Bundled mode - assets are in Contents/Resources/assets
            bundle_dir = Path(sys.executable).parent.parent
            return bundle_dir / "Resources" / "assets"
        else:
            # Development mode - find assets relative to main script
            import __main__
            if hasattr(__main__, "__file__") and __main__.__file__:
                script_dir = Path(__main__.__file__).parent
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
            Resolved absolute path, or original path if not found in assets.
        """
        # Don't resolve absolute paths or URLs
        if relative_path.startswith("/") or relative_path.startswith(("http://", "https://")):
            return relative_path

        # Initialize assets dir if not done yet
        if not cls._assets_dir_initialized:
            cls._assets_dir = cls._auto_detect_assets_dir()
            cls._assets_dir_initialized = True

        # Resolve relative to assets dir
        if cls._assets_dir and cls._assets_dir.exists():
            asset_path = cls._assets_dir / relative_path
            if asset_path.exists():
                return str(asset_path)

        # Fallback: return as-is
        return relative_path

    def __init__(
        self,
        title: Optional[str] = None,
        icon: Optional[Union[str, "SFSymbol"]] = None,
    ):
        self._title = title
        self._icon: Optional[Union[str, "SFSymbol"]] = icon  # Keep full object for serialization
        self._root_view: Optional[View] = None
        self._show_quit_item = False
        self._width: Optional[float] = None
        self._height: Optional[float] = None
        self._connection: Optional[Connection] = None
        self._runtime_process: Optional[subprocess.Popen] = None
        self._socket_path: Optional[str] = None
        self._action_map: Dict[str, Callable] = {}
        self._change_map: Dict[str, Callable] = {}
        self._running = False
        self._previous_tree: Optional[dict] = None  # For diffing
        self._render_scheduled = False
        self._render_lock = None  # Will be threading.Lock()
        # Menu bar right-click menu
        self._menu: List["MenuItem"] = []
        self._menu_action_map: Dict[str, Callable] = {}
        # Hotkeys
        self._hotkey_map: Dict[str, Callable] = {}
        # File dialog callbacks
        self._file_dialog_callbacks: Dict[str, Callable] = {}
        # Clipboard read callbacks
        self._clipboard_callbacks: Dict[str, Callable] = {}
        # Drop handlers
        self._drop_map: Dict[str, Callable] = {}
        # Custom fonts
        self._fonts: Dict[str, str] = {}

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
    def icon(self, value: Union[str, "SFSymbol"]) -> None:
        """Set the app icon (SF Symbol name or SFSymbol instance)."""
        self._icon = value

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

    def open_file_dialog(
        self,
        callback: Callable[[List[str]], None],
        title: Optional[str] = None,
        types: Optional[List[str]] = None,
        multiple: bool = False,
        directory: Optional[str] = None,
    ) -> None:
        """
        Show an open file dialog.

        Args:
            callback: Called with list of selected file paths (empty if cancelled).
            title: Dialog title.
            types: Allowed file extensions (e.g., ["txt", "md"]).
            multiple: Allow selecting multiple files.
            directory: Starting directory.
        """
        if self._connection:
            request_id = str(uuid.uuid4())
            self._file_dialog_callbacks[request_id] = callback
            self._connection.send_file_dialog(
                action="open",
                request_id=request_id,
                title=title,
                types=types,
                multiple=multiple,
                directory=directory,
            )

    def save_file_dialog(
        self,
        callback: Callable[[str], None],
        title: Optional[str] = None,
        types: Optional[List[str]] = None,
        default_name: Optional[str] = None,
        directory: Optional[str] = None,
    ) -> None:
        """
        Show a save file dialog.

        Args:
            callback: Called with selected file path (empty if cancelled).
            title: Dialog title.
            types: Allowed file extensions.
            default_name: Default filename.
            directory: Starting directory.
        """
        if self._connection:
            request_id = str(uuid.uuid4())
            self._file_dialog_callbacks[request_id] = lambda paths: callback(paths[0] if paths else "")
            self._connection.send_file_dialog(
                action="save",
                request_id=request_id,
                title=title,
                types=types,
                directory=directory,
                default_name=default_name,
            )

    def quit(self) -> None:
        """Quit the application."""
        self._running = False

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

    def build(self, view: View) -> None:
        """
        Set the root view of the app and trigger a rerender if running.

        Args:
            view: The root view to display.
        """
        self._root_view = view
        # Set app reference on all views for reactive updates
        view._set_app(self)
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
            self._render()
            self._main_loop()
        except KeyboardInterrupt:
            pass
        finally:
            self._teardown()

    def _trigger_rerender(self) -> None:
        """Trigger a re-render of the UI (debounced to prevent CPU spikes)."""
        if not self._running or not self._connection:
            return

        # Initialize lock if needed
        if self._render_lock is None:
            self._render_lock = threading.Lock()

        with self._render_lock:
            if self._render_scheduled:
                return  # Already scheduled, skip
            self._render_scheduled = True

        # Schedule render after short delay to batch rapid updates
        def do_render():
            time.sleep(0.016)  # ~60fps max
            with self._render_lock:
                self._render_scheduled = False
            if self._running:
                self._render()

        threading.Thread(target=do_render, daemon=True).start()

    def _setup(self) -> None:
        """Set up the application."""
        # Generate socket path
        self._socket_path = f"/tmp/nib-{os.getpid()}.sock"

        # Find and launch the Swift runtime
        runtime_path = self._find_runtime()
        if not runtime_path:
            raise RuntimeError(
                "Could not find nib-runtime. "
                "Please build the Swift runtime first:\n"
                "  cd swift && swift build -c release"
            )

        # Launch runtime with socket path
        env = os.environ.copy()
        env["NIB_SOCKET"] = self._socket_path

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

        # Handle signals
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _find_runtime(self) -> Optional[Path]:
        """Find the nib-runtime executable."""
        import shutil

        # Check for bundled runtime (py2app bundle)
        # When running as a bundled app, sys.frozen is set to True
        if getattr(sys, "frozen", False):
            # Running inside a py2app bundle
            # sys.executable points to Contents/MacOS/<app>
            # nib-runtime is at Contents/Resources/nib-runtime
            bundle_dir = Path(sys.executable).parent.parent
            runtime = bundle_dir / "Resources" / "nib-runtime"
            if runtime.exists():
                return runtime

        # Check common locations
        # Path(__file__) = .../nib/python/nib/core/app.py
        # .parent.parent.parent.parent = .../nib
        nib_root = Path(__file__).parent.parent.parent.parent
        locations = [
            # Development: relative to this file
            nib_root / "swift" / ".build" / "release" / "nib-runtime",
            nib_root / "swift" / ".build" / "debug" / "nib-runtime",
            # Also check current working directory
            Path.cwd() / "swift" / ".build" / "release" / "nib-runtime",
            Path.cwd() / "swift" / ".build" / "debug" / "nib-runtime",
            # Installed in PATH
            Path("/usr/local/bin/nib-runtime"),
            # User local bin
            Path.home() / ".local" / "bin" / "nib-runtime",
        ]

        for path in locations:
            if path.exists() and path.is_file():
                return path

        # Check PATH
        path_runtime = shutil.which("nib-runtime")
        if path_runtime:
            return Path(path_runtime)

        return None

    def _render(self) -> None:
        """Render the current UI state."""
        if not self._connection:
            return

        # Clear action maps
        self._action_map.clear()
        self._change_map.clear()
        self._drop_map.clear()

        # Build view tree
        root = self.body()

        # Collect actions (also assigns IDs)
        self._collect_actions(root)

        # Serialize
        root_dict = root.to_dict()

        # Compute diff with previous tree
        patches = diff_trees(self._previous_tree, root_dict)

        # Debug output
        if self._previous_tree is None:
            print(f"[nib] Initial render with root type: {root_dict.get('type')}")
        else:
            print(f"[nib] Sending {len(patches)} patches:")
            for p in patches:
                print(f"  - {p['op']} @ {p['id']}: {p.get('props', p.get('node', {}).get('props', ''))}")

        # Send patches or full render
        # NOTE: Incremental patching disabled - Swift-side handling has bugs
        if self._previous_tree is None or len(patches) > 5 or True:  # Always full render
            # First render or too many changes - send full tree
            # Build menu config
            menu_config = None
            if self._menu:
                menu_config = [item.to_dict() for item in self._menu]

            # Get hotkey list
            hotkeys = list(self._hotkey_map.keys()) if self._hotkey_map else None

            self._connection.send_render(
                root=root_dict,
                icon=self._serialize_icon(),
                title=self._title,
                width=self._width,
                height=self._height,
                menu=menu_config,
                hotkeys=hotkeys,
                fonts=self._fonts if self._fonts else None,
            )
        else:
            # Send incremental patches
            self._connection.send_patch(
                patches=patches,
                icon=self._serialize_icon(),
                title=self._title,
                width=self._width,
                height=self._height,
            )

        # Store for next diff
        self._previous_tree = root_dict

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

        # Collect drop handlers
        if hasattr(view, "_on_drop") and view._on_drop is not None:
            self._drop_map[view._id] = view._on_drop

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

    def _handle_event(self, node_id: str, event: str) -> None:
        """Handle an event from the Swift runtime."""
        # Handle tap events
        if event == "tap" and node_id in self._action_map:
            action = self._action_map[node_id]
            try:
                action()
            except Exception as e:
                print(f"Error in action handler: {e}")

        # Handle menu tap events
        elif event == "menu:tap" and node_id in self._menu_action_map:
            action = self._menu_action_map[node_id]
            try:
                action()
            except Exception as e:
                print(f"Error in menu action handler: {e}")

        # Handle hotkey events
        elif event.startswith("hotkey:"):
            shortcut = event[7:]  # Remove "hotkey:" prefix
            if shortcut in self._hotkey_map:
                try:
                    self._hotkey_map[shortcut]()
                except Exception as e:
                    print(f"Error in hotkey handler: {e}")

        # Handle clipboard read response
        elif event.startswith("clipboard:"):
            content = event[10:]  # Remove "clipboard:" prefix
            if node_id in self._clipboard_callbacks:
                callback = self._clipboard_callbacks.pop(node_id)
                try:
                    callback(content)
                except Exception as e:
                    print(f"Error in clipboard callback: {e}")

        # Handle file dialog response
        elif event.startswith("fileDialog:"):
            paths_str = event[11:]  # Remove "fileDialog:" prefix
            if node_id in self._file_dialog_callbacks:
                callback = self._file_dialog_callbacks.pop(node_id)
                paths = [p for p in paths_str.split("\n") if p] if paths_str else []
                try:
                    callback(paths)
                except Exception as e:
                    print(f"Error in file dialog callback: {e}")

        # Handle drop events
        elif event.startswith("drop:") and node_id in self._drop_map:
            paths_str = event[5:]  # Remove "drop:" prefix
            paths = [p for p in paths_str.split("\n") if p] if paths_str else []
            handler = self._drop_map[node_id]
            try:
                handler(paths)
            except Exception as e:
                print(f"Error in drop handler: {e}")

        # Handle change events (change:value)
        elif event.startswith("change:") and node_id in self._change_map:
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
                print(f"Error in change handler: {e}")

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
        self._running = False

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
    # Set assets directory before creating app
    if assets_dir is not None:
        App.set_assets_dir(assets_dir)

    app = App()
    main(app)
    app.run()


class MenuItem:
    """
    A menu item for the right-click context menu.

    Supports nested submenus, keyboard shortcuts, badges, and state indicators.

    Args:
        title: The menu item text.
        action: Callback when item is clicked.
        icon: SF Symbol name (str) or SFSymbol view with configuration.
        menu: List of child MenuItems for submenus.
        shortcut: Keyboard shortcut (e.g., "cmd+q", "cmd+shift+n", "opt+x").
        state: Checkmark state - "on" (checkmark), "off" (none), or "mixed" (dash).
        badge: Badge text shown on the right (macOS 14+).
        enabled: Whether the item is clickable (default True).

    Usage:
        app.menu = [
            # Simple string icon
            nib.MenuItem("Settings", action=open_settings, icon="gear", shortcut="cmd+,"),

            # SFSymbol with configuration
            nib.MenuItem(
                "Favorites",
                action=show_favorites,
                icon=nib.SFSymbol("star.fill", weight="bold", foreground_color="#FFD700"),
            ),

            nib.MenuItem("Check for Updates", action=check_updates),
            nib.MenuItem("Dark Mode", action=toggle_dark, state="on"),
            nib.MenuItem("Downloads", badge="3"),
            nib.MenuItem(
                "More Options",
                icon="ellipsis.circle",
                menu=[
                    nib.MenuItem("Option A", action=option_a, shortcut="cmd+1"),
                    nib.MenuItem("Option B", action=option_b, shortcut="cmd+2"),
                ],
            ),
            nib.MenuDivider(),
            nib.MenuItem("Quit", action=app.quit, shortcut="cmd+q"),
        ]
    """

    def __init__(
        self,
        title: str,
        action: Optional[Callable[[], None]] = None,
        icon: Optional[Union[str, "SFSymbol"]] = None,
        menu: Optional[List["MenuItem"]] = None,
        shortcut: Optional[str] = None,
        state: Optional[str] = None,
        badge: Optional[str] = None,
        enabled: bool = True,
    ):
        self._id = str(uuid.uuid4())
        self.title = title
        self.action = action
        self.icon = icon
        self.menu = menu or []
        self.shortcut = shortcut
        self.state = state
        self.badge = badge
        self.enabled = enabled

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
