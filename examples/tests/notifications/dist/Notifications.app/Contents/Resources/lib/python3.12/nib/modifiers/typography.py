"""Typography modifiers: font, fontWeight."""

from typing import Any, Dict, Optional

from ..types import Font, _resolve_weight
from .registry import ModifierRegistry


@ModifierRegistry.modifier("font", ["font", "font_weight"])
def apply_font(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply font modifier."""
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
