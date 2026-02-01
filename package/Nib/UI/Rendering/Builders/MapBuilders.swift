import SwiftUI
import MapKit

// MARK: - Map Builder

extension DynamicView {
    @ViewBuilder
    func buildMap() -> some View {
        let lat = node.props.latitude ?? 0
        let lon = node.props.longitude ?? 0
        let zoom = node.props.zoom ?? 0.1

        let center = CLLocationCoordinate2D(latitude: lat, longitude: lon)
        let span = MKCoordinateSpan(latitudeDelta: zoom, longitudeDelta: zoom)
        let region = MKCoordinateRegion(center: center, span: span)

        MapViewWrapper(
            region: region,
            markers: node.props.markers ?? [],
            annotations: node.props.annotations ?? [],
            circles: node.props.circles ?? [],
            polylines: node.props.polylines ?? [],
            polygons: node.props.polygons ?? [],
            settings: node.props.mapSettings,
            onEvent: onEvent
        )
    }
}

// MARK: - Map View Wrapper

/// SwiftUI wrapper for Map view with markers and annotations
struct MapViewWrapper: View {
    let region: MKCoordinateRegion
    let markers: [ViewNode.MapMarkerData]
    let annotations: [ViewNode.MapAnnotationData]
    let circles: [ViewNode.MapCircleData]
    let polylines: [ViewNode.MapPolylineData]
    let polygons: [ViewNode.MapPolygonData]
    let settings: ViewNode.MapSettings?
    let onEvent: (String, String) -> Void

    @State private var position: MapCameraPosition

    init(region: MKCoordinateRegion,
         markers: [ViewNode.MapMarkerData],
         annotations: [ViewNode.MapAnnotationData],
         circles: [ViewNode.MapCircleData],
         polylines: [ViewNode.MapPolylineData],
         polygons: [ViewNode.MapPolygonData],
         settings: ViewNode.MapSettings?,
         onEvent: @escaping (String, String) -> Void) {
        self.region = region
        self.markers = markers
        self.annotations = annotations
        self.circles = circles
        self.polylines = polylines
        self.polygons = polygons
        self.settings = settings
        self.onEvent = onEvent
        self._position = State(initialValue: .region(region))
    }

    var body: some View {
        Map(position: $position, interactionModes: interactionModes) {
            // Add circles
            ForEach(Array(circles.enumerated()), id: \.offset) { index, circle in
                let coord = CLLocationCoordinate2D(latitude: circle.latitude, longitude: circle.longitude)
                MapCircle(center: coord, radius: circle.radius)
                    .foregroundStyle(circle.fill.map { Color(nibColor: $0) } ?? .blue.opacity(0.2))
                    .stroke(circle.stroke.map { Color(nibColor: $0) } ?? .blue, lineWidth: circle.strokeWidth ?? 1)
            }

            // Add polylines
            ForEach(Array(polylines.enumerated()), id: \.offset) { index, polyline in
                let coords = polyline.coordinates.map {
                    CLLocationCoordinate2D(latitude: $0.latitude, longitude: $0.longitude)
                }
                MapPolyline(coordinates: coords)
                    .stroke(polyline.stroke.map { Color(nibColor: $0) } ?? .blue, lineWidth: polyline.strokeWidth ?? 2)
            }

            // Add polygons
            ForEach(Array(polygons.enumerated()), id: \.offset) { index, polygon in
                let coords = polygon.coordinates.map {
                    CLLocationCoordinate2D(latitude: $0.latitude, longitude: $0.longitude)
                }
                MapPolygon(coordinates: coords)
                    .foregroundStyle(polygon.fill.map { Color(nibColor: $0) } ?? .blue.opacity(0.2))
                    .stroke(polygon.stroke.map { Color(nibColor: $0) } ?? .blue, lineWidth: polygon.strokeWidth ?? 1)
            }

            // Add markers
            ForEach(Array(markers.enumerated()), id: \.offset) { index, marker in
                let coord = CLLocationCoordinate2D(latitude: marker.latitude, longitude: marker.longitude)
                let tintColor = marker.tint.map { Color(nibColor: $0) } ?? .red

                if let systemImage = marker.systemImage {
                    Marker(marker.title ?? "", systemImage: systemImage, coordinate: coord)
                        .tint(tintColor)
                } else {
                    Marker(marker.title ?? "", coordinate: coord)
                        .tint(tintColor)
                }
            }

            // Add annotations with custom content
            ForEach(Array(annotations.enumerated()), id: \.offset) { index, annotation in
                let coord = CLLocationCoordinate2D(latitude: annotation.latitude, longitude: annotation.longitude)

                if let contentNode = annotation.content {
                    Annotation("", coordinate: coord, anchor: anchorPoint(annotation.anchor)) {
                        DynamicView(node: contentNode, onEvent: onEvent)
                    }
                }
            }
        }
        .mapStyle(mapStyle)
        .mapControls {
            if settings?.showsCompass == true {
                MapCompass()
            }
            if settings?.showsScale == true {
                MapScaleView()
            }
            if settings?.showsUserLocation == true {
                MapUserLocationButton()
            }
        }
    }

    private var interactionModes: MapInteractionModes {
        guard let modes = settings?.interactionModes else {
            return .all
        }

        if modes.contains("all") {
            return .all
        }

        var result: MapInteractionModes = []
        if modes.contains("pan") { result.insert(.pan) }
        if modes.contains("zoom") { result.insert(.zoom) }
        if modes.contains("rotate") { result.insert(.rotate) }
        if modes.contains("pitch") { result.insert(.pitch) }

        return result.isEmpty ? .all : result
    }

    private var mapStyle: MapStyle {
        guard let style = settings?.style else {
            return .standard
        }

        let elevation: MapStyle.Elevation = settings?.elevation == "realistic" ? .realistic : .flat

        switch style.lowercased() {
        case "satellite":
            return .imagery(elevation: elevation)
        case "hybrid":
            return .hybrid(elevation: elevation)
        case "imagery":
            return .imagery(elevation: elevation)
        default:
            return .standard(elevation: elevation)
        }
    }

    private func anchorPoint(_ anchor: String?) -> UnitPoint {
        switch anchor?.lowercased() {
        case "top": return .top
        case "center": return .center
        case "bottom": return .bottom
        default: return .bottom
        }
    }
}
