ShareLink
=========

A button that presents the native macOS share sheet.

.. code-block:: python

    import nib

    share = nib.ShareLink(
        items=["Check out this app!"],
        label="Share",
    )

Parameters
----------

items : list[str]
    Items to share (text, URLs, or file paths).

content : View, optional
    Custom view to use as the button label.

label : str, optional
    Text label for the button (used if content is not provided).

icon : str, optional
    SF Symbol name to display with the label.

subject : str, optional
    Subject line for email shares.

message : str, optional
    Message body for social shares.

Simple Label
------------

.. code-block:: python

    # Text label
    share = nib.ShareLink(
        items=["Hello, world!"],
        label="Share",
    )

    # Label with icon
    share = nib.ShareLink(
        items=["https://example.com"],
        label="Share Link",
        icon="square.and.arrow.up",
    )

Custom View Label
-----------------

For full control over the button's appearance, use the ``content`` parameter:

.. code-block:: python

    share = nib.ShareLink(
        items=["Check out this amazing app!"],
        content=nib.HStack(
            controls=[
                nib.SFSymbol("square.and.arrow.up"),
                nib.Text("Share"),
            ],
            spacing=4,
        ),
    )

Sharing URLs
------------

.. code-block:: python

    share = nib.ShareLink(
        items=["https://github.com/your-repo/nib"],
        label="Share Repository",
    )

Sharing Files
-------------

.. code-block:: python

    share = nib.ShareLink(
        items=["/path/to/document.pdf"],
        label="Share Document",
    )

Multiple Items
--------------

.. code-block:: python

    share = nib.ShareLink(
        items=[
            "Check out these links:",
            "https://example.com/page1",
            "https://example.com/page2",
        ],
        label="Share All",
    )

Example: Share Button
---------------------

.. code-block:: python

    import nib

    def main(app: nib.App):
        app.title = "Share Demo"

        app.build(
            nib.VStack(
                controls=[
                    nib.Text("Share this app with friends!"),
                    nib.ShareLink(
                        items=["I'm using this awesome menu bar app!"],
                        content=nib.HStack(
                            controls=[
                                nib.SFSymbol(
                                    "square.and.arrow.up",
                                    foreground_color=nib.Color.BLUE,
                                ),
                                nib.Text("Share"),
                            ],
                            spacing=8,
                        ),
                    ),
                ],
                spacing=16,
                padding=16,
            )
        )

    nib.run(main)

.. note::

    ShareLink requires macOS 13.0 or later. On older systems, a fallback
    button is provided that opens the share picker manually.
