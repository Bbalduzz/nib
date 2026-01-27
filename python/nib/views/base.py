"""Base View class for Nib views with declarative parameter-based styling.

This module provides the :class:`View` base class that all Nib UI components
inherit from. It implements the modifier system that allows styling views
through constructor parameters.

The View class handles:
    - Modifier application (layout, appearance, animation)
    - View tree serialization for the Swift runtime
    - Reactive updates when properties change
    - Background and overlay view composition

Design Philosophy:
    Nib uses a declarative parameter-based API instead of method chaining.
    All styling is done through constructor parameters, making the code
    more readable and easier to understand.

Example:
    Styling with constructor parameters::

        # Instead of: Text("Hello").font(.title).foregroundColor(.blue)
        # Nib uses:
        nib.Text(
            "Hello",
            font=nib.Font.TITLE,
            foreground_color=nib.Color.BLUE,
            padding=16,
        )

    Container with background::

        nib.VStack(
            controls=[nib.Text("Item 1"), nib.Text("Item 2")],
            spacing=8,
            background=nib.RoundedRectangle(corner_radius=10, fill="#333"),
            padding=16,
        )
"""

from typing import TYPE_CHECKING, Callable, List, Optional, Union

from ..types import (
    Animation,
    BlendMode,
    ColorLike,
    ContentTransition,
    Font,
    FontWeight,
    FontWeightLike,
    Transition,
    resolve_color,
    _resolve_weight,
)
from ..modifiers import ModifierRegistry

if TYPE_CHECKING:
    from ..core.app import App


def _float(value: Optional[Union[int, float]]) -> Optional[float]:
    """Convert numeric value to float for MessagePack compatibility.

    Args:
        value: An int, float, or None.

    Returns:
        The value as a float, or None.
    """
    return float(value) if value is not None else None


def _resolve_shape(shape) -> tuple[str, Optional[float]]:
    """Extract shape type and corner radius from a shape view or string.

    Args:
        shape: A shape View instance (e.g., Circle, Capsule) or string
            shape name ("circle", "capsule").

    Returns:
        Tuple of (shape_type, corner_radius). Shape type is the lowercase
        name, corner_radius is extracted from RoundedRectangle views.
    """
    if shape is None:
        return None, None
    if hasattr(shape, '_type'):
        shape_type = shape._type.lower()
        corner_radius = getattr(shape, '_corner_radius', None)
        return shape_type, corner_radius
    return shape, None


class View:
    """Base class for all Nib views.

    All Nib UI components inherit from View and share a common set of
    modifier parameters for styling. Views are styled through constructor
    parameters rather than method chaining.

    Attributes:
        _type: The SwiftUI view type name (e.g., "Text", "VStack").
        _id: Position-based identifier assigned during tree traversal.
        _modifiers: List of modifier dictionaries to apply.
        _app: Reference to the parent App for triggering re-renders.

    Modifier Parameters:
        Layout:
            - width, height: Fixed dimensions in points
            - min_width, min_height: Minimum dimensions
            - max_width, max_height: Maximum dimensions (use "infinity" for max)
            - padding: Uniform float or dict with sides

        Appearance:
            - background: Color or View for background
            - foreground_color: Text/content color
            - fill, stroke, stroke_width: Shape fill and stroke
            - opacity: View opacity (0.0 - 1.0)
            - corner_radius: Corner rounding in points

        Typography:
            - font: Font instance or system font name
            - font_weight: FontWeight enum or string

        Effects:
            - shadow_color, shadow_radius, shadow_x, shadow_y: Drop shadow
            - border_color, border_width: Border styling
            - clip_shape: Clip view to shape ("circle", "capsule", or View)
            - blend_mode: Layer blending mode
            - scale: Scale transform

        Animation:
            - animation: Animation configuration
            - content_transition: How content changes animate
            - transition: How view appearance/disappearance animates

        Interaction:
            - on_drop: Callback for drag-and-drop file handling

    Example:
        Basic text styling::

            nib.Text(
                "Hello World",
                font=nib.Font.TITLE,
                foreground_color=nib.Color.BLUE,
                padding=16,
            )

        Container with complex styling::

            nib.VStack(
                controls=[...],
                spacing=8,
                background=nib.RoundedRectangle(
                    corner_radius=10,
                    fill="#262626",
                    stroke_color="#383837",
                ),
                shadow_radius=5,
                shadow_y=2,
            )
    """

    _type: str = "View"

    def __init__(
        self,
        # Layout modifiers
        width: Optional[float] = None,
        height: Optional[float] = None,
        min_width: Optional[float] = None,
        min_height: Optional[float] = None,
        max_width: Optional[Union[float, str]] = None,
        max_height: Optional[Union[float, str]] = None,
        padding: Optional[Union[float, dict]] = None,
        # Appearance modifiers
        background: Optional[ColorLike] = None,
        foreground_color: Optional[ColorLike] = None,
        fill: Optional[ColorLike] = None,
        stroke: Optional[ColorLike] = None,
        stroke_width: Optional[float] = None,
        opacity: Optional[float] = None,
        corner_radius: Optional[float] = None,
        # Font modifiers
        font: Optional[Union[str, Font]] = None,
        font_weight: Optional[FontWeightLike] = None,
        # Shape modifiers
        clip_shape: Optional[Union[str, "View"]] = None,
        shadow_color: Optional[str] = None,
        shadow_radius: Optional[float] = None,
        shadow_x: Optional[float] = None,
        shadow_y: Optional[float] = None,
        border_color: Optional[ColorLike] = None,
        border_width: Optional[float] = None,
        # Animation & Transitions
        animation: Optional[Animation] = None,
        content_transition: Optional[Union[ContentTransition, str]] = None,
        transition: Optional[Union[Transition, str]] = None,
        # Blend mode
        blend_mode: Optional[Union[BlendMode, str]] = None,
        # Transform
        scale: Optional[float] = None,
        # Overlay (View, like background)
        overlay: Optional["View"] = None,
        # Drag and drop
        on_drop: Optional[Callable[[List[str]], None]] = None,
    ) -> None:
        """Initialize a View with modifier parameters.

        Args:
            width: Fixed width in points.
            height: Fixed height in points.
            min_width: Minimum width in points.
            min_height: Minimum height in points.
            max_width: Maximum width in points, or "infinity".
            max_height: Maximum height in points, or "infinity".
            padding: Padding around content. Either a uniform float or a dict
                with keys: top, bottom, leading, trailing, horizontal, vertical.
            background: Background color (string or Color) or a View.
            foreground_color: Content/text color.
            fill: Fill color for shapes.
            stroke: Stroke color for shapes.
            stroke_width: Stroke width for shapes.
            opacity: View opacity from 0.0 (transparent) to 1.0 (opaque).
            corner_radius: Corner rounding in points.
            font: Font instance or system font name.
            font_weight: Text weight (FontWeight enum or string).
            clip_shape: Clip to shape ("circle", "capsule", or a shape View).
            shadow_color: Shadow color.
            shadow_radius: Shadow blur radius.
            shadow_x: Shadow horizontal offset.
            shadow_y: Shadow vertical offset.
            border_color: Border color.
            border_width: Border width.
            animation: Animation configuration for property changes.
            content_transition: Animation for content changes.
            transition: Animation for view appearance/disappearance.
            blend_mode: Layer blending mode.
            scale: Scale transform factor.
            overlay: View to render on top of this view.
            on_drop: Callback for drag-and-drop file handling.
        """
        self._id: Optional[str] = None  # Set during tree traversal
        self._action: Optional[Callable] = None
        self._app = None  # Reference to parent App for triggering rerenders
        self._on_drop = on_drop

        # Handle special cases: background/overlay views
        if background is not None and hasattr(background, "_type"):
            self._background_view = background
        else:
            self._background_view = None

        if overlay is not None:
            self._overlay_view = overlay
        else:
            self._overlay_view = None

        # Build kwargs for modifier registry
        kwargs = {
            "width": width,
            "height": height,
            "min_width": min_width,
            "min_height": min_height,
            "max_width": max_width,
            "max_height": max_height,
            "padding": padding,
            "background": background,
            "foreground_color": foreground_color,
            "fill": fill,
            "stroke": stroke,
            "stroke_width": stroke_width,
            "opacity": opacity,
            "corner_radius": corner_radius,
            "font": font,
            "font_weight": font_weight,
            "clip_shape": clip_shape,
            "shadow_color": shadow_color,
            "shadow_radius": shadow_radius,
            "shadow_x": shadow_x,
            "shadow_y": shadow_y,
            "border_color": border_color,
            "border_width": border_width,
            "animation": animation,
            "content_transition": content_transition,
            "transition": transition,
            "blend_mode": blend_mode,
            "scale": scale,
        }

        # Apply all modifiers via registry
        self._modifiers: List[dict] = ModifierRegistry.apply_all(kwargs)

    def _add_modifier(self, type: str, **args) -> None:
        """Add a modifier to the view's modifier list.

        Used by subclasses to add view-specific modifiers beyond the
        standard ones handled by the modifier registry.

        Args:
            type: The modifier type name (e.g., "textStyle", "buttonStyle").
            **args: Modifier arguments. None values are filtered out.
        """
        filtered_args = {k: v for k, v in args.items() if v is not None}
        if filtered_args:
            self._modifiers.append({"type": type, "args": filtered_args})

    def to_dict(self, path: str = "0") -> dict:
        """Convert the view to a dictionary for serialization.

        Serializes the view and its children into a dictionary structure
        that can be sent to the Swift runtime via MessagePack.

        Args:
            path: Position-based path for stable view identity
                (e.g., "0", "0.0", "0.1.2").

        Returns:
            Dictionary containing id, type, props, children, modifiers,
            and optional backgroundView/overlayView.
        """
        # Use pre-assigned _id if available (from _collect_actions), otherwise use path
        view_id = self._id if self._id is not None else path
        props = self._get_props()
        # Add onDrop if handler is set
        if hasattr(self, "_on_drop") and self._on_drop is not None:
            props["onDrop"] = True
        result = {
            "id": view_id,
            "type": self._type,
            "props": props,
            "children": self._get_children(path),
            "modifiers": self._modifiers if self._modifiers else None,
        }
        # Add background view if present
        if hasattr(self, "_background_view") and self._background_view is not None:
            result["backgroundView"] = self._background_view.to_dict(f"{path}.bg")
        # Add overlay view if present
        if hasattr(self, "_overlay_view") and self._overlay_view is not None:
            result["overlayView"] = self._overlay_view.to_dict(f"{path}.ov")
        return result

    def _get_props(self) -> dict:
        """Get view-specific properties for serialization.

        Override in subclasses to return view-specific properties
        (e.g., content for Text, action for Button).

        Returns:
            Dictionary of properties to include in the serialized view.
        """
        return {}

    def _get_children(self, parent_path: str) -> Optional[List[dict]]:
        """Get serialized child views.

        Override in container subclasses (VStack, HStack, etc.) to return
        the list of serialized child view dictionaries.

        Args:
            parent_path: The path of this view, used to generate child paths.

        Returns:
            List of child view dictionaries, or None if no children.
        """
        return None

    def _trigger_update(self) -> None:
        """Trigger a UI re-render when a property changes.

        Called by reactive property setters to notify the App that
        the UI needs to be re-rendered.
        """
        if self._app is not None:
            self._app._trigger_rerender()

    def _set_app(self, app: "App") -> None:
        """Set the parent App reference recursively.

        Called during :meth:`App.build` to establish the connection
        between views and the App for reactive updates.

        Args:
            app: The parent App instance.
        """
        self._app = app
        # Recursively set on children
        if hasattr(self, "_children") and self._children:
            for child in self._children:
                if isinstance(child, View):
                    child._set_app(app)
        if hasattr(self, "_content") and self._content is not None:
            if isinstance(self._content, View):
                self._content._set_app(app)
        # Set on background view if present
        if hasattr(self, "_background_view") and self._background_view is not None:
            self._background_view._set_app(app)
        # Set on overlay view if present
        if hasattr(self, "_overlay_view") and self._overlay_view is not None:
            self._overlay_view._set_app(app)
