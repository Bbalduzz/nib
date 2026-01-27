"""Connection layer for communicating with the Swift runtime."""

import socket
import struct
import threading
from typing import Callable, Optional, Any
import msgpack


class Connection:
    """Unix socket connection to the Swift runtime."""

    def __init__(self, socket_path: str):
        self.socket_path = socket_path
        self._socket: Optional[socket.socket] = None
        self._connected = False
        self._read_thread: Optional[threading.Thread] = None
        self._on_event: Optional[Callable[[str, str], None]] = None
        self._send_lock = threading.Lock()

    def connect(self, retries: int = 10, delay: float = 0.2) -> bool:
        """Connect to the Swift runtime socket."""
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
        """Disconnect from the Swift runtime."""
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
        """Send a render message to the Swift runtime."""
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
        print(f"[nib.connection] Sending message type: {message['type']}")
        import json

        print("Sending:", json.dumps(message, indent=2, default=str))
        self._send(message)

    def send_patch(
        self,
        patches: list,
        icon: Optional[str] = None,
        title: Optional[str] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
    ) -> None:
        """Send a patch message to the Swift runtime (incremental update)."""
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
        print(f"[nib.connection] Sending patch with {len(patches)} changes")
        self._send(message)

    def send_quit(self) -> None:
        """Send a quit message to the Swift runtime."""
        self._send({"type": "quit"})

    def send_notify(
        self,
        title: str,
        body: Optional[str] = None,
        subtitle: Optional[str] = None,
        sound: bool = True,
        identifier: Optional[str] = None,
    ) -> None:
        """Send a notification message to the Swift runtime."""
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
        """Write content to the system clipboard."""
        message = {
            "type": "clipboard",
            "payload": {
                "action": "write",
                "content": content,
            },
        }
        self._send(message)

    def send_clipboard_read(self, request_id: str) -> None:
        """Request clipboard content (response comes via event)."""
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
        """Show a file open/save dialog."""
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

    def set_event_handler(self, handler: Callable[[str, str], None]) -> None:
        """Set the handler for events from the Swift runtime."""
        self._on_event = handler

    def _send(self, message: Any) -> None:
        """Send a message to the Swift runtime."""
        if not self._connected or not self._socket:
            return

        with self._send_lock:
            try:
                packed = msgpack.packb(message, use_bin_type=True)
                # Length prefix (4 bytes, big-endian)
                length = struct.pack(">I", len(packed))
                self._socket.sendall(length + packed)
            except Exception as e:
                print(f"[nib] Error sending message: {e}")
                self._connected = False

    def _start_read_thread(self) -> None:
        """Start the background thread for reading events."""
        self._read_thread = threading.Thread(target=self._read_loop, daemon=True)
        self._read_thread.start()

    def _read_loop(self) -> None:
        """Background loop for reading events from the Swift runtime."""
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
                        print(f"Error unpacking message: {e}")

            except Exception as e:
                if self._connected:
                    print(f"Error reading from socket: {e}")
                break

        self._connected = False

    def _handle_message(self, message: dict) -> None:
        """Handle a message from the Swift runtime."""
        msg_type = message.get("type")

        if msg_type == "event" and self._on_event:
            node_id = message.get("nodeId", "")
            event = message.get("event", "")
            try:
                self._on_event(node_id, event)
            except Exception as e:
                print(f"[nib] Error in event handler: {e}")
                import traceback

                traceback.print_exc()
