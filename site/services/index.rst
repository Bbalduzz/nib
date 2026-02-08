System Services
===============

Access macOS system information and features.

Battery
-------

Monitor battery status.

.. code-block:: python

    from nib.services import Battery

    battery = Battery()

    # Get current status
    level = battery.level          # 0-100
    is_charging = battery.is_charging
    is_plugged = battery.is_plugged_in
    time_remaining = battery.time_remaining  # Minutes or -1

    # Subscribe to changes
    def on_battery_change(level: int, is_charging: bool):
        print(f"Battery: {level}%, charging: {is_charging}")

    battery.on_change = on_battery_change

    # Start monitoring
    battery.start()

    # Stop when done
    battery.stop()

Screen
------

Get display information.

.. code-block:: python

    from nib.services import Screen

    screen = Screen()

    # Main screen info
    width = screen.width
    height = screen.height
    scale = screen.scale_factor    # 2.0 for Retina
    name = screen.name

    # All screens
    for s in Screen.all_screens():
        print(f"{s.name}: {s.width}x{s.height}")

    # Menu bar height
    menu_height = screen.menu_bar_height

Connectivity
------------

Monitor network status.

.. code-block:: python

    from nib.services import Connectivity

    conn = Connectivity()

    # Current status
    is_connected = conn.is_connected
    is_wifi = conn.is_wifi
    is_cellular = conn.is_cellular
    is_expensive = conn.is_expensive

    # Subscribe to changes
    def on_connectivity_change(connected: bool):
        print(f"Connected: {connected}")

    conn.on_change = on_connectivity_change
    conn.start()

Keychain
--------

Secure storage for credentials.

.. code-block:: python

    from nib.services import Keychain

    keychain = Keychain(service="com.myapp.credentials")

    # Save password
    keychain.set("api_key", "secret123")

    # Read password
    api_key = keychain.get("api_key")

    # Delete
    keychain.delete("api_key")

    # Check if exists
    if keychain.contains("api_key"):
        print("Key exists")

Camera
------

Capture photos and video.

.. code-block:: python

    from nib.services import Camera

    camera = Camera()

    # Capture photo
    def on_photo(data: bytes):
        with open("photo.jpg", "wb") as f:
            f.write(data)

    camera.capture_photo(callback=on_photo)

    # Check availability
    if camera.is_available:
        print("Camera ready")

Use with ``CameraPreview`` view for live feed:

.. code-block:: python

    nib.CameraPreview(width=320, height=240)

UserDefaults
------------

Persistent key-value storage.

.. code-block:: python

    from nib import UserDefaults

    defaults = UserDefaults()

    # Set values (supports str, int, float, bool, list, dict)
    defaults["username"] = "john"
    defaults["volume"] = 0.8
    defaults["dark_mode"] = True
    defaults["recent_files"] = ["/path/a", "/path/b"]
    defaults["settings"] = {"key": "value"}

    # Get values with default
    username = defaults.get("username", "guest")
    volume = defaults.get("volume", 1.0)

    # Check existence
    if "username" in defaults:
        print(f"Hello, {defaults['username']}")

    # Delete
    del defaults["username"]

    # Custom suite (app group)
    shared = UserDefaults(suite="group.com.myapp.shared")

Example: Settings App
---------------------

.. code-block:: python

    import nib
    from nib import UserDefaults
    from nib.services import Battery, Screen

    def main(app: nib.App):
        app.title = "System Info"
        app.icon = nib.SFSymbol("gear")
        app.width = 300
        app.height = 400

        defaults = UserDefaults()
        battery = Battery()
        screen = Screen()

        # Create views
        battery_text = nib.Text(f"Battery: {battery.level}%")
        screen_text = nib.Text(f"Screen: {screen.width}x{screen.height}")

        dark_mode = nib.Toggle(
            "Dark Mode",
            value=defaults.get("dark_mode", False),
            on_change=lambda v: defaults.__setitem__("dark_mode", v),
        )

        # Update battery on change
        def update_battery(level, charging):
            status = "⚡" if charging else ""
            battery_text.content = f"Battery: {level}% {status}"

        battery.on_change = update_battery
        battery.start()

        app.build(
            nib.VStack(
                controls=[
                    nib.Text("System Info", font=nib.Font.TITLE),
                    nib.Divider(),
                    battery_text,
                    screen_text,
                    nib.Divider(),
                    nib.Text("Settings", font=nib.Font.HEADLINE),
                    dark_mode,
                ],
                spacing=12,
                padding=16,
            )
        )

        app.on_quit = battery.stop

    nib.run(main)
