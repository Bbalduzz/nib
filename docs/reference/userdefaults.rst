UserDefaults
============

Persistent key-value storage using macOS UserDefaults.

.. autoclass:: nib.UserDefaults
   :members:
   :undoc-members:

Usage
-----

.. code-block:: python

    import nib

    # Create a UserDefaults instance
    defaults = nib.UserDefaults()

    # Store values
    defaults.set("username", "john_doe")
    defaults.set("volume", 75)
    defaults.set("dark_mode", True)

    # Retrieve values
    username = defaults.get("username")  # "john_doe"
    volume = defaults.get("volume")  # 75
    dark_mode = defaults.get("dark_mode")  # True

    # With default value
    theme = defaults.get("theme", default="light")

    # Remove a value
    defaults.remove("username")

Supported Types
---------------

UserDefaults supports these Python types:

- ``str`` - Strings
- ``int`` - Integers
- ``float`` - Floating point numbers
- ``bool`` - Booleans
- ``list`` - Lists (of supported types)
- ``dict`` - Dictionaries (with string keys)

Examples
--------

**Remember User Preferences**

.. code-block:: python

    def main(app: nib.App):
        defaults = nib.UserDefaults()

        # Load saved preference or default to False
        dark_mode = defaults.get("dark_mode", default=False)

        toggle = nib.Toggle("Dark Mode", value=dark_mode)

        def on_toggle(value: bool):
            defaults.set("dark_mode", value)

        toggle.on_change = on_toggle

        app.build(toggle)

**Save Window Size**

.. code-block:: python

    def main(app: nib.App):
        defaults = nib.UserDefaults()

        # Restore saved dimensions
        app.width = defaults.get("window_width", default=300)
        app.height = defaults.get("window_height", default=400)

        def save_size():
            defaults.set("window_width", app.width)
            defaults.set("window_height", app.height)

        # Call save_size when user resizes window

**Store Recent Items**

.. code-block:: python

    def main(app: nib.App):
        defaults = nib.UserDefaults()

        # Load recent items
        recent = defaults.get("recent_items", default=[])

        def add_recent(item: str):
            recent.insert(0, item)
            recent = recent[:10]  # Keep last 10
            defaults.set("recent_items", recent)

**API Token Storage**

.. code-block:: python

    def main(app: nib.App):
        defaults = nib.UserDefaults()

        token_field = nib.SecureField(
            value=defaults.get("api_token", default=""),
            placeholder="API Token",
        )

        def save_token():
            defaults.set("api_token", token_field.value)

        app.build(
            nib.VStack(
                controls=[
                    token_field,
                    nib.Button("Save", action=save_token),
                ],
                spacing=8,
            )
        )

Persistence
-----------

Values stored with UserDefaults persist across app launches. They are stored
in the standard macOS user defaults system at:

``~/Library/Preferences/<app-bundle-id>.plist``

.. note::

    UserDefaults is best for small amounts of data like preferences and
    settings. For larger data, consider using file storage or a database.
