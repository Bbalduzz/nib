"""Image drawing primitive for Canvas.

This module provides the Image primitive for drawing images on a Canvas.

Example:
    Drawing from file::

        with open("image.jpg", "rb") as f:
            canvas.draw([nib.draw.Image(data=f.read(), x=10, y=10)])

    Drawing with PIL::

        from PIL import Image
        import io

        img = Image.open("photo.jpg")
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        canvas.draw([nib.draw.Image(data=buffer.getvalue(), x=0, y=0)])
"""

from dataclasses import dataclass
from typing import Optional

from .primitives import DrawCommand


@dataclass
class Image(DrawCommand):
    """An image drawing command.

    Draws an image on the canvas from raw JPEG/PNG bytes.

    Args:
        data: Raw image bytes (JPEG, PNG, etc.)
        x: X coordinate of top-left corner.
        y: Y coordinate of top-left corner.
        width: Width to draw the image (None = original size).
        height: Height to draw the image (None = original size).
        opacity: Opacity from 0.0 to 1.0.

    Example:
        Drawing from file::

            with open("photo.jpg", "rb") as f:
                nib.draw.Image(data=f.read(), x=0, y=0)

        Drawing with scaling::

            nib.draw.Image(data=jpeg_bytes, x=10, y=10, width=200, height=150)
    """

    data: bytes
    x: float = 0
    y: float = 0
    width: Optional[float] = None
    height: Optional[float] = None
    opacity: float = 1.0

    def to_dict(self) -> dict:
        return {
            "type": "image",
            "data": self.data,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "opacity": self.opacity,
        }
