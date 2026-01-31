Building & Distribution
=======================

Package your Nib app as a standalone macOS application.

Development
-----------

Running with Hot Reload
~~~~~~~~~~~~~~~~~~~~~~~

Use ``nib run`` for development with hot reload:

.. code-block:: bash

    nib run my_app.py

    # Watch subdirectories recursively
    nib run my_app.py --recursive

Changes to Python files trigger automatic reload while keeping
the Swift runtime alive.

Running Directly
~~~~~~~~~~~~~~~~

.. code-block:: bash

    python my_app.py

Building the Swift Runtime
--------------------------

Before running apps, build the Swift runtime:

.. code-block:: bash

    cd swift
    swift build -c release

The binary is at ``swift/.build/release/nib-runtime``.

**Runtime Discovery:**

Nib looks for the runtime in this order:

1. ``NIB_RUNTIME`` environment variable
2. System PATH
3. ``~/.local/bin/nib-runtime``
4. ``~/.nib/bin/nib-runtime``
5. ``/usr/local/bin/nib-runtime``
6. ``/opt/homebrew/bin/nib-runtime``
7. Relative to nib package (for development)
8. ``./swift/.build/*/nib-runtime``

Building a Standalone App
-------------------------

Use ``nib build`` to create a ``.app`` bundle:

.. code-block:: bash

    nib build my_app.py

    # With options
    nib build my_app.py \
        --name "My App" \
        --bundle-id "com.mycompany.myapp" \
        --icon icon.icns \
        --output ./dist

**Build Options:**

- ``--name`` - Application name (default: script name)
- ``--bundle-id`` - Bundle identifier
- ``--icon`` - App icon (.icns file)
- ``--output`` - Output directory
- ``--version`` - App version string

Assets
------

Place assets in an ``assets/`` folder next to your script:

.. code-block:: text

    my_app/
    ├── my_app.py
    └── assets/
        ├── icon.png
        ├── logo.png
        └── sounds/
            └── notification.wav

Reference assets by name:

.. code-block:: python

    nib.Image(name="icon.png")
    nib.Image(name="logo.png")

Code Signing
------------

For distribution, sign your app:

.. code-block:: bash

    codesign --deep --force --sign "Developer ID Application: Your Name" \
        "My App.app"

Notarization
------------

For distribution outside the App Store:

.. code-block:: bash

    # Create a zip for notarization
    ditto -c -k --keepParent "My App.app" "My App.zip"

    # Submit for notarization
    xcrun notarytool submit "My App.zip" \
        --keychain-profile "notary-profile" \
        --wait

    # Staple the ticket
    xcrun stapler staple "My App.app"

Distribution
------------

After signing and notarizing:

1. Create a DMG with ``create-dmg`` or similar
2. Or create a zip for direct download
3. Distribute via your website or update mechanism

Dependencies
------------

If your app uses external Python packages:

.. code-block:: bash

    # Create requirements
    pip freeze > requirements.txt

    # Or list dependencies in pyproject.toml
    [project]
    dependencies = [
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
    ]

The build process includes dependencies in the app bundle.

Troubleshooting
---------------

**App doesn't start:**

- Check Console.app for crash logs
- Ensure Swift runtime is accessible
- Verify Python version compatibility (3.10+)

**Assets not found:**

- Ensure assets/ is next to your script
- Use exact filename including extension
- Check file permissions

**Signing fails:**

- Verify your Developer ID certificate
- Check keychain access
- Ensure runtime is also signed

**Notarization fails:**

- Enable hardened runtime
- Include necessary entitlements
- Check for unsigned frameworks
