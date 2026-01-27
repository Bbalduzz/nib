Section
=======

A container for grouping content with an optional header and footer.

.. code-block:: python

    nib.Section(
        header=nib.Text("Settings"),
        controls=[
            nib.Toggle("Notifications", value=True),
            nib.Toggle("Dark Mode", value=False),
        ],
    )

.. autoclass:: nib.Section
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``controls`` - List of child views in the section
- ``header`` - Optional header view
- ``footer`` - Optional footer view

Examples
--------

**Section with Header**

.. code-block:: python

    nib.Section(
        header=nib.Text("Account"),
        controls=[
            nib.Text("Username: john_doe"),
            nib.Text("Email: john@example.com"),
        ],
    )

**Section with Header and Footer**

.. code-block:: python

    nib.Section(
        header=nib.Text("Privacy"),
        footer=nib.Text("Your data is stored securely"),
        controls=[
            nib.Toggle("Share Analytics", value=False),
            nib.Toggle("Personalized Ads", value=False),
        ],
    )

**Multiple Sections in a List**

.. code-block:: python

    nib.List(
        controls=[
            nib.Section(
                header=nib.Text("General"),
                controls=[
                    nib.Label("Language", system_image="globe"),
                    nib.Label("Region", system_image="map"),
                ],
            ),
            nib.Section(
                header=nib.Text("Support"),
                controls=[
                    nib.Label("Help Center", system_image="questionmark.circle"),
                    nib.Label("Contact Us", system_image="envelope"),
                ],
            ),
        ],
    )
