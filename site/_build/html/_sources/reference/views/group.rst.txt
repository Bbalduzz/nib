Group
=====

A transparent container that groups views without affecting layout.

Use ``Group`` to apply modifiers to multiple views at once or to return
multiple views from a conditional.

.. code-block:: python

    nib.Group(
        controls=[
            nib.Text("First"),
            nib.Text("Second"),
        ],
        foreground_color=nib.Color.BLUE,
    )

.. autoclass:: nib.Group
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``controls`` - List of child views

Examples
--------

**Apply Modifier to Multiple Views**

.. code-block:: python

    nib.Group(
        controls=[
            nib.Text("Title"),
            nib.Text("Subtitle"),
            nib.Text("Description"),
        ],
        foreground_color=nib.Color.SECONDARY,
        padding=8,
    )

**Conditional Content**

.. code-block:: python

    def get_content(is_logged_in: bool):
        if is_logged_in:
            return nib.Group(
                controls=[
                    nib.Text("Welcome back!"),
                    nib.Button("Logout", action=logout),
                ],
            )
        else:
            return nib.Group(
                controls=[
                    nib.Text("Please log in"),
                    nib.Button("Login", action=login),
                ],
            )
