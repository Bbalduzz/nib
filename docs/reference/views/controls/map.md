# Map

![Map control](../../../assets/img/controls/map.png)

An interactive map view powered by MapKit. Map supports markers, custom annotations with arbitrary views, circle overlays, polylines, polygons, multiple map styles, and user location display. The center coordinates and zoom level are reactive.

## Constructor

```python
nib.Map(
    latitude=0.0,
    longitude=0.0,
    zoom=0.1,
    markers=None,
    annotations=None,
    circles=None,
    polylines=None,
    polygons=None,
    style=None,
    elevation=None,
    shows_traffic=False,
    shows_compass=False,
    shows_scale=False,
    shows_user_location=False,
    interaction_modes=None,
    on_region_change=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `latitude` | `float` | `0.0` | Center latitude coordinate (-90 to 90). |
| `longitude` | `float` | `0.0` | Center longitude coordinate (-180 to 180). |
| `zoom` | `float` | `0.1` | Zoom level as coordinate span in degrees. Smaller values zoom in more. Use `0.01` for a neighborhood, `0.1` for a city, `1.0` for a country. |
| `markers` | `list[MapMarker]` | `None` | List of `MapMarker` objects to display as pins. |
| `annotations` | `list[MapAnnotation]` | `None` | List of `MapAnnotation` objects for custom view content at coordinates. |
| `circles` | `list[MapCircle]` | `None` | List of `MapCircle` overlays. |
| `polylines` | `list[MapPolyline]` | `None` | List of `MapPolyline` line paths. |
| `polygons` | `list[MapPolygon]` | `None` | List of `MapPolygon` filled areas. |
| `style` | `MapStyle \| str` | `None` | Map style. Options: `MapStyle.STANDARD`, `MapStyle.SATELLITE`, `MapStyle.HYBRID`, `MapStyle.IMAGERY`. |
| `elevation` | `str` | `None` | Elevation style. Options: `"flat"`, `"realistic"` (3D terrain). |
| `shows_traffic` | `bool` | `False` | Whether to show traffic conditions overlay. |
| `shows_compass` | `bool` | `False` | Whether to show the compass control. |
| `shows_scale` | `bool` | `False` | Whether to show the scale indicator. |
| `shows_user_location` | `bool` | `False` | Whether to show the user's current location. |
| `interaction_modes` | `list[MapInteractionMode \| str]` | `None` | Allowed interactions. If `None`, all are enabled. Options: `"pan"`, `"zoom"`, `"rotate"`, `"pitch"`, `"all"`. |
| `on_region_change` | `Callable[[float, float, float], None]` | `None` | Callback when the visible region changes. Receives `(latitude, longitude, zoom)`. |
| `**modifiers` | | | Common view modifiers: `width`, `height`, `corner_radius`, `padding`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `latitude` | `float` | Get or set the center latitude. Triggers a UI update. |
| `longitude` | `float` | Get or set the center longitude. Triggers a UI update. |
| `zoom` | `float` | Get or set the zoom level. Triggers a UI update. |
| `markers` | `list[MapMarker]` | Get or set the markers. Triggers a UI update. |

## Methods

| Method | Description |
|--------|-------------|
| `add_marker(marker)` | Add a single `MapMarker` to the map. |
| `clear_markers()` | Remove all markers from the map. |

---

## Helper Classes

### MapMarker

A pin marker displayed at specific coordinates.

```python
nib.MapMarker(
    latitude,
    longitude,
    title=None,
    subtitle=None,
    tint=None,
    system_image=None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `latitude` | `float` | *(required)* | Latitude coordinate. |
| `longitude` | `float` | *(required)* | Longitude coordinate. |
| `title` | `str` | `None` | Title displayed with the marker. |
| `subtitle` | `str` | `None` | Subtitle displayed below the title. |
| `tint` | `Color \| str` | `None` | Tint color for the marker. |
| `system_image` | `str` | `None` | SF Symbol name for a custom marker icon. |

### MapAnnotation

A custom view displayed at specific coordinates.

```python
nib.MapAnnotation(
    latitude,
    longitude,
    content,
    anchor="bottom",
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `latitude` | `float` | *(required)* | Latitude coordinate. |
| `longitude` | `float` | *(required)* | Longitude coordinate. |
| `content` | `View` | *(required)* | The view to display at this location. |
| `anchor` | `str` | `"bottom"` | Anchor point. Options: `"center"`, `"bottom"`, `"top"`. |

### MapCircle

A circular overlay on the map.

```python
nib.MapCircle(
    latitude,
    longitude,
    radius,
    fill=None,
    stroke=None,
    stroke_width=None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `latitude` | `float` | *(required)* | Center latitude. |
| `longitude` | `float` | *(required)* | Center longitude. |
| `radius` | `float` | *(required)* | Radius in meters. |
| `fill` | `Color \| str` | `None` | Fill color. |
| `stroke` | `Color \| str` | `None` | Stroke color. |
| `stroke_width` | `float` | `None` | Stroke width. |

### MapPolyline

A line connecting multiple coordinates.

```python
nib.MapPolyline(
    coordinates,
    stroke=None,
    stroke_width=None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `coordinates` | `list[tuple[float, float]]` | *(required)* | List of `(latitude, longitude)` tuples. |
| `stroke` | `Color \| str` | `None` | Stroke color. |
| `stroke_width` | `float` | `None` | Line width. |

### MapPolygon

A filled polygon on the map.

```python
nib.MapPolygon(
    coordinates,
    fill=None,
    stroke=None,
    stroke_width=None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `coordinates` | `list[tuple[float, float]]` | *(required)* | List of `(latitude, longitude)` tuples defining vertices. |
| `fill` | `Color \| str` | `None` | Fill color. |
| `stroke` | `Color \| str` | `None` | Stroke color. |
| `stroke_width` | `float` | `None` | Border width. |

---

## Examples

### Map with markers

```python
import nib

def main(app: nib.App):
    app.build(
        nib.Map(
            latitude=37.7749,
            longitude=-122.4194,
            zoom=0.05,
            markers=[
                nib.MapMarker(37.7749, -122.4194, title="San Francisco",
                               tint=nib.Color.RED),
                nib.MapMarker(37.8044, -122.2712, title="Oakland",
                               tint=nib.Color.BLUE),
            ],
            style=nib.MapStyle.STANDARD,
            shows_compass=True,
            width=400,
            height=300,
            corner_radius=12,
            padding=16,
        )
    )

nib.run(main)
```

### Map with custom annotations

```python
import nib

def main(app: nib.App):
    app.build(
        nib.Map(
            latitude=48.8566,
            longitude=2.3522,
            zoom=0.02,
            annotations=[
                nib.MapAnnotation(
                    latitude=48.8584,
                    longitude=2.2945,
                    content=nib.VStack(controls=[
                        nib.Image(system_name="star.fill",
                                   foreground_color=nib.Color.YELLOW),
                        nib.Text("Eiffel Tower", font=nib.Font.CAPTION),
                    ], padding=4, background=nib.Color.WHITE,
                       corner_radius=6),
                ),
            ],
            style=nib.MapStyle.HYBRID,
            width=400,
            height=300,
            corner_radius=12,
            padding=16,
        )
    )

nib.run(main)
```

### Map with overlays

```python
import nib

def main(app: nib.App):
    app.build(
        nib.Map(
            latitude=37.7749,
            longitude=-122.4194,
            zoom=0.05,
            circles=[
                nib.MapCircle(37.7749, -122.4194, radius=1000,
                               fill="#0000FF33", stroke=nib.Color.BLUE,
                               stroke_width=2),
            ],
            polylines=[
                nib.MapPolyline(
                    coordinates=[
                        (37.7749, -122.4194),
                        (37.8044, -122.2712),
                        (37.8716, -122.2727),
                    ],
                    stroke=nib.Color.RED,
                    stroke_width=3,
                ),
            ],
            width=400,
            height=300,
            padding=16,
        )
    )

nib.run(main)
```
