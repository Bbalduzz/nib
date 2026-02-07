"""Persistent key-value storage using macOS UserDefaults.

This module provides the :class:`UserDefaults` class for storing and
retrieving persistent application data using the macOS UserDefaults system.

UserDefaults is ideal for storing user preferences, settings, and small
pieces of data that need to persist across app launches.

Supported Value Types:
    - Strings
    - Integers
    - Floats
    - Booleans
    - Lists (JSON-serializable)
    - Dictionaries (JSON-serializable)
    - Binary data (base64-encoded)

Example:
    Storing and retrieving preferences::

        import nib

        def main(app: nib.App):
            defaults = nib.UserDefaults()

            # Store values
            defaults.set("username", "john_doe")
            defaults.set("login_count", 42)
            defaults.set("dark_mode", True)

            # Retrieve values
            username = defaults.get("username", default="guest")
            count = defaults.get("login_count", default=0)

            # Check existence
            if defaults.contains_key("api_token"):
                token = defaults.get("api_token")

            # Get all keys with prefix
            settings_keys = defaults.get_keys("settings.")

Note:
    All read operations are blocking with a configurable timeout.
    The underlying communication with the Swift runtime is asynchronous,
    but the Python API waits for the response.
"""

import json
import uuid
from typing import Any, List, Optional, TYPE_CHECKING

from .pending import PendingRequests

if TYPE_CHECKING:
    from .app import App

# Module-level reference to the current running app
_current_app: Optional["App"] = None

# Thread-safe storage for blocking responses
_pending = PendingRequests()


def _set_current_app(app: Optional["App"]) -> None:
    """Set the current running app instance.

    Called by :func:`~nib.run` to set the global app reference that
    UserDefaults instances use by default.

    Args:
        app: The running App instance, or None to clear.
    """
    global _current_app
    _current_app = app


def _get_current_app() -> Optional["App"]:
    """Get the current running app instance.

    Returns:
        The current App instance, or None if no app is running.
    """
    return _current_app


def _handle_user_defaults_response(request_id: str, action: str, value: str) -> None:
    """Handle a response from Swift UserDefaults.

    Called from :meth:`App._handle_event` when a userDefaults event
    is received. Sets the response and signals the waiting thread.

    Args:
        request_id: The unique request ID to match.
        action: The action that was performed ("get", "containsKey", etc.).
        value: The encoded response value.
    """
    _pending.resolve(request_id, (action, value))


class UserDefaults:
    """
    Service that provides access to persistent key-value storage.

    Uses macOS UserDefaults under the hood for persistence.

    Usage:
        # Set a value
        nib.UserDefaults().set("my_key", "my_value")
        nib.UserDefaults().set("count", 42)
        nib.UserDefaults().set("enabled", True)

        # Get a value (blocking)
        value = nib.UserDefaults().get("my_key")
        print(f"Got: {value}")

        # Check if key exists
        exists = nib.UserDefaults().contains_key("my_key")

        # Get all keys with prefix
        keys = nib.UserDefaults().get_keys("settings.")

        # Remove a key
        nib.UserDefaults().remove("my_key")

        # Clear all keys
        nib.UserDefaults().clear()
    """

    def __init__(self, app: Optional["App"] = None):
        """
        Create a UserDefaults service.

        Args:
            app: Optional App instance. If not provided, uses the current running app.
        """
        self._app = app

    def _get_app(self) -> Optional["App"]:
        """Get the app instance to use for operations."""
        return self._app or _get_current_app()

    def _wait_for_response(self, request_id: str, timeout: float = 5.0) -> Optional[tuple]:
        """Wait for a response from Swift."""
        return _pending.wait(request_id, timeout)

    def set(self, key: str, value: Any) -> None:
        """
        Sets a value for the given key.

        Args:
            key: The key to store the value under.
            value: The value to store. Supports strings, numbers, booleans,
                   lists, and dictionaries.

        Example:
            nib.UserDefaults().set("username", "john")
            nib.UserDefaults().set("score", 100)
            nib.UserDefaults().set("dark_mode", True)
        """
        app = self._get_app()
        if app and app._connection:
            app._connection.send_user_defaults(
                action="set",
                key=key,
                value=value,
            )

    def get(self, key: str, default: Any = None, timeout: float = 5.0) -> Any:
        """
        Gets the value for the given key.

        Args:
            key: The key to retrieve.
            default: Default value if key not found (default: None).
            timeout: Max time to wait for response in seconds (default: 5.0).

        Returns:
            The stored value, or default if not found.

        Example:
            username = nib.UserDefaults().get("username")
            score = nib.UserDefaults().get("score", default=0)
        """
        app = self._get_app()
        if not app or not app._connection:
            return default

        request_id = str(uuid.uuid4())
        _pending.create(request_id)

        app._connection.send_user_defaults(
            action="get",
            key=key,
            request_id=request_id,
        )

        result = self._wait_for_response(request_id, timeout)
        if result:
            action, encoded_value = result
            if action == "get":
                value = _decode_user_defaults_value(encoded_value)
                return value if value is not None else default
        return default

    def remove(self, key: str) -> None:
        """
        Removes the value for the given key.

        Args:
            key: The key to remove.

        Example:
            nib.UserDefaults().remove("old_setting")
        """
        app = self._get_app()
        if app and app._connection:
            app._connection.send_user_defaults(
                action="remove",
                key=key,
            )

    def clear(self) -> None:
        """
        Clears all keys and values.

        Example:
            nib.UserDefaults().clear()
        """
        app = self._get_app()
        if app and app._connection:
            app._connection.send_user_defaults(action="clear")

    def contains_key(self, key: str, timeout: float = 5.0) -> bool:
        """
        Checks if the given key exists.

        Args:
            key: The key to check.
            timeout: Max time to wait for response in seconds (default: 5.0).

        Returns:
            True if key exists, False otherwise.

        Example:
            if nib.UserDefaults().contains_key("api_key"):
                print("API key is set")
        """
        app = self._get_app()
        if not app or not app._connection:
            return False

        request_id = str(uuid.uuid4())
        _pending.create(request_id)

        app._connection.send_user_defaults(
            action="containsKey",
            key=key,
            request_id=request_id,
        )

        result = self._wait_for_response(request_id, timeout)
        if result:
            action, value = result
            if action == "containsKey":
                return value.lower() == "true"
        return False

    def get_keys(self, prefix: str = "", timeout: float = 5.0) -> List[str]:
        """
        Gets all keys with the given prefix.

        Args:
            prefix: Filter keys by this prefix (default: "" for all keys).
            timeout: Max time to wait for response in seconds (default: 5.0).

        Returns:
            List of matching keys.

        Example:
            # Get all keys starting with "user."
            keys = nib.UserDefaults().get_keys("user.")

            # Get all keys
            all_keys = nib.UserDefaults().get_keys()
        """
        app = self._get_app()
        if not app or not app._connection:
            return []

        request_id = str(uuid.uuid4())
        _pending.create(request_id)

        app._connection.send_user_defaults(
            action="getKeys",
            prefix=prefix,
            request_id=request_id,
        )

        result = self._wait_for_response(request_id, timeout)
        if result:
            action, value = result
            if action == "getKeys":
                return [k for k in value.split("\n") if k]
        return []


def _decode_user_defaults_value(encoded: str) -> Any:
    """Decode a value received from Swift UserDefaults.

    Parses the type-prefixed string format used for Swift-to-Python
    value transmission.

    Args:
        encoded: The encoded string in format "type:value".

    Returns:
        The decoded Python value with appropriate type.

    Format:
        The encoded string uses the format ``type:value`` where type is:

        - ``string:value`` - String (with escaped special chars)
        - ``int:value`` - Integer
        - ``float:value`` - Float
        - ``bool:value`` - Boolean ("true" or "false")
        - ``data:value`` - Binary data (base64-encoded)
        - ``array:value`` - List (JSON-encoded)
        - ``dict:value`` - Dictionary (JSON-encoded)
        - ``null`` - None (no colon or value)

    Example:
        >>> _decode_user_defaults_value("string:hello")
        'hello'
        >>> _decode_user_defaults_value("int:42")
        42
        >>> _decode_user_defaults_value("bool:true")
        True
    """
    if encoded == "null":
        return None

    # Find the type prefix
    colon_idx = encoded.find(":")
    if colon_idx == -1:
        return encoded

    value_type = encoded[:colon_idx]
    value_str = encoded[colon_idx + 1 :]

    if value_type == "string":
        # Unescape special characters
        return (
            value_str.replace("\\:", ":")
            .replace("\\n", "\n")
            .replace("\\\\", "\\")
        )
    elif value_type == "int":
        return int(value_str)
    elif value_type == "float":
        return float(value_str)
    elif value_type == "bool":
        return value_str.lower() == "true"
    elif value_type == "data":
        import base64
        return base64.b64decode(value_str)
    elif value_type == "array":
        return json.loads(value_str)
    elif value_type == "dict":
        return json.loads(value_str)
    else:
        return value_str
