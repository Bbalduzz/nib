Menu
====

Right-click on the menu bar icon to show a context menu. Configure it with ``MenuItem``
and ``MenuDivider``.

Quick Start
-----------

.. code-block:: python

    import nib

    def main(app: nib.App):
        def open_settings():
            print("Settings clicked")

        app.menu = [
            nib.MenuItem("Settings", action=open_settings, icon="gear"),
            nib.MenuItem("Check for Updates", action=check_updates),
            nib.MenuDivider(),
            nib.MenuItem("Quit", action=app.quit),
        ]

        app.build(nib.Text("Hello"))

    nib.run(main)

MenuItem
--------

.. autoclass:: nib.MenuItem
   :members:
   :undoc-members:
   :show-inheritance:

**Parameters:**

- ``title`` - The text displayed in the menu item
- ``action`` - Callback function when clicked
- ``icon`` - Optional SF Symbol name (e.g., "gear", "star.fill")

MenuDivider
-----------

A visual separator line between menu items.

.. autoclass:: nib.MenuDivider
   :members:
   :undoc-members:
   :show-inheritance:

Examples
--------

**Basic Menu**

.. code-block:: python

    app.menu = [
        nib.MenuItem("Action 1", action=action1),
        nib.MenuItem("Action 2", action=action2),
        nib.MenuDivider(),
        nib.MenuItem("Quit", action=app.quit),
    ]

**Menu with Icons**

.. code-block:: python

    app.menu = [
        nib.MenuItem("Settings", action=settings, icon="gear"),
        nib.MenuItem("Profile", action=profile, icon="person.circle"),
        nib.MenuItem("Help", action=help, icon="questionmark.circle"),
        nib.MenuDivider(),
        nib.MenuItem("Quit", action=app.quit, icon="power"),
    ]
