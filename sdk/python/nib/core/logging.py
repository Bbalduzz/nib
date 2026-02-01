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
        """Format current time in ISO8601 format (matches Swift)."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _format_message(
        self, level: LogLevel, message: str, **kwargs: Any
    ) -> str:
        """Format a log message with timestamp and level.

        Args:
            level: Log level
            message: Main message
            **kwargs: Additional key-value pairs to include

        Returns:
            Formatted log line
        """
        timestamp = self._format_timestamp()
        level_name = _LEVEL_NAMES[level]

        # Build the log line
        line = f"[{timestamp}] [{level_name}] [Python] {message}"

        # Append key-value pairs if provided
        if kwargs:
            pairs = " ".join(f"{k}={v}" for k, v in kwargs.items())
            line = f"{line} ({pairs})"

        return line

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
error = logger.error
