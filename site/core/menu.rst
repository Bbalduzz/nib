Context Menu
============

Add a right-click context menu to your menu bar app.

Basic Menu
----------

.. code-block:: python

    def open_settings():
        print("Opening settings...")

    def check_updates():
        print("Checking for updates...")

    app.menu = [
        nib.MenuItem("Settings", action=open_settings, icon="gear"),
        nib.MenuItem("Check for Updates", action=check_updates),
        nib.MenuDivider(),
        nib.MenuItem("Quit", action=app.quit),
    ]

MenuItem
--------

.. code-block:: python

    nib.MenuItem(
        title="Settings",
        action=open_settings,
        icon="gear",              # SF Symbol name
        shortcut="cmd+,",         # Keyboard shortcut
        disabled=False,
    )

**Parameters:**

- ``title`` - Menu item text
- ``action`` - Callback function
- ``icon`` - SF Symbol name (optional)
- ``shortcut`` - Keyboard shortcut string (optional)
- ``disabled`` - Whether the item is grayed out

MenuDivider
-----------

Visual separator between menu items.

.. code-block:: python

    app.menu = [
        nib.MenuItem("Action 1", action=fn1),
        nib.MenuItem("Action 2", action=fn2),
        nib.MenuDivider(),
        nib.MenuItem("Quit", action=app.quit),
    ]

Dynamic Menus
-------------

Update the menu based on state:

.. code-block:: python

    is_connected = False

    def toggle_connection():
        global is_connected
        is_connected = not is_connected
        update_menu()

    def update_menu():
        status = "Disconnect" if is_connected else "Connect"
        icon = "wifi" if is_connected else "wifi.slash"

        app.menu = [
            nib.MenuItem(status, action=toggle_connection, icon=icon),
            nib.MenuDivider(),
            nib.MenuItem("Quit", action=app.quit),
        ]

    update_menu()

Keyboard Shortcuts
------------------

.. code-block:: python

    nib.MenuItem("New Window", action=new_window, shortcut="cmd+n")
    nib.MenuItem("Close", action=close, shortcut="cmd+w")
    nib.MenuItem("Preferences", action=prefs, shortcut="cmd+,")

**Modifier Keys:**

- ``cmd`` - Command key
- ``ctrl`` - Control key
- ``alt`` or ``option`` - Option key
- ``shift`` - Shift key

Combine with ``+``: ``cmd+shift+n``

Complete Example
----------------

.. code-block:: python

    import nib

    def main(app: nib.App):
        app.title = "My App"
        app.icon = nib.SFSymbol("star.fill")

        is_paused = False

        def toggle_pause():
            nonlocal is_paused
            is_paused = not is_paused
            update_menu()
            app.notify(
                "Status Changed",
                "Paused" if is_paused else "Running"
            )

        def update_menu():
            label = "Resume" if is_paused else "Pause"
            icon = "play.fill" if is_paused else "pause.fill"

            app.menu = [
                nib.MenuItem(label, action=toggle_pause, icon=icon),
                nib.MenuItem("Settings", action=lambda: None, icon="gear"),
                nib.MenuDivider(),
                nib.MenuItem("Quit", action=app.quit, shortcut="cmd+q"),
            ]

        update_menu()

        app.build(
            nib.VStack(
                controls=[
                    nib.Text("Right-click the menu bar icon!"),
                ],
                padding=20,
            )
        )

    nib.run(main)
