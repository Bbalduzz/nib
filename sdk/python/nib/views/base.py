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
    Offset,
    Transition,
    resolve_color,
    _resolve_weight,
)
from ..modifiers import ModifierRegistry

if TYPE_CHECKING:
    from ..core.app import App

# Maximum depth for view tree to prevent stack overflow in Swift runtime
MAX_TREE_DEPTH = 100


class NibDepthError(Exception):
    """Raised when view tree exceeds maximum allowed depth."""

    def __init__(self, depth: int, max_depth: int = MAX_TREE_DEPTH):
        self.depth = depth
        self.max_depth = max_depth
        super().__init__(
            f"View tree exceeds maximum depth of {max_depth} (current: {depth}). "
            "Simplify your view hierarchy or check for unintended nesting."
        )


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
            - padding: Uniform float or dict with sides (inside background)
            - margin: Uniform float or dict with sides (outside background)

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
            - offset: Position offset (Offset with x, y)

        Animation:
            - animation: Animation configuration
            - content_transition: How content changes animate
            - transition: How view appearance/disappearance animates

        Interaction:
            - on_drop: Callback for drag-and-drop file handling
            - on_hover: Callback when mouse enters/exits the view
            - on_click: Callback when view is clicked/tapped
            - tooltip: Tooltip text shown on hover (string or Text view)

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
        margin: Optional[Union[float, dict]] = None,
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
        # Offset (for positioning in ZStack, etc.)
        offset: Optional[Offset] = None,
        # Overlay (View, like background)
        overlay: Optional["View"] = None,
        # Drag and drop
        on_drop: Optional[Callable[[List[str]], None]] = None,
        # Hover
        on_hover: Optional[Callable[[bool], None]] = None,
        # Click
        on_click: Optional[Callable[[], None]] = None,
        # Tooltip
        tooltip: Optional[Union[str, "View"]] = None,
        # Context menu (right-click menu items)
        context_menu: Optional[List["View"]] = None,
        # Visibility (if False, view is removed from tree entirely)
        visible: bool = True,
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
            margin: Outer spacing (applied after background). Either a uniform
                float or a dict with keys: top, bottom, leading, trailing,
                horizontal, vertical.
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
            offset: Position offset (Offset instance with x, y values).
            overlay: View to render on top of this view.
            on_drop: Callback for drag-and-drop file handling.
            on_hover: Callback when mouse enters/exits the view. Receives a bool
                (True when mouse enters, False when mouse exits).
            on_click: Callback when view is clicked/tapped. Receives no arguments.
            tooltip: Tooltip text shown on hover. Can be a string or a Text view.
            visible: Whether the view is included in the tree. If False,
                the view is completely removed (doesn't take up space).
                Unlike opacity=0, invisible views don't occupy layout space.
        """
        self._id: Optional[str] = None  # Set during tree traversal
        self._action: Optional[Callable] = None
        self._app = None  # Reference to parent App for triggering rerenders
        self._on_drop = on_drop
        self._on_hover = on_hover
        self._on_click = on_click
        self._tooltip = tooltip
        self._visible = visible

        # Sticky animation - persists across property changes and applies to all mutations
        self._sticky_animation: Optional[Animation] = animation

        # Handle special cases: background/overlay views
        if background is not None and hasattr(background, "_type"):
            self._background_view = background
        else:
            self._background_view = None

        if overlay is not None:
            self._overlay_view = overlay
        else:
            self._overlay_view = None

        # Context menu views
        self._context_menu_views: List["View"] = context_menu if context_menu else []

        # Build kwargs for modifier registry - store for later mutation
        self._modifier_kwargs = {
            "width": width,
            "height": height,
            "min_width": min_width,
            "min_height": min_height,
            "max_width": max_width,
            "max_height": max_height,
            "padding": padding,
            "margin": margin,
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
            "offset": offset,
        }

        # Apply all modifiers via registry
        self._modifiers: List[dict] = ModifierRegistry.apply_all(self._modifier_kwargs)

    # Modifier parameter names that can be mutated after construction
    _MODIFIER_PARAMS = {
        "width", "height", "min_width", "min_height", "max_width", "max_height",
        "padding", "margin", "background", "foreground_color", "fill", "stroke",
        "stroke_width", "opacity", "corner_radius", "font", "font_weight",
        "clip_shape", "shadow_color", "shadow_radius", "shadow_x", "shadow_y",
        "border_color", "border_width", "animation", "content_transition",
        "transition", "blend_mode", "scale", "offset",
    }

    def __setattr__(self, name: str, value) -> None:
        """Override setattr to trigger re-render on any property change.

        For modifier parameters (like fill, padding, opacity), this also
        updates the internal modifier list so the change is reflected in
        the rendered UI.

        Animation is handled specially - when set, it becomes "sticky" and
        applies to all future property changes on this view.
        """
        # Always set the attribute
        object.__setattr__(self, name, value)

        # Check if this is a modifier parameter change
        modifier_kwargs = getattr(self, "_modifier_kwargs", None)
        if modifier_kwargs is not None and name in self._MODIFIER_PARAMS:
            # Update the stored kwargs and re-compute modifiers
            modifier_kwargs[name] = value

            # Handle animation specially - make it sticky
            if name == "animation" and value is not None:
                object.__setattr__(self, "_sticky_animation", value)

            # Handle background/overlay views specially
            if name == "background":
                if hasattr(value, "_type"):
                    object.__setattr__(self, "_background_view", value)
                    # Set app reference on new background view
                    app = getattr(self, "_app", None)
                    if app is not None:
                        value._set_app(app)
                else:
                    object.__setattr__(self, "_background_view", None)
            # Re-apply all modifiers
            new_modifiers = ModifierRegistry.apply_all(modifier_kwargs)
            object.__setattr__(self, "_modifiers", new_modifiers)

        # Handle overlay separately (it's not in _modifier_kwargs but should trigger updates)
        if name == "overlay":
            if hasattr(value, "_type"):
                object.__setattr__(self, "_overlay_view", value)
                app = getattr(self, "_app", None)
                if app is not None:
                    value._set_app(app)
            else:
                object.__setattr__(self, "_overlay_view", None)

        # Only trigger re-render if connected to an app
        app = getattr(self, "_app", None)
        if app is None:
            return

        # Skip internal bookkeeping attributes
        if name in ("_id", "_app", "_action", "_modifiers", "_modifier_kwargs"):
            return

        # Trigger re-render
        app._trigger_rerender()

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

    def _serialize_animation_context(self) -> Optional[dict]:
        """Serialize the sticky animation context for this view.

        Returns the animation configuration that should apply to all property
        changes on this view. This is sent separately from modifiers so Swift
        can apply per-view animations.

        Returns:
            Dictionary with animation config, or None if no animation.
        """
        anim = getattr(self, "_sticky_animation", None)
        if anim is None:
            # Fall back to animation in modifier_kwargs if sticky not set
            anim = self._modifier_kwargs.get("animation")
        if anim is None:
            return None
        return anim.to_dict()

    def to_dict(self, path: str = "0", depth: int = 0) -> dict:
        """Convert the view to a dictionary for serialization.

        Serializes the view and its children into a dictionary structure
        that can be sent to the Swift runtime via MessagePack.

        Args:
            path: Position-based path for stable view identity
                (e.g., "0", "0.0", "0.1.2").
            depth: Current depth in the view tree (for stack overflow protection).

        Returns:
            Dictionary containing id, type, props, children, modifiers,
            animationContext, and optional backgroundView/overlayView.

        Raises:
            NibDepthError: If view tree depth exceeds MAX_TREE_DEPTH.
        """
        # Check depth limit to prevent stack overflow in Swift runtime
        if depth > MAX_TREE_DEPTH:
            raise NibDepthError(depth)

        # Use pre-assigned _id if available (from _collect_actions), otherwise use path
        view_id = self._id if self._id is not None else path
        props = self._get_props()
        # Add interaction handlers
        if hasattr(self, "_on_drop") and self._on_drop is not None:
            props["onDrop"] = True
        if hasattr(self, "_on_hover") and self._on_hover is not None:
            props["onHover"] = True
        if hasattr(self, "_on_click") and self._on_click is not None:
            props["onClick"] = True
        # Add tooltip if set
        if hasattr(self, "_tooltip") and self._tooltip is not None:
            if isinstance(self._tooltip, str):
                props["tooltip"] = self._tooltip
            elif hasattr(self._tooltip, "_content"):
                # Text view - extract content
                props["tooltip"] = self._tooltip._content
            elif hasattr(self._tooltip, "content"):
                props["tooltip"] = self._tooltip.content
        result = {
            "id": view_id,
            "type": self._type,
            "props": props,
            "children": self._get_children(path, depth),
            "modifiers": self._modifiers if self._modifiers else None,
        }
        # Add animation context for per-view reactive animations
        anim_context = self._serialize_animation_context()
        if anim_context is not None:
            result["animationContext"] = anim_context
        # Add background view if present
        if hasattr(self, "_background_view") and self._background_view is not None:
            result["backgroundView"] = self._background_view.to_dict(f"{path}.bg", depth + 1)
        # Add overlay view if present
        if hasattr(self, "_overlay_view") and self._overlay_view is not None:
            result["overlayView"] = self._overlay_view.to_dict(f"{path}.ov", depth + 1)
        return result

    def to_flat_list(self, path: str = "0") -> tuple[list[dict], str]:
        """Convert the view tree to a flat list of nodes.

        Instead of nested children, each node has parentId and childIds references.
        This enables iterative (non-recursive) parsing on the Swift side.

        Args:
            path: Position-based path for stable view identity.

        Returns:
            Tuple of (flat_nodes_list, root_id).
            Each node dict has: id, type, props, modifiers, animationContext,
            parentId, childIds, backgroundId, overlayId.

        Raises:
            NibDepthError: If view tree depth exceeds MAX_TREE_DEPTH.
        """
        nodes = []
        # Use explicit stack instead of recursion: (view, path, depth, parent_id)
        stack: list[tuple["View", str, int, Optional[str]]] = [(self, path, 0, None)]
        root_id = path

        while stack:
            view, current_path, depth, parent_id = stack.pop()

            # Check depth limit
            if depth > MAX_TREE_DEPTH:
                raise NibDepthError(depth)

            # Use pre-assigned _id if available, otherwise use path
            view_id = view._id if view._id is not None else current_path

            # Get props
            props = view._get_props()
            if hasattr(view, "_on_drop") and view._on_drop is not None:
                props["onDrop"] = True
            if hasattr(view, "_on_hover") and view._on_hover is not None:
                props["onHover"] = True
            if hasattr(view, "_on_click") and view._on_click is not None:
                props["onClick"] = True
            if hasattr(view, "_tooltip") and view._tooltip is not None:
                if isinstance(view._tooltip, str):
                    props["tooltip"] = view._tooltip
                elif hasattr(view._tooltip, "_content"):
                    props["tooltip"] = view._tooltip._content
                elif hasattr(view._tooltip, "content"):
                    props["tooltip"] = view._tooltip.content

            # Collect child IDs
            child_ids = []
            if hasattr(view, "_children"):
                visible = [c for c in view._children if c._visible]
                for i, child in enumerate(visible):
                    child_path = f"{current_path}.{i}"
                    child_id = child._id if child._id is not None else child_path
                    child_ids.append(child_id)
                    # Add to stack (reverse order so first child is processed first)
                    stack.append((child, child_path, depth + 1, view_id))

            # Handle special child containers (e.g., _content, _destination)
            if hasattr(view, "_content") and view._content is not None and isinstance(view._content, View) and view._content._visible:
                child_path = f"{current_path}.0"
                child_id = view._content._id if view._content._id is not None else child_path
                child_ids.append(child_id)
                stack.append((view._content, child_path, depth + 1, view_id))

            if hasattr(view, "_destination"):
                visible = [c for c in view._destination if c._visible]
                for i, child in enumerate(visible):
                    child_path = f"{current_path}.{i}"
                    child_id = child._id if child._id is not None else child_path
                    child_ids.append(child_id)
                    stack.append((child, child_path, depth + 1, view_id))

            # Handle chart marks (_marks are BaseMark objects, not Views)
            if hasattr(view, "_marks") and view._marks:
                for i, mark in enumerate(view._marks):
                    mark_path = f"{current_path}.{i}"
                    mark_dict = mark.to_dict(mark_path)
                    child_ids.append(mark_dict["id"])
                    # Add mark as a flat node directly (marks are not Views)
                    nodes.append({
                        "id": mark_dict["id"],
                        "type": mark_dict["type"],
                        "props": mark_dict["props"],
                        "modifiers": None,
                        "parentId": view_id,
                        "childIds": None,
                        "backgroundId": None,
                        "overlayId": None,
                    })

            # Background and overlay
            background_id = None
            if hasattr(view, "_background_view") and view._background_view is not None:
                bg_path = f"{current_path}.bg"
                background_id = view._background_view._id if view._background_view._id else bg_path
                stack.append((view._background_view, bg_path, depth + 1, view_id))

            overlay_id = None
            if hasattr(view, "_overlay_view") and view._overlay_view is not None:
                ov_path = f"{current_path}.ov"
                overlay_id = view._overlay_view._id if view._overlay_view._id else ov_path
                stack.append((view._overlay_view, ov_path, depth + 1, view_id))

            # Context menu views
            context_menu_ids = None
            if hasattr(view, "_context_menu_views") and view._context_menu_views:
                context_menu_ids = []
                for i, ctx_view in enumerate(view._context_menu_views):
                    ctx_path = f"{current_path}.ctx.{i}"
                    ctx_id = ctx_view._id if ctx_view._id is not None else ctx_path
                    context_menu_ids.append(ctx_id)
                    stack.append((ctx_view, ctx_path, depth + 1, view_id))

            # Build flat node
            node = {
                "id": view_id,
                "type": view._type,
                "props": props,
                "modifiers": view._modifiers if view._modifiers else None,
                "parentId": parent_id,
                "childIds": child_ids if child_ids else None,
                "backgroundId": background_id,
                "overlayId": overlay_id,
                "contextMenuIds": context_menu_ids,
            }

            # Add animation context if present
            anim_context = view._serialize_animation_context()
            if anim_context is not None:
                node["animationContext"] = anim_context

            nodes.append(node)

        return nodes, root_id

    def _get_props(self) -> dict:
        """Get view-specific properties for serialization.

        Override in subclasses to return view-specific properties
        (e.g., content for Text, action for Button).

        Returns:
            Dictionary of properties to include in the serialized view.
        """
        return {}

    def _get_children(self, parent_path: str, depth: int = 0) -> Optional[List[dict]]:
        """Get serialized child views.

        Override in container subclasses (VStack, HStack, etc.) to return
        the list of serialized child view dictionaries.

        Args:
            parent_path: The path of this view, used to generate child paths.
            depth: Current depth in the view tree (for stack overflow protection).

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

    def update(self) -> None:
        """Manually trigger a UI re-render for this view.

        Use this to force an update when you've made changes that the
        automatic reactivity system might not detect.

        Example:
            # Force update after modifying nested data
            view.some_list.append("new item")
            view.update()
        """
        self._trigger_update()

    def _update_modifier(self, modifier_type: str, **args) -> None:
        """Update or add a modifier and trigger re-render.

        Args:
            modifier_type: The modifier type (e.g., "opacity", "frame").
            **args: The modifier arguments.
        """
        # Find existing modifier of this type
        for mod in self._modifiers:
            if mod.get("type") == modifier_type:
                mod["args"] = {k: v for k, v in args.items() if v is not None}
                self._trigger_update()
                return
        # Add new modifier if not found
        filtered_args = {k: v for k, v in args.items() if v is not None}
        if filtered_args:
            self._modifiers.append({"type": modifier_type, "args": filtered_args})
        self._trigger_update()

    @property
    def opacity(self) -> Optional[float]:
        """Get the view's opacity."""
        for mod in self._modifiers:
            if mod.get("type") == "opacity":
                return mod.get("args", {}).get("opacity")
        return None

    @opacity.setter
    def opacity(self, value: Optional[float]) -> None:
        """Set the view's opacity and trigger UI update."""
        self._update_modifier("opacity", opacity=value)

    @property
    def visible(self) -> bool:
        """Get whether the view is visible (included in the tree)."""
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        """Set whether the view is visible and trigger UI update.

        When visible=False, the view is completely removed from the tree
        and doesn't take up any layout space.
        """
        self._visible = value
        self._trigger_update()

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
        # Set on context menu views if present
        if hasattr(self, "_context_menu_views") and self._context_menu_views:
            for child in self._context_menu_views:
                child._set_app(app)
