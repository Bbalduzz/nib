"""Base Shape class for custom shape views.

This module provides the Shape class, which allows users to create
custom shapes using path operations. Shapes can be defined either
by subclassing and overriding build_path(), or by passing a Path
directly.

Example:
    Subclassing to create a reusable shape::

        class Triangle(nib.Shape):
            view_box = (100, 100)

            def build_path(self, path: nib.Path) -> nib.Path:
                return (path
                    .move_to(50, 0)
                    .line_to(100, 100)
                    .line_to(0, 100)
                    .close())

        # Use the shape
        triangle = Triangle(fill="red", width=200, height=200)

    Inline shape definition::

        shape = nib.Shape(
            path=nib.Path().move_to(0, 0).line_to(100, 100).close(),
            fill="blue",
        )
"""

from typing import TYPE_CHECKING, Any, ClassVar, Optional, Tuple, Union

from ..base import View
from .path import Path

if TYPE_CHECKING:
    from .gradients import LinearGradient, RadialGradient, AngularGradient, EllipticalGradient


class Shape(View):
    """Base class for custom shapes.

    Shape allows you to define custom shapes using path operations.
    You can either subclass and override build_path(), or pass a
    Path object directly to the constructor.

    The optional view_box attribute defines the coordinate system
    used by the path. When rendered, the path will be scaled to
    fit within the view's bounds while preserving aspect ratio.

    Class Attributes:
        view_box: Optional tuple (width, height) defining the coordinate
            system for path operations. When set, the path will be scaled
            to fit the view bounds.

    Example:
        Creating a custom logo shape::

            class LogoShape(nib.Shape):
                view_box = (100, 100)

                def build_path(self, path: nib.Path) -> nib.Path:
                    # Pentagon
                    path.move_to(50, 0)
                    path.line_to(100, 38)
                    path.line_to(81, 100)
                    path.line_to(19, 100)
                    path.line_to(0, 38)
                    path.close()
                    return path

            logo = LogoShape(fill="#3B82F6", width=64, height=64)
    """

    _type = "Shape"
    view_box: ClassVar[Optional[Tuple[float, float]]] = None

    def __init__(
        self,
        path: Optional[Path] = None,
        view_box: Optional[Tuple[float, float]] = None,
        fill: Optional[Union[str, Any]] = None,
        stroke: Optional[str] = None,
        stroke_width: Optional[float] = None,
        **kwargs,
    ):
        """Initialize a Shape.

        Args:
            path: Optional Path object with path operations. If not provided,
                build_path() will be called to generate the path.
            view_box: Optional coordinate system as (width, height). Overrides
                the class-level view_box if provided.
            fill: Fill color as hex string (e.g., "#FF0000"), color name, or
                gradient (LinearGradient, RadialGradient, etc.)
            stroke: Stroke color as hex string or color name.
            stroke_width: Width of the stroke in points.
            **kwargs: Additional view modifiers (width, height, padding, etc.)

        Example:
            Inline shape with color fill::

                shape = Shape(
                    path=Path().move_to(0, 0).line_to(100, 100).close(),
                    fill="red",
                    width=200,
                    height=200,
                )

            Shape with gradient fill::

                shape = Shape(
                    path=Path().add_circle(50, 50, 40),
                    fill=nib.LinearGradient(colors=["#FF0000", "#0000FF"]),
                    view_box=(100, 100),
                    width=100,
                )

            Subclassed shape::

                class MyShape(Shape):
                    view_box = (100, 100)
                    def build_path(self, path):
                        return path.move_to(50, 0).line_to(100, 100).line_to(0, 100).close()

                shape = MyShape(fill="blue")
        """
        super().__init__(**kwargs)
        self._path = path
        self._view_box = view_box or self.__class__.view_box
        self._shape_fill = fill
        self._shape_stroke = stroke
        self._shape_stroke_width = stroke_width

    def build_path(self, path: Path) -> Path:
        """Build the shape's path.

        Override this method in subclasses to define custom shapes.
        The method receives an empty Path and should return the same
        Path with operations added.

        Args:
            path: Empty Path builder to add operations to.

        Returns:
            The path with operations added.

        Example:
            class Star(Shape):
                view_box = (100, 100)

                def build_path(self, path):
                    # 5-pointed star
                    import math
                    cx, cy, outer, inner = 50, 50, 50, 20
                    for i in range(10):
                        angle = math.pi / 2 + i * math.pi / 5
                        r = outer if i % 2 == 0 else inner
                        x = cx + r * math.cos(angle)
                        y = cy - r * math.sin(angle)
                        if i == 0:
                            path.move_to(x, y)
                        else:
                            path.line_to(x, y)
                    return path.close()
        """
        return path

    def _get_path_operations(self) -> list:
        """Get the path operations for serialization.

        Returns:
            List of path operation dictionaries.
        """
        if self._path is not None:
            return self._path.to_list()
        # Build path from subclass method
        path = Path()
        self.build_path(path)
        return path.to_list()

    def _get_props(self) -> dict:
        """Get shape properties for serialization.

        Returns:
            Dictionary of shape properties.
        """
        props = {
            "pathOperations": self._get_path_operations(),
        }

        if self._view_box is not None:
            props["viewBox"] = {
                "w": float(self._view_box[0]),
                "h": float(self._view_box[1]),
            }

        if self._shape_fill is not None:
            if isinstance(self._shape_fill, str):
                # Simple color string
                props["fill"] = self._shape_fill
            elif hasattr(self._shape_fill, "_type"):
                # Gradient view - serialize gradient config
                gradient_type = self._shape_fill._type
                gradient_props = self._shape_fill._get_props()
                props["fillGradient"] = {
                    "type": gradient_type,
                    **gradient_props,
                }

        if self._shape_stroke is not None:
            props["stroke"] = self._shape_stroke

        if self._shape_stroke_width is not None:
            props["strokeWidth"] = float(self._shape_stroke_width)

        return props
