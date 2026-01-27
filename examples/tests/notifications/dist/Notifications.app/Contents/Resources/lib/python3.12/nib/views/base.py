"""Base View class for Nib - Declarative parameter-based API."""

from typing import Callable, List, Optional, Union

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


def _float(value: Optional[Union[int, float]]) -> Optional[float]:
    """Convert numeric value to float for MessagePack compatibility."""
    return float(value) if value is not None else None


def _resolve_shape(shape) -> tuple[str, Optional[float]]:
    """Extract shape type and corner radius from a shape view or string."""
    if shape is None:
        return None, None
    if hasattr(shape, '_type'):
        shape_type = shape._type.lower()
        corner_radius = getattr(shape, '_corner_radius', None)
        return shape_type, corner_radius
    return shape, None


class View:
    """
    Base class for all Nib views.

    All styling is done via constructor parameters - no method chaining.

    Example:
        Text(
            "Hello World",
            font=Font.title,
            foreground_color=Color.blue,
            padding=16,
        )

        VStack(
            controls=[Text("Item 1"), Text("Item 2")],
            spacing=8,
            background=Color.gray,
            corner_radius=10,
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
    ):
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
        """Add a modifier to the view (for subclass use)."""
        filtered_args = {k: v for k, v in args.items() if v is not None}
        if filtered_args:
            self._modifiers.append({"type": type, "args": filtered_args})

    def to_dict(self, path: str = "0") -> dict:
        """Convert the view to a dictionary for serialization.

        Args:
            path: Position-based path for stable view identity (e.g., "0", "0.0", "0.1.2")
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
        """Get view-specific properties. Override in subclasses."""
        return {}

    def _get_children(self, parent_path: str) -> Optional[List[dict]]:
        """Get child views. Override in subclasses.

        Args:
            parent_path: The path of this view, used to generate child paths
        """
        return None

    def _trigger_update(self) -> None:
        """Trigger a UI update when a property changes."""
        if self._app is not None:
            self._app._trigger_rerender()

    def _set_app(self, app: "App") -> None:
        """Set the parent App reference (called during build)."""
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
