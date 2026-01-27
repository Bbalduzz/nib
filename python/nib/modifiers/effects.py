"""Effects modifiers for visual effects and transformations.

This module provides modifiers that add visual effects to views, including
shadows, borders, clipping, animations, transitions, blend modes, and
scaling. These modifiers map to various SwiftUI view modifiers for
creating rich visual experiences.

The effects modifiers support:
    - Shadows with configurable color, radius, and offset
    - Borders with color and width
    - Clip shapes for masking view content
    - Animations for property changes
    - Transitions for view appearance/disappearance
    - Content transitions for content changes
    - Blend modes for compositing
    - Scale transformations

Example:
    Using effects modifiers::

        import nib

        # Shadow effect
        card = nib.VStack(
            controls=[...],
            shadow_color="#000000",
            shadow_radius=10,
            shadow_x=0,
            shadow_y=4
        )

        # Border
        box = nib.Rectangle(
            fill="white",
            border_color="#CCCCCC",
            border_width=1
        )

        # Clip shape
        avatar = nib.Image(
            "profile.png",
            clip_shape="circle"
        )

        # Animation
        animated = nib.Text(
            "Fade In",
            animation=nib.Animation.easeInOut(0.3)
        )

        # Scale
        zoomed = nib.Image("icon.png", scale=1.5)

Attributes:
    apply_shadow: Modifier function for shadow effects.
    apply_border: Modifier function for view borders.
    apply_clip_shape: Modifier function for shape clipping.
    apply_animation: Modifier function for animations.
    apply_content_transition: Modifier function for content transitions.
    apply_transition: Modifier function for view transitions.
    apply_blend_mode: Modifier function for blend modes.
    apply_scale: Modifier function for scale transformations.
"""

from typing import Any, Dict, Optional, Union

from ..types import Animation, resolve_color
from .registry import ModifierRegistry


def _float(value: Optional[Union[int, float]]) -> Optional[float]:
    """Convert a numeric value to float for MessagePack compatibility.

    The Swift runtime expects floating-point values for numeric parameters.
    This helper ensures integers are properly converted while preserving
    None values for optional parameters.

    Args:
        value: A numeric value (int or float) or None.

    Returns:
        The value converted to float, or None if the input was None.

    Example:
        >>> _float(10)
        10.0
        >>> _float(None)
        None
    """
    return float(value) if value is not None else None


def _resolve_shape(shape) -> tuple:
    """Extract shape type and corner radius from a shape view or string.

    Clip shapes can be specified either as a string (e.g., "circle", "capsule")
    or as a shape View object (e.g., nib.RoundedRectangle(corner_radius=10)).
    This function normalizes both formats into a (shape_type, corner_radius) tuple.

    Args:
        shape: Either a string naming the shape type, or a shape View object
            with a _type attribute and optional _corner_radius attribute.

    Returns:
        A tuple of (shape_type, corner_radius) where:
        - shape_type is a lowercase string like "circle", "capsule", "roundedrectangle"
        - corner_radius is a float or None

    Example:
        >>> _resolve_shape("circle")
        ('circle', None)
        >>> _resolve_shape(nib.RoundedRectangle(corner_radius=10))
        ('roundedrectangle', 10)
        >>> _resolve_shape(None)
        (None, None)
    """
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
    """Apply the shadow modifier for drop shadow effects.

    The shadow modifier adds a drop shadow behind a view. It maps to SwiftUI's
    .shadow() view modifier and supports configuring the shadow's color, blur
    radius, and offset position.

    Default values are applied when individual parameters are not specified:
    - shadow_radius: 4.0 (blur amount)
    - shadow_x: 0.0 (horizontal offset)
    - shadow_y: 2.0 (vertical offset, positive is down)

    This modifier is registered with "shadow_color", "shadow_radius",
    "shadow_x", and "shadow_y" parameters.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            Relevant keys are:
            - "shadow_color": The shadow color (hex or named)
            - "shadow_radius": The blur radius in points
            - "shadow_x": Horizontal offset in points (positive is right)
            - "shadow_y": Vertical offset in points (positive is down)

    Returns:
        A modifier dictionary with type "shadow" and args containing the
        shadow configuration, or None if no shadow parameters are specified.

    Example:
        Basic shadow::

            kwargs = {"shadow_color": "#000000"}
            result = apply_shadow(kwargs)
            # Returns: {
            #     "type": "shadow",
            #     "args": {
            #         "shadowColor": "#000000",
            #         "shadowRadius": 4.0,
            #         "shadowX": 0.0,
            #         "shadowY": 2.0
            #     }
            # }

        Custom shadow::

            kwargs = {
                "shadow_color": "black",
                "shadow_radius": 10,
                "shadow_x": 2,
                "shadow_y": 4
            }
            result = apply_shadow(kwargs)
            # Returns: {
            #     "type": "shadow",
            #     "args": {
            #         "shadowColor": "black",
            #         "shadowRadius": 10.0,
            #         "shadowX": 2.0,
            #         "shadowY": 4.0
            #     }
            # }

        No shadow::

            kwargs = {"fill": "blue"}
            result = apply_shadow(kwargs)
            # Returns: None
    """
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
    """Apply the border modifier for view outlines.

    The border modifier draws a border around a view's bounds. It maps to
    SwiftUI's .border() view modifier. Unlike the stroke modifier (which
    is for shapes), borders work on any view type.

    The border color is required; border_width defaults to 1 point if not
    specified.

    This modifier is registered with "border_color" and "border_width" parameters.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            Relevant keys are:
            - "border_color": The border color (required for modifier to apply)
            - "border_width": The border width in points (defaults to 1)

    Returns:
        A modifier dictionary with type "border" and args containing the
        border configuration, or None if no border color is specified.

    Example:
        Default border width::

            kwargs = {"border_color": "#CCCCCC"}
            result = apply_border(kwargs)
            # Returns: {
            #     "type": "border",
            #     "args": {"borderColor": "#CCCCCC", "borderWidth": 1.0}
            # }

        Custom border width::

            kwargs = {"border_color": "red", "border_width": 2}
            result = apply_border(kwargs)
            # Returns: {
            #     "type": "border",
            #     "args": {"borderColor": "red", "borderWidth": 2.0}
            # }

        No border (even with border_width)::

            kwargs = {"border_width": 2}
            result = apply_border(kwargs)
            # Returns: None (border_color is required)
    """
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
    """Apply the clip shape modifier for masking view content.

    The clip shape modifier masks a view's content to a specified shape.
    It maps to SwiftUI's .clipShape() view modifier. Content outside the
    shape bounds is hidden.

    Shapes can be specified as:
    - A string: "circle", "capsule", "rectangle"
    - A shape View: nib.Circle(), nib.RoundedRectangle(corner_radius=10)

    When using a RoundedRectangle View, its corner_radius is preserved.

    This modifier is registered with the "clip_shape" parameter.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            The relevant key is "clip_shape", which can be:
            - A string naming the shape type
            - A shape View object

    Returns:
        A modifier dictionary with type "clipShape" and args containing
        the shape type and optional corner radius, or None if no clip
        shape is specified.

    Example:
        String clip shape::

            kwargs = {"clip_shape": "circle"}
            result = apply_clip_shape(kwargs)
            # Returns: {"type": "clipShape", "args": {"shape": "circle"}}

        Shape View clip::

            kwargs = {"clip_shape": nib.RoundedRectangle(corner_radius=10)}
            result = apply_clip_shape(kwargs)
            # Returns: {
            #     "type": "clipShape",
            #     "args": {"shape": "roundedrectangle", "cornerRadius": 10.0}
            # }

        Capsule clip::

            kwargs = {"clip_shape": "capsule"}
            result = apply_clip_shape(kwargs)
            # Returns: {"type": "clipShape", "args": {"shape": "capsule"}}

        No clip shape::

            kwargs = {"fill": "blue"}
            result = apply_clip_shape(kwargs)
            # Returns: None
    """
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
    """Apply the animation modifier for animating property changes.

    The animation modifier specifies how property changes should be animated.
    It maps to SwiftUI's .animation() view modifier. When a view's properties
    change, this modifier controls the timing and style of the transition.

    Animation objects are created using nib.Animation factory methods:
    - Animation.spring() - Spring animation
    - Animation.easeIn(duration) - Ease-in timing
    - Animation.easeOut(duration) - Ease-out timing
    - Animation.easeInOut(duration) - Ease-in-out timing
    - Animation.linear(duration) - Linear timing

    This modifier is registered with the "animation" parameter.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            The relevant key is "animation", which should be an Animation
            object created using the Animation class factory methods.

    Returns:
        A modifier dictionary with type "animation" and args containing
        the serialized animation configuration, or None if no animation
        is specified.

    Example:
        Spring animation::

            kwargs = {"animation": Animation.spring()}
            result = apply_animation(kwargs)
            # Returns: {"type": "animation", "args": {"animationType": "spring", ...}}

        Timed animation::

            kwargs = {"animation": Animation.easeInOut(0.3)}
            result = apply_animation(kwargs)
            # Returns: {
            #     "type": "animation",
            #     "args": {"animationType": "easeInOut", "duration": 0.3}
            # }

        No animation::

            kwargs = {"opacity": 0.5}
            result = apply_animation(kwargs)
            # Returns: None
    """
    animation = kwargs.get("animation")
    if animation is None:
        return None
    return {"type": "animation", "args": animation.to_dict()}


@ModifierRegistry.modifier("contentTransition", ["content_transition"])
def apply_content_transition(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply the content transition modifier for content changes.

    The content transition modifier specifies how a view's content should
    animate when it changes. It maps to SwiftUI's .contentTransition() view
    modifier. This is useful for text changes, image swaps, and other
    content updates.

    Content transitions can be specified as:
    - A ContentTransition enum value
    - A string naming the transition type

    Common transition types include: "opacity", "interpolate", "numericText"

    This modifier is registered with the "content_transition" parameter.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            The relevant key is "content_transition", which can be:
            - A ContentTransition enum value (with .value attribute)
            - A string naming the transition type

    Returns:
        A modifier dictionary with type "contentTransition" and args
        containing the transition type, or None if no content transition
        is specified.

    Example:
        Enum transition::

            kwargs = {"content_transition": ContentTransition.opacity}
            result = apply_content_transition(kwargs)
            # Returns: {"type": "contentTransition", "args": {"transitionType": "opacity"}}

        String transition::

            kwargs = {"content_transition": "numericText"}
            result = apply_content_transition(kwargs)
            # Returns: {"type": "contentTransition", "args": {"transitionType": "numericText"}}

        No content transition::

            kwargs = {"content": "Hello"}
            result = apply_content_transition(kwargs)
            # Returns: None
    """
    transition = kwargs.get("content_transition")
    if transition is None:
        return None

    value = transition.value if hasattr(transition, "value") else transition
    return {"type": "contentTransition", "args": {"transitionType": value}}


@ModifierRegistry.modifier("transition", ["transition"])
def apply_transition(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply the transition modifier for view appearance/disappearance.

    The transition modifier specifies how a view should animate when it
    appears or disappears from the view hierarchy. It maps to SwiftUI's
    .transition() view modifier.

    Transitions can be specified as:
    - A Transition enum value
    - A string naming the transition type

    Common transition types include: "opacity", "slide", "scale", "move"

    This modifier is registered with the "transition" parameter.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            The relevant key is "transition", which can be:
            - A Transition enum value (with .value attribute)
            - A string naming the transition type

    Returns:
        A modifier dictionary with type "transition" and args containing
        the transition type, or None if no transition is specified.

    Example:
        Enum transition::

            kwargs = {"transition": Transition.slide}
            result = apply_transition(kwargs)
            # Returns: {"type": "transition", "args": {"transitionType": "slide"}}

        String transition::

            kwargs = {"transition": "opacity"}
            result = apply_transition(kwargs)
            # Returns: {"type": "transition", "args": {"transitionType": "opacity"}}

        No transition::

            kwargs = {"content": "Hello"}
            result = apply_transition(kwargs)
            # Returns: None
    """
    transition = kwargs.get("transition")
    if transition is None:
        return None

    value = transition.value if hasattr(transition, "value") else transition
    return {"type": "transition", "args": {"transitionType": value}}


@ModifierRegistry.modifier("blendMode", ["blend_mode"])
def apply_blend_mode(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply the blend mode modifier for compositing.

    The blend mode modifier controls how a view is composited with content
    behind it. It maps to SwiftUI's .blendMode() view modifier.

    Blend modes can be specified as:
    - A BlendMode enum value
    - A string naming the blend mode

    Common blend modes include: "normal", "multiply", "screen", "overlay",
    "darken", "lighten", "colorDodge", "colorBurn", "softLight", "hardLight",
    "difference", "exclusion", "hue", "saturation", "color", "luminosity"

    This modifier is registered with the "blend_mode" parameter.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            The relevant key is "blend_mode", which can be:
            - A BlendMode enum value (with .value attribute)
            - A string naming the blend mode

    Returns:
        A modifier dictionary with type "blendMode" and args containing
        the blend mode, or None if no blend mode is specified.

    Example:
        Enum blend mode::

            kwargs = {"blend_mode": BlendMode.multiply}
            result = apply_blend_mode(kwargs)
            # Returns: {"type": "blendMode", "args": {"mode": "multiply"}}

        String blend mode::

            kwargs = {"blend_mode": "overlay"}
            result = apply_blend_mode(kwargs)
            # Returns: {"type": "blendMode", "args": {"mode": "overlay"}}

        No blend mode::

            kwargs = {"fill": "blue"}
            result = apply_blend_mode(kwargs)
            # Returns: None
    """
    mode = kwargs.get("blend_mode")
    if mode is None:
        return None

    value = mode.value if hasattr(mode, "value") else mode
    return {"type": "blendMode", "args": {"mode": value}}


@ModifierRegistry.modifier("scale", ["scale"])
def apply_scale(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply the scale modifier for size transformations.

    The scale modifier applies a uniform scale transformation to a view.
    It maps to SwiftUI's .scaleEffect() view modifier. The view is scaled
    from its center point.

    Scale values:
    - 1.0 = original size (100%)
    - 0.5 = half size (50%)
    - 2.0 = double size (200%)

    This modifier is registered with the "scale" parameter.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            The relevant key is "scale", which should be a positive number
            representing the scale factor.

    Returns:
        A modifier dictionary with type "scale" and args containing the
        scale factor as a float, or None if no scale is specified.

    Example:
        Scale up::

            kwargs = {"scale": 1.5}
            result = apply_scale(kwargs)
            # Returns: {"type": "scale", "args": {"scale": 1.5}}

        Scale down::

            kwargs = {"scale": 0.5}
            result = apply_scale(kwargs)
            # Returns: {"type": "scale", "args": {"scale": 0.5}}

        No scale::

            kwargs = {"width": 100}
            result = apply_scale(kwargs)
            # Returns: None
    """
    scale = kwargs.get("scale")
    if scale is None:
        return None
    return {"type": "scale", "args": {"scale": float(scale)}}
