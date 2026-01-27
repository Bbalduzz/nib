Video
=====

A view that displays video content from a file or URL.

.. code-block:: python

    nib.Video(path="/path/to/video.mp4")
    nib.Video(url="https://example.com/video.mp4")

.. autoclass:: nib.Video
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``path`` - Local file path to the video
- ``url`` - URL of the video to load
- ``autoplay`` - Whether to start playing automatically (default: False)
- ``loop`` - Whether to loop playback (default: False)
- ``muted`` - Whether to mute audio (default: False)
- ``gravity`` - How the video fills its frame (:class:`~nib.VideoGravity`)

VideoGravity
------------

.. autoclass:: nib.VideoGravity
   :members:
   :undoc-members:

Examples
--------

**From File Path**

.. code-block:: python

    nib.Video(path="/path/to/video.mp4")

**From URL**

.. code-block:: python

    nib.Video(url="https://example.com/video.mp4")

**Autoplay with Loop**

.. code-block:: python

    nib.Video(
        path="/path/to/background.mp4",
        autoplay=True,
        loop=True,
        muted=True,
    )

**With Size Constraints**

.. code-block:: python

    nib.Video(
        path="/path/to/video.mp4",
        width=320,
        height=240,
    )

**Video Gravity Options**

.. code-block:: python

    # Resize to fill, may crop
    nib.Video(
        path="/path/to/video.mp4",
        gravity=nib.VideoGravity.RESIZEFILL,
    )

    # Resize to fit, may letterbox
    nib.Video(
        path="/path/to/video.mp4",
        gravity=nib.VideoGravity.RESIZEASPECT,
    )

    # Resize to fill while maintaining aspect ratio
    nib.Video(
        path="/path/to/video.mp4",
        gravity=nib.VideoGravity.RESIZEASPECTFILL,
    )

**Background Video**

.. code-block:: python

    nib.ZStack(
        controls=[
            nib.Video(
                url="https://example.com/background.mp4",
                autoplay=True,
                loop=True,
                muted=True,
            ),
            nib.VStack(
                controls=[
                    nib.Text("Welcome", font=nib.Font.LARGE_TITLE),
                ],
            ),
        ],
    )
