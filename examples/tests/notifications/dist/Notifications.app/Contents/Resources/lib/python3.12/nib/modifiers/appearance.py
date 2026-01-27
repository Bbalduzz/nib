"""Appearance modifiers: background, foreground, fill, stroke, opacity, cornerRadius."""

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..types import resolve_color

if TYPE_CHECKING:
    from ..views.base import View

from .registry import ModifierRegistry


def _float(value: Optional[Union[int, float]]) -> Optional[float]:
    """Convert numeric value to float for MessagePack compatibility."""
    return float(value) if value is not None else None


@ModifierRegistry.modifier("background", ["background"])
def apply_background(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply background modifier (color only, View backgrounds handled separately)."""
    background = kwargs.get("background")
    if background is None:
        return None

    # Check if it's a View (has _type attribute)
    if hasattr(background, "_type"):
        # View backgrounds are handled separately in View.to_dict()
        return None

    return {"type": "background", "args": {"color": resolve_color(background)}}


@ModifierRegistry.modifier("foregroundColor", ["foreground_color"])
def apply_foreground_color(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply foreground color modifier."""
    color = kwargs.get("foreground_color")
    if color is None:
        return None
    return {"type": "foregroundColor", "args": {"color": resolve_color(color)}}


@ModifierRegistry.modifier("fill", ["fill"])
def apply_fill(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply fill modifier for shapes."""
    fill = kwargs.get("fill")
    if fill is None:
        return None
    return {"type": "fill", "args": {"color": resolve_color(fill)}}


@ModifierRegistry.modifier("stroke", ["stroke", "stroke_width"])
def apply_stroke(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply stroke modifier for shapes."""
    stroke = kwargs.get("stroke")
    if stroke is None:
        return None

    args = {"color": resolve_color(stroke)}
    stroke_width = kwargs.get("stroke_width")
    if stroke_width is not None:
        args["lineWidth"] = _float(stroke_width)

    return {"type": "stroke", "args": args}


@ModifierRegistry.modifier("opacity", ["opacity"])
def apply_opacity(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply opacity modifier."""
    opacity = kwargs.get("opacity")
    if opacity is None:
        return None
    return {"type": "opacity", "args": {"opacity": float(opacity)}}


@ModifierRegistry.modifier("cornerRadius", ["corner_radius"])
def apply_corner_radius(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply corner radius modifier."""
    radius = kwargs.get("corner_radius")
    if radius is None:
        return None
    return {"type": "cornerRadius", "args": {"value": float(radius)}}
