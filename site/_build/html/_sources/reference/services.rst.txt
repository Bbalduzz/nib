System Services
===============

Nib provides access to various macOS system services for querying device status
and securely storing credentials.

Battery
-------

Query the device's battery status:

.. code-block:: python

    from nib.services import Battery

    def check_battery(app: nib.App):
        def on_status(info):
            print(f"Level: {info.level}%")
            print(f"Charging: {info.is_charging}")
            print(f"Plugged in: {info.is_plugged_in}")

        Battery.get_status(app, on_status)

The callback receives a ``BatteryInfo`` object with:

- ``level``: Battery percentage (0-100)
- ``is_charging``: Whether the battery is currently charging
- ``is_plugged_in``: Whether the device is connected to power

Connectivity
------------

Check network connectivity status:

.. code-block:: python

    from nib.services import Connectivity

    def check_network(app: nib.App):
        def on_status(info):
            print(f"Connected: {info.is_connected}")
            print(f"Type: {info.connection_type}")  # "wifi", "ethernet", "cellular", "none"
            print(f"WiFi SSID: {info.wifi_ssid}")

        Connectivity.get_status(app, on_status)

The callback receives a ``ConnectivityInfo`` object with:

- ``is_connected``: Whether the device has network connectivity
- ``connection_type``: Type of connection ("wifi", "ethernet", "cellular", "none")
- ``wifi_ssid``: Name of the connected WiFi network (if applicable)

Screen
------

Query display information:

.. code-block:: python

    from nib.services import Screen

    def check_screen(app: nib.App):
        def on_status(info):
            print(f"Brightness: {info.brightness}")
            print(f"Width: {info.width}")
            print(f"Height: {info.height}")
            print(f"Scale: {info.scale}")

        Screen.get_status(app, on_status)

The callback receives a ``ScreenInfo`` object with:

- ``brightness``: Screen brightness (0.0 to 1.0)
- ``width``: Screen width in points
- ``height``: Screen height in points
- ``scale``: Display scale factor (e.g., 2.0 for Retina)

Keychain
--------

Securely store and retrieve credentials using the macOS Keychain:

Saving Credentials
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from nib.services import Keychain

    def save_api_token(app: nib.App, token: str):
        def on_complete(success: bool):
            if success:
                print("Token saved!")
            else:
                print("Failed to save token")

        Keychain.set(
            app,
            service="MyApp",
            account="api_token",
            password=token,
            callback=on_complete,
        )

Retrieving Credentials
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from nib.services import Keychain

    def get_api_token(app: nib.App):
        def on_result(password: str | None):
            if password:
                print(f"Got token: {password}")
            else:
                print("No token found")

        Keychain.get(
            app,
            service="MyApp",
            account="api_token",
            callback=on_result,
        )

Deleting Credentials
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from nib.services import Keychain

    def delete_api_token(app: nib.App):
        def on_complete(success: bool):
            print("Deleted!" if success else "Failed to delete")

        Keychain.delete(
            app,
            service="MyApp",
            account="api_token",
            callback=on_complete,
        )

Checking Existence
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from nib.services import Keychain

    def check_token_exists(app: nib.App):
        def on_result(exists: bool):
            print(f"Token exists: {exists}")

        Keychain.exists(
            app,
            service="MyApp",
            account="api_token",
            callback=on_result,
        )

.. note::

    Keychain items are scoped to your app's bundle identifier. Built apps will use
    their configured ``identifier`` from pyproject.toml.

Launch at Login
---------------

To configure your app to start automatically at login, use the ``launch_at_login``
setting in your ``pyproject.toml``:

.. code-block:: toml

    [tool.nib.build]
    name = "My App"
    launch_at_login = true

See :doc:`build` for more details on build configuration.

.. note::

    Launch at login requires macOS 13+ and works best with signed applications.
    The app registers itself with ``SMAppService`` on first launch.
