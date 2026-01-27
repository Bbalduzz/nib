"""Video - A view that displays and plays video content."""

from enum import Enum
from typing import Any, Optional, Union

from ..base import View


class VideoGravity(Enum):
    """Video gravity/scaling modes."""

    RESIZE_ASPECT = "resizeAspect"
    """Fit within bounds, preserve aspect ratio (default)."""

    RESIZE_ASPECT_FILL = "resizeAspectFill"
    """Fill bounds, preserve aspect ratio (may clip)."""

    RESIZE = "resize"
    """Stretch to fill bounds (distorts)."""


class Video(View):
    """
    A view that displays and plays video content.

    Supports URL videos and local file paths.

    Example:
        # URL video with autoplay
        Video(
            src="https://example.com/video.mp4",
            autoplay=True,
            width=300,
            height=200,
        )

        # Local file with loop
        Video(
            src="/path/to/video.mp4",
            autoplay=True,
            loop=True,
            muted=True,
        )

        # Video with controls hidden
        Video(
            src="https://example.com/video.mp4",
            controls=False,
            autoplay=True,
            loop=True,
        )

        # Video with gravity (aspect ratio handling)
        Video(
            src="https://example.com/video.mp4",
            gravity="resizeAspectFill",
            width=400,
            height=300,
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
        """
        Create a video view.

        Args:
            src: Video source - URL (http/https) or local file path
            autoplay: Whether to start playing automatically (default False)
            loop: Whether to loop the video (default False)
            muted: Whether to mute audio (default False)
            controls: Whether to show playback controls (default True)
            gravity: Video gravity/scaling mode (VideoGravity enum or string):
                     - VideoGravity.RESIZE_ASPECT (default): Fit within bounds, preserve aspect ratio
                     - VideoGravity.RESIZE_ASPECT_FILL: Fill bounds, preserve aspect ratio (may clip)
                     - VideoGravity.RESIZE: Stretch to fill bounds (distorts)
            **kwargs: Standard view modifiers (width, height, opacity, corner_radius, etc.)
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
        """Get the video source."""
        return self._src

    @src.setter
    def src(self, value: Optional[str]) -> None:
        """Set the video source and trigger re-render."""
        self._src = value
        if value is not None:
            self._process_source(value)
        else:
            self._source_type = None
            self._source_value = None
        self._trigger_update()

    def _process_source(self, src: str) -> None:
        """Process the source and determine type."""
        from ...core.app import App

        if src.startswith(("http://", "https://")):
            # URL
            self._source_type = "url"
            self._source_value = src
        else:
            # Local file path - resolve through assets system
            resolved = App.resolve_asset(src)
            self._source_type = "file"
            self._source_value = resolved

    @property
    def autoplay(self) -> bool:
        """Get autoplay setting."""
        return self._autoplay

    @autoplay.setter
    def autoplay(self, value: bool) -> None:
        """Set autoplay and trigger re-render."""
        self._autoplay = value
        self._trigger_update()

    @property
    def loop(self) -> bool:
        """Get loop setting."""
        return self._loop

    @loop.setter
    def loop(self, value: bool) -> None:
        """Set loop and trigger re-render."""
        self._loop = value
        self._trigger_update()

    @property
    def muted(self) -> bool:
        """Get muted setting."""
        return self._muted

    @muted.setter
    def muted(self, value: bool) -> None:
        """Set muted and trigger re-render."""
        self._muted = value
        self._trigger_update()

    @property
    def controls(self) -> bool:
        """Get controls visibility setting."""
        return self._controls

    @controls.setter
    def controls(self, value: bool) -> None:
        """Set controls visibility and trigger re-render."""
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
