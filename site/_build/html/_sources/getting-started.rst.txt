Getting Started
===============

This guide will help you get started with Nib, a Python framework for building
native macOS menu bar applications using SwiftUI.

Installation
------------

Prerequisites
~~~~~~~~~~~~~

- macOS 12.0 or later
- Python 3.11 or later
- Swift toolchain (comes with Xcode)

Install from Source
~~~~~~~~~~~~~~~~~~~

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/your-repo/nib.git
       cd nib

2. Build the Swift runtime:

   .. code-block:: bash

       cd swift
       swift build -c release
       cd ..

3. Install the Python package:

   .. code-block:: bash

       pip install -e ./python

Quick Start
-----------

Creating Your First App
~~~~~~~~~~~~~~~~~~~~~~~

Create a new Python file (e.g., ``my_app.py``):

.. code-block:: python

    import nib

    def main(app: nib.App):
        # Configure the app
        app.title = "My First Nib App"
        app.icon = nib.SFSymbol("star.fill")
        app.width = 300
        app.height = 200

        # Create UI elements
        greeting = nib.Text("Hello, World!")

        app.build(
            nib.VStack(
                controls=[greeting],
                spacing=8,
                padding=16,
            )
        )

    nib.run(main)

Run your app:

.. code-block:: bash

    python my_app.py

Core Concepts
-------------

Views
~~~~~

All UI elements in Nib inherit from :class:`~nib.View`. Views are styled through
constructor parameters:

.. code-block:: python

    nib.Text(
        "Hello",
        font=nib.Font.title,
        foreground_color=nib.Color.blue,
        padding=16,
    )

Layout Containers
~~~~~~~~~~~~~~~~~

Use layout containers to organize views:

- :class:`~nib.VStack` - Vertical stack
- :class:`~nib.HStack` - Horizontal stack
- :class:`~nib.ZStack` - Overlay stack

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Text("Title"),
            nib.Text("Subtitle"),
            nib.Button("Action", action=my_function),
        ],
        spacing=8,
    )

Reactivity
~~~~~~~~~~

Mutate view properties to trigger re-renders:

.. code-block:: python

    text = nib.Text("Hello")
    text.content = "World"  # Triggers automatic re-render

    field = nib.TextField(value="")
    field.value = "new value"  # Also triggers re-render

Event Handling
~~~~~~~~~~~~~~

Handle user interactions with callbacks:

.. code-block:: python

    def on_click():
        print("Button clicked!")

    button = nib.Button("Click Me", action=on_click)

    def on_change(new_value: str):
        print(f"Value changed to: {new_value}")

    field = nib.TextField(value="", on_change=on_change)

App Features
------------

Notifications
~~~~~~~~~~~~~

Send macOS system notifications:

.. code-block:: python

    app.notify("Title", "Body text")

    # With more options
    app.notify(
        title="Download Complete",
        body="File saved successfully",
        subtitle="Downloader",
        sound=True,
    )

Keyboard Shortcuts
~~~~~~~~~~~~~~~~~~

Register global hotkeys:

.. code-block:: python

    app.on_hotkey("cmd+shift+n", my_function)

    # Or use the decorator
    @app.hotkey("cmd+k")
    def quick_action():
        pass

Menu Bar Context Menu
~~~~~~~~~~~~~~~~~~~~~

Add a right-click menu to your app:

.. code-block:: python

    app.menu = [
        nib.MenuItem("Settings", action=open_settings, icon="gear"),
        nib.MenuItem("Check for Updates", action=check_updates),
        nib.MenuDivider(),
        nib.MenuItem("Quit", action=app.quit),
    ]

File Dialogs
~~~~~~~~~~~~

Open or save files:

.. code-block:: python

    def on_files(paths: list[str]):
        print(f"Selected: {paths}")

    app.open_file_dialog(
        callback=on_files,
        title="Select files",
        types=["txt", "md"],
        multiple=True,
    )

    app.save_file_dialog(
        callback=lambda path: print(f"Save to: {path}"),
        title="Save as",
        default_name="untitled.txt",
    )

Clipboard
~~~~~~~~~

Read and write to the system clipboard:

.. code-block:: python

    # Write to clipboard
    app.clipboard = "Hello World"

    # Read from clipboard (async)
    app.get_clipboard(lambda text: print(f"Clipboard: {text}"))

Next Steps
----------

- Explore the :doc:`API Reference <api/modules>` for detailed documentation
- Check out the example apps in the ``examples/`` directory
- Learn about available :class:`views <nib.View>`, :class:`controls <nib.Button>`,
  and :class:`shapes <nib.Circle>`
