Label
=====

A view that displays a title and an icon.

.. code-block:: python

    nib.Label("Downloads", system_image="arrow.down.circle")

.. autoclass:: nib.Label
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``title`` - The text to display
- ``system_image`` - SF Symbol name for the icon
- ``style`` - Label style (:class:`~nib.LabelStyle`)

Examples
--------

**Basic Label**

.. code-block:: python

    nib.Label("Settings", system_image="gear")

**Menu Items**

.. code-block:: python

    nib.List(
        controls=[
            nib.Label("Profile", system_image="person.circle"),
            nib.Label("Settings", system_image="gear"),
            nib.Label("Help", system_image="questionmark.circle"),
        ],
    )

**Status Indicators**

.. code-block:: python

    nib.Label("Connected", system_image="wifi")
    nib.Label("Offline", system_image="wifi.slash")
    nib.Label("Syncing", system_image="arrow.triangle.2.circlepath")

**File Types**

.. code-block:: python

    nib.Label("document.pdf", system_image="doc.fill")
    nib.Label("image.png", system_image="photo")
    nib.Label("archive.zip", system_image="doc.zipper")

**Title Only Style**

.. code-block:: python

    nib.Label(
        "Title Only",
        system_image="star",
        style=nib.LabelStyle.TITLEONLY,
    )

**Icon Only Style**

.. code-block:: python

    nib.Label(
        "Icon Only",
        system_image="star.fill",
        style=nib.LabelStyle.ICONONLY,
    )

**With Colors**

.. code-block:: python

    nib.Label(
        "Error",
        system_image="exclamationmark.triangle",
        foreground_color=nib.Color.RED,
    )

    nib.Label(
        "Success",
        system_image="checkmark.circle",
        foreground_color=nib.Color.GREEN,
    )
