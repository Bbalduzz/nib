Link
====

A control that opens a URL when tapped.

.. code-block:: python

    nib.Link("Visit Website", url="https://example.com")

.. autoclass:: nib.Link
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``label`` - The text to display
- ``url`` - The URL to open when clicked

Examples
--------

**Basic Link**

.. code-block:: python

    nib.Link("Open Documentation", url="https://docs.example.com")

**External Resources**

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Link("GitHub", url="https://github.com/example/repo"),
            nib.Link("Documentation", url="https://docs.example.com"),
            nib.Link("Report Issue", url="https://github.com/example/repo/issues"),
        ],
        spacing=8,
    )

**In Footer**

.. code-block:: python

    nib.VStack(
        controls=[
            # Main content
            nib.Text("App content here"),
            nib.Spacer(),
            # Footer with links
            nib.HStack(
                controls=[
                    nib.Link("Privacy", url="https://example.com/privacy"),
                    nib.Text(" | "),
                    nib.Link("Terms", url="https://example.com/terms"),
                ],
            ),
        ],
    )

**Styled Link**

.. code-block:: python

    nib.Link(
        "Learn More",
        url="https://example.com",
        foreground_color=nib.Color.BLUE,
        font=nib.Font.CALLOUT,
    )
