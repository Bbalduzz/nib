"""Settings management with sync cache and async persistence.

This module provides the :class:`Settings` class for managing application
settings with instant reads and background writes.

The Settings class provides:
- Instant reads from local cache (no blocking)
- Automatic background persistence to UserDefaults
- Type-safe attribute access via dot notation
- Initial loading from UserDefaults on startup

Example:
    Basic settings usage::

        import nib

        def main(app: nib.App):
            # Define settings with defaults
            settings = nib.Settings({
                "dark_mode": False,
                "font_size": 14,
                "username": "",
            })

            # Register with app for persistence
            app.register_settings(settings)

            # Read instantly from cache
            if settings.dark_mode:
                print("Dark mode enabled")

            # Write updates cache immediately, persists in background
            settings.dark_mode = True
            settings.font_size = 16

            app.build(nib.VStack([...]))

        nib.run(main)
"""

import threading
import uuid
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .connection import Connection

# Storage for batch load responses
_batch_responses: Dict[str, Dict[str, Any]] = {}
_batch_events: Dict[str, threading.Event] = {}


def _handle_settings_batch_response(request_id: str, values: Dict[str, Any]) -> None:
    """Handle a batch settings response from Swift.

    Called when the settings batch load completes.

    Args:
        request_id: The unique request ID to match.
        values: Dictionary of key-value pairs loaded from UserDefaults.
    """
    if request_id in _batch_events:
        _batch_responses[request_id] = values
        _batch_events[request_id].set()


class Settings:
    """Settings manager with sync cache and async persistence.

    Provides instant reads from a local cache and automatic background
    persistence to UserDefaults. This ensures UI responsiveness while
    maintaining data persistence.

    Attributes are accessed using dot notation::

        settings = nib.Settings({"dark_mode": False})
        print(settings.dark_mode)  # Instant read from cache
        settings.dark_mode = True  # Updates cache, persists in background

    Args:
        defaults: Dictionary of setting names to default values.
            These defaults are used when no saved value exists.

    Example:
        Creating and using settings::

            settings = nib.Settings({
                "theme": "light",
                "notifications": True,
                "volume": 50,
            })

            # Register with app
            app.register_settings(settings)

            # Access settings
            print(settings.theme)        # "light" (or saved value)
            settings.volume = 75         # Instant update + background save
    """

    def __init__(self, defaults: Dict[str, Any]):
        """Initialize Settings with default values.

        Args:
            defaults: Dictionary mapping setting names to their default values.
        """
        object.__setattr__(self, "_defaults", defaults)
        object.__setattr__(self, "_cache", dict(defaults))
        object.__setattr__(self, "_connection", None)
        object.__setattr__(self, "_loaded", threading.Event())
        object.__setattr__(self, "_loading", False)

    def _set_connection(self, connection: "Connection") -> None:
        """Set the connection for persistence operations.

        Called by App.register_settings() to inject the connection.

        Args:
            connection: The Connection instance for Swift communication.
        """
        object.__setattr__(self, "_connection", connection)
        # Don't auto-load here - it causes race conditions during startup.
        # Loading will happen on first access if needed, or can be triggered
        # manually with load() method.

    def _load_initial(self) -> None:
        """Load saved values from UserDefaults.

        Performs a non-blocking batch load of all setting keys from
        UserDefaults and merges them into the cache.
        """
        connection = object.__getattribute__(self, "_connection")
        defaults = object.__getattribute__(self, "_defaults")

        if not connection or object.__getattribute__(self, "_loading"):
            return

        object.__setattr__(self, "_loading", True)

        # Load each key individually using existing UserDefaults mechanism
        # This is done in a background thread to avoid blocking
        def load_settings():
            cache = object.__getattribute__(self, "_cache")
            for key in defaults.keys():
                try:
                    # Use the connection's user_defaults get with callback
                    value = self._get_from_user_defaults(key)
                    if value is not None:
                        cache[key] = value
                except Exception:
                    pass  # Use default on error
            object.__getattribute__(self, "_loaded").set()
            object.__setattr__(self, "_loading", False)

        thread = threading.Thread(target=load_settings, daemon=True)
        thread.start()

    def _get_from_user_defaults(self, key: str, timeout: float = 2.0) -> Optional[Any]:
        """Get a single value from UserDefaults (blocking).

        Used during initial load only.

        Args:
            key: The setting key to load.
            timeout: Maximum wait time in seconds.

        Returns:
            The loaded value, or None if not found or timeout.
        """
        from .user_defaults import UserDefaults, _get_current_app

        app = _get_current_app()
        if app:
            defaults = UserDefaults(app)
            return defaults.get(key, default=None, timeout=timeout)
        return None

    def _persist_async(self, key: str, value: Any) -> None:
        """Persist a value to UserDefaults in the background.

        Fire-and-forget: the write is sent to Swift but we don't
        wait for confirmation.

        Args:
            key: The setting key to persist.
            value: The value to persist.
        """
        connection = object.__getattribute__(self, "_connection")
        if connection:
            # Use send_user_defaults which is fire-and-forget for "set" action
            connection.send_user_defaults(
                action="set",
                key=key,
                value=value,
            )

    def __getattr__(self, name: str) -> Any:
        """Get a setting value from the cache.

        Provides instant access to settings via dot notation.

        Args:
            name: The setting name.

        Returns:
            The setting value from cache.

        Raises:
            AttributeError: If the setting is not defined.
        """
        if name.startswith("_"):
            return object.__getattribute__(self, name)

        cache = object.__getattribute__(self, "_cache")
        if name in cache:
            return cache[name]

        raise AttributeError(f"Setting '{name}' not defined in defaults")

    def __setattr__(self, name: str, value: Any) -> None:
        """Set a setting value.

        Updates the cache immediately for instant UI response,
        then persists to UserDefaults in the background.

        Args:
            name: The setting name.
            value: The new value.
        """
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return

        cache = object.__getattribute__(self, "_cache")
        defaults = object.__getattribute__(self, "_defaults")

        if name not in defaults:
            raise AttributeError(f"Setting '{name}' not defined in defaults")

        cache[name] = value
        self._persist_async(name, value)

    def get(self, name: str, default: Any = None) -> Any:
        """Get a setting value with an optional default.

        Args:
            name: The setting name.
            default: Value to return if setting not found.

        Returns:
            The setting value, or default if not found.
        """
        cache = object.__getattribute__(self, "_cache")
        return cache.get(name, default)

    def set(self, name: str, value: Any) -> None:
        """Set a setting value (alternative to attribute assignment).

        Args:
            name: The setting name.
            value: The new value.
        """
        self.__setattr__(name, value)

    def wait_for_load(self, timeout: float = 5.0) -> bool:
        """Wait for initial settings to load from UserDefaults.

        Usually not needed since defaults are used immediately.
        Call this if you need to ensure saved values are loaded.

        Args:
            timeout: Maximum wait time in seconds.

        Returns:
            True if loading completed, False if timeout.
        """
        loaded = object.__getattribute__(self, "_loaded")
        return loaded.wait(timeout=timeout)

    def to_dict(self) -> Dict[str, Any]:
        """Get all settings as a dictionary.

        Returns:
            Dictionary of all setting names and values.
        """
        cache = object.__getattribute__(self, "_cache")
        return dict(cache)

    def reset(self, name: Optional[str] = None) -> None:
        """Reset settings to defaults.

        Args:
            name: Specific setting to reset, or None to reset all.
        """
        cache = object.__getattribute__(self, "_cache")
        defaults = object.__getattribute__(self, "_defaults")

        if name:
            if name in defaults:
                cache[name] = defaults[name]
                self._persist_async(name, defaults[name])
        else:
            for key, value in defaults.items():
                cache[key] = value
                self._persist_async(key, value)
