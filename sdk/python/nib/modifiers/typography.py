"""Typography modifiers for text styling.

This module provides modifiers that control text appearance, including font
family, size, weight, and style. These modifiers map to SwiftUI's .font()
view modifier and related typography features.

The typography modifiers support:
    - System fonts with semantic sizes (title, headline, body, etc.)
    - Custom font sizes with Font.system()
    - Font weights (light, regular, medium, semibold, bold, heavy, black)
    - Font design (default, rounded, serif, monospaced)
    - Named fonts (custom font families by name)

Font objects from nib.types provide a fluent interface for building font
configurations that are serialized into modifier dictionaries.

Example:
    Using typography modifiers::

        import nib

        # System font with semantic size
        title = nib.Text("Welcome", font=nib.Font.title)

        # Custom font size
        large = nib.Text("Big Text", font=nib.Font.system(size=24))

        # Font with weight
        bold = nib.Text("Important", font=nib.Font.body, font_weight="bold")

        # Custom font size and weight
        custom = nib.Text(
            "Custom",
            font=nib.Font.system(size=18, weight="semibold")
        )

        # Font design variants
        mono = nib.Text("Code", font=nib.Font.system(size=14, design="monospaced"))

        # Named font (custom font family)
        branded = nib.Text("Brand", font="Helvetica Neue")

Attributes:
    apply_font: Modifier function for font styling.
"""

from typing import Any, Dict, Optional

from ..types import Font, _resolve_weight
from .registry import ModifierRegistry


@ModifierRegistry.modifier("font", ["font", "font_weight"])
def apply_font(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply the font modifier for text styling.

    The font modifier controls the typography of text views. It supports
    multiple input formats:

    1. Font objects: nib.Font.title, nib.Font.system(size=18), etc.
       These are serialized using their to_dict() method.

    2. Font name strings: "Helvetica Neue", "SF Pro", etc.
       These set a custom font family by name.

    3. Font weight: Can be combined with either of the above to override
       or set the font weight independently.

    This modifier is registered with "font" and "font_weight" parameters.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            Relevant keys are:
            - "font": A Font object or font family name string
            - "font_weight": A weight string ("light", "regular", "bold", etc.)
              or a FontWeight enum value

    Returns:
        A modifier dictionary with type "font" and args containing the
        font configuration, or None if neither font nor font_weight is
        specified, or if the args would be empty.

    Example:
        Using a Font object::

            kwargs = {"font": Font.title}
            result = apply_font(kwargs)
            # Returns: {"type": "font", "args": {"fontName": "title"}}

        Using Font.system()::

            kwargs = {"font": Font.system(size=18, weight="bold")}
            result = apply_font(kwargs)
            # Returns: {"type": "font", "args": {"fontSize": 18.0, "fontWeight": "bold"}}

        Using a font name string::

            kwargs = {"font": "Helvetica Neue"}
            result = apply_font(kwargs)
            # Returns: {"type": "font", "args": {"fontName": "Helvetica Neue"}}

        Using font_weight alone::

            kwargs = {"font_weight": "semibold"}
            result = apply_font(kwargs)
            # Returns: {"type": "font", "args": {"fontWeight": "semibold"}}

        Combining font and font_weight::

            kwargs = {"font": Font.body, "font_weight": "bold"}
            result = apply_font(kwargs)
            # Returns: {"type": "font", "args": {"fontName": "body", "fontWeight": "bold"}}

        No font specified::

            kwargs = {"content": "Hello"}
            result = apply_font(kwargs)
            # Returns: None

    Note:
        When both a Font object with a weight and a separate font_weight
        parameter are provided, the font_weight parameter takes precedence
        and overrides the Font object's weight.
    """
    font = kwargs.get("font")
    font_weight = kwargs.get("font_weight")

    if font is None and font_weight is None:
        return None

    args = {}

    if font is not None:
        if isinstance(font, str):
            args["fontName"] = font
        elif isinstance(font, Font):
            args.update(font.to_dict())

    if font_weight is not None:
        args["fontWeight"] = _resolve_weight(font_weight)

    return {"type": "font", "args": args} if args else None
