import Foundation
import SwiftUI

// MARK: - Map Types

extension ViewNode {
    /// Map marker data
    struct MapMarkerData: Codable, Equatable {
        var latitude: Double
        var longitude: Double
        var title: String?
        var subtitle: String?
        var tint: String?
        var systemImage: String?
    }

    /// Map annotation data
    struct MapAnnotationData: Codable, Equatable {
        var latitude: Double
        var longitude: Double
        var anchor: String?  // "center", "bottom", "top"
        var content: ViewNode?  // Custom view content
    }

    /// Map settings
    struct MapSettings: Codable, Equatable {
        var style: String?            // "standard", "satellite", "hybrid", "imagery"
        var elevation: String?        // "flat", "realistic"
        var showsTraffic: Bool?
        var showsCompass: Bool?
        var showsScale: Bool?
        var showsUserLocation: Bool?
        var interactionModes: [String]?  // ["pan", "zoom", "rotate", "pitch", "all"]
    }

    /// Map circle overlay data
    struct MapCircleData: Codable, Equatable {
        var latitude: Double
        var longitude: Double
        var radius: Double  // in meters
        var fill: String?
        var stroke: String?
        var strokeWidth: Double?
    }

    /// Map coordinate for polylines and polygons
    struct MapCoordinate: Codable, Equatable {
        var latitude: Double
        var longitude: Double
    }

    /// Map polyline data
    struct MapPolylineData: Codable, Equatable {
        var coordinates: [MapCoordinate]
        var stroke: String?
        var strokeWidth: Double?
    }

    /// Map polygon data
    struct MapPolygonData: Codable, Equatable {
        var coordinates: [MapCoordinate]
        var fill: String?
        var stroke: String?
        var strokeWidth: Double?
    }
}
