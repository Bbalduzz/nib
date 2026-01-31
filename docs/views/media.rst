Media Views
===========

Views for displaying images, video, and web content.

Image
-----

Display images from files, URLs, or SF Symbols.

.. code-block:: python

    # From assets folder
    nib.Image(name="logo.png")

    # From URL
    nib.Image(url="https://example.com/image.jpg")

    # SF Symbol
    nib.Image(
        system_name="star.fill",
        foreground_color=nib.Color.YELLOW,
    )

    # Sized image
    nib.Image(
        name="photo.jpg",
        width=200,
        height=150,
        content_mode=nib.ContentMode.FIT,
    )

**Parameters:**

- ``name`` - Asset image name (from assets/ folder)
- ``url`` - Remote image URL
- ``system_name`` - SF Symbol name
- ``width``, ``height`` - Size constraints
- ``content_mode`` - ``FIT``, ``FILL``
- ``resizable`` - Whether image can resize
- ``foreground_color`` - Tint color for SF Symbols

Video
-----

Play video files with controls.

.. code-block:: python

    # From assets
    nib.Video(
        name="intro.mp4",
        width=400,
        height=300,
        autoplay=True,
        loop=True,
        muted=False,
    )

    # From URL
    nib.Video(
        url="https://example.com/video.mp4",
        controls_visible=True,
    )

**Parameters:**

- ``name`` - Asset video name
- ``url`` - Remote video URL
- ``autoplay`` - Start playing automatically
- ``loop`` - Loop playback
- ``muted`` - Start muted
- ``controls_visible`` - Show playback controls
- ``gravity`` - ``RESIZE_ASPECT``, ``RESIZE_ASPECT_FILL``, ``RESIZE``

CameraPreview
-------------

Live camera feed preview.

.. code-block:: python

    nib.CameraPreview(
        width=320,
        height=240,
    )

Use with the Camera service for capture:

.. code-block:: python

    from nib.services import Camera

    camera = Camera()
    camera.capture_photo(lambda data: print(f"Got {len(data)} bytes"))

WebView
-------

Embedded web browser.

.. code-block:: python

    nib.WebView(
        url="https://example.com",
        width=400,
        height=300,
    )

    # With JavaScript interaction
    def on_message(message: dict):
        print(f"JS says: {message}")

    webview = nib.WebView(
        url="https://example.com",
        on_message=on_message,
    )

    # Execute JavaScript
    webview.evaluate_javascript("document.title")

**Parameters:**

- ``url`` - URL to load
- ``html`` - HTML content to render (alternative to url)
- ``on_message`` - Callback for JavaScript messages
- ``on_navigation`` - Callback for navigation events

Map
---

Interactive Apple Maps view.

.. code-block:: python

    nib.Map(
        latitude=37.7749,
        longitude=-122.4194,
        zoom=12,
        style=nib.MapStyle.STANDARD,
        markers=[
            nib.MapMarker(
                latitude=37.7749,
                longitude=-122.4194,
                title="San Francisco",
            ),
        ],
    )

**Map Styles:** ``STANDARD``, ``SATELLITE``, ``HYBRID``

**Map Overlays:**

.. code-block:: python

    nib.Map(
        latitude=37.7749,
        longitude=-122.4194,
        annotations=[
            nib.MapMarker(lat=37.77, lon=-122.41, title="Point A"),
            nib.MapCircle(
                latitude=37.78,
                longitude=-122.42,
                radius=500,  # meters
                fill_color="#FF000033",
                stroke_color="#FF0000",
            ),
            nib.MapPolyline(
                coordinates=[(37.77, -122.41), (37.78, -122.42), (37.79, -122.41)],
                stroke_color="#0000FF",
                stroke_width=3,
            ),
        ],
    )

**Parameters:**

- ``latitude``, ``longitude`` - Center coordinates
- ``zoom`` - Zoom level (1-20)
- ``style`` - Map style
- ``markers`` - List of MapMarker
- ``annotations`` - List of MapMarker, MapCircle, MapPolyline, MapPolygon
- ``interaction_modes`` - Enabled interactions: ``PAN``, ``ZOOM``, ``ROTATE``, ``PITCH``
