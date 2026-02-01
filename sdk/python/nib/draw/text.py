"""Text drawing primitive for Canvas.

This module provides the Text primitive for drawing text on a Canvas.

All color values accept either:
- Hex strings: "#FF0000", "#ff0000", "FF0000"
- nib.Color objects: nib.Color.RED, nib.Color(hex="#FF0000")

Example:
    Drawing text with nib types::

        import nib

        canvas.draw([
            nib.draw.Text("Hello World", x=10, y=50, fill=nib.Color.WHITE),
            nib.draw.Text(
                "Styled Text",
                x=10, y=100,
                font=nib.Font.system(24, weight=nib.FontWeight.BOLD),
                fill=nib.Color.GREEN,
                alignment=nib.HorizontalAlignment.CENTER,
            ),
        ])
"""

from dataclasses import dataclass
from typing import Optional, Any, Union

from .primitives import DrawCommand
from .paint import _resolve_color_to_hex
from ..types import ColorLike, HorizontalAlignment, Font, TextStyle, resolve_enum


@dataclass
class Text(DrawCommand):
    """A text drawing command.

    Args:
        content: The text string to draw.
        x: X coordinate of the text origin.
        y: Y coordinate of the text origin.
        font: Font configuration (nib.Font instance or None for system default).
        fill: Text color (hex string or nib.Color).
        alignment: Text alignment (nib.HorizontalAlignment or string "left"/"center"/"right").
        opacity: Opacity from 0.0 to 1.0.
        style: Optional nib.TextStyle for additional text styling.

    Example:
        Simple text with nib.Color::

            nib.draw.Text("Hello", x=10, y=50, fill=nib.Color.BLACK)

        Styled text with nib.Font and alignment::

            nib.draw.Text(
                "Bold Title",
                x=100, y=50,
                font=nib.Font.system(20, weight=nib.FontWeight.BOLD),
                fill=nib.Color.RED,
                alignment=nib.HorizontalAlignment.CENTER,
            )
    """

    content: str
    x: float
    y: float
    font: Optional[Font] = None
    fill: ColorLike = "#000000"
    alignment: Union[HorizontalAlignment, str] = "left"
    opacity: float = 1.0
    style: Optional[TextStyle] = None

    def to_dict(self) -> dict:
        # Resolve alignment (HorizontalAlignment enum or string)
        alignment_value = resolve_enum(self.alignment) or "left"

        result = {
            "type": "text",
            "content": self.content,
            "x": self.x,
            "y": self.y,
            "fill": _resolve_color_to_hex(self.fill),
            "alignment": alignment_value,
            "opacity": self.opacity,
        }

        # Add font config if provided
        if self.font is not None:
            if hasattr(self.font, "to_dict"):
                result["font"] = self.font.to_dict()
            elif isinstance(self.font, dict):
                result["font"] = self.font

        # Add text style if provided (for additional styling like bold, italic, etc.)
        if self.style is not None:
            if hasattr(self.style, "to_dict"):
                result["textStyle"] = self.style.to_dict()

        return result
