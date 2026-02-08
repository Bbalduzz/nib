Building & Distribution
=======================

Nib provides tools to build standalone macOS applications from your Python scripts.
Built apps are self-contained and can be distributed without requiring Python to be
installed on the target system.

Building Your App
-----------------

Basic Build
~~~~~~~~~~~

Build a standalone app from your script:

.. code-block:: bash

    nib build myapp.py

This creates a ``.app`` bundle in the ``dist/`` directory.

Build Options
~~~~~~~~~~~~~

.. code-block:: bash

    nib build myapp.py \
        --name "My Application" \
        --icon assets/icon.png \
        --identifier com.example.myapp \
        --version "1.0.0"

Configuration via pyproject.toml
--------------------------------

For project-based configuration, add a ``[tool.nib]`` section to your ``pyproject.toml``:

.. code-block:: toml

    [project]
    name = "my-app"
    version = "1.0.0"
    dependencies = [
        "requests",
        "pillow",
    ]

    [tool.nib]
    # Entry point for the application
    entry = "src/main.py"

    [tool.nib.build]
    # App display name
    name = "My Application"

    # Bundle identifier
    identifier = "com.example.myapp"

    # App version (defaults to project version)
    version = "1.0.0"

    # Icon file path
    icon = "src/assets/icon.png"

    # Minimum macOS version
    min_macos = "13.0"

    # Start app automatically at login (requires signed app)
    launch_at_login = false

    # Target architecture: "arm64" or "x86_64"
    # arch = "arm64"

    # Additional dependencies to include
    # extra_deps = ["some-package"]

Then build with just:

.. code-block:: bash

    nib build

Info.plist Options
~~~~~~~~~~~~~~~~~~

Customize the app's Info.plist via ``[tool.nib.build.plist]``:

.. code-block:: toml

    [tool.nib.build.plist]
    copyright = "Copyright 2025 Your Name"
    category = "public.app-category.utilities"
    notification_style = "banner"  # "banner", "alert", or "none"
    url_schemes = ["myapp"]        # Custom URL schemes

    [tool.nib.build.plist.usage]
    # Privacy usage descriptions
    microphone = "This app needs microphone access for..."
    camera = "This app needs camera access for..."
    location = "This app needs location access for..."

    [tool.nib.build.plist.custom]
    # Arbitrary custom plist keys
    MyCustomKey = "value"

Launch at Login
---------------

To have your app start automatically when the user logs in, set ``launch_at_login = true``
in your pyproject.toml:

.. code-block:: toml

    [tool.nib.build]
    name = "My App"
    launch_at_login = true

**Requirements:**

- macOS 13.0 or later
- App must be properly signed for reliable operation
- For development builds, the registration may not persist across restarts

When enabled, the app registers itself with macOS's ``SMAppService`` on first launch.
This is handled automatically by the runtime - no code changes required.

Bundle Structure
----------------

The built app bundle has this structure:

.. code-block:: text

    MyApp.app/
      Contents/
        Info.plist
        MacOS/
          MyApp           # Swift runtime
          python/         # Embedded Python
            bin/python3
            lib/python3.12/
        Resources/
          AppIcon.icns
          assets/         # Your assets
          app/
            main.py       # Your entry point
            vendor/       # Dependencies

Custom Fonts
~~~~~~~~~~~~

Place font files (``.ttf``, ``.otf``) in your ``assets/`` directory. They will be
automatically registered in the app's Info.plist and available at runtime.

.. code-block:: text

    assets/
      fonts/
        MyFont-Regular.ttf
        MyFont-Bold.ttf

Use them in your app:

.. code-block:: python

    text = nib.Text(
        "Hello",
        font=nib.Font.custom("MyFont-Regular", 16)
    )

Code Signing
------------

For distribution outside the Mac App Store, sign your app with Developer ID:

.. code-block:: bash

    codesign --sign "Developer ID Application: Your Name" \
             --options runtime \
             --deep \
             "dist/My App.app"

For notarization:

.. code-block:: bash

    # Create a zip for notarization
    ditto -c -k --keepParent "dist/My App.app" "My App.zip"

    # Submit for notarization
    xcrun notarytool submit "My App.zip" \
        --apple-id "your@email.com" \
        --team-id "YOUR_TEAM_ID" \
        --password "@keychain:AC_PASSWORD" \
        --wait

    # Staple the ticket
    xcrun stapler staple "dist/My App.app"
