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
- **Full macOS Integration**: Notifications, keyboard shortcuts, file dialogs, clipboard, and more

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   getting-started

.. toctree::
   :maxdepth: 2
   :caption: Core

   reference/app
   reference/menu

.. toctree::
   :maxdepth: 2
   :caption: Views - Layout

   reference/views/vstack
   reference/views/hstack
   reference/views/zstack
   reference/views/spacer
   reference/views/scrollview
   reference/views/list
   reference/views/section
   reference/views/group
   reference/views/navigation
   reference/views/disclosure

.. toctree::
   :maxdepth: 2
   :caption: Views - Controls

   reference/views/text
   reference/views/button
   reference/views/textfield
   reference/views/toggle
   reference/views/slider
   reference/views/picker
   reference/views/progressview
   reference/views/label
   reference/views/link
   reference/views/image
   reference/views/video
   reference/views/divider

.. toctree::
   :maxdepth: 2
   :caption: Views - Shapes

   reference/views/rectangle
   reference/views/roundedrectangle
   reference/views/circle
   reference/views/ellipse
   reference/views/capsule

.. toctree::
   :maxdepth: 2
   :caption: Views - Charts

   reference/views/chart
   reference/views/marks

.. toctree::
   :maxdepth: 2
   :caption: Types & Styling

   reference/types/color
   reference/types/font
   reference/types/animation
   reference/types/enums

.. toctree::
   :maxdepth: 2
   :caption: Advanced

   reference/modifiers
   reference/state
   reference/userdefaults


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
