Image
=====

A view that displays an image from a file path or URL.

.. code-block:: python

    nib.Image(path="/path/to/image.png")
    nib.Image(url="https://example.com/image.png")

.. autoclass:: nib.Image
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``path`` - Local file path to the image
- ``url`` - URL of the image to load
- ``content_mode`` - How the image fills its frame (:class:`~nib.ContentMode`)
- ``rendering_mode`` - How the image is rendered (:class:`~nib.ImageRenderingMode`)

Examples
--------

**From File Path**

.. code-block:: python

    nib.Image(path="/Users/me/Pictures/photo.jpg")

**From URL**

.. code-block:: python

    nib.Image(url="https://example.com/avatar.png")

**With Size Constraints**

.. code-block:: python

    nib.Image(
        path="/path/to/image.png",
        width=100,
        height=100,
    )

**Content Modes**

.. code-block:: python

    # Fill the frame, may crop
    nib.Image(
        path="/path/to/image.png",
        content_mode=nib.ContentMode.FILL,
        width=200,
        height=150,
    )

    # Fit within frame, may have letterboxing
    nib.Image(
        path="/path/to/image.png",
        content_mode=nib.ContentMode.FIT,
        width=200,
        height=150,
    )

**Rounded Image**

.. code-block:: python

    nib.Image(
        path="/path/to/avatar.png",
        width=64,
        height=64,
        clip_shape="circle",
    )

**Template Rendering (Tintable)**

.. code-block:: python

    nib.Image(
        path="/path/to/icon.png",
        rendering_mode=nib.ImageRenderingMode.TEMPLATE,
        foreground_color=nib.Color.BLUE,
    )

**Image Gallery Row**

.. code-block:: python

    nib.HStack(
        controls=[
            nib.Image(path=img, width=80, height=80, corner_radius=8)
            for img in image_paths
        ],
        spacing=8,
    )
