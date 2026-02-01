"""Central modifier registry for view styling.

This module provides the ModifierRegistry class that manages the registration
and application of view modifiers. Modifiers are registered using the
@ModifierRegistry.modifier decorator and are automatically applied to views
based on their constructor parameters.

The modifier system enables declarative view styling in Nib by:
    1. Allowing modifiers to be defined with their parameter names
    2. Automatically detecting which modifiers apply based on kwargs
    3. Generating modifier dictionaries for the Swift runtime

When a View is rendered, the registry examines all constructor kwargs and
applies any registered modifiers whose parameters are present.

Example:
    Registering a custom modifier::

        from nib.modifiers.registry import ModifierRegistry

        @ModifierRegistry.modifier("myModifier", ["value", "enabled"])
        def apply_my_modifier(kwargs):
            value = kwargs.get("value")
            if value is not None:
                return {"type": "myModifier", "args": {"value": value}}
            return None

    Using modifiers in a View::

        import nib

        # The width and padding modifiers are automatically applied
        text = nib.Text("Hello", width=100, padding=16)

Attributes:
    ModifierDef: A dataclass representing a modifier definition.
    ModifierRegistry: The central registry class for managing modifiers.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


@dataclass
class ModifierDef:
    """Definition for a single modifier.

    A ModifierDef encapsulates all the information needed to apply a modifier
    to a view, including its name, the parameters it handles, and the function
    that generates the modifier dictionary.

    Attributes:
        name: The unique identifier for this modifier (e.g., "frame", "padding").
            This name is sent to the Swift runtime to identify the modifier type.
        params: A list of parameter names that this modifier handles. When any
            of these parameters are present in a View's kwargs, the modifier's
            apply function will be called.
        apply: A callable that takes a dictionary of kwargs and returns either
            a modifier dictionary (with "type" and "args" keys) or None if the
            modifier should not be applied.

    Example:
        Creating a ModifierDef directly::

            def apply_opacity(kwargs):
                opacity = kwargs.get("opacity")
                if opacity is None:
                    return None
                return {"type": "opacity", "args": {"opacity": float(opacity)}}

            mod_def = ModifierDef(
                name="opacity",
                params=["opacity"],
                apply=apply_opacity
            )
    """

    name: str
    params: List[str]
    apply: Callable[[Dict[str, Any]], Optional[Dict[str, Any]]]


class ModifierRegistry:
    """Central registry for all available view modifiers.

    ModifierRegistry is a class-level registry that stores all modifier definitions
    and provides methods to register new modifiers and apply them to view kwargs.
    It follows a singleton-like pattern using class methods and class variables.

    The registry supports two ways to register modifiers:
        1. Using the @modifier decorator (recommended)
        2. Using the register() class method directly

    When views are rendered, they call apply_all() with their kwargs to get
    a list of modifier dictionaries that will be sent to the Swift runtime.

    Attributes:
        _modifiers: A class-level dictionary mapping modifier names to their
            ModifierDef instances.

    Example:
        Registering a modifier with the decorator::

            @ModifierRegistry.modifier("frame", ["width", "height", "min_width"])
            def apply_frame(kwargs):
                width = kwargs.get("width")
                height = kwargs.get("height")
                if width is None and height is None:
                    return None
                return {
                    "type": "frame",
                    "args": {"width": width, "height": height}
                }

        Applying modifiers to view kwargs::

            kwargs = {"width": 100, "padding": 16, "content": "Hello"}
            modifiers = ModifierRegistry.apply_all(kwargs)
            # Returns: [{"type": "frame", "args": {...}}, {"type": "padding", ...}]
    """

    _modifiers: Dict[str, ModifierDef] = {}

    @classmethod
    def register(
        cls,
        name: str,
        params: List[str],
        apply_fn: Callable[[Dict[str, Any]], Optional[Dict[str, Any]]],
    ) -> None:
        """Register a modifier definition with the registry.

        This method adds a new modifier to the registry. It is typically called
        indirectly through the @modifier decorator, but can be used directly
        when programmatic registration is needed.

        Args:
            name: Unique identifier for this modifier. This name is used as the
                "type" field in the modifier dictionary sent to Swift. Common
                examples include "frame", "padding", "background", etc.
            params: List of parameter names this modifier handles. When any of
                these parameters are present in a View's kwargs, the modifier's
                apply function will be invoked.
            apply_fn: A callable that takes a dictionary of kwargs and returns
                either a modifier dictionary or None. The returned dictionary
                must have "type" and "args" keys.

        Example:
            Registering a modifier directly::

                def apply_blur(kwargs):
                    radius = kwargs.get("blur_radius")
                    if radius is None:
                        return None
                    return {"type": "blur", "args": {"radius": float(radius)}}

                ModifierRegistry.register("blur", ["blur_radius"], apply_blur)
        """
        cls._modifiers[name] = ModifierDef(name=name, params=params, apply=apply_fn)

    @classmethod
    def modifier(
        cls, name: str, params: List[str]
    ) -> Callable[[Callable], Callable]:
        """Decorator to register a modifier function.

        This is the recommended way to register modifiers. The decorator
        automatically calls register() with the provided name, params, and
        the decorated function.

        Args:
            name: Unique identifier for this modifier (e.g., "frame", "opacity").
            params: List of parameter names this modifier handles.

        Returns:
            A decorator function that registers the decorated function as a
            modifier and returns it unchanged.

        Example:
            Basic modifier registration::

                @ModifierRegistry.modifier("opacity", ["opacity"])
                def apply_opacity(kwargs):
                    opacity = kwargs.get("opacity")
                    if opacity is None:
                        return None
                    return {"type": "opacity", "args": {"opacity": float(opacity)}}

            Modifier with multiple parameters::

                @ModifierRegistry.modifier("shadow", ["shadow_color", "shadow_radius"])
                def apply_shadow(kwargs):
                    color = kwargs.get("shadow_color")
                    radius = kwargs.get("shadow_radius", 4.0)
                    if color is None:
                        return None
                    return {
                        "type": "shadow",
                        "args": {"color": color, "radius": radius}
                    }
        """

        def decorator(fn: Callable) -> Callable:
            cls.register(name, params, fn)
            return fn

        return decorator

    @classmethod
    def apply_all(cls, kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply all registered modifiers to the given kwargs.

        This method iterates through all registered modifiers and checks if any
        of their parameters are present in the kwargs. For each modifier with
        at least one relevant parameter, the apply function is called and any
        non-None result is added to the returned list.

        Args:
            kwargs: Dictionary of all parameters passed to a View constructor.
                This typically includes both view-specific parameters (like
                "content" for Text) and modifier parameters (like "padding").

        Returns:
            A list of modifier dictionaries, each containing "type" and "args"
            keys. This list is used by the View to build the modifier chain
            sent to the Swift runtime.

        Example:
            Applying modifiers to view kwargs::

                kwargs = {
                    "content": "Hello World",
                    "width": 200,
                    "padding": 16,
                    "opacity": 0.8
                }
                modifiers = ModifierRegistry.apply_all(kwargs)
                # Returns something like:
                # [
                #     {"type": "frame", "args": {"width": 200.0}},
                #     {"type": "padding", "args": {"value": 16.0}},
                #     {"type": "opacity", "args": {"opacity": 0.8}}
                # ]
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
        """Get a list of all parameter names handled by registered modifiers.

        This method collects all parameter names from all registered modifiers.
        It is useful for introspection and for determining which kwargs should
        be treated as modifier parameters vs. view-specific parameters.

        Returns:
            A list of all parameter names across all registered modifiers.
            Note that this list may contain duplicates if multiple modifiers
            share parameter names (though this is not recommended).

        Example:
            Getting all modifier parameters::

                params = ModifierRegistry.get_all_params()
                # Returns: ["width", "height", "padding", "opacity", ...]
        """
        params = []
        for mod_def in cls._modifiers.values():
            params.extend(mod_def.params)
        return params

    @classmethod
    def clear(cls) -> None:
        """Clear all registered modifiers from the registry.

        This method removes all modifier definitions from the registry. It is
        primarily useful for testing scenarios where you need to start with
        a clean slate or verify modifier registration behavior.

        Warning:
            Calling this method in production code will break modifier
            application for all views. Only use this in test fixtures.

        Example:
            Using clear() in tests::

                def test_custom_modifier():
                    # Start with clean registry
                    ModifierRegistry.clear()

                    # Register test modifier
                    @ModifierRegistry.modifier("test", ["test_value"])
                    def apply_test(kwargs):
                        return {"type": "test", "args": {}}

                    # Verify registration
                    assert "test" in ModifierRegistry._modifiers
        """
        cls._modifiers = {}
