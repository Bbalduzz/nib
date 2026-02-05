"""Consistent logging system for nib.

Provides structured logging with levels, timestamps, and file output
that matches the Swift runtime's logging format.

Log Levels:
    - DEBUG: Detailed debugging info (message bytes, buffer operations)
    - INFO: General information (connections, renders, events)
    - WARN: Warnings (missing assets, deprecated usage)
    - ERROR: Errors (exceptions, failures)

Configuration:
    Set the NIB_LOG_LEVEL environment variable to control verbosity:
    - NIB_LOG_LEVEL=debug (most verbose)
    - NIB_LOG_LEVEL=info (default)
    - NIB_LOG_LEVEL=warn
    - NIB_LOG_LEVEL=error (least verbose)

    Set NIB_LOG_FILE to change log file location (default: /tmp/nib.log)

Example:
    from nib.core.logging import logger

    logger.info("Connected to runtime")
    logger.debug(f"Received {len(data)} bytes")
    logger.warn("Asset not found", path=relative_path)
    logger.error("Handler failed", error=str(e))
"""

import os
import sys
import traceback
from datetime import datetime, timezone
from enum import IntEnum
from pathlib import Path
from typing import Any, Optional


class LogLevel(IntEnum):
    """Log levels matching Swift implementation."""

    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3


# Level name mappings
_LEVEL_NAMES = {
    LogLevel.DEBUG: "DEBUG",
    LogLevel.INFO: "INFO",
    LogLevel.WARN: "WARN",
    LogLevel.ERROR: "ERROR",
}

_NAME_TO_LEVEL = {
    "debug": LogLevel.DEBUG,
    "info": LogLevel.INFO,
    "warn": LogLevel.WARN,
    "warning": LogLevel.WARN,
    "error": LogLevel.ERROR,
}


class NibLogger:
    """Logger for nib framework with file and console output.

    Writes to both the log file (shared with Swift runtime) and stdout,
    with consistent formatting and timestamps.
    """

    def __init__(self):
        """Initialize the logger with default settings."""
        self._log_file: Optional[Path] = None
        self._level: LogLevel = LogLevel.INFO
        self._console_enabled: bool = True
        self._file_enabled: bool = True
        self._initialized: bool = False

    def _ensure_initialized(self) -> None:
        """Lazy initialization from environment variables."""
        if self._initialized:
            return

        self._initialized = True

        # Get log level from environment
        level_str = os.environ.get("NIB_LOG_LEVEL", "info").lower()
        self._level = _NAME_TO_LEVEL.get(level_str, LogLevel.INFO)

        # Get log file path from environment
        log_path = os.environ.get("NIB_LOG_FILE", "/tmp/nib.log")
        self._log_file = Path(log_path)

        # Check if console output is disabled
        if os.environ.get("NIB_LOG_CONSOLE", "1").lower() in ("0", "false", "no"):
            self._console_enabled = False

        # Check if file output is disabled
        if os.environ.get("NIB_LOG_FILE_ENABLED", "1").lower() in ("0", "false", "no"):
            self._file_enabled = False

    def set_level(self, level: LogLevel) -> None:
        """Set the minimum log level.

        Args:
            level: Minimum level to log (DEBUG, INFO, WARN, ERROR)
        """
        self._level = level

    def set_file(self, path: Optional[str]) -> None:
        """Set the log file path.

        Args:
            path: Path to log file, or None to disable file logging
        """
        self._log_file = Path(path) if path else None
        self._file_enabled = path is not None

    def _format_timestamp(self) -> str:
        """Format current time in loguru style."""
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S.") + f"{now.microsecond // 1000:03d}"

    def _format_message(
        self, level: LogLevel, message: str, caller_info: tuple = None, **kwargs: Any
    ) -> str:
        """Format a log message with timestamp and level.

        Args:
            level: Log level
            message: Main message
            caller_info: Optional (module, func, line) tuple
            **kwargs: Additional key-value pairs to include

        Returns:
            Formatted log line
        """
        timestamp = self._format_timestamp()
        level_name = _LEVEL_NAMES[level].ljust(8)

        # Get caller info if not provided
        if caller_info is None:
            import inspect
            # Go up the stack to find the actual caller
            # Stack: _format_message -> _write -> info/debug/etc -> actual caller
            frame = inspect.currentframe()
            for _ in range(3):  # Skip 3 frames to get to actual caller
                if frame is not None:
                    frame = frame.f_back
            if frame:
                module = Path(frame.f_code.co_filename).stem
                func = frame.f_code.co_name
                lineno = frame.f_lineno
                caller_info = (module, func, lineno)
            else:
                caller_info = ("unknown", "unknown", 0)

        module, func, lineno = caller_info
        location = f"{module}:{func}:{lineno}"

        # Build the log line
        if kwargs:
            pairs = " ".join(f"{k}={v}" for k, v in kwargs.items())
            message = f"{message} ({pairs})"

        return f"{timestamp} | {level_name} | python | {location} - {message}"

    def _write(self, level: LogLevel, message: str, **kwargs: Any) -> None:
        """Write a log message if level is enabled.

        Args:
            level: Log level
            message: Main message
            **kwargs: Additional context
        """
        self._ensure_initialized()

        if level < self._level:
            return

        formatted = self._format_message(level, message, **kwargs)

        # Write to console
        if self._console_enabled:
            print(formatted, file=sys.stderr if level >= LogLevel.ERROR else sys.stdout)

        # Write to file
        if self._file_enabled and self._log_file:
            try:
                with open(self._log_file, "a", encoding="utf-8") as f:
                    f.write(formatted + "\n")
            except OSError:
                pass  # Silently ignore file write errors

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a debug message.

        Args:
            message: Debug message
            **kwargs: Additional context
        """
        self._write(LogLevel.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log an info message.

        Args:
            message: Info message
            **kwargs: Additional context
        """
        self._write(LogLevel.INFO, message, **kwargs)

    def warn(self, message: str, **kwargs: Any) -> None:
        """Log a warning message.

        Args:
            message: Warning message
            **kwargs: Additional context
        """
        self._write(LogLevel.WARN, message, **kwargs)

    # Alias for compatibility with Python's logging module
    warning = warn

    def success(self, message: str, **kwargs: Any) -> None:
        """Log a success message (logs at INFO level).

        Args:
            message: Success message
            **kwargs: Additional context
        """
        self._write(LogLevel.INFO, message, **kwargs)

    def progress(self, current: int, total: int, message: str = "") -> None:
        """Print an inline progress bar (overwrites current line).

        Uses the standard log format prefix for consistency.

        Args:
            current: Current step (1-based).
            total: Total steps.
            message: Optional label to show before the bar.
        """
        self._ensure_initialized()
        if not self._console_enabled or self._level > LogLevel.INFO:
            return

        import inspect
        frame = inspect.currentframe()
        if frame and frame.f_back:
            f = frame.f_back
            caller_info = (Path(f.f_code.co_filename).stem, f.f_code.co_name, f.f_lineno)
        else:
            caller_info = ("unknown", "unknown", 0)

        timestamp = self._format_timestamp()
        level_name = _LEVEL_NAMES[LogLevel.INFO].ljust(8)
        module, func, lineno = caller_info
        location = f"{module}:{func}:{lineno}"
        prefix = f"{timestamp} | {level_name} | python | {location} - "

        width = 25
        filled = int(width * current / total) if total > 0 else 0
        bar = "\u2588" * filled + "\u2591" * (width - filled)
        pct = int(100 * current / total) if total > 0 else 0
        line = f"\r{prefix}{message} [{bar}] {current}/{total} ({pct}%)"
        sys.stdout.write(line)
        sys.stdout.flush()
        if current >= total:
            sys.stdout.write("\n")
            sys.stdout.flush()

    def error(self, message: str, exc: Optional[Exception] = None, **kwargs: Any) -> None:
        """Log an error message, optionally with exception details.

        Args:
            message: Error message
            exc: Optional exception to include traceback
            **kwargs: Additional context
        """
        self._write(LogLevel.ERROR, message, **kwargs)

        # Log traceback for exceptions at debug level
        if exc is not None:
            tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            for line in tb.strip().split("\n"):
                self._write(LogLevel.DEBUG, f"  {line}")


# Global logger instance
logger = NibLogger()


# Convenience exports
debug = logger.debug
info = logger.info
warn = logger.warn
warning = logger.warning  # Alias for Python logging compatibility
success = logger.success
error = logger.error
