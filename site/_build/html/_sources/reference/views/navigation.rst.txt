Navigation
==========

Navigation components for creating drill-down interfaces.

NavigationStack
---------------

A container that manages navigation between views.

.. code-block:: python

    nib.NavigationStack(
        content=nib.List(
            controls=[
                nib.NavigationLink(
                    destination=detail_view,
                    label=nib.Text("Item 1"),
                ),
            ],
        ),
    )

.. autoclass:: nib.NavigationStack
   :members:
   :undoc-members:
   :show-inheritance:

NavigationLink
--------------

A button that triggers navigation to a destination view.

.. code-block:: python

    nib.NavigationLink(
        destination=nib.Text("Detail View"),
        label=nib.Text("Go to Details"),
    )

.. autoclass:: nib.NavigationLink
   :members:
   :undoc-members:
   :show-inheritance:

Examples
--------

**Basic Navigation**

.. code-block:: python

    nib.NavigationStack(
        content=nib.List(
            controls=[
                nib.NavigationLink(
                    destination=nib.VStack(
                        controls=[
                            nib.Text("Settings Detail"),
                            nib.Toggle("Enable Feature", value=True),
                        ],
                    ),
                    label=nib.Label("Settings", system_image="gear"),
                ),
                nib.NavigationLink(
                    destination=nib.Text("About this app"),
                    label=nib.Label("About", system_image="info.circle"),
                ),
            ],
        ),
    )

**Navigation with Title**

.. code-block:: python

    nib.NavigationStack(
        title="My App",
        content=nib.VStack(
            controls=[
                nib.NavigationLink(
                    destination=profile_view,
                    label=nib.Text("View Profile"),
                ),
            ],
        ),
    )
