"""Gradient shape views.

This module provides gradient views that can be used as backgrounds, overlays,
or standalone views in Nib applications.

Supported gradients:
    - :class:`LinearGradient`: Colors along a line from start to end points
    - :class:`RadialGradient`: Colors radiating from a center point
    - :class:`AngularGradient`: Colors rotating around a center point
    - :class:`EllipticalGradient`: Colors in an elliptical pattern

Example:
    Linear gradient background::

        nib.VStack(
            controls=[nib.Text("Hello")],
            background=nib.LinearGradient(
                colors=["#FF0000", "#0000FF"],
                start=(0, 0),
                end=(1, 1),
            ),
        )

    Gradient with explicit stops::

        nib.LinearGradient(
            stops=[
                (0.0, "#FF0000"),
                (0.3, "#FFFF00"),
                (1.0, "#0000FF"),
            ],
        )
"""

from typing import Any, Optional, Union
from ..base import View
from ...types import ColorLike, resolve_color


# Type alias for gradient stops: (position, color) where position is 0.0-1.0
GradientStop = tuple[float, ColorLike]


class LinearGradient(View):
    """A gradient that varies colors along a line from start to end points.

    LinearGradient creates a smooth color transition along a straight line.
    The start and end points are specified in unit coordinates (0-1) where
    (0, 0) is top-left and (1, 1) is bottom-right.

    Args:
        colors: List of colors for the gradient, evenly distributed.
            Use this OR stops, not both.
        stops: List of (position, color) tuples for explicit control.
            Positions are 0.0-1.0. Use this OR colors, not both.
        start: Start point as (x, y) in unit coordinates. Default (0.5, 0) is top-center.
        end: End point as (x, y) in unit coordinates. Default (0.5, 1) is bottom-center.
        **kwargs: Additional view modifiers.

    Example:
        Simple two-color gradient::

            nib.LinearGradient(colors=["red", "blue"])

        Diagonal gradient with explicit stops::

            nib.LinearGradient(
                stops=[(0.0, "red"), (0.5, "yellow"), (1.0, "blue")],
                start=(0, 0),
                end=(1, 1),
            )
    """

    _type = "LinearGradient"

    def __init__(
        self,
        colors: Optional[list[ColorLike]] = None,
        stops: Optional[list[GradientStop]] = None,
        start: tuple[float, float] = (0.5, 0),
        end: tuple[float, float] = (0.5, 1),
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._colors = colors
        self._stops = stops
        self._start = start
        self._end = end

    def _get_props(self) -> dict:
        props: dict[str, Any] = {
            "startPoint": [float(self._start[0]), float(self._start[1])],
            "endPoint": [float(self._end[0]), float(self._end[1])],
        }
        if self._colors is not None:
            props["colors"] = [resolve_color(c) for c in self._colors]
        if self._stops is not None:
            props["stops"] = [[float(s[0]), resolve_color(s[1])] for s in self._stops]
        return props


class RadialGradient(View):
    """A gradient that radiates outward from a center point.

    RadialGradient creates a circular color transition from center outward.
    Colors transition from start_radius to end_radius.

    Args:
        colors: List of colors for the gradient, evenly distributed.
            Use this OR stops, not both.
        stops: List of (position, color) tuples for explicit control.
            Positions are 0.0-1.0. Use this OR colors, not both.
        center: Center point as (x, y) in unit coordinates. Default (0.5, 0.5) is center.
        start_radius: Inner radius where gradient begins. Default 0.
        end_radius: Outer radius where gradient ends. Default 100.
        **kwargs: Additional view modifiers.

    Example:
        Simple radial gradient::

            nib.RadialGradient(
                colors=["white", "black"],
                center=(0.5, 0.5),
                start_radius=0,
                end_radius=100,
            )
    """

    _type = "RadialGradient"

    def __init__(
        self,
        colors: Optional[list[ColorLike]] = None,
        stops: Optional[list[GradientStop]] = None,
        center: tuple[float, float] = (0.5, 0.5),
        start_radius: float = 0,
        end_radius: float = 100,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._colors = colors
        self._stops = stops
        self._center = center
        self._start_radius = start_radius
        self._end_radius = end_radius

    def _get_props(self) -> dict:
        props: dict[str, Any] = {
            "center": [float(self._center[0]), float(self._center[1])],
            "startRadius": float(self._start_radius),
            "endRadius": float(self._end_radius),
        }
        if self._colors is not None:
            props["colors"] = [resolve_color(c) for c in self._colors]
        if self._stops is not None:
            props["stops"] = [[float(s[0]), resolve_color(s[1])] for s in self._stops]
        return props


class AngularGradient(View):
    """A gradient that rotates colors around a center point.

    AngularGradient (also known as conic gradient) creates a color wheel effect
    where colors transition around a central point.

    Args:
        colors: List of colors for the gradient, evenly distributed.
            Use this OR stops, not both.
        stops: List of (position, color) tuples for explicit control.
            Positions are 0.0-1.0. Use this OR colors, not both.
        center: Center point as (x, y) in unit coordinates. Default (0.5, 0.5).
        start_angle: Starting angle in degrees. Default 0 (top).
        end_angle: Ending angle in degrees. Default 360 (full circle).
        **kwargs: Additional view modifiers.

    Example:
        Color wheel::

            nib.AngularGradient(
                colors=["red", "yellow", "green", "cyan", "blue", "magenta", "red"],
                center=(0.5, 0.5),
            )

        Partial arc::

            nib.AngularGradient(
                colors=["blue", "purple"],
                start_angle=0,
                end_angle=180,
            )
    """

    _type = "AngularGradient"

    def __init__(
        self,
        colors: Optional[list[ColorLike]] = None,
        stops: Optional[list[GradientStop]] = None,
        center: tuple[float, float] = (0.5, 0.5),
        start_angle: float = 0,
        end_angle: float = 360,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._colors = colors
        self._stops = stops
        self._center = center
        self._start_angle = start_angle
        self._end_angle = end_angle

    def _get_props(self) -> dict:
        props: dict[str, Any] = {
            "center": [float(self._center[0]), float(self._center[1])],
            "startAngle": float(self._start_angle),
            "endAngle": float(self._end_angle),
        }
        if self._colors is not None:
            props["colors"] = [resolve_color(c) for c in self._colors]
        if self._stops is not None:
            props["stops"] = [[float(s[0]), resolve_color(s[1])] for s in self._stops]
        return props


class EllipticalGradient(View):
    """A gradient that radiates outward in an elliptical shape.

    EllipticalGradient is similar to RadialGradient but stretches to fill
    the view's frame, creating an elliptical pattern rather than circular.

    Args:
        colors: List of colors for the gradient, evenly distributed.
            Use this OR stops, not both.
        stops: List of (position, color) tuples for explicit control.
            Positions are 0.0-1.0. Use this OR colors, not both.
        center: Center point as (x, y) in unit coordinates. Default (0.5, 0.5).
        start_radius_fraction: Fraction of view size where gradient starts. Default 0.
        end_radius_fraction: Fraction of view size where gradient ends. Default 0.5.
        **kwargs: Additional view modifiers.

    Example:
        Elliptical spotlight effect::

            nib.EllipticalGradient(
                colors=["white", "black"],
                center=(0.5, 0.5),
                start_radius_fraction=0,
                end_radius_fraction=0.7,
            )
    """

    _type = "EllipticalGradient"

    def __init__(
        self,
        colors: Optional[list[ColorLike]] = None,
        stops: Optional[list[GradientStop]] = None,
        center: tuple[float, float] = (0.5, 0.5),
        start_radius_fraction: float = 0,
        end_radius_fraction: float = 0.5,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._colors = colors
        self._stops = stops
        self._center = center
        self._start_radius_fraction = start_radius_fraction
        self._end_radius_fraction = end_radius_fraction

    def _get_props(self) -> dict:
        props: dict[str, Any] = {
            "center": [float(self._center[0]), float(self._center[1])],
            "startRadiusFraction": float(self._start_radius_fraction),
            "endRadiusFraction": float(self._end_radius_fraction),
        }
        if self._colors is not None:
            props["colors"] = [resolve_color(c) for c in self._colors]
        if self._stops is not None:
            props["stops"] = [[float(s[0]), resolve_color(s[1])] for s in self._stops]
        return props
