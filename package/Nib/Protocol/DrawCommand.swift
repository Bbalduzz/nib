import Foundation
import CoreGraphics

/// A drawing command for Canvas views.
///
/// DrawCommand represents a single drawing operation that can be rendered
/// using Core Graphics. Commands are sent from Python and decoded for rendering.
struct DrawCommand: Codable, Equatable {
    /// The type of drawing command (rect, circle, line, path, image, text, points, shadow, fill, colorFill)
    let type: String

    // MARK: - Position & Size (Rect, Ellipse, Image)

    var x: Double?
    var y: Double?
    var width: Double?
    var height: Double?
    var cornerRadius: Double?

    // MARK: - Circle/Ellipse/Arc

    var cx: Double?
    var cy: Double?
    var radius: Double?
    var rx: Double?
    var ry: Double?

    // MARK: - Arc specific

    var startAngle: Double?
    var endAngle: Double?
    var clockwise: Bool?

    // MARK: - Line

    var x1: Double?
    var y1: Double?
    var x2: Double?
    var y2: Double?

    // MARK: - Path/Polygon/Points

    var points: [[Double]]?
    var closed: Bool?
    var pointMode: String?  // "points", "lines", "polygon"

    // MARK: - BezierPath

    var elements: [PathElement]?  // For bezierPath type (new format)
    var commands: [BezierCommand]?  // For bezierPath type (legacy format)

    // MARK: - Styling

    var fill: FillValue?  // Can be color string or gradient
    var stroke: String?
    var strokeWidth: Double?
    var strokeCap: String?  // "butt", "round", "square"
    var lineCap: String?    // Alias for strokeCap
    var lineJoin: String?   // "miter", "round", "bevel"
    var opacity: Double?
    var blendMode: String?

    // MARK: - Shadow

    var elevation: Double?
    var color: String?  // For shadow and colorFill

    // MARK: - Image

    var data: Data?  // Raw image bytes (MessagePack bin type)

    // MARK: - Text

    var content: String?
    var font: DrawFontConfig?
    var alignment: String?

    // MARK: - Computed properties

    var effectiveLineCap: String? {
        strokeCap ?? lineCap
    }
}

// MARK: - Fill Value (Color or Gradient)

/// Represents a fill value that can be either a color string or a gradient
enum FillValue: Codable, Equatable {
    case color(String)
    case gradient(GradientConfig)

    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()

        // Try string first (color)
        if let colorString = try? container.decode(String.self) {
            self = .color(colorString)
            return
        }

        // Try gradient dict
        if let gradientWrapper = try? container.decode(GradientWrapper.self) {
            self = .gradient(gradientWrapper.gradient)
            return
        }

        throw DecodingError.typeMismatch(
            FillValue.self,
            DecodingError.Context(codingPath: decoder.codingPath, debugDescription: "Expected String or gradient dict")
        )
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        switch self {
        case .color(let color):
            try container.encode(color)
        case .gradient(let gradient):
            try container.encode(GradientWrapper(gradient: gradient))
        }
    }

    var colorValue: String? {
        if case .color(let color) = self {
            return color
        }
        return nil
    }

    var gradientValue: GradientConfig? {
        if case .gradient(let gradient) = self {
            return gradient
        }
        return nil
    }
}

struct GradientWrapper: Codable, Equatable {
    let gradient: GradientConfig
}

/// Gradient configuration
struct GradientConfig: Codable, Equatable {
    let type: String  // "linear", "radial", "sweep"
    var start: [Double]?
    var end: [Double]?
    var center: [Double]?
    var radius: Double?
    var focus: [Double]?
    var colors: [String]
    var stops: [Double]?
    var startAngle: Double?
    var endAngle: Double?

    enum CodingKeys: String, CodingKey {
        case type, start, end, center, radius, focus, colors, stops, startAngle, endAngle
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        type = try container.decode(String.self, forKey: .type)
        colors = try container.decode([String].self, forKey: .colors)

        // Decode optional arrays with flexible numeric handling
        start = try Self.decodeNumericArray(from: container, forKey: .start)
        end = try Self.decodeNumericArray(from: container, forKey: .end)
        center = try Self.decodeNumericArray(from: container, forKey: .center)
        focus = try Self.decodeNumericArray(from: container, forKey: .focus)
        stops = try Self.decodeNumericArray(from: container, forKey: .stops)

        // Decode optional numbers
        radius = try Self.decodeNumber(from: container, forKey: .radius)
        startAngle = try Self.decodeNumber(from: container, forKey: .startAngle)
        endAngle = try Self.decodeNumber(from: container, forKey: .endAngle)
    }

    private static func decodeNumericArray(from container: KeyedDecodingContainer<CodingKeys>, forKey key: CodingKeys) throws -> [Double]? {
        guard container.contains(key) else { return nil }
        if let arr = try? container.decode([Double].self, forKey: key) {
            return arr
        }
        if let arr = try? container.decode([Int].self, forKey: key) {
            return arr.map { Double($0) }
        }
        return nil
    }

    private static func decodeNumber(from container: KeyedDecodingContainer<CodingKeys>, forKey key: CodingKeys) throws -> Double? {
        guard container.contains(key) else { return nil }
        if let d = try? container.decode(Double.self, forKey: key) {
            return d
        }
        if let i = try? container.decode(Int.self, forKey: key) {
            return Double(i)
        }
        return nil
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(type, forKey: .type)
        try container.encode(colors, forKey: .colors)
        try container.encodeIfPresent(start, forKey: .start)
        try container.encodeIfPresent(end, forKey: .end)
        try container.encodeIfPresent(center, forKey: .center)
        try container.encodeIfPresent(radius, forKey: .radius)
        try container.encodeIfPresent(focus, forKey: .focus)
        try container.encodeIfPresent(stops, forKey: .stops)
        try container.encodeIfPresent(startAngle, forKey: .startAngle)
        try container.encodeIfPresent(endAngle, forKey: .endAngle)
    }
}

// MARK: - DrawCommand Codable

extension DrawCommand {
    enum CodingKeys: String, CodingKey {
        case type
        case x, y, width, height, cornerRadius
        case cx, cy, radius, rx, ry
        case startAngle, endAngle, clockwise
        case x1, y1, x2, y2
        case points, closed, pointMode
        case elements  // For bezierPath (new format)
        case commands  // For bezierPath (legacy format)
        case fill, stroke, strokeWidth, strokeCap, lineCap, lineJoin, opacity, blendMode
        case elevation, color
        case data
        case content, font, alignment
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)

        type = try container.decode(String.self, forKey: .type)

        // Use flexible numeric decoding for all Double fields
        x = try Self.decodeNumber(from: container, forKey: .x)
        y = try Self.decodeNumber(from: container, forKey: .y)
        width = try Self.decodeNumber(from: container, forKey: .width)
        height = try Self.decodeNumber(from: container, forKey: .height)
        cornerRadius = try Self.decodeNumber(from: container, forKey: .cornerRadius)

        cx = try Self.decodeNumber(from: container, forKey: .cx)
        cy = try Self.decodeNumber(from: container, forKey: .cy)
        radius = try Self.decodeNumber(from: container, forKey: .radius)
        rx = try Self.decodeNumber(from: container, forKey: .rx)
        ry = try Self.decodeNumber(from: container, forKey: .ry)

        startAngle = try Self.decodeNumber(from: container, forKey: .startAngle)
        endAngle = try Self.decodeNumber(from: container, forKey: .endAngle)
        clockwise = try container.decodeIfPresent(Bool.self, forKey: .clockwise)

        x1 = try Self.decodeNumber(from: container, forKey: .x1)
        y1 = try Self.decodeNumber(from: container, forKey: .y1)
        x2 = try Self.decodeNumber(from: container, forKey: .x2)
        y2 = try Self.decodeNumber(from: container, forKey: .y2)

        // Points need special handling - array of arrays that might contain Int or Double
        if container.contains(.points) {
            points = try Self.decodePoints(from: container, forKey: .points)
        } else {
            points = nil
        }
        closed = try container.decodeIfPresent(Bool.self, forKey: .closed)
        pointMode = try container.decodeIfPresent(String.self, forKey: .pointMode)

        // BezierPath elements (new format)
        elements = try container.decodeIfPresent([PathElement].self, forKey: .elements)
        // BezierPath commands (legacy format)
        commands = try container.decodeIfPresent([BezierCommand].self, forKey: .commands)

        // Fill can be string or gradient dict
        fill = try container.decodeIfPresent(FillValue.self, forKey: .fill)

        stroke = try container.decodeIfPresent(String.self, forKey: .stroke)
        strokeWidth = try Self.decodeNumber(from: container, forKey: .strokeWidth)
        strokeCap = try container.decodeIfPresent(String.self, forKey: .strokeCap)
        lineCap = try container.decodeIfPresent(String.self, forKey: .lineCap)
        lineJoin = try container.decodeIfPresent(String.self, forKey: .lineJoin)
        opacity = try Self.decodeNumber(from: container, forKey: .opacity)
        blendMode = try container.decodeIfPresent(String.self, forKey: .blendMode)

        elevation = try Self.decodeNumber(from: container, forKey: .elevation)
        color = try container.decodeIfPresent(String.self, forKey: .color)

        data = try container.decodeIfPresent(Data.self, forKey: .data)

        content = try container.decodeIfPresent(String.self, forKey: .content)
        font = try container.decodeIfPresent(DrawFontConfig.self, forKey: .font)
        alignment = try container.decodeIfPresent(String.self, forKey: .alignment)
    }

    /// Decode a numeric value that might be Int or Double from MessagePack
    private static func decodeNumber(from container: KeyedDecodingContainer<CodingKeys>, forKey key: CodingKeys) throws -> Double? {
        guard container.contains(key) else { return nil }

        // Try Double first
        if let d = try? container.decode(Double.self, forKey: key) {
            return d
        }
        // Try Int and convert
        if let i = try? container.decode(Int.self, forKey: key) {
            return Double(i)
        }
        // Key exists but value is null
        if (try? container.decodeNil(forKey: key)) == true {
            return nil
        }
        return nil
    }

    /// Decode points array handling Int/Double values
    private static func decodePoints(from container: KeyedDecodingContainer<CodingKeys>, forKey key: CodingKeys) throws -> [[Double]]? {
        guard container.contains(key) else { return nil }

        // Try to decode as array of NumericArrays
        if let numericArrays = try? container.decode([NumericArray].self, forKey: key) {
            return numericArrays.map { $0.values }
        }
        return nil
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)

        try container.encode(type, forKey: .type)

        try container.encodeIfPresent(x, forKey: .x)
        try container.encodeIfPresent(y, forKey: .y)
        try container.encodeIfPresent(width, forKey: .width)
        try container.encodeIfPresent(height, forKey: .height)
        try container.encodeIfPresent(cornerRadius, forKey: .cornerRadius)

        try container.encodeIfPresent(cx, forKey: .cx)
        try container.encodeIfPresent(cy, forKey: .cy)
        try container.encodeIfPresent(radius, forKey: .radius)
        try container.encodeIfPresent(rx, forKey: .rx)
        try container.encodeIfPresent(ry, forKey: .ry)

        try container.encodeIfPresent(startAngle, forKey: .startAngle)
        try container.encodeIfPresent(endAngle, forKey: .endAngle)
        try container.encodeIfPresent(clockwise, forKey: .clockwise)

        try container.encodeIfPresent(x1, forKey: .x1)
        try container.encodeIfPresent(y1, forKey: .y1)
        try container.encodeIfPresent(x2, forKey: .x2)
        try container.encodeIfPresent(y2, forKey: .y2)

        try container.encodeIfPresent(points, forKey: .points)
        try container.encodeIfPresent(closed, forKey: .closed)
        try container.encodeIfPresent(pointMode, forKey: .pointMode)
        try container.encodeIfPresent(elements, forKey: .elements)
        try container.encodeIfPresent(commands, forKey: .commands)

        try container.encodeIfPresent(fill, forKey: .fill)
        try container.encodeIfPresent(stroke, forKey: .stroke)
        try container.encodeIfPresent(strokeWidth, forKey: .strokeWidth)
        try container.encodeIfPresent(strokeCap, forKey: .strokeCap)
        try container.encodeIfPresent(lineCap, forKey: .lineCap)
        try container.encodeIfPresent(lineJoin, forKey: .lineJoin)
        try container.encodeIfPresent(opacity, forKey: .opacity)
        try container.encodeIfPresent(blendMode, forKey: .blendMode)

        try container.encodeIfPresent(elevation, forKey: .elevation)
        try container.encodeIfPresent(color, forKey: .color)

        try container.encodeIfPresent(data, forKey: .data)

        try container.encodeIfPresent(content, forKey: .content)
        try container.encodeIfPresent(font, forKey: .font)
        try container.encodeIfPresent(alignment, forKey: .alignment)
    }

    static func == (lhs: DrawCommand, rhs: DrawCommand) -> Bool {
        return lhs.type == rhs.type &&
            lhs.x == rhs.x && lhs.y == rhs.y &&
            lhs.width == rhs.width && lhs.height == rhs.height &&
            lhs.cornerRadius == rhs.cornerRadius &&
            lhs.cx == rhs.cx && lhs.cy == rhs.cy &&
            lhs.radius == rhs.radius &&
            lhs.rx == rhs.rx && lhs.ry == rhs.ry &&
            lhs.startAngle == rhs.startAngle && lhs.endAngle == rhs.endAngle &&
            lhs.clockwise == rhs.clockwise &&
            lhs.x1 == rhs.x1 && lhs.y1 == rhs.y1 &&
            lhs.x2 == rhs.x2 && lhs.y2 == rhs.y2 &&
            lhs.points == rhs.points && lhs.closed == rhs.closed &&
            lhs.fill == rhs.fill && lhs.stroke == rhs.stroke &&
            lhs.strokeWidth == rhs.strokeWidth &&
            lhs.lineCap == rhs.lineCap && lhs.lineJoin == rhs.lineJoin &&
            lhs.opacity == rhs.opacity &&
            lhs.data == rhs.data &&
            lhs.content == rhs.content &&
            lhs.alignment == rhs.alignment
    }
}

/// Helper to decode an array of numeric values (Int or Double)
struct NumericArray: Codable {
    let values: [Double]

    init(from decoder: Decoder) throws {
        var container = try decoder.unkeyedContainer()
        var result: [Double] = []

        while !container.isAtEnd {
            if let d = try? container.decode(Double.self) {
                result.append(d)
            } else if let i = try? container.decode(Int.self) {
                result.append(Double(i))
            } else {
                // Skip unknown values
                _ = try? container.decode(String.self)
            }
        }
        values = result
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.unkeyedContainer()
        for value in values {
            try container.encode(value)
        }
    }
}

// MARK: - Path Element (New Format)

/// A single element in a bezier path (new typed format)
struct PathElement: Codable, Equatable {
    let type: String

    // MoveTo, LineTo
    var x: Double?
    var y: Double?

    // CubicTo
    var cp1x: Double?
    var cp1y: Double?
    var cp2x: Double?
    var cp2y: Double?

    // QuadraticTo (also uses cp1x, cp1y, x, y)
    var w: Double?  // Weight for conic sections

    // Arc (path element)
    var width: Double?
    var height: Double?
    var startAngle: Double?
    var sweepAngle: Double?

    // ArcTo
    var radius: Double?
    var rotation: Double?
    var largeArc: Bool?
    var clockwise: Bool?

    // Rect (path element)
    var borderRadius: Double?

    // SubPath
    var elements: [PathElement]?

    enum CodingKeys: String, CodingKey {
        case type, x, y, cp1x, cp1y, cp2x, cp2y, w
        case width, height, startAngle, sweepAngle
        case radius, rotation, largeArc, clockwise
        case borderRadius, elements
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)

        type = try container.decode(String.self, forKey: .type)

        // Decode numeric values with flexible Int/Double handling
        x = try Self.decodeNumber(from: container, forKey: .x)
        y = try Self.decodeNumber(from: container, forKey: .y)
        cp1x = try Self.decodeNumber(from: container, forKey: .cp1x)
        cp1y = try Self.decodeNumber(from: container, forKey: .cp1y)
        cp2x = try Self.decodeNumber(from: container, forKey: .cp2x)
        cp2y = try Self.decodeNumber(from: container, forKey: .cp2y)
        w = try Self.decodeNumber(from: container, forKey: .w)
        width = try Self.decodeNumber(from: container, forKey: .width)
        height = try Self.decodeNumber(from: container, forKey: .height)
        startAngle = try Self.decodeNumber(from: container, forKey: .startAngle)
        sweepAngle = try Self.decodeNumber(from: container, forKey: .sweepAngle)
        radius = try Self.decodeNumber(from: container, forKey: .radius)
        rotation = try Self.decodeNumber(from: container, forKey: .rotation)
        borderRadius = try Self.decodeNumber(from: container, forKey: .borderRadius)

        largeArc = try container.decodeIfPresent(Bool.self, forKey: .largeArc)
        clockwise = try container.decodeIfPresent(Bool.self, forKey: .clockwise)
        elements = try container.decodeIfPresent([PathElement].self, forKey: .elements)
    }

    private static func decodeNumber(from container: KeyedDecodingContainer<CodingKeys>, forKey key: CodingKeys) throws -> Double? {
        guard container.contains(key) else { return nil }
        if let d = try? container.decode(Double.self, forKey: key) {
            return d
        }
        if let i = try? container.decode(Int.self, forKey: key) {
            return Double(i)
        }
        return nil
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(type, forKey: .type)
        try container.encodeIfPresent(x, forKey: .x)
        try container.encodeIfPresent(y, forKey: .y)
        try container.encodeIfPresent(cp1x, forKey: .cp1x)
        try container.encodeIfPresent(cp1y, forKey: .cp1y)
        try container.encodeIfPresent(cp2x, forKey: .cp2x)
        try container.encodeIfPresent(cp2y, forKey: .cp2y)
        try container.encodeIfPresent(w, forKey: .w)
        try container.encodeIfPresent(width, forKey: .width)
        try container.encodeIfPresent(height, forKey: .height)
        try container.encodeIfPresent(startAngle, forKey: .startAngle)
        try container.encodeIfPresent(sweepAngle, forKey: .sweepAngle)
        try container.encodeIfPresent(radius, forKey: .radius)
        try container.encodeIfPresent(rotation, forKey: .rotation)
        try container.encodeIfPresent(largeArc, forKey: .largeArc)
        try container.encodeIfPresent(clockwise, forKey: .clockwise)
        try container.encodeIfPresent(borderRadius, forKey: .borderRadius)
        try container.encodeIfPresent(elements, forKey: .elements)
    }
}

// MARK: - Bezier Path Command (Legacy Format)

/// A single command in a bezier path (legacy dict format)
enum BezierCommand: Codable, Equatable {
    case move([Double])      // [x, y]
    case line([Double])      // [x, y]
    case curve([Double])     // [cp1x, cp1y, cp2x, cp2y, x, y] - cubic bezier
    case quad([Double])      // [cpx, cpy, x, y] - quadratic bezier
    case close

    enum CodingKeys: String, CodingKey {
        case move, line, curve, quad, close
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)

        if container.contains(.move) {
            let values = try Self.decodeNumericArray(from: container, forKey: .move)
            self = .move(values)
        } else if container.contains(.line) {
            let values = try Self.decodeNumericArray(from: container, forKey: .line)
            self = .line(values)
        } else if container.contains(.curve) {
            let values = try Self.decodeNumericArray(from: container, forKey: .curve)
            self = .curve(values)
        } else if container.contains(.quad) {
            let values = try Self.decodeNumericArray(from: container, forKey: .quad)
            self = .quad(values)
        } else if container.contains(.close) {
            self = .close
        } else {
            throw DecodingError.dataCorrupted(
                DecodingError.Context(codingPath: decoder.codingPath, debugDescription: "Unknown bezier command")
            )
        }
    }

    private static func decodeNumericArray(from container: KeyedDecodingContainer<CodingKeys>, forKey key: CodingKeys) throws -> [Double] {
        // Try Double array first
        if let arr = try? container.decode([Double].self, forKey: key) {
            return arr
        }
        // Try Int array and convert
        if let arr = try? container.decode([Int].self, forKey: key) {
            return arr.map { Double($0) }
        }
        // Try mixed array using NumericArray helper
        if let numericArray = try? container.decode(NumericArray.self, forKey: key) {
            return numericArray.values
        }
        return []
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        switch self {
        case .move(let values):
            try container.encode(values, forKey: .move)
        case .line(let values):
            try container.encode(values, forKey: .line)
        case .curve(let values):
            try container.encode(values, forKey: .curve)
        case .quad(let values):
            try container.encode(values, forKey: .quad)
        case .close:
            try container.encode(true, forKey: .close)
        }
    }
}

/// Font configuration for text drawing commands.
struct DrawFontConfig: Codable, Equatable {
    var size: Double?
    var weight: String?
    var design: String?
    var name: String?

    enum CodingKeys: String, CodingKey {
        case size, weight, design, name
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)

        // Flexible numeric decode for size
        if container.contains(.size) {
            if let d = try? container.decode(Double.self, forKey: .size) {
                size = d
            } else if let i = try? container.decode(Int.self, forKey: .size) {
                size = Double(i)
            } else {
                size = nil
            }
        } else {
            size = nil
        }

        weight = try container.decodeIfPresent(String.self, forKey: .weight)
        design = try container.decodeIfPresent(String.self, forKey: .design)
        name = try container.decodeIfPresent(String.self, forKey: .name)
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encodeIfPresent(size, forKey: .size)
        try container.encodeIfPresent(weight, forKey: .weight)
        try container.encodeIfPresent(design, forKey: .design)
        try container.encodeIfPresent(name, forKey: .name)
    }
}
