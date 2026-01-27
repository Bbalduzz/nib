"""Modifier registry system for declarative modifier definitions."""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


@dataclass
class ModifierDef:
    """Definition for a modifier."""

    name: str
    params: List[str]
    apply: Callable[[Dict[str, Any]], Optional[Dict[str, Any]]]


class ModifierRegistry:
    """
    Registry for all available view modifiers.

    Modifiers are registered with their parameter names and an apply function
    that takes kwargs and returns a modifier dict if applicable.

    Example:
        @ModifierRegistry.modifier("frame", ["width", "height", "min_width", ...])
        def apply_frame(kwargs):
            if any(kwargs.get(k) is not None for k in ["width", "height"]):
                return {"type": "frame", "args": {...}}
            return None
    """

    _modifiers: Dict[str, ModifierDef] = {}

    @classmethod
    def register(
        cls,
        name: str,
        params: List[str],
        apply_fn: Callable[[Dict[str, Any]], Optional[Dict[str, Any]]],
    ) -> None:
        """
        Register a modifier definition.

        Args:
            name: Unique name for this modifier (e.g., "frame", "padding")
            params: List of parameter names this modifier handles
            apply_fn: Function that takes kwargs and returns modifier dict or None
        """
        cls._modifiers[name] = ModifierDef(name=name, params=params, apply=apply_fn)

    @classmethod
    def modifier(
        cls, name: str, params: List[str]
    ) -> Callable[[Callable], Callable]:
        """
        Decorator to register a modifier.

        Example:
            @ModifierRegistry.modifier("frame", ["width", "height"])
            def apply_frame(kwargs):
                ...
        """

        def decorator(fn: Callable) -> Callable:
            cls.register(name, params, fn)
            return fn

        return decorator

    @classmethod
    def apply_all(cls, kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Apply all registered modifiers to the given kwargs.

        Args:
            kwargs: Dictionary of all parameters passed to a View

        Returns:
            List of modifier dicts to be applied to the view
        """
        modifiers = []
        for mod_def in cls._modifiers.values():
            # Check if any of this modifier's params are present
            if any(kwargs.get(p) is not None for p in mod_def.params):
                result = mod_def.apply(kwargs)
                if result is not None:
                    modifiers.append(result)
        return modifiers

    @classmethod
    def get_all_params(cls) -> List[str]:
        """Get a list of all parameter names handled by registered modifiers."""
        params = []
        for mod_def in cls._modifiers.values():
            params.extend(mod_def.params)
        return params

    @classmethod
    def clear(cls) -> None:
        """Clear all registered modifiers (useful for testing)."""
        cls._modifiers = {}
