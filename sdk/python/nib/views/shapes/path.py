"""Path builder for custom shapes.

This module provides a fluent Path builder for constructing custom shapes
using bezier paths, arcs, and geometric primitives.

Example:
    Creating a triangle::

        path = nib.Path()
        path.move_to(50, 0)
        path.line_to(100, 100)
        path.line_to(0, 100)
        path.close()

    Creating a heart shape::

        path = (nib.Path()
            .move_to(100, 50)
            .curve_to(100, 0, control1=(100, 25), control2=(75, 0))
            .curve_to(50, 50, control1=(25, 0), control2=(50, 25))
            .curve_to(100, 150, control1=(50, 75), control2=(100, 125))
            .curve_to(150, 50, control1=(100, 125), control2=(150, 75))
            .curve_to(100, 0, control1=(150, 25), control2=(125, 0))
            .curve_to(100, 50, control1=(100, 25), control2=(100, 50))
            .close())
"""

from typing import List, Optional, Tuple


class Path:
    """Fluent path builder for custom shapes.

    Path provides a chainable API for building complex shapes using
    bezier curves, arcs, and geometric primitives. The path can be
    used with nib.Shape to create custom shape views.

    All methods return self for method chaining.

    Attributes:
        _operations: Internal list of path operations.

    Example:
        Using fluent API::

            path = (nib.Path()
                .move_to(0, 0)
                .line_to(100, 0)
                .line_to(100, 100)
                .line_to(0, 100)
                .close())

        Using individual calls::

            path = nib.Path()
            path.move_to(0, 0)
            path.line_to(100, 100)
            path.close()
    """

    def __init__(self):
        """Initialize an empty path."""
        self._operations: List[dict] = []

    def move_to(self, x: float, y: float) -> "Path":
        """Move to a point without drawing.

        Starts a new subpath at the given point. This is typically
        the first operation in a path.

        Args:
            x: X coordinate.
            y: Y coordinate.

        Returns:
            Self for method chaining.
        """
        self._operations.append({"op": "move", "x": float(x), "y": float(y)})
        return self

    def line_to(self, x: float, y: float) -> "Path":
        """Draw a straight line to a point.

        Adds a straight line segment from the current point to the
        specified point.

        Args:
            x: X coordinate of endpoint.
            y: Y coordinate of endpoint.

        Returns:
            Self for method chaining.
        """
        self._operations.append({"op": "line", "x": float(x), "y": float(y)})
        return self

    def curve_to(
        self,
        x: float,
        y: float,
        control1: Tuple[float, float],
        control2: Tuple[float, float],
    ) -> "Path":
        """Draw a cubic bezier curve.

        Adds a cubic bezier curve from the current point to (x, y)
        using two control points.

        Args:
            x: X coordinate of endpoint.
            y: Y coordinate of endpoint.
            control1: First control point as (x, y) tuple.
            control2: Second control point as (x, y) tuple.

        Returns:
            Self for method chaining.

        Example:
            Drawing an S-curve::

                path.move_to(0, 0)
                path.curve_to(100, 100,
                              control1=(0, 50),
                              control2=(100, 50))
        """
        self._operations.append({
            "op": "curve",
            "x": float(x),
            "y": float(y),
            "c1x": float(control1[0]),
            "c1y": float(control1[1]),
            "c2x": float(control2[0]),
            "c2y": float(control2[1]),
        })
        return self

    def quad_curve_to(
        self,
        x: float,
        y: float,
        control: Tuple[float, float],
    ) -> "Path":
        """Draw a quadratic bezier curve.

        Adds a quadratic bezier curve from the current point to (x, y)
        using a single control point.

        Args:
            x: X coordinate of endpoint.
            y: Y coordinate of endpoint.
            control: Control point as (x, y) tuple.

        Returns:
            Self for method chaining.
        """
        self._operations.append({
            "op": "quad",
            "x": float(x),
            "y": float(y),
            "cx": float(control[0]),
            "cy": float(control[1]),
        })
        return self

    def arc(
        self,
        center: Tuple[float, float],
        radius: float,
        start_angle: float,
        end_angle: float,
        clockwise: bool = True,
    ) -> "Path":
        """Draw an arc.

        Adds an arc centered at the given point with the specified radius,
        from start_angle to end_angle.

        Args:
            center: Center point as (x, y) tuple.
            radius: Radius of the arc.
            start_angle: Starting angle in radians.
            end_angle: Ending angle in radians.
            clockwise: Direction of the arc. Defaults to True.

        Returns:
            Self for method chaining.

        Note:
            Angles are in radians. 0 is at the 3 o'clock position,
            and angles increase clockwise.
        """
        self._operations.append({
            "op": "arc",
            "cx": float(center[0]),
            "cy": float(center[1]),
            "radius": float(radius),
            "startAngle": float(start_angle),
            "endAngle": float(end_angle),
            "clockwise": clockwise,
        })
        return self

    def close(self) -> "Path":
        """Close the current subpath.

        Draws a straight line from the current point back to the
        starting point of the current subpath.

        Returns:
            Self for method chaining.
        """
        self._operations.append({"op": "close"})
        return self

    def add_rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> "Path":
        """Add a rectangle to the path.

        Adds a new subpath containing the specified rectangle.

        Args:
            x: X coordinate of top-left corner.
            y: Y coordinate of top-left corner.
            width: Width of rectangle.
            height: Height of rectangle.

        Returns:
            Self for method chaining.
        """
        self._operations.append({
            "op": "rect",
            "x": float(x),
            "y": float(y),
            "w": float(width),
            "h": float(height),
        })
        return self

    def add_rounded_rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        corner_radius: float,
    ) -> "Path":
        """Add a rounded rectangle to the path.

        Adds a new subpath containing a rectangle with rounded corners.

        Args:
            x: X coordinate of top-left corner.
            y: Y coordinate of top-left corner.
            width: Width of rectangle.
            height: Height of rectangle.
            corner_radius: Radius of the rounded corners.

        Returns:
            Self for method chaining.
        """
        self._operations.append({
            "op": "roundedRect",
            "x": float(x),
            "y": float(y),
            "w": float(width),
            "h": float(height),
            "cornerRadius": float(corner_radius),
        })
        return self

    def add_ellipse(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> "Path":
        """Add an ellipse to the path.

        Adds a new subpath containing an ellipse that fits within
        the specified bounding rectangle.

        Args:
            x: X coordinate of bounding rectangle.
            y: Y coordinate of bounding rectangle.
            width: Width of bounding rectangle.
            height: Height of bounding rectangle.

        Returns:
            Self for method chaining.
        """
        self._operations.append({
            "op": "ellipse",
            "x": float(x),
            "y": float(y),
            "w": float(width),
            "h": float(height),
        })
        return self

    def add_circle(
        self,
        center_x: float,
        center_y: float,
        radius: float,
    ) -> "Path":
        """Add a circle to the path.

        Adds a new subpath containing a circle.

        Args:
            center_x: X coordinate of center.
            center_y: Y coordinate of center.
            radius: Radius of the circle.

        Returns:
            Self for method chaining.
        """
        self._operations.append({
            "op": "circle",
            "cx": float(center_x),
            "cy": float(center_y),
            "r": float(radius),
        })
        return self

    def to_list(self) -> List[dict]:
        """Convert path to list of operations for serialization.

        Returns:
            List of operation dictionaries.
        """
        return self._operations

    def __repr__(self) -> str:
        return f"Path({len(self._operations)} operations)"
