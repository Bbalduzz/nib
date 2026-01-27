"""Image view for displaying images from URLs, files, or raw bytes.

The Image view displays images from various sources including remote URLs,
local file paths, asset references, and raw byte data. It supports aspect
ratio control, blur effects, and shape clipping.

Example:
    URL image::

        nib.Image(
            src="https://example.com/photo.jpg",
            label="Profile photo",
            width=100,
            height=100,
        )

    Asset image (from assets/ directory)::

        nib.Image(
            src="logo.png",  # Resolves to assets/logo.png
            label="App logo",
        )

    Local file with styling::

        nib.Image(
            src="/path/to/image.png",
            aspect_ratio=nib.ContentMode.FIT,
            corner_radius=12,
        )

    Circular avatar::

        nib.Image(
            src=avatar_url,
            label="User avatar",
            clip_shape=nib.Circle(),
            width=48,
            height=48,
        )
"""

import base64
from typing import Any, Optional, Union

from ..base import View
from ...types import ContentMode, resolve_enum


class Image(View):
    """A view that displays an image from various sources.

    Image supports multiple source types:
    - Remote URLs (http:// or https://)
    - Local file paths (absolute paths starting with /)
    - Asset references (relative paths resolved from assets/ directory)
    - Raw bytes (for dynamically generated images)

    The src property is reactive - changing it triggers a UI update with
    the new image.

    Attributes:
        src: The image source (URL, path, or bytes).
        label: Accessibility label for the image.

    Example:
        Remote image with aspect ratio::

            nib.Image(
                src="https://example.com/banner.jpg",
                label="Banner image",
                aspect_ratio=nib.ContentMode.FIT,
                width=300,
            )

        Asset image from project assets::

            nib.Image(
                src="icons/settings.png",  # Resolves to assets/icons/settings.png
                label="Settings icon",
            )

        Dynamic image from bytes::

            nib.Image(
                src=screenshot_bytes,
                label="Screenshot",
                antialiased=True,
            )

        Circular profile picture::

            nib.Image(
                src=user.avatar_url,
                label=f"{user.name}'s avatar",
                clip_shape=nib.Circle(),
                width=64,
                height=64,
            )

        Blurred background image::

            nib.Image(
                src="background.jpg",
                aspect_ratio=nib.ContentMode.FILL,
                blur=10,
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
        """Initialize an Image view.

        Args:
            src: Image source. Supported formats:
                - URL string: "https://example.com/image.jpg" (http or https)
                - Absolute path: "/Users/name/Pictures/photo.png"
                - Asset reference: "logo.png" (resolved to assets/logo.png)
                - Nested asset: "images/icon.png" (resolved to assets/images/icon.png)
                - Raw bytes: bytes object containing image data (PNG, JPEG, etc.)
            label: Accessibility label describing the image content.
                Important for VoiceOver and other assistive technologies.
            aspect_ratio: How to scale the image within its frame. Options:
                - ContentMode.FIT: Scale to fit within bounds, preserving aspect
                  ratio. May leave empty space (letterboxing).
                - ContentMode.FILL: Scale to fill bounds, preserving aspect ratio.
                  May crop edges.
            antialiased: Whether to apply antialiasing for smoother edges.
                Defaults to True. Set to False for pixel-art or sharp edges.
            blur: Blur radius to apply to the image. Higher values create
                stronger blur effects. Useful for backgrounds.
            **kwargs: Standard view modifiers including:
                - width, height: Image dimensions
                - corner_radius: Rounded corners
                - clip_shape: Shape to clip the image (Circle, Capsule, etc.)
                - opacity: Transparency (0.0 to 1.0)
                - shadow_color, shadow_radius: Drop shadow effects

        Example:
            Create a product thumbnail::

                nib.Image(
                    src=product.image_url,
                    label=product.name,
                    aspect_ratio=nib.ContentMode.FIT,
                    width=120,
                    height=120,
                    corner_radius=8,
                    background=nib.Color.gray,
                )
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
        """Get the image source.

        Returns:
            The current image source (URL string, file path, or bytes),
            or None if no source is set.
        """
        return self._src

    @src.setter
    def src(self, value: Optional[Union[str, bytes]]) -> None:
        """Set the image source and trigger re-render.

        Args:
            value: New image source. Can be a URL string, file path,
                asset reference, raw bytes, or None to clear the image.

        Note:
            Changing the source triggers an immediate UI update to display
            the new image.
        """
        self._src = value
        if value is not None:
            self._process_source(value)
        else:
            self._source_type = None
            self._source_value = None
        self._trigger_update()

    def _process_source(self, src: Union[str, bytes]) -> None:
        """Process the source and determine its type.

        Args:
            src: The image source to process.

        Note:
            This method determines whether the source is a URL, local file,
            or raw bytes, and prepares it for transmission to the Swift runtime.
        """
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
        """Get the accessibility label.

        Returns:
            The current accessibility label, or None if not set.
        """
        return self._label

    @label.setter
    def label(self, value: Optional[str]) -> None:
        """Set the accessibility label and trigger re-render.

        Args:
            value: New accessibility label describing the image content.
                Set to None to remove the label.
        """
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
