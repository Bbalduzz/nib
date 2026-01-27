"""Layout modifiers: frame, padding."""

from typing import Any, Dict, Optional, Union

from .registry import ModifierRegistry


def _float(value: Optional[Union[int, float]]) -> Optional[float]:
    """Convert numeric value to float for MessagePack compatibility."""
    return float(value) if value is not None else None


def _resolve_max(value: Optional[Union[float, str]]) -> Optional[Union[float, str]]:
    """Resolve max width/height values, handling infinity."""
    if value is None:
        return None
    if value == float("inf") or value == "infinity":
        return "infinity"
    if isinstance(value, (int, float)):
        return float(value)
    return value


@ModifierRegistry.modifier(
    "frame",
    ["width", "height", "min_width", "min_height", "max_width", "max_height"],
)
def apply_frame(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply frame modifier for sizing."""
    width = kwargs.get("width")
    height = kwargs.get("height")
    min_width = kwargs.get("min_width")
    min_height = kwargs.get("min_height")
    max_width = kwargs.get("max_width")
    max_height = kwargs.get("max_height")

    if not any(
        v is not None
        for v in [width, height, min_width, min_height, max_width, max_height]
    ):
        return None

    args = {}
    if width is not None:
        args["width"] = _float(width)
    if height is not None:
        args["height"] = _float(height)
    if min_width is not None:
        args["minWidth"] = _float(min_width)
    if min_height is not None:
        args["minHeight"] = _float(min_height)
    if max_width is not None:
        args["maxWidth"] = _resolve_max(max_width)
    if max_height is not None:
        args["maxHeight"] = _resolve_max(max_height)

    return {"type": "frame", "args": args}


@ModifierRegistry.modifier("padding", ["padding"])
def apply_padding(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply padding modifier."""
    padding = kwargs.get("padding")
    if padding is None:
        return None

    if isinstance(padding, dict):
        args = {}
        if "horizontal" in padding:
            args["horizontal"] = _float(padding["horizontal"])
        if "vertical" in padding:
            args["vertical"] = _float(padding["vertical"])
        if "top" in padding:
            args["top"] = _float(padding["top"])
        if "leading" in padding:
            args["leading"] = _float(padding["leading"])
        if "bottom" in padding:
            args["bottom"] = _float(padding["bottom"])
        if "trailing" in padding:
            args["trailing"] = _float(padding["trailing"])
        return {"type": "padding", "args": args}
    else:
        return {"type": "padding", "args": {"value": _float(padding)}}
