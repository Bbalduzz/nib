App
===

The ``App`` class is the main entry point for Nib applications.

Basic Usage
-----------

.. code-block:: python

    import nib

    def main(app: nib.App):
        app.title = "My App"
        app.icon = nib.SFSymbol("star.fill")
        app.width = 300
        app.height = 200

        app.build(
            nib.Text("Hello, World!")
        )

    nib.run(main)

Configuration
-------------

Title & Icon
~~~~~~~~~~~~

.. code-block:: python

    # Window title (shown in tooltip)
    app.title = "My App"

    # Menu bar icon (SF Symbol)
    app.icon = nib.SFSymbol("star.fill")
    app.icon = nib.SFSymbol(
        "star.fill",
        weight=nib.SymbolWeight.BOLD,
        scale=nib.SymbolScale.LARGE,
        rendering=nib.SymbolRenderingMode.HIERARCHICAL,
    )

    # Menu bar icon (custom image from assets/)
    app.icon = "custom_icon.png"

Window Size
~~~~~~~~~~~

.. code-block:: python

    app.width = 300
    app.height = 400

Building the UI
---------------

.. code-block:: python

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Title"),
                nib.Button("Action", action=on_click),
            ],
            spacing=8,
            padding=16,
        )
    )

System Features
---------------

Notifications
~~~~~~~~~~~~~

.. code-block:: python

    # Simple notification
    app.notify("Title", "Body text")

    # With options
    app.notify(
        title="Download Complete",
        body="File saved to Downloads",
        subtitle="Downloader",
        sound=True,
    )

Clipboard
~~~~~~~~~

.. code-block:: python

    # Write to clipboard
    app.clipboard = "Hello World"

    # Read from clipboard (async)
    app.get_clipboard(lambda text: print(f"Got: {text}"))

Keyboard Shortcuts
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Register global hotkey
    app.on_hotkey("cmd+shift+n", show_window)

    # Using decorator
    @app.hotkey("cmd+k")
    def quick_action():
        pass

**Modifier Keys:** ``cmd``, ``ctrl``, ``alt/option``, ``shift``

File Dialogs
~~~~~~~~~~~~

.. code-block:: python

    # Open file picker
    def on_files(paths: list[str]):
        for path in paths:
            print(f"Selected: {path}")

    app.open_file_dialog(
        callback=on_files,
        title="Select files",
        types=["txt", "md", "py"],
        multiple=True,
        directory=False,
    )

    # Save file picker
    app.save_file_dialog(
        callback=lambda path: print(f"Save to: {path}"),
        title="Save as",
        default_name="untitled.txt",
        types=["txt"],
    )

Lifecycle Callbacks
-------------------

.. code-block:: python

    def on_disappear():
        print("Popover closed")

    def on_quit():
        print("App quitting")
        # Clean up resources

    app.on_disappear = on_disappear
    app.on_quit = on_quit

Quitting
--------

.. code-block:: python

    app.quit()

SFSymbol
--------

Apple SF Symbols with customization.

.. code-block:: python

    # Basic symbol
    nib.SFSymbol("star.fill")

    # Customized
    nib.SFSymbol(
        "arrow.down.circle.fill",
        weight=nib.SymbolWeight.SEMIBOLD,
        scale=nib.SymbolScale.LARGE,
        rendering=nib.SymbolRenderingMode.PALETTE,
        primary_color="#FF0000",
        secondary_color="#00FF00",
    )

**Symbol Weights:** ``ULTRALIGHT``, ``THIN``, ``LIGHT``, ``REGULAR``, ``MEDIUM``, ``SEMIBOLD``, ``BOLD``, ``HEAVY``, ``BLACK``

**Symbol Scales:** ``SMALL``, ``MEDIUM``, ``LARGE``

**Rendering Modes:** ``MONOCHROME``, ``MULTICOLOR``, ``HIERARCHICAL``, ``PALETTE``

Find symbols at: https://developer.apple.com/sf-symbols/

run Function
------------

Start the Nib application.

.. code-block:: python

    nib.run(main)

    # With custom socket path
    nib.run(main, socket_path="/tmp/my-app.sock")
