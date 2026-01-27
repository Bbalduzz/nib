"""Effects modifiers: shadow, border, clipShape, animation, transitions, blendMode, scale."""

from typing import Any, Dict, Optional, Union

from ..types import Animation, resolve_color
from .registry import ModifierRegistry


def _float(value: Optional[Union[int, float]]) -> Optional[float]:
    """Convert numeric value to float for MessagePack compatibility."""
    return float(value) if value is not None else None


def _resolve_shape(shape) -> tuple:
    """Extract shape type and corner radius from a shape view or string."""
    if shape is None:
        return None, None
    if hasattr(shape, "_type"):
        shape_type = shape._type.lower()
        corner_radius = getattr(shape, "_corner_radius", None)
        return shape_type, corner_radius
    return shape, None


@ModifierRegistry.modifier(
    "shadow", ["shadow_color", "shadow_radius", "shadow_x", "shadow_y"]
)
def apply_shadow(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply shadow modifier."""
    color = kwargs.get("shadow_color")
    radius = kwargs.get("shadow_radius")
    x = kwargs.get("shadow_x")
    y = kwargs.get("shadow_y")

    if not any(v is not None for v in [color, radius, x, y]):
        return None

    return {
        "type": "shadow",
        "args": {
            "shadowColor": color,
            "shadowRadius": float(radius) if radius is not None else 4.0,
            "shadowX": float(x) if x is not None else 0.0,
            "shadowY": float(y) if y is not None else 2.0,
        },
    }


@ModifierRegistry.modifier("border", ["border_color", "border_width"])
def apply_border(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply border modifier."""
    color = kwargs.get("border_color")
    if color is None:
        return None

    width = kwargs.get("border_width")
    return {
        "type": "border",
        "args": {
            "borderColor": resolve_color(color),
            "borderWidth": float(width) if width else 1,
        },
    }


@ModifierRegistry.modifier("clipShape", ["clip_shape"])
def apply_clip_shape(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply clip shape modifier."""
    clip_shape = kwargs.get("clip_shape")
    if clip_shape is None:
        return None

    shape_type, shape_radius = _resolve_shape(clip_shape)
    args = {"shape": shape_type}
    if shape_radius is not None:
        args["cornerRadius"] = _float(shape_radius)

    return {"type": "clipShape", "args": args}


@ModifierRegistry.modifier("animation", ["animation"])
def apply_animation(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply animation modifier."""
    animation = kwargs.get("animation")
    if animation is None:
        return None
    return {"type": "animation", "args": animation.to_dict()}


@ModifierRegistry.modifier("contentTransition", ["content_transition"])
def apply_content_transition(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply content transition modifier."""
    transition = kwargs.get("content_transition")
    if transition is None:
        return None

    value = transition.value if hasattr(transition, "value") else transition
    return {"type": "contentTransition", "args": {"transitionType": value}}


@ModifierRegistry.modifier("transition", ["transition"])
def apply_transition(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply transition modifier."""
    transition = kwargs.get("transition")
    if transition is None:
        return None

    value = transition.value if hasattr(transition, "value") else transition
    return {"type": "transition", "args": {"transitionType": value}}


@ModifierRegistry.modifier("blendMode", ["blend_mode"])
def apply_blend_mode(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply blend mode modifier."""
    mode = kwargs.get("blend_mode")
    if mode is None:
        return None

    value = mode.value if hasattr(mode, "value") else mode
    return {"type": "blendMode", "args": {"mode": value}}


@ModifierRegistry.modifier("scale", ["scale"])
def apply_scale(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply scale modifier."""
    scale = kwargs.get("scale")
    if scale is None:
        return None
    return {"type": "scale", "args": {"scale": float(scale)}}
