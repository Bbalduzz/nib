DisclosureGroup
===============

An expandable container that shows or hides its content.

.. code-block:: python

    nib.DisclosureGroup(
        label=nib.Text("Advanced Options"),
        content=nib.VStack(
            controls=[
                nib.Toggle("Option 1", value=True),
                nib.Toggle("Option 2", value=False),
            ],
        ),
    )

.. autoclass:: nib.DisclosureGroup
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``label`` - The always-visible label/header
- ``content`` - The content to show when expanded
- ``is_expanded`` - Initial expansion state (default: False)

Examples
--------

**Basic Disclosure**

.. code-block:: python

    nib.DisclosureGroup(
        label=nib.Text("Show More"),
        content=nib.Text("Hidden content that can be revealed"),
    )

**Settings Group**

.. code-block:: python

    nib.DisclosureGroup(
        label=nib.Label("Advanced", system_image="gear"),
        content=nib.VStack(
            controls=[
                nib.Toggle("Debug Mode", value=False),
                nib.Toggle("Verbose Logging", value=False),
                nib.Slider(value=50, range=(0, 100)),
            ],
            spacing=8,
        ),
        is_expanded=False,
    )

**Initially Expanded**

.. code-block:: python

    nib.DisclosureGroup(
        label=nib.Text("Details"),
        content=nib.Text("This is visible by default"),
        is_expanded=True,
    )

**Multiple Disclosure Groups**

.. code-block:: python

    nib.VStack(
        controls=[
            nib.DisclosureGroup(
                label=nib.Text("Section 1"),
                content=nib.Text("Content 1"),
            ),
            nib.DisclosureGroup(
                label=nib.Text("Section 2"),
                content=nib.Text("Content 2"),
            ),
            nib.DisclosureGroup(
                label=nib.Text("Section 3"),
                content=nib.Text("Content 3"),
            ),
        ],
        spacing=8,
    )
