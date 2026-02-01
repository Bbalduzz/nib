import Foundation

// MARK: - Path Operation Types

/// A single path operation for custom shapes.
/// Represents operations like move, line, curve, arc, close, etc.
struct PathOperation: Codable, Equatable {
    /// Operation type: "move", "line", "curve", "quad", "arc", "close",
    /// "rect", "roundedRect", "ellipse", "circle"
    let op: String

    // Point coordinates (for move, line, curve, quad)
    var x: Double?
    var y: Double?

    // Cubic bezier control points (for curve)
    var c1x: Double?
    var c1y: Double?
    var c2x: Double?
    var c2y: Double?

    // Quadratic bezier / arc center control point
    var cx: Double?
    var cy: Double?

    // Dimensions (for rect, roundedRect, ellipse)
    var w: Double?
    var h: Double?

    // Radius (for circle, arc)
    var r: Double?
    var radius: Double?

    // Corner radius (for roundedRect)
    var cornerRadius: Double?

    // Arc angles (in radians)
    var startAngle: Double?
    var endAngle: Double?

    // Arc direction
    var clockwise: Bool?
}

/// Defines the coordinate system for a custom shape.
/// When rendering, the path is scaled to fit within the view bounds.
struct ViewBox: Codable, Equatable {
    let w: Double
    let h: Double
}

/// Per-corner radius configuration for Rectangle shapes.
/// Uses SwiftUI's naming convention: topLeading, topTrailing, bottomLeading, bottomTrailing.
struct CornerRadii: Codable, Equatable {
    var topLeading: CGFloat
    var topTrailing: CGFloat
    var bottomLeading: CGFloat
    var bottomTrailing: CGFloat

    init(topLeading: CGFloat = 0, topTrailing: CGFloat = 0, bottomLeading: CGFloat = 0, bottomTrailing: CGFloat = 0) {
        self.topLeading = topLeading
        self.topTrailing = topTrailing
        self.bottomLeading = bottomLeading
        self.bottomTrailing = bottomTrailing
    }

    /// Check if all corners have the same radius
    var isUniform: Bool {
        topLeading == topTrailing && topLeading == bottomLeading && topLeading == bottomTrailing
    }
}

/// Gradient configuration for shape fills.
struct ShapeGradient: Codable, Equatable {
    /// Gradient type: "LinearGradient", "RadialGradient", "AngularGradient", "EllipticalGradient"
    let type: String

    // Colors (simple list)
    var colors: [String]?

    // Explicit stops: [[position, color], ...]
    var stops: [[Double]]?  // Actually mixed, but we'll parse manually

    // LinearGradient points
    var startPoint: [Double]?
    var endPoint: [Double]?

    // RadialGradient / AngularGradient / EllipticalGradient
    var center: [Double]?
    var startRadius: Double?
    var endRadius: Double?
    var startAngle: Double?
    var endAngle: Double?
    var startRadiusFraction: Double?
    var endRadiusFraction: Double?
}
