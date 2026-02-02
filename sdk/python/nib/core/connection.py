"""Connection layer for communicating with the Swift runtime.

This module provides the :class:`Connection` class that handles all
communication between Python and the Swift runtime over Unix sockets
using MessagePack serialization.

The communication protocol uses length-prefixed MessagePack messages:

- **Python → Swift messages**: ``render``, ``patch``, ``notify``, ``quit``,
  ``clipboard``, ``fileDialog``, ``userDefaults``
- **Swift → Python messages**: ``event`` (user interactions)

Note:
    This module is for internal use. Applications should use the high-level
    :class:`~nib.App` API instead of interacting with Connection directly.
"""

import socket
import struct
import threading
from typing import Callable, Optional, Any
import msgpack

from .logging import logger


class Connection:
    """Unix socket connection to the Swift runtime.

    Manages bidirectional communication with the nib-runtime Swift process
    using length-prefixed MessagePack messages over a Unix domain socket.

    Messages are sent with a 4-byte big-endian length prefix followed by
    the MessagePack-encoded payload. Events from Swift are received on
    a background thread and dispatched to a registered handler.

    Attributes:
        socket_path: Path to the Unix domain socket.

    Example:
        Internal usage by App::

            conn = Connection("/tmp/nib-12345.sock")
            if conn.connect():
                conn.set_event_handler(handle_event)
                conn.send_render(root=view_tree)
                # ... later ...
                conn.send_quit()
                conn.disconnect()
    """

    def __init__(self, socket_path: str) -> None:
        """Initialize a new Connection.

        Args:
            socket_path: Path to the Unix domain socket file.
        """
        self.socket_path = socket_path
        self._socket: Optional[socket.socket] = None
        self._connected = False
        self._read_thread: Optional[threading.Thread] = None
        self._on_event: Optional[Callable[[str, str], None]] = None
        self._send_lock = threading.Lock()

    def connect(self, retries: int = 10, delay: float = 0.2) -> bool:
        """Connect to the Swift runtime socket.

        Attempts to connect to the Unix socket with retries, as the Swift
        runtime may take time to start and create the socket.

        Args:
            retries: Maximum number of connection attempts.
            delay: Seconds to wait between retry attempts.

        Returns:
            True if connection succeeded, False otherwise.
        """
        import time

        for attempt in range(retries):
            try:
                self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self._socket.connect(self.socket_path)
                self._connected = True
                self._start_read_thread()
                return True
            except (FileNotFoundError, ConnectionRefusedError):
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    return False
        return False

    def disconnect(self) -> None:
        """Disconnect from the Swift runtime.

        Closes the socket connection and stops the read thread.
        Safe to call multiple times.
        """
        self._connected = False
        if self._socket:
            try:
                self._socket.close()
            except Exception:
                pass
            self._socket = None

    def send_render(
        self,
        root: Optional[dict],
        icon: Optional[str] = None,
        title: Optional[str] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
        menu: Optional[list] = None,
        hotkeys: Optional[list] = None,
        fonts: Optional[dict] = None,
    ) -> None:
        """Send a full render message to the Swift runtime.

        This sends the complete view tree and app configuration to Swift
        for rendering. Used for initial render or when incremental
        patching would be too complex.

        Args:
            root: Serialized view tree dictionary.
            icon: Menu bar icon (SF Symbol name or config dict).
            title: Menu bar title text.
            width: Popover window width in points.
            height: Popover window height in points.
            menu: List of serialized menu item dictionaries.
            hotkeys: List of hotkey strings to register.
            fonts: Dictionary mapping font names to paths/URLs.
        """
        window = {}
        if width is not None:
            window["width"] = float(width)
        if height is not None:
            window["height"] = float(height)

        message = {
            "type": "render",
            "payload": {
                "root": root,
                "statusBar": {"icon": icon, "title": title},
                "window": window if window else None,
                "menu": menu,
                "hotkeys": hotkeys,
                "fonts": fonts,
            },
        }
        self._send(message)

    def send_flat_render(
        self,
        nodes: list[dict],
        root_id: str,
        icon: Optional[str] = None,
        title: Optional[str] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
        menu: Optional[list] = None,
        hotkeys: Optional[list] = None,
        fonts: Optional[dict] = None,
    ) -> None:
        """Send a flat render message to the Swift runtime.

        Uses flat node list instead of nested tree structure.
        This enables iterative (non-recursive) parsing on Swift side,
        preventing stack overflow with deeply nested views.

        Args:
            nodes: List of flat node dictionaries with parentId references.
            root_id: ID of the root node.
            icon: Menu bar icon (SF Symbol name or config dict).
            title: Menu bar title text.
            width: Popover window width in points.
            height: Popover window height in points.
            menu: List of serialized menu item dictionaries.
            hotkeys: List of hotkey strings to register.
            fonts: Dictionary mapping font names to paths/URLs.
        """
        window = {}
        if width is not None:
            window["width"] = float(width)
        if height is not None:
            window["height"] = float(height)

        message = {
            "type": "flatRender",
            "payload": {
                "nodes": nodes,
                "rootId": root_id,
                "statusBar": {"icon": icon, "title": title},
                "window": window if window else None,
                "menu": menu,
                "hotkeys": hotkeys,
                "fonts": fonts,
            },
        }
        self._send(message)

    def send_patch(
        self,
        patches: list,
        icon: Optional[str] = None,
        title: Optional[str] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
    ) -> None:
        """Send incremental patches to the Swift runtime.

        Instead of re-rendering the entire view tree, this sends only
        the changes (patches) needed to update the UI.

        Note:
            Currently disabled in favor of full renders due to Swift-side
            handling issues.

        Args:
            patches: List of patch operations from :func:`diff_trees`.
            icon: Menu bar icon (SF Symbol name or config dict).
            title: Menu bar title text.
            width: Popover window width in points.
            height: Popover window height in points.
        """
        window = {}
        if width is not None:
            window["width"] = float(width)
        if height is not None:
            window["height"] = float(height)

        message = {
            "type": "patch",
            "payload": {
                "patches": patches,
                "statusBar": {"icon": icon, "title": title},
                "window": window if window else None,
            },
        }
        self._send(message)

    def send_quit(self) -> None:
        """Send a quit message to terminate the Swift runtime."""
        self._send({"type": "quit"})

    def send_notify(
        self,
        title: str,
        body: Optional[str] = None,
        subtitle: Optional[str] = None,
        sound: bool = True,
        identifier: Optional[str] = None,
    ) -> None:
        """Send a macOS notification through the Swift runtime.

        Args:
            title: The notification title (required).
            body: The notification body text.
            subtitle: A subtitle shown below the title.
            sound: Whether to play the default notification sound.
            identifier: Unique ID for updating/removing the notification.
        """
        message = {
            "type": "notify",
            "payload": {
                "title": title,
                "body": body,
                "subtitle": subtitle,
                "sound": sound,
                "identifier": identifier,
            },
        }
        self._send(message)

    def send_clipboard_write(self, content: str) -> None:
        """Write content to the system clipboard.

        Args:
            content: The text to copy to the clipboard.
        """
        message = {
            "type": "clipboard",
            "payload": {
                "action": "write",
                "content": content,
            },
        }
        self._send(message)

    def send_clipboard_read(self, request_id: str) -> None:
        """Request clipboard content asynchronously.

        The clipboard content will be returned via an event callback
        with the format ``clipboard:<content>``.

        Args:
            request_id: Unique ID to match the response callback.
        """
        message = {
            "type": "clipboard",
            "payload": {
                "action": "read",
                "requestId": request_id,
            },
        }
        self._send(message)

    def send_file_dialog(
        self,
        action: str,
        request_id: str,
        title: Optional[str] = None,
        types: Optional[list] = None,
        multiple: bool = False,
        directory: Optional[str] = None,
        default_name: Optional[str] = None,
    ) -> None:
        """Show a file open or save dialog.

        The selected file path(s) will be returned via an event callback
        with the format ``fileDialog:<paths>``.

        Args:
            action: Either "open" or "save".
            request_id: Unique ID to match the response callback.
            title: Dialog window title.
            types: Allowed file extensions (e.g., ["txt", "md"]).
            multiple: Allow selecting multiple files (open only).
            directory: Starting directory path.
            default_name: Default filename (save only).
        """
        message = {
            "type": "fileDialog",
            "payload": {
                "action": action,
                "requestId": request_id,
                "title": title,
                "types": types,
                "multiple": multiple,
                "directory": directory,
                "defaultName": default_name,
            },
        }
        self._send(message)

    def send_user_defaults(
        self,
        action: str,
        key: Optional[str] = None,
        value: Any = None,
        prefix: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> None:
        """Send a UserDefaults operation to the Swift runtime.

        Args:
            action: Operation type - "set", "get", "remove", "clear",
                "containsKey", or "getKeys".
            key: The key for get/set/remove/containsKey operations.
            value: The value to store (set operation only).
            prefix: Key prefix filter (getKeys operation only).
            request_id: Unique ID for async response matching.
        """
        message = {
            "type": "userDefaults",
            "payload": {
                "action": action,
                "key": key,
                "value": value,
                "prefix": prefix,
                "requestId": request_id,
            },
        }
        self._send(message)

    def send_service_query(
        self,
        service: str,
        action: str,
        request_id: str,
        params: Optional[dict] = None,
    ) -> None:
        """Query a system service.

        Args:
            service: Service name ("battery", "connectivity", "screen").
            action: Action to perform (e.g., "status", "info", "setBrightness").
            request_id: Unique ID to match the response callback.
            params: Optional parameters for the action.
        """
        message = {
            "type": "service",
            "payload": {
                "service": service,
                "action": action,
                "requestId": request_id,
            },
        }
        if params:
            message["payload"]["params"] = params
        self._send(message)

    def send_action(
        self,
        node_id: str,
        action: str,
        params: Optional[dict] = None,
    ) -> None:
        """Send an action to a specific view node.

        Used for triggering actions on views like WebView (reload, goBack, etc.).

        Args:
            node_id: The ID of the target view node.
            action: The action to perform (e.g., "reload", "goBack", "goForward").
            params: Optional parameters for the action.
        """
        message = {
            "type": "action",
            "payload": {
                "nodeId": node_id,
                "action": action,
            },
        }
        if params:
            message["payload"]["params"] = params
        self._send(message)

    def send_settings_render(self, settings_config: dict) -> None:
        """Send settings page configuration to the Swift runtime.

        This creates or updates the settings window with the specified
        tabs and content.

        Args:
            settings_config: Dictionary with width, height, title, and tabs.
        """
        message = {
            "type": "settingsRender",
            "payload": settings_config,
        }
        self._send(message)

    def send_settings_open(self) -> None:
        """Open the settings window.

        The settings window must have been rendered first via
        send_settings_render().
        """
        message = {
            "type": "settingsOpen",
            "payload": {},
        }
        self._send(message)

    def send_settings_close(self) -> None:
        """Close the settings window."""
        message = {
            "type": "settingsClose",
            "payload": {},
        }
        self._send(message)

    def set_event_handler(self, handler: Callable[[str, str], None]) -> None:
        """Set the handler for events from the Swift runtime.

        Args:
            handler: Callback function receiving (node_id, event_string).
                The event string format varies by event type:
                - "tap" - User tapped a button
                - "change:<value>" - Value changed (TextField, Toggle, etc.)
                - "hotkey:<shortcut>" - Global hotkey pressed
                - "drop:<paths>" - Files dropped on a view
                - "clipboard:<content>" - Clipboard read response
                - "fileDialog:<paths>" - File dialog response
        """
        self._on_event = handler

    def _send(self, message: Any) -> None:
        """Send a message to the Swift runtime.

        Messages are serialized with MessagePack and sent with a 4-byte
        big-endian length prefix.

        Args:
            message: Dictionary to serialize and send.
        """
        if not self._connected or not self._socket:
            return

        with self._send_lock:
            try:
                packed = msgpack.packb(message, use_bin_type=True)
                # Length prefix (4 bytes, big-endian)
                length = struct.pack(">I", len(packed))
                self._socket.sendall(length + packed)
            except Exception as e:
                logger.error("Error sending message", exc=e)
                self._connected = False

    def _start_read_thread(self) -> None:
        """Start the background thread for reading events.

        Creates a daemon thread that continuously reads messages from
        the Swift runtime and dispatches them to the event handler.
        """
        self._read_thread = threading.Thread(target=self._read_loop, daemon=True)
        self._read_thread.start()

    def _read_loop(self) -> None:
        """Background loop for reading events from the Swift runtime.

        Continuously reads length-prefixed MessagePack messages from
        the socket and passes them to :meth:`_handle_message`.
        """
        buffer = b""

        while self._connected and self._socket:
            try:
                data = self._socket.recv(4096)
                if not data:
                    break

                buffer += data

                # Extract complete messages
                while len(buffer) >= 4:
                    length = struct.unpack(">I", buffer[:4])[0]
                    if len(buffer) < 4 + length:
                        break

                    message_data = buffer[4 : 4 + length]
                    buffer = buffer[4 + length :]

                    try:
                        message = msgpack.unpackb(message_data, raw=False)
                        self._handle_message(message)
                    except Exception as e:
                        logger.error("Error unpacking message", exc=e)

            except Exception as e:
                if self._connected:
                    logger.error("Error reading from socket", exc=e)
                break

        self._connected = False

    def _handle_message(self, message: dict) -> None:
        """Handle a message from the Swift runtime."""
        msg_type = message.get("type")

        if msg_type == "event" and self._on_event:
            node_id = message.get("nodeId", "")
            event = message.get("event", "")
            # Run event handlers on a separate thread to avoid blocking the read loop
            # This allows service requests made in callbacks to complete
            threading.Thread(
                target=self._dispatch_event,
                args=(node_id, event),
                daemon=True,
            ).start()

        elif msg_type == "serviceResponse":
            self._handle_service_response(message)

    def _dispatch_event(self, node_id: str, event: str) -> None:
        """Dispatch an event to the handler (runs on separate thread)."""
        try:
            self._on_event(node_id, event)
        except Exception as e:
            logger.error("Error in event handler", exc=e, node_id=node_id, event=event)

    def _handle_service_response(self, message: dict) -> None:
        """Handle a service query response."""
        service = message.get("service", "")
        request_id = message.get("requestId", "")
        data = message.get("data", {})

        try:
            # Handle camera stream frames specially (no request_id)
            if service == "camera" and data.get("isStreamFrame"):
                from ..services.camera import Camera
                Camera._handle_stream_frame(data)
                return

            # All other service responses go through Service base class
            from ..services.base import Service
            Service._handle_response(request_id, data)
        except Exception as e:
            logger.error("Error handling service response", exc=e, service=service)
