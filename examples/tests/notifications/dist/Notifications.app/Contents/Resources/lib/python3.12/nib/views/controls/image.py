"""Image - A view that displays an image from URL, local path, or raw bytes."""

import base64
from typing import Any, Optional, Union

from ..base import View
from ...types import ContentMode, resolve_enum


class Image(View):
    """
    A view that displays an image.

    Supports URL images, local file paths (including assets), and raw bytes.

    Example:
        # URL image
        Image(
            src="https://example.com/image.jpg",
            label="Example image",
            width=100,
            height=100,
            aspect_ratio=ContentMode.FIT,
        )

        # Asset image (auto-resolved from assets/ directory)
        Image(
            src="logo.png",  # Resolves to assets/logo.png
            label="Logo",
        )

        # Nested asset path
        Image(
            src="images/icon.png",  # Resolves to assets/images/icon.png
            label="Icon",
        )

        # Absolute local file
        Image(
            src="/path/to/image.png",
            label="Local image",
            aspect_ratio=ContentMode.FILL,
            corner_radius=8,
        )

        # Raw bytes
        Image(
            src=image_bytes,
            label="Dynamic image",
            antialiased=True,
            blur=5,
        )

        # With clip shape
        Image(
            src="https://example.com/avatar.jpg",
            label="Avatar",
            clip_shape=nib.Circle(),
        )
    """

    _type = "Image"

    def __init__(
        self,
        src: Optional[Union[str, bytes]] = None,
        label: Optional[str] = None,
        # Image-specific styling
        aspect_ratio: Optional[Union[ContentMode, str]] = None,
        antialiased: bool = True,
        blur: Optional[float] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """
        Create an image view.

        Args:
            src: Image source - URL (http/https), local file path, or raw bytes
            label: Accessibility label for the image
            aspect_ratio: How to scale the image (ContentMode.FIT or ContentMode.FILL)
            antialiased: Whether to apply antialiasing (default True)
            blur: Blur radius to apply to the image
            **kwargs: Standard view modifiers (width, height, opacity, corner_radius, clip_shape, etc.)
        """
        super().__init__(**kwargs)
        self._src = src
        self._label = label
        self._aspect_ratio = aspect_ratio
        self._antialiased = antialiased
        self._blur = blur

        # Determine source type and process accordingly
        self._source_type: Optional[str] = None
        self._source_value: Optional[str] = None

        if src is not None:
            self._process_source(src)

    @property
    def src(self) -> Optional[Union[str, bytes]]:
        """Get the image source."""
        return self._src

    @src.setter
    def src(self, value: Optional[Union[str, bytes]]) -> None:
        """Set the image source and trigger re-render."""
        self._src = value
        if value is not None:
            self._process_source(value)
        else:
            self._source_type = None
            self._source_value = None
        self._trigger_update()

    def _process_source(self, src: Union[str, bytes]) -> None:
        """Process the source and determine type."""
        from ...core.app import App

        if isinstance(src, bytes):
            # Raw bytes - encode as base64
            self._source_type = "data"
            self._source_value = base64.b64encode(src).decode("utf-8")
        elif isinstance(src, str):
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
    def label(self) -> Optional[str]:
        """Get the accessibility label."""
        return self._label

    @label.setter
    def label(self, value: Optional[str]) -> None:
        """Set the accessibility label and trigger re-render."""
        self._label = value
        self._trigger_update()

    def _get_props(self) -> dict:
        props = {}

        # Source info
        if self._source_type:
            props["sourceType"] = self._source_type
            props["sourceValue"] = self._source_value

        # Accessibility label
        if self._label:
            props["label"] = self._label

        # Image styles
        image_styles = {}

        if self._aspect_ratio is not None:
            aspect = resolve_enum(self._aspect_ratio)
            if aspect == "fit":
                image_styles["scaledToFit"] = True
            elif aspect == "fill":
                image_styles["scaledToFill"] = True
            # Always make resizable when aspect ratio is set
            image_styles["resizable"] = True

        if not self._antialiased:
            image_styles["antialiased"] = False

        if self._blur is not None:
            image_styles["blur"] = float(self._blur)

        if image_styles:
            props["imageStyles"] = image_styles

        return props
