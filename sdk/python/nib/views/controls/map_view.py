"""Map view for displaying interactive maps with markers and annotations.

The Map view provides an interactive map using MapKit. It supports markers,
annotations with custom views, different map styles, and camera position control.

Example:
    Basic map centered on a location::

        nib.Map(
            latitude=37.7749,
            longitude=-122.4194,
            zoom=0.05,
        )

    Map with markers::

        nib.Map(
            latitude=37.7749,
            longitude=-122.4194,
            markers=[
                nib.MapMarker(
                    latitude=37.7749,
                    longitude=-122.4194,
                    title="San Francisco",
                    tint=nib.Color.RED,
                ),
            ],
        )

    Map with custom annotation views::

        nib.Map(
            latitude=37.7749,
            longitude=-122.4194,
            annotations=[
                nib.MapAnnotation(
                    latitude=37.7749,
                    longitude=-122.4194,
                    content=nib.HStack(
                        controls=[
                            nib.Text("📍"),
                            nib.Text("SF", font=nib.Font.caption),
                        ],
                        padding=4,
                        background=nib.Color.WHITE,
                        corner_radius=6,
                    ),
                ),
            ],
        )

    Satellite map with custom controls::

        nib.Map(
            latitude=51.5074,
            longitude=-0.1278,
            style=nib.MapStyle.SATELLITE,
            shows_compass=True,
            shows_scale=True,
        )
"""

from typing import Any, Callable, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

from ..base import View, _float
from ...types import ColorLike, resolve_color


class MapStyle(Enum):
    """Map display styles."""
    STANDARD = "standard"
    SATELLITE = "satellite"
    HYBRID = "hybrid"
    IMAGERY = "imagery"


class MapInteractionMode(Enum):
    """Map interaction modes."""
    ALL = "all"
    PAN = "pan"
    ZOOM = "zoom"
    ROTATE = "rotate"
    PITCH = "pitch"


@dataclass
class MapMarker:
    """A marker to display on the map.

    Markers appear as pins at specific coordinates with an optional title
    and custom tint color.

    Attributes:
        latitude: The latitude coordinate.
        longitude: The longitude coordinate.
        title: Optional title displayed with the marker.
        subtitle: Optional subtitle displayed below the title.
        tint: Optional tint color for the marker.
        system_image: Optional SF Symbol name for custom marker icon.

    Example:
        Create a marker::

            nib.MapMarker(
                latitude=37.7749,
                longitude=-122.4194,
                title="San Francisco",
                tint=nib.Color.BLUE,
            )
    """
    latitude: float
    longitude: float
    title: Optional[str] = None
    subtitle: Optional[str] = None
    tint: Optional[ColorLike] = None
    system_image: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        result = {
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
        }
        if self.title:
            result["title"] = self.title
        if self.subtitle:
            result["subtitle"] = self.subtitle
        if self.tint:
            result["tint"] = resolve_color(self.tint)
        if self.system_image:
            result["systemImage"] = self.system_image
        return result


@dataclass
class MapCircle:
    """A circular overlay on the map.

    Displays a circle with a specified center and radius.

    Attributes:
        latitude: Center latitude coordinate.
        longitude: Center longitude coordinate.
        radius: Radius in meters.
        fill: Optional fill color.
        stroke: Optional stroke color.
        stroke_width: Optional stroke width.

    Example:
        Create a circle overlay::

            nib.MapCircle(
                latitude=37.7749,
                longitude=-122.4194,
                radius=1000,  # 1km radius
                fill=nib.Color.BLUE.with_opacity(0.2),
                stroke=nib.Color.BLUE,
                stroke_width=2,
            )
    """
    latitude: float
    longitude: float
    radius: float  # in meters
    fill: Optional[ColorLike] = None
    stroke: Optional[ColorLike] = None
    stroke_width: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        result = {
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "radius": float(self.radius),
        }
        if self.fill:
            result["fill"] = resolve_color(self.fill)
        if self.stroke:
            result["stroke"] = resolve_color(self.stroke)
        if self.stroke_width is not None:
            result["strokeWidth"] = float(self.stroke_width)
        return result


@dataclass
class MapPolyline:
    """A line connecting multiple coordinates on the map.

    Displays a line path through the specified coordinates.

    Attributes:
        coordinates: List of (latitude, longitude) tuples.
        stroke: Stroke color.
        stroke_width: Line width.

    Example:
        Create a route line::

            nib.MapPolyline(
                coordinates=[
                    (37.7749, -122.4194),  # San Francisco
                    (37.8044, -122.2712),  # Oakland
                    (37.8716, -122.2727),  # Berkeley
                ],
                stroke=nib.Color.BLUE,
                stroke_width=3,
            )
    """
    coordinates: List[tuple]  # List of (lat, lon) tuples
    stroke: Optional[ColorLike] = None
    stroke_width: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        result = {
            "coordinates": [
                {"latitude": float(lat), "longitude": float(lon)}
                for lat, lon in self.coordinates
            ],
        }
        if self.stroke:
            result["stroke"] = resolve_color(self.stroke)
        if self.stroke_width is not None:
            result["strokeWidth"] = float(self.stroke_width)
        return result


@dataclass
class MapPolygon:
    """A filled polygon on the map.

    Displays a closed polygon shape defined by coordinates.

    Attributes:
        coordinates: List of (latitude, longitude) tuples defining vertices.
        fill: Fill color for the polygon interior.
        stroke: Stroke color for the polygon border.
        stroke_width: Border line width.

    Example:
        Create a polygon area::

            nib.MapPolygon(
                coordinates=[
                    (37.78, -122.42),
                    (37.77, -122.40),
                    (37.76, -122.42),
                    (37.77, -122.44),
                ],
                fill=nib.Color.GREEN.with_opacity(0.3),
                stroke=nib.Color.GREEN,
                stroke_width=2,
            )
    """
    coordinates: List[tuple]  # List of (lat, lon) tuples
    fill: Optional[ColorLike] = None
    stroke: Optional[ColorLike] = None
    stroke_width: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        result = {
            "coordinates": [
                {"latitude": float(lat), "longitude": float(lon)}
                for lat, lon in self.coordinates
            ],
        }
        if self.fill:
            result["fill"] = resolve_color(self.fill)
        if self.stroke:
            result["stroke"] = resolve_color(self.stroke)
        if self.stroke_width is not None:
            result["strokeWidth"] = float(self.stroke_width)
        return result


class MapAnnotation:
    """A custom annotation to display on the map.

    Annotations allow custom view content at specific coordinates.

    Attributes:
        latitude: The latitude coordinate.
        longitude: The longitude coordinate.
        content: The View to display at the annotation location.
        anchor: Anchor point ("center", "bottom", "top").

    Example:
        Create an annotation with custom content::

            nib.MapAnnotation(
                latitude=37.7749,
                longitude=-122.4194,
                content=nib.VStack(
                    controls=[
                        nib.Image(src="pin.png", width=24, height=24),
                        nib.Text("San Francisco", font=nib.Font.caption),
                    ],
                    padding=4,
                    background=nib.Color.WHITE,
                    corner_radius=8,
                ),
            )

        Simple text annotation::

            nib.MapAnnotation(
                latitude=37.7749,
                longitude=-122.4194,
                content=nib.Text("📍 Here"),
            )
    """

    def __init__(
        self,
        latitude: float,
        longitude: float,
        content: "View",
        anchor: str = "bottom",
    ):
        """Initialize a MapAnnotation.

        Args:
            latitude: The latitude coordinate.
            longitude: The longitude coordinate.
            content: The View to display at this location.
            anchor: Anchor point - "center", "bottom", or "top".
        """
        self.latitude = latitude
        self.longitude = longitude
        self.content = content
        self.anchor = anchor

    def to_dict(self, path: str) -> dict:
        """Convert to dictionary for serialization.

        Args:
            path: Base path for generating child view IDs.
        """
        return {
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "anchor": self.anchor,
            "content": self.content.to_dict(path),
        }


class Map(View):
    """An interactive map view using MapKit.

    Map displays an interactive map with support for markers, annotations,
    different styles, and user interaction. The map can be centered on
    specific coordinates with adjustable zoom level.

    Attributes:
        latitude: Center latitude coordinate.
        longitude: Center longitude coordinate.
        zoom: Zoom level (span in degrees, smaller = more zoomed in).
        markers: List of MapMarker objects to display.
        annotations: List of MapAnnotation objects to display.
        style: Map style (standard, satellite, hybrid).

    Example:
        Map centered on New York::

            nib.Map(
                latitude=40.7128,
                longitude=-74.0060,
                zoom=0.1,
                style=nib.MapStyle.STANDARD,
            )

        Map with multiple markers::

            nib.Map(
                latitude=37.7749,
                longitude=-122.4194,
                zoom=0.05,
                markers=[
                    nib.MapMarker(37.7749, -122.4194, "San Francisco"),
                    nib.MapMarker(37.8044, -122.2712, "Oakland"),
                ],
            )

        Satellite map with controls::

            nib.Map(
                latitude=48.8566,
                longitude=2.3522,
                zoom=0.02,
                style=nib.MapStyle.SATELLITE,
                shows_compass=True,
                shows_scale=True,
                shows_user_location=True,
            )
    """

    _type = "Map"

    def __init__(
        self,
        latitude: float = 0.0,
        longitude: float = 0.0,
        zoom: float = 0.1,
        # Map content
        markers: Optional[List[MapMarker]] = None,
        annotations: Optional[List[MapAnnotation]] = None,
        circles: Optional[List[MapCircle]] = None,
        polylines: Optional[List[MapPolyline]] = None,
        polygons: Optional[List[MapPolygon]] = None,
        # Map style
        style: Optional[Union[MapStyle, str]] = None,
        elevation: Optional[str] = None,  # "flat", "realistic"
        shows_traffic: bool = False,
        # Map controls
        shows_compass: bool = False,
        shows_scale: bool = False,
        shows_user_location: bool = False,
        # Interaction
        interaction_modes: Optional[List[Union[MapInteractionMode, str]]] = None,
        on_region_change: Optional[Callable[[float, float, float], None]] = None,
        # View modifiers
        **kwargs: Any,
    ):
        """Initialize a Map view.

        Args:
            latitude: Center latitude coordinate (-90 to 90).
            longitude: Center longitude coordinate (-180 to 180).
            zoom: Zoom level as coordinate span in degrees. Smaller values
                mean more zoomed in. Default 0.1 shows roughly a city.
                Use 0.01 for a neighborhood, 1.0 for a country.
            markers: List of MapMarker objects to display as pins.
            annotations: List of MapAnnotation objects for custom content.
            circles: List of MapCircle objects for circular overlays.
            polylines: List of MapPolyline objects for line paths.
            polygons: List of MapPolygon objects for filled areas.
            style: Map style - "standard", "satellite", "hybrid", or MapStyle enum.
            elevation: Elevation style - "flat" or "realistic" (3D terrain).
            shows_traffic: Whether to show traffic conditions overlay.
            shows_compass: Whether to show the compass control.
            shows_scale: Whether to show the scale indicator.
            shows_user_location: Whether to show the user's current location.
            interaction_modes: List of allowed interactions. If None, all are enabled.
                Options: "pan", "zoom", "rotate", "pitch", "all".
            on_region_change: Callback when the visible region changes.
                Receives (latitude, longitude, zoom) of the new center.
            **kwargs: Standard view modifiers including width, height,
                corner_radius, padding, etc.

        Example:
            Create a map showing Paris::

                nib.Map(
                    latitude=48.8566,
                    longitude=2.3522,
                    zoom=0.05,
                    markers=[
                        nib.MapMarker(
                            48.8584, 2.2945,
                            title="Eiffel Tower",
                            system_image="star.fill",
                        ),
                    ],
                    style=nib.MapStyle.HYBRID,
                    shows_compass=True,
                    width=400,
                    height=300,
                    corner_radius=12,
                )
        """
        super().__init__(**kwargs)
        self._latitude = latitude
        self._longitude = longitude
        self._zoom = zoom
        self._markers = markers or []
        self._annotations = annotations or []
        self._circles = circles or []
        self._polylines = polylines or []
        self._polygons = polygons or []
        self._on_region_change = on_region_change

        # Build map settings
        self._map_settings: dict = {}

        if style is not None:
            if isinstance(style, MapStyle):
                self._map_settings["style"] = style.value
            else:
                self._map_settings["style"] = style

        if elevation:
            self._map_settings["elevation"] = elevation

        if shows_traffic:
            self._map_settings["showsTraffic"] = True

        if shows_compass:
            self._map_settings["showsCompass"] = True

        if shows_scale:
            self._map_settings["showsScale"] = True

        if shows_user_location:
            self._map_settings["showsUserLocation"] = True

        if interaction_modes is not None:
            modes = []
            for mode in interaction_modes:
                if isinstance(mode, MapInteractionMode):
                    modes.append(mode.value)
                else:
                    modes.append(mode)
            self._map_settings["interactionModes"] = modes

    @property
    def latitude(self) -> float:
        """Get the center latitude."""
        return self._latitude

    @latitude.setter
    def latitude(self, value: float) -> None:
        """Set the center latitude and update the map."""
        self._latitude = value
        self._trigger_update()

    @property
    def longitude(self) -> float:
        """Get the center longitude."""
        return self._longitude

    @longitude.setter
    def longitude(self, value: float) -> None:
        """Set the center longitude and update the map."""
        self._longitude = value
        self._trigger_update()

    @property
    def zoom(self) -> float:
        """Get the zoom level."""
        return self._zoom

    @zoom.setter
    def zoom(self, value: float) -> None:
        """Set the zoom level and update the map."""
        self._zoom = value
        self._trigger_update()

    @property
    def markers(self) -> List[MapMarker]:
        """Get the list of markers."""
        return self._markers

    @markers.setter
    def markers(self, value: List[MapMarker]) -> None:
        """Set the markers and update the map."""
        self._markers = value
        self._trigger_update()

    def add_marker(self, marker: MapMarker) -> None:
        """Add a marker to the map.

        Args:
            marker: The MapMarker to add.
        """
        self._markers.append(marker)
        self._trigger_update()

    def clear_markers(self) -> None:
        """Remove all markers from the map."""
        self._markers.clear()
        self._trigger_update()

    def _get_props(self) -> dict:
        props = {
            "latitude": _float(self._latitude),
            "longitude": _float(self._longitude),
            "zoom": _float(self._zoom),
        }

        if self._markers:
            props["markers"] = [m.to_dict() for m in self._markers]

        if self._circles:
            props["circles"] = [c.to_dict() for c in self._circles]

        if self._polylines:
            props["polylines"] = [p.to_dict() for p in self._polylines]

        if self._polygons:
            props["polygons"] = [p.to_dict() for p in self._polygons]

        # Annotations are serialized in to_dict since they need paths
        if self._map_settings:
            props["mapSettings"] = self._map_settings

        return props

    def to_dict(self, path: str = "0") -> dict:
        """Convert the view to a dictionary for serialization."""
        result = super().to_dict(path)

        # Add annotations with proper paths for their content views
        if self._annotations:
            result["props"]["annotations"] = [
                a.to_dict(f"{path}.ann.{i}")
                for i, a in enumerate(self._annotations)
                if a.content._visible
            ]

        return result

    def _set_app(self, app) -> None:
        """Set the parent App reference recursively."""
        super()._set_app(app)
        # Propagate to annotation content views
        for annotation in self._annotations:
            if hasattr(annotation.content, "_set_app"):
                annotation.content._set_app(app)
