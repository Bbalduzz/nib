"""Video view for displaying and playing video content.

The Video view displays video content from URLs or local files with playback
controls. It supports autoplay, looping, muting, and various scaling modes.

Example:
    Video with autoplay::

        nib.Video(
            src="https://example.com/intro.mp4",
            autoplay=True,
            width=300,
            height=200,
        )

    Looping background video::

        nib.Video(
            src="background.mp4",
            autoplay=True,
            loop=True,
            muted=True,
            controls=False,
        )

    Video with custom scaling::

        nib.Video(
            src="https://example.com/video.mp4",
            gravity=nib.VideoGravity.RESIZE_ASPECT_FILL,
            width=400,
            height=300,
        )
"""

from enum import Enum
from typing import Any, Optional, Union

from ..base import View


class VideoGravity(Enum):
    """Video gravity/scaling modes for controlling how video fills its frame.

    These modes determine how the video content is scaled and positioned
    within its container bounds.

    Attributes:
        RESIZE_ASPECT: Scale to fit within bounds while preserving aspect ratio.
            This is the default mode. May result in letterboxing (empty space).
        RESIZE_ASPECT_FILL: Scale to fill bounds while preserving aspect ratio.
            May crop edges of the video to fill the entire frame.
        RESIZE: Stretch to fill bounds exactly. This distorts the video if the
            aspect ratios don't match.

    Example:
        Fit video within bounds (letterbox)::

            nib.Video(src=url, gravity=nib.VideoGravity.RESIZE_ASPECT)

        Fill bounds (may crop)::

            nib.Video(src=url, gravity=nib.VideoGravity.RESIZE_ASPECT_FILL)

        Stretch to fill (distorts)::

            nib.Video(src=url, gravity=nib.VideoGravity.RESIZE)
    """

    RESIZE_ASPECT = "resizeAspect"
    """Fit within bounds, preserve aspect ratio (default)."""

    RESIZE_ASPECT_FILL = "resizeAspectFill"
    """Fill bounds, preserve aspect ratio (may clip)."""

    RESIZE = "resize"
    """Stretch to fill bounds (distorts)."""


class Video(View):
    """A view that displays and plays video content.

    Video displays video from URLs or local file paths with optional playback
    controls. It supports autoplay, looping, audio muting, and various scaling
    modes for controlling how the video fills its frame.

    The src, autoplay, loop, muted, and controls properties are reactive -
    changing them triggers a UI update.

    Attributes:
        src: The video source (URL or file path).
        autoplay: Whether video plays automatically.
        loop: Whether video loops when finished.
        muted: Whether audio is muted.
        controls: Whether playback controls are visible.

    Example:
        Basic video player::

            nib.Video(
                src="https://example.com/tutorial.mp4",
                width=640,
                height=360,
            )

        Autoplay video with loop::

            nib.Video(
                src="promo.mp4",
                autoplay=True,
                loop=True,
                width=400,
                height=225,
            )

        Silent background video::

            nib.Video(
                src="ambient.mp4",
                autoplay=True,
                loop=True,
                muted=True,
                controls=False,
                gravity=nib.VideoGravity.RESIZE_ASPECT_FILL,
            )

        Video from assets::

            nib.Video(
                src="videos/intro.mp4",  # Resolves to assets/videos/intro.mp4
                autoplay=True,
            )
    """

    _type = "Video"

    def __init__(
        self,
        src: Optional[str] = None,
        autoplay: bool = False,
        loop: bool = False,
        muted: bool = False,
        controls: bool = True,
        gravity: Optional[Union[VideoGravity, str]] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a Video view.

        Args:
            src: Video source. Supported formats:
                - URL string: "https://example.com/video.mp4" (http or https)
                - Absolute path: "/Users/name/Movies/clip.mp4"
                - Asset reference: "intro.mp4" (resolved to assets/intro.mp4)
                - Nested asset: "videos/tutorial.mp4" (resolved to assets/videos/tutorial.mp4)
            autoplay: Whether to start playing automatically when the video
                loads. Defaults to False. Set to True for background videos
                or automatic playback experiences.
            loop: Whether to restart playback automatically when the video
                ends. Defaults to False. Useful for background videos or
                animated content.
            muted: Whether to mute the audio track. Defaults to False.
                Set to True for silent background videos or when audio
                would be disruptive.
            controls: Whether to show playback controls (play/pause, scrubber,
                volume). Defaults to True. Set to False for background videos
                or when you want a cleaner appearance.
            gravity: How the video scales within its frame. Options:
                - VideoGravity.RESIZE_ASPECT: Fit within bounds, preserve aspect
                  ratio. May show letterboxing. This is the default.
                - VideoGravity.RESIZE_ASPECT_FILL: Fill bounds, preserve aspect
                  ratio. May crop edges.
                - VideoGravity.RESIZE: Stretch to fill bounds exactly. Distorts
                  the video if aspect ratios don't match.
            **kwargs: Standard view modifiers including:
                - width, height: Video player dimensions
                - corner_radius: Rounded corners
                - opacity: Transparency (0.0 to 1.0)
                - padding: Space around the video

        Example:
            Create a video player with controls::

                nib.Video(
                    src="https://example.com/demo.mp4",
                    width=640,
                    height=360,
                    corner_radius=8,
                )
        """
        super().__init__(**kwargs)
        self._src = src
        self._autoplay = autoplay
        self._loop = loop
        self._muted = muted
        self._controls = controls
        # Convert enum to string value
        if isinstance(gravity, VideoGravity):
            self._gravity = gravity.value
        else:
            self._gravity = gravity

        # Determine source type
        self._source_type: Optional[str] = None
        self._source_value: Optional[str] = None

        if src is not None:
            self._process_source(src)

    @property
    def src(self) -> Optional[str]:
        """Get the video source.

        Returns:
            The current video source (URL or file path), or None if not set.
        """
        return self._src

    @src.setter
    def src(self, value: Optional[str]) -> None:
        """Set the video source and trigger re-render.

        Args:
            value: New video source. Can be a URL string, file path,
                asset reference, or None to clear the video.

        Note:
            Changing the source triggers an immediate UI update. The new
            video will begin loading and may reset playback position.
        """
        self._src = value
        if value is not None:
            self._process_source(value)
        else:
            self._source_type = None
            self._source_value = None
        self._trigger_update()

    def _process_source(self, src: str) -> None:
        """Process the source and determine its type.

        Args:
            src: The video source to process.

        Note:
            This method determines whether the source is a URL or local file,
            and prepares it for transmission to the Swift runtime.
        """
        from ...core.app import App

        if src.startswith(("http://", "https://")):
            # URL
            self._source_type = "url"
            self._source_value = src
        else:
            # Local file path - resolve through assets system
            resolved = App.resolve_asset(src)
            if resolved:
                self._source_type = "file"
                self._source_value = resolved
            else:
                # Asset not found
                self._source_type = None
                self._source_value = None

    @property
    def autoplay(self) -> bool:
        """Get autoplay setting.

        Returns:
            True if video plays automatically, False otherwise.
        """
        return self._autoplay

    @autoplay.setter
    def autoplay(self, value: bool) -> None:
        """Set autoplay and trigger re-render.

        Args:
            value: True to enable autoplay, False to disable.
        """
        self._autoplay = value
        self._trigger_update()

    @property
    def loop(self) -> bool:
        """Get loop setting.

        Returns:
            True if video loops when finished, False otherwise.
        """
        return self._loop

    @loop.setter
    def loop(self, value: bool) -> None:
        """Set loop and trigger re-render.

        Args:
            value: True to enable looping, False to disable.
        """
        self._loop = value
        self._trigger_update()

    @property
    def muted(self) -> bool:
        """Get muted setting.

        Returns:
            True if audio is muted, False otherwise.
        """
        return self._muted

    @muted.setter
    def muted(self, value: bool) -> None:
        """Set muted and trigger re-render.

        Args:
            value: True to mute audio, False to unmute.
        """
        self._muted = value
        self._trigger_update()

    @property
    def controls(self) -> bool:
        """Get controls visibility setting.

        Returns:
            True if playback controls are visible, False otherwise.
        """
        return self._controls

    @controls.setter
    def controls(self, value: bool) -> None:
        """Set controls visibility and trigger re-render.

        Args:
            value: True to show playback controls, False to hide them.
        """
        self._controls = value
        self._trigger_update()

    def _get_props(self) -> dict:
        props = {}

        # Source info
        if self._source_type:
            props["sourceType"] = self._source_type
            props["sourceValue"] = self._source_value

        # Video settings
        video_settings = {}

        if self._autoplay:
            video_settings["autoplay"] = True

        if self._loop:
            video_settings["loop"] = True

        if self._muted:
            video_settings["muted"] = True

        if not self._controls:
            video_settings["controls"] = False

        if self._gravity:
            video_settings["gravity"] = self._gravity

        if video_settings:
            props["videoSettings"] = video_settings

        return props
