"""Canvas view for Core Graphics drawing.

The Canvas view provides a drawing surface where you can render shapes,
images, and text using declarative drawing commands. It uses Core Graphics
on the Swift side for GPU-accelerated rendering.

Example:
    Basic drawing::

        import nib

        canvas = nib.Canvas(width=400, height=300)
        canvas.draw([
            nib.draw.Rect(x=10, y=10, width=100, height=50, fill="#3498db"),
            nib.draw.Circle(cx=200, cy=100, radius=40, fill="#e74c3c"),
            nib.draw.Text("Hello!", x=10, y=250, fill="#ffffff"),
        ])

        app.build(canvas)

    Drawing with gestures (like Flet)::

        canvas = nib.Canvas(width=400, height=300, enable_gestures=True)
        last_pos = None

        def on_pan_start(e):
            nonlocal last_pos
            last_pos = (e.x, e.y)

        def on_pan_update(e):
            nonlocal last_pos
            canvas.append(nib.draw.Line(
                x1=last_pos[0], y1=last_pos[1],
                x2=e.x, y2=e.y,
                stroke="#000000", stroke_width=3
            ))
            last_pos = (e.x, e.y)

        canvas.on_pan_start = on_pan_start
        canvas.on_pan_update = on_pan_update
"""

from dataclasses import dataclass
from typing import Any, Callable, List, Optional

from .base import View
from ..draw import DrawCommand


@dataclass
class PanEvent:
    """Event data for pan/drag gestures.

    Attributes:
        x: X coordinate of the event in canvas coordinates.
        y: Y coordinate of the event in canvas coordinates.
    """

    x: float
    y: float


class Canvas(View):
    """A drawing canvas for Core Graphics rendering.

    Canvas provides a surface for drawing shapes, images, and text using
    declarative commands. Drawing is performed via Core Graphics on macOS,
    with GPU acceleration when available.

    The canvas is reactive - calling `draw()` with new commands triggers
    a re-render to update the display.

    Attributes:
        canvas_width: Width of the drawing area in points.
        canvas_height: Height of the drawing area in points.
        background_color: Background color (hex string or None for transparent).
        enable_gestures: Whether to enable pan/hover gesture tracking.

    Example:
        Drawing shapes::

            canvas = nib.Canvas(width=400, height=300, background_color="#1a1a1a")
            canvas.draw([
                nib.draw.Rect(x=10, y=10, width=100, height=80, fill="#3498db"),
                nib.draw.Circle(cx=250, cy=50, radius=30, stroke="#e74c3c"),
            ])

        Drawing with mouse/pen::

            canvas = nib.Canvas(width=400, height=300, enable_gestures=True)

            def on_pan_update(e):
                canvas.append(nib.draw.Circle(cx=e.x, cy=e.y, radius=3, fill="#000"))

            canvas.on_pan_update = on_pan_update
    """

    _type = "Canvas"

    def __init__(
        self,
        width: float = 100,
        height: float = 100,
        commands: Optional[List[DrawCommand]] = None,
        background_color: Optional[str] = None,
        enable_gestures: bool = False,
        on_pan_start: Optional[Callable[[PanEvent], None]] = None,
        on_pan_update: Optional[Callable[[PanEvent], None]] = None,
        on_pan_end: Optional[Callable[[PanEvent], None]] = None,
        on_hover: Optional[Callable[[PanEvent], None]] = None,
        # Standard view modifiers
        **kwargs: Any,
    ) -> None:
        """Initialize a Canvas view.

        Args:
            width: Width of the canvas in points.
            height: Height of the canvas in points.
            commands: Initial list of drawing commands.
            background_color: Background color as hex string (e.g., "#1a1a1a")
                or None for transparent.
            enable_gestures: Enable pan/hover gesture tracking. Required for
                on_pan_* and on_hover callbacks.
            on_pan_start: Callback when mouse/pen pressed down.
            on_pan_update: Callback when mouse/pen dragged.
            on_pan_end: Callback when mouse/pen released.
            on_hover: Callback when mouse moves over canvas (not dragging).
            **kwargs: Standard view modifiers (padding, opacity, etc.).
        """
        super().__init__(**kwargs)
        self._canvas_width = float(width)
        self._canvas_height = float(height)
        self._commands: List[DrawCommand] = commands or []
        self._background_color = background_color
        self._enable_gestures = enable_gestures or any([
            on_pan_start, on_pan_update, on_pan_end, on_hover
        ])

        # Gesture callbacks
        self._on_pan_start = on_pan_start
        self._on_pan_update = on_pan_update
        self._on_pan_end = on_pan_end
        self._on_hover = on_hover

    @property
    def canvas_width(self) -> float:
        """Get the canvas width."""
        return self._canvas_width

    @canvas_width.setter
    def canvas_width(self, value: float) -> None:
        """Set the canvas width and trigger re-render."""
        self._canvas_width = float(value)
        self._trigger_update()

    @property
    def canvas_height(self) -> float:
        """Get the canvas height."""
        return self._canvas_height

    @canvas_height.setter
    def canvas_height(self, value: float) -> None:
        """Set the canvas height and trigger re-render."""
        self._canvas_height = float(value)
        self._trigger_update()

    @property
    def background_color(self) -> Optional[str]:
        """Get the background color."""
        return self._background_color

    @background_color.setter
    def background_color(self, value: Optional[str]) -> None:
        """Set the background color and trigger re-render."""
        self._background_color = value
        self._trigger_update()

    @property
    def commands(self) -> List[DrawCommand]:
        """Get the current drawing commands."""
        return self._commands

    @property
    def on_pan_start(self) -> Optional[Callable[[PanEvent], None]]:
        """Get the pan start callback."""
        return self._on_pan_start

    @on_pan_start.setter
    def on_pan_start(self, value: Optional[Callable[[PanEvent], None]]) -> None:
        """Set the pan start callback."""
        self._on_pan_start = value
        if value:
            self._enable_gestures = True

    @property
    def on_pan_update(self) -> Optional[Callable[[PanEvent], None]]:
        """Get the pan update callback."""
        return self._on_pan_update

    @on_pan_update.setter
    def on_pan_update(self, value: Optional[Callable[[PanEvent], None]]) -> None:
        """Set the pan update callback."""
        self._on_pan_update = value
        if value:
            self._enable_gestures = True

    @property
    def on_pan_end(self) -> Optional[Callable[[PanEvent], None]]:
        """Get the pan end callback."""
        return self._on_pan_end

    @on_pan_end.setter
    def on_pan_end(self, value: Optional[Callable[[PanEvent], None]]) -> None:
        """Set the pan end callback."""
        self._on_pan_end = value
        if value:
            self._enable_gestures = True

    @property
    def on_hover(self) -> Optional[Callable[[PanEvent], None]]:
        """Get the hover callback."""
        return self._on_hover

    @on_hover.setter
    def on_hover(self, value: Optional[Callable[[PanEvent], None]]) -> None:
        """Set the hover callback."""
        self._on_hover = value
        if value:
            self._enable_gestures = True

    def draw(self, commands: List[DrawCommand]) -> None:
        """Set drawing commands and trigger re-render.

        Replaces all current drawing commands with the provided list
        and updates the display.

        Args:
            commands: List of drawing commands (Rect, Circle, Image, etc.).

        Example:
            Update canvas with new shapes::

                canvas.draw([
                    nib.draw.Rect(x=0, y=0, width=100, height=100, fill="#FF0000"),
                    nib.draw.Circle(cx=150, cy=50, radius=30, fill="#00FF00"),
                ])
        """
        self._commands = commands
        self._trigger_update()

    def clear(self) -> None:
        """Clear all drawing commands and update display."""
        self._commands = []
        self._trigger_update()

    def append(self, command: DrawCommand) -> None:
        """Add a drawing command to the canvas.

        Args:
            command: A drawing command to add.

        Example:
            Add a circle to existing commands::

                canvas.append(nib.draw.Circle(cx=100, cy=100, radius=20, fill="#FF0000"))
        """
        self._commands.append(command)
        self._trigger_update()

    def _trigger_update(self) -> None:
        """Trigger a re-render if connected to an app."""
        app = getattr(self, "_app", None)
        if app is not None:
            app._trigger_rerender()

    def _get_props(self) -> dict:
        """Get view properties for serialization."""
        return {
            "canvasWidth": self._canvas_width,
            "canvasHeight": self._canvas_height,
            "commands": [cmd.to_dict() for cmd in self._commands],
            "backgroundColor": self._background_color,
            "canvasGestures": self._enable_gestures,
        }
