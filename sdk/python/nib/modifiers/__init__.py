"""Nib Modifiers Package - Declarative view styling system.

This package provides a declarative modifier registry system for styling
views in Nib applications. Modifiers are automatically applied to views
based on their constructor parameters, translating Python kwargs into
modifier dictionaries that the Swift runtime can apply.

The modifier system is organized into themed modules:
    - registry: Core ModifierRegistry class and ModifierDef dataclass
    - layout: Frame sizing and padding modifiers
    - appearance: Colors, fills, strokes, opacity, corner radius
    - typography: Font family, size, weight, and style
    - effects: Shadows, borders, clips, animations, transitions, blend modes, scale

How Modifiers Work:
    1. Modifiers are registered with the @ModifierRegistry.modifier decorator
    2. Each modifier declares which parameters it handles
    3. When a View is rendered, ModifierRegistry.apply_all() is called
    4. All matching modifiers generate dictionaries sent to Swift
    5. The Swift runtime applies the modifiers to the SwiftUI view

Built-in Modifier Parameters:
    Layout:
        - width, height, min_width, min_height, max_width, max_height
        - padding (float or dict with edge/direction keys)

    Appearance:
        - background (color string or View)
        - foreground_color
        - fill, stroke, stroke_width (for shapes)
        - opacity
        - corner_radius

    Typography:
        - font (Font object or string)
        - font_weight

    Effects:
        - shadow_color, shadow_radius, shadow_x, shadow_y
        - border_color, border_width
        - clip_shape
        - animation
        - content_transition, transition
        - blend_mode
        - scale

Example:
    Using modifiers in a View::

        import nib

        text = nib.Text(
            "Hello World",
            font=nib.Font.title,
            foreground_color=nib.Color.white,
            background="#262626",
            padding=16,
            corner_radius=8,
            shadow_color="black",
            shadow_radius=4
        )

    Adding a custom modifier::

        from nib.modifiers.registry import ModifierRegistry

        @ModifierRegistry.modifier("blur", ["blur_radius"])
        def apply_blur(kwargs):
            radius = kwargs.get("blur_radius")
            if radius is None:
                return None
            return {"type": "blur", "args": {"radius": float(radius)}}

        # Now you can use blur_radius on any view
        blurred = nib.Image("photo.png", blur_radius=10)

    Programmatic modifier registration::

        from nib.modifiers.registry import ModifierRegistry

        def apply_rotation(kwargs):
            angle = kwargs.get("rotation")
            if angle is None:
                return None
            return {"type": "rotation", "args": {"angle": float(angle)}}

        ModifierRegistry.register("rotation", ["rotation"], apply_rotation)

Attributes:
    ModifierRegistry: The central class for registering and applying modifiers.
        Use ModifierRegistry.modifier() as a decorator or ModifierRegistry.register()
        for programmatic registration.

Note:
    Importing this package automatically registers all built-in modifiers.
    Custom modifiers should be registered before creating any views that
    use them.
"""

from .registry import ModifierRegistry

# Import modifier modules to register them
from . import layout
from . import appearance
from . import typography
from . import effects

__all__ = ["ModifierRegistry"]
