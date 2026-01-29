"""Layout modifiers for view sizing and spacing.

This module provides modifiers that control the size and spacing of views,
including frame dimensions, padding, and margin. These modifiers map to SwiftUI's
.frame() and .padding() view modifiers.

The layout modifiers support:
    - Fixed dimensions (width, height)
    - Minimum and maximum constraints (min_width, max_width, etc.)
    - Uniform padding/margin (single value)
    - Edge-specific padding/margin (top, bottom, leading, trailing)
    - Directional padding/margin (horizontal, vertical)

Note: Padding is applied inside the view's background, while margin is applied
outside (after the background), creating spacing between the view and its siblings.

All numeric values are converted to floats for MessagePack serialization
to ensure compatibility with the Swift runtime.

Example:
    Using frame modifier::

        import nib

        # Fixed size
        box = nib.Rectangle(width=100, height=50)

        # Flexible size with constraints
        container = nib.VStack(
            controls=[...],
            min_width=200,
            max_width=float("inf"),  # Expand to fill available space
            height=300
        )

    Using padding modifier::

        # Uniform padding
        text = nib.Text("Hello", padding=16)

        # Edge-specific padding
        text = nib.Text("Hello", padding={
            "top": 8,
            "bottom": 8,
            "leading": 16,
            "trailing": 16
        })

        # Directional padding
        text = nib.Text("Hello", padding={
            "horizontal": 16,
            "vertical": 8
        })

Attributes:
    apply_frame: Modifier function for view sizing.
    apply_padding: Modifier function for inner spacing (inside background).
    apply_margin: Modifier function for outer spacing (outside background).
"""

from typing import Any, Dict, Optional, Union

from .registry import ModifierRegistry


def _float(value: Optional[Union[int, float]]) -> Optional[float]:
    """Convert a numeric value to float for MessagePack compatibility.

    The Swift runtime expects floating-point values for dimensions. This
    helper ensures integers are properly converted while preserving None
    values for optional parameters.

    Args:
        value: A numeric value (int or float) or None.

    Returns:
        The value converted to float, or None if the input was None.

    Example:
        >>> _float(100)
        100.0
        >>> _float(None)
        None
    """
    return float(value) if value is not None else None


def _resolve_max(value: Optional[Union[float, str]]) -> Optional[Union[float, str]]:
    """Resolve max width/height values, handling infinity.

    SwiftUI's .frame() modifier accepts .infinity for max dimensions to
    indicate the view should expand to fill available space. This function
    converts Python's float("inf") to the string "infinity" which the Swift
    runtime recognizes.

    Args:
        value: A numeric value, the string "infinity", float("inf"), or None.

    Returns:
        - None if the input is None
        - The string "infinity" if the input represents infinity
        - The value as a float for numeric inputs
        - The original value for other string inputs

    Example:
        >>> _resolve_max(float("inf"))
        'infinity'
        >>> _resolve_max("infinity")
        'infinity'
        >>> _resolve_max(300)
        300.0
        >>> _resolve_max(None)
        None
    """
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
    """Apply the frame modifier for view sizing.

    The frame modifier maps to SwiftUI's .frame() view modifier and controls
    the size of a view. It supports both fixed dimensions and flexible sizing
    with minimum/maximum constraints.

    This modifier is registered with the following parameters:
        - width: Fixed width in points
        - height: Fixed height in points
        - min_width: Minimum width constraint
        - min_height: Minimum height constraint
        - max_width: Maximum width constraint (supports "infinity" or float("inf"))
        - max_height: Maximum height constraint (supports "infinity" or float("inf"))

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            Relevant keys are width, height, min_width, min_height,
            max_width, and max_height.

    Returns:
        A modifier dictionary with type "frame" and args containing the
        dimension values, or None if no frame parameters are specified.

    Example:
        Applying frame to kwargs::

            kwargs = {"width": 100, "height": 50}
            result = apply_frame(kwargs)
            # Returns: {"type": "frame", "args": {"width": 100.0, "height": 50.0}}

            kwargs = {"min_width": 100, "max_width": float("inf")}
            result = apply_frame(kwargs)
            # Returns: {"type": "frame", "args": {"minWidth": 100.0, "maxWidth": "infinity"}}

            kwargs = {"content": "Hello"}  # No frame params
            result = apply_frame(kwargs)
            # Returns: None
    """
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
    """Apply the padding modifier for view spacing.

    The padding modifier maps to SwiftUI's .padding() view modifier and adds
    space around a view's content. It supports three padding styles:

    1. Uniform padding: A single numeric value applies equal padding to all edges
    2. Directional padding: A dict with "horizontal" and/or "vertical" keys
    3. Edge-specific padding: A dict with "top", "bottom", "leading", "trailing" keys

    This modifier is registered with the "padding" parameter.

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            The relevant key is "padding", which can be:
            - A number (int or float) for uniform padding
            - A dict with edge-specific or directional values

    Returns:
        A modifier dictionary with type "padding" and args containing the
        padding values, or None if no padding is specified.

    Example:
        Uniform padding::

            kwargs = {"padding": 16}
            result = apply_padding(kwargs)
            # Returns: {"type": "padding", "args": {"value": 16.0}}

        Edge-specific padding::

            kwargs = {"padding": {"top": 8, "bottom": 8, "leading": 16, "trailing": 16}}
            result = apply_padding(kwargs)
            # Returns: {"type": "padding", "args": {"top": 8.0, "bottom": 8.0, ...}}

        Directional padding::

            kwargs = {"padding": {"horizontal": 16, "vertical": 8}}
            result = apply_padding(kwargs)
            # Returns: {"type": "padding", "args": {"horizontal": 16.0, "vertical": 8.0}}

        No padding::

            kwargs = {"content": "Hello"}
            result = apply_padding(kwargs)
            # Returns: None
    """
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


@ModifierRegistry.modifier("margin", ["margin"])
def apply_margin(kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Apply the margin modifier for outer spacing.

    The margin modifier adds space outside a view's bounds, applied after
    the background. This creates spacing between the view (including its
    background) and surrounding content.

    Unlike padding (which is inside the background), margin creates space
    outside the visual bounds of the view.

    This modifier supports the same format as padding:
    1. Uniform margin: A single numeric value applies equal margin to all edges
    2. Directional margin: A dict with "horizontal" and/or "vertical" keys
    3. Edge-specific margin: A dict with "top", "bottom", "leading", "trailing" keys

    Args:
        kwargs: Dictionary containing the view's constructor parameters.
            The relevant key is "margin", which can be:
            - A number (int or float) for uniform margin
            - A dict with edge-specific or directional values

    Returns:
        A modifier dictionary with type "margin" and args containing the
        margin values, or None if no margin is specified.

    Example:
        Uniform margin::

            kwargs = {"margin": 16}
            result = apply_margin(kwargs)
            # Returns: {"type": "margin", "args": {"value": 16.0}}

        Edge-specific margin::

            kwargs = {"margin": {"top": 8, "bottom": 8}}
            result = apply_margin(kwargs)
            # Returns: {"type": "margin", "args": {"top": 8.0, "bottom": 8.0}}
    """
    margin = kwargs.get("margin")
    if margin is None:
        return None

    if isinstance(margin, dict):
        args = {}
        if "horizontal" in margin:
            args["horizontal"] = _float(margin["horizontal"])
        if "vertical" in margin:
            args["vertical"] = _float(margin["vertical"])
        if "top" in margin:
            args["top"] = _float(margin["top"])
        if "leading" in margin:
            args["leading"] = _float(margin["leading"])
        if "bottom" in margin:
            args["bottom"] = _float(margin["bottom"])
        if "trailing" in margin:
            args["trailing"] = _float(margin["trailing"])
        return {"type": "margin", "args": args}
    else:
        return {"type": "margin", "args": {"value": _float(margin)}}
