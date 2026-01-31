Nib Documentation
==================

**Nib** is a Python framework for building native macOS menu bar applications using SwiftUI.

Write macOS status bar apps in Python with a declarative, SwiftUI-inspired API. Python code
communicates with a Swift runtime over Unix sockets using MessagePack serialization.

.. code-block:: python

    import nib

    def main(app: nib.App):
        app.title = "My App"
        app.icon = nib.SFSymbol("star.fill")

        counter = nib.Text("0")

        def increment():
            counter.content = str(int(counter.content) + 1)

        app.build(
            nib.VStack(
                controls=[counter, nib.Button("Add", action=increment)],
                spacing=8,
                padding=16,
            )
        )

    nib.run(main)

Features
--------

- **Declarative UI**: Build interfaces with a SwiftUI-like API
- **Native Performance**: Swift runtime renders actual SwiftUI views
- **Python Logic**: Handle events and state in Python
- **Full macOS Integration**: Notifications, keyboard shortcuts, file dialogs, clipboard
- **Canvas Drawing**: Core Graphics drawing with gestures
- **Charts**: SwiftUI Charts for data visualization
- **Hot Reload**: ``nib run`` for instant development feedback

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   getting-started

.. toctree::
   :maxdepth: 2
   :caption: Core

   core/app
   core/menu
   core/state

.. toctree::
   :maxdepth: 2
   :caption: Views

   views/layout
   views/text
   views/controls
   views/media
   views/shapes
   views/charts
   views/canvas
   views/effects

.. toctree::
   :maxdepth: 2
   :caption: Reference

   types/index
   services/index
   building


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
