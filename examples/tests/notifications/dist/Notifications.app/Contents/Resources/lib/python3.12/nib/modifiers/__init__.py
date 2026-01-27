"""
Nib Modifiers Package.

This package provides a declarative modifier registry system.
Import this package to register all built-in modifiers.

Example - Adding a new modifier:

    from nib.modifiers.registry import ModifierRegistry

    @ModifierRegistry.modifier("blur", ["blur_radius"])
    def apply_blur(kwargs):
        radius = kwargs.get("blur_radius")
        if radius is None:
            return None
        return {"type": "blur", "args": {"radius": float(radius)}}
"""

from .registry import ModifierRegistry

# Import modifier modules to register them
from . import layout
from . import appearance
from . import typography
from . import effects

__all__ = ["ModifierRegistry"]
