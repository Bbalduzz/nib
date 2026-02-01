"""Nib core functionality for application lifecycle and system integration.

This module provides the core classes and functions for creating and
running Nib menu bar applications.

Classes:
    :class:`App` - Main application class managing lifecycle and UI
    :class:`SFSymbol` - SF Symbol (Apple system icon) view
    :class:`MenuItem` - Menu item for right-click context menus
    :class:`MenuDivider` - Separator for context menus
    :class:`State` - Reactive state descriptor for class-based apps
    :class:`Binding` - Two-way binding for state values
    :class:`Connection` - Unix socket connection to Swift runtime
    :class:`UserDefaults` - Persistent key-value storage

Functions:
    :func:`run` - Entry point for function-based applications

Example:
    Function-based app (recommended)::

        import nib

        def main(app: nib.App):
            app.title = "My App"
            app.icon = nib.SFSymbol("star.fill")
            app.build(nib.Text("Hello!"))

        nib.run(main)

    Class-based app::

        import nib

        class MyApp(nib.App):
            def body(self):
                return nib.Text("Hello!")

        MyApp(icon="star.fill").run()
"""

from .app import App, SFSymbol, run, MenuItem, MenuDivider
from .state import State, Binding
from .connection import Connection
from .user_defaults import UserDefaults
from .logging import logger, LogLevel

__all__ = [
    "App",
    "SFSymbol",
    "run",
    "MenuItem",
    "MenuDivider",
    "State",
    "Binding",
    "Connection",
    "UserDefaults",
    "logger",
    "LogLevel",
]
