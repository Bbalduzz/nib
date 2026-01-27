App
===

The ``App`` class is the main entry point for creating Nib applications. It manages the
application lifecycle, window configuration, and UI rendering.

Quick Start
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

App Class
---------

.. autoclass:: nib.App
   :members:
   :undoc-members:
   :show-inheritance:

run Function
------------

.. autofunction:: nib.run

SFSymbol
--------

SF Symbols are Apple's system icons. Use them for menu bar icons and within your UI.

.. code-block:: python

    # As menu bar icon
    app.icon = nib.SFSymbol("star.fill")

    # In UI with styling
    nib.Label(
        "Favorites",
        system_image="star.fill",
    )

.. autoclass:: nib.SFSymbol
   :members:
   :undoc-members:
   :show-inheritance:

Window Configuration
--------------------

Configure the popover window that appears when clicking the menu bar icon:

.. code-block:: python

    app.title = "My App"      # Window title
    app.width = 300           # Window width in points
    app.height = 400          # Window height in points

System Features
---------------

**Notifications**

.. code-block:: python

    app.notify("Download Complete", "Your file has been saved")

    # With more options
    app.notify(
        title="Download Complete",
        body="File saved to Downloads",
        subtitle="Downloader",
        sound=True,
    )

**Clipboard**

.. code-block:: python

    # Write to clipboard
    app.clipboard = "Hello World"

    # Read from clipboard (async)
    app.get_clipboard(lambda text: print(f"Got: {text}"))

**Keyboard Shortcuts**

.. code-block:: python

    # Register global hotkey
    app.on_hotkey("cmd+shift+n", show_window)

    # Using decorator
    @app.hotkey("cmd+k")
    def quick_action():
        pass

**File Dialogs**

.. code-block:: python

    # Open file picker
    app.open_file_dialog(
        callback=lambda paths: print(paths),
        title="Select files",
        types=["txt", "md"],
        multiple=True,
    )

    # Save file picker
    app.save_file_dialog(
        callback=lambda path: print(path),
        title="Save as",
        default_name="untitled.txt",
    )
