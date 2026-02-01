"""Appearance modifiers for view styling and visual presentation.

This module provides modifiers that control the visual appearance of views,
including colors, fills, strokes, opacity, and corner radius. These modifiers
map to SwiftUI's appearance-related view modifiers.

The appearance modifiers support:
    - Background colors and views
    - Foreground (text/icon) colors
    - Shape fills and strokes
    - Opacity/transparency
    - Corner radius for rounded corners

Colors can be specified in multiple formats:
    - Hex strings: "#FF0000", "#FF0000FF" (with alpha)
    - Named colors: "red", "blue", "clear"
    - Color objects: nib.Color.red, nib.Color.blue

Example:
    Using appearance modifiers::

        import nib

        # Background and foreground colors
        text = nib.Text(
            "Hello",
            background="#262626",
            foreground_color=nib.Color.white
        )

        # Shape fill and stroke
        circle = nib.Circle(
            fill=nib.Color.blue,
            stroke="#FF0000",
            stroke_width=2
        )

        # Opacity and corner radius
        box = nib.Rectangle(
            fill="blue",
            opacity=0.8,
            corner_radius=10
        )

Attributes:
    apply_background: Modifier function for background colors.
    apply_foreground_color: Modifier function for foreground colors.
    apply_fill: Modifier function for shape fills.
    apply_stroke: Modifier function for shape strokes.
    apply_opacity: Modifier function for view transparency.
    apply_corner_radius: Modifier function for rounded corners.
"""

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..types import resolve_color

if TYPE_CHECKING:
    from ..views.base import View

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
        >>> _float(2)
        2.0
        >>> _float(None)
        None
    """
    return float(value) if value is not None else None


@ModifierRegistry.modifier("background", ["background"])
def apply_background(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply the background modifier for view backgrounds.

    The background modifier sets a color or gradient behind a view's content.
    For non-gradient Views (like RoundedRectangle), backgrounds are handled
    separately in View.to_dict() as background views.

    This modifier is registered with the "background" parameter.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            The relevant key is "background", which can be:
            - A color string (hex like "#FF0000" or named like "red")
            - A Color object (nib.Color.blue)
            - A gradient View (LinearGradient, RadialGradient, etc.)
            - A non-gradient View (handled separately, returns None here)

    Returns:
        A modifier dictionary with type "background" and args containing
        the resolved color or gradient data, or None if:
        - No background is specified
        - The background is a non-gradient View (has _type attribute)

    Example:
        Color background::

            kwargs = {"background": "#FF0000"}
            result = apply_background(kwargs)
            # Returns: {"type": "background", "args": {"color": "#FF0000"}}

        Gradient background::

            kwargs = {"background": nib.LinearGradient(colors=["red", "blue"])}
            result = apply_background(kwargs)
            # Returns: {"type": "background", "args": {"gradientType": "LinearGradient", ...}}

        View background (handled elsewhere)::

            kwargs = {"background": nib.RoundedRectangle(corner_radius=10)}
            result = apply_background(kwargs)
            # Returns: None (View backgrounds handled in View.to_dict())

        No background::

            kwargs = {"content": "Hello"}
            result = apply_background(kwargs)
            # Returns: None
    """
    background = kwargs.get("background")
    if background is None:
        return None

    # Check if it's a gradient View - handle here as modifier
    if hasattr(background, "_type") and background._type in GRADIENT_TYPES:
        args = {"gradientType": background._type}
        args.update(background._get_props())
        return {"type": "background", "args": args}

    # Check if it's a non-gradient View (has _type attribute)
    if hasattr(background, "_type"):
        # Non-gradient View backgrounds are handled separately in View.to_dict()
        return None

    return {"type": "background", "args": {"color": resolve_color(background)}}


@ModifierRegistry.modifier("foregroundColor", ["foreground_color"])
def apply_foreground_color(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply the foreground color modifier for text and icon colors.

    The foreground color modifier sets the color of text, icons, and other
    foreground content within a view. It maps to SwiftUI's .foregroundColor()
    or .foregroundStyle() view modifier.

    This modifier is registered with the "foreground_color" parameter.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            The relevant key is "foreground_color", which can be:
            - A color string (hex like "#FFFFFF" or named like "white")
            - A Color object (nib.Color.white)

    Returns:
        A modifier dictionary with type "foregroundColor" and args containing
        the resolved color, or None if no foreground color is specified.

    Example:
        Setting foreground color::

            kwargs = {"foreground_color": "#FFFFFF"}
            result = apply_foreground_color(kwargs)
            # Returns: {"type": "foregroundColor", "args": {"color": "#FFFFFF"}}

            kwargs = {"foreground_color": nib.Color.blue}
            result = apply_foreground_color(kwargs)
            # Returns: {"type": "foregroundColor", "args": {"color": "blue"}}

        No foreground color::

            kwargs = {"content": "Hello"}
            result = apply_foreground_color(kwargs)
            # Returns: None
    """
    color = kwargs.get("foreground_color")
    if color is None:
        return None
    return {"type": "foregroundColor", "args": {"color": resolve_color(color)}}


GRADIENT_TYPES = ("LinearGradient", "RadialGradient", "AngularGradient", "EllipticalGradient")


@ModifierRegistry.modifier("fill", ["fill"])
def apply_fill(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply the fill modifier for shape interiors.

    The fill modifier sets the interior color or gradient of shape views like
    Rectangle, Circle, Capsule, etc. It maps to SwiftUI's .fill() shape modifier.

    Note: This modifier is intended for shape views. Using it on non-shape
    views may have no effect or unexpected behavior.

    This modifier is registered with the "fill" parameter.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            The relevant key is "fill", which can be:
            - A color string (hex like "#0000FF" or named like "blue")
            - A Color object (nib.Color.blue)
            - A gradient View (LinearGradient, RadialGradient, etc.)

    Returns:
        A modifier dictionary with type "fill" and args containing the
        resolved color or gradient data, or None if no fill is specified.

    Example:
        Filling a shape with color::

            kwargs = {"fill": "#0000FF"}
            result = apply_fill(kwargs)
            # Returns: {"type": "fill", "args": {"color": "#0000FF"}}

        Filling a shape with gradient::

            kwargs = {"fill": nib.LinearGradient(colors=["red", "blue"])}
            result = apply_fill(kwargs)
            # Returns: {"type": "fill", "args": {"gradientType": "LinearGradient", ...}}

        No fill::

            kwargs = {"stroke": "#000000"}
            result = apply_fill(kwargs)
            # Returns: None
    """
    fill = kwargs.get("fill")
    if fill is None:
        return None

    # Check if it's a gradient View
    if hasattr(fill, "_type") and fill._type in GRADIENT_TYPES:
        args = {"gradientType": fill._type}
        # Include gradient props (colors, stops, points, etc.)
        args.update(fill._get_props())
        return {"type": "fill", "args": args}

    # Regular color
    return {"type": "fill", "args": {"color": resolve_color(fill)}}


@ModifierRegistry.modifier("stroke", ["stroke", "stroke_width"])
def apply_stroke(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply the stroke modifier for shape outlines.

    The stroke modifier draws an outline around shape views like Rectangle,
    Circle, Capsule, etc. It maps to SwiftUI's .stroke() shape modifier.

    The stroke color is required; stroke_width is optional and defaults to
    1 point in the Swift runtime if not specified.

    Note: This modifier is intended for shape views. Using it on non-shape
    views may have no effect or unexpected behavior.

    This modifier is registered with "stroke" and "stroke_width" parameters.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            Relevant keys are:
            - "stroke": The stroke color (required for this modifier to apply)
            - "stroke_width": The line width in points (optional)

    Returns:
        A modifier dictionary with type "stroke" and args containing the
        color and optional line width, or None if no stroke color is specified.

    Example:
        Stroke with default width::

            kwargs = {"stroke": "#FF0000"}
            result = apply_stroke(kwargs)
            # Returns: {"type": "stroke", "args": {"color": "#FF0000"}}

        Stroke with custom width::

            kwargs = {"stroke": "#FF0000", "stroke_width": 2}
            result = apply_stroke(kwargs)
            # Returns: {"type": "stroke", "args": {"color": "#FF0000", "lineWidth": 2.0}}

        No stroke (even with stroke_width)::

            kwargs = {"stroke_width": 2}
            result = apply_stroke(kwargs)
            # Returns: None (stroke color is required)
    """
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
    """Apply the opacity modifier for view transparency.

    The opacity modifier controls the transparency of a view and all its
    children. It maps to SwiftUI's .opacity() view modifier.

    Values range from 0.0 (fully transparent) to 1.0 (fully opaque).
    Values outside this range may be clamped by the Swift runtime.

    This modifier is registered with the "opacity" parameter.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            The relevant key is "opacity", which should be a number
            between 0.0 and 1.0.

    Returns:
        A modifier dictionary with type "opacity" and args containing
        the opacity value as a float, or None if no opacity is specified.

    Example:
        Setting opacity::

            kwargs = {"opacity": 0.5}
            result = apply_opacity(kwargs)
            # Returns: {"type": "opacity", "args": {"opacity": 0.5}}

            kwargs = {"opacity": 0}
            result = apply_opacity(kwargs)
            # Returns: {"type": "opacity", "args": {"opacity": 0.0}}

        No opacity::

            kwargs = {"content": "Hello"}
            result = apply_opacity(kwargs)
            # Returns: None
    """
    opacity = kwargs.get("opacity")
    if opacity is None:
        return None
    return {"type": "opacity", "args": {"opacity": float(opacity)}}


@ModifierRegistry.modifier("cornerRadius", ["corner_radius"])
def apply_corner_radius(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply the corner radius modifier for rounded corners.

    The corner radius modifier rounds the corners of a view's bounds.
    It maps to SwiftUI's .cornerRadius() view modifier (or the newer
    .clipShape(.rect(cornerRadius:)) pattern).

    The radius is specified in points. Larger values create more
    pronounced rounding. For pill-shaped views, use a radius equal
    to half the view's height.

    This modifier is registered with the "corner_radius" parameter.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            The relevant key is "corner_radius", which should be a
            positive number representing the radius in points.

    Returns:
        A modifier dictionary with type "cornerRadius" and args containing
        the radius value as a float, or None if no corner radius is specified.

    Example:
        Setting corner radius::

            kwargs = {"corner_radius": 10}
            result = apply_corner_radius(kwargs)
            # Returns: {"type": "cornerRadius", "args": {"value": 10.0}}

            kwargs = {"corner_radius": 25}  # Pill shape for 50pt height
            result = apply_corner_radius(kwargs)
            # Returns: {"type": "cornerRadius", "args": {"value": 25.0}}

        No corner radius::

            kwargs = {"fill": "blue"}
            result = apply_corner_radius(kwargs)
            # Returns: None
    """
    radius = kwargs.get("corner_radius")
    if radius is None:
        return None
    return {"type": "cornerRadius", "args": {"value": float(radius)}}
