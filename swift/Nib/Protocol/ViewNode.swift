import Foundation
import SwiftUI

struct ViewNode: Codable, Identifiable, Equatable, Hashable {
    var id: String
    let type: ViewType
    var props: Props
    var children: [ViewNode]?
    var modifiers: [ViewModifier]?
    // Use array to avoid recursive value type issue (arrays are reference-counted)
    var backgroundViews: [ViewNode]?
    var overlayViews: [ViewNode]?

    // MARK: - Equatable (for SwiftUI diffing optimization)
    static func == (lhs: ViewNode, rhs: ViewNode) -> Bool {
        lhs.id == rhs.id &&
        lhs.type == rhs.type &&
        lhs.props == rhs.props &&
        lhs.children == rhs.children &&
        lhs.modifiers == rhs.modifiers &&
        lhs.backgroundViews == rhs.backgroundViews &&
        lhs.overlayViews == rhs.overlayViews
    }

    // MARK: - Hashable
    func hash(into hasher: inout Hasher) {
        hasher.combine(id)
        hasher.combine(type)
    }

    /// Convenience accessor for the single background view
    var backgroundView: ViewNode? {
        backgroundViews?.first
    }

    /// Convenience accessor for the single overlay view
    var overlayView: ViewNode? {
        overlayViews?.first
    }

    // Custom decoder to handle missing props
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        id = try container.decode(String.self, forKey: .id)
        type = try container.decode(ViewType.self, forKey: .type)
        props = try container.decodeIfPresent(Props.self, forKey: .props) ?? Props()
        children = try container.decodeIfPresent([ViewNode].self, forKey: .children)
        modifiers = try container.decodeIfPresent([ViewModifier].self, forKey: .modifiers)
        // Decode single backgroundView into array
        if let bgView = try container.decodeIfPresent(ViewNode.self, forKey: .backgroundView) {
            backgroundViews = [bgView]
        } else {
            backgroundViews = nil
        }
        // Decode single overlayView into array
        if let ovView = try container.decodeIfPresent(ViewNode.self, forKey: .overlayView) {
            overlayViews = [ovView]
        } else {
            overlayViews = nil
        }
    }

    private enum CodingKeys: String, CodingKey {
        case id, type, props, children, modifiers, backgroundView, backgroundViews, overlayView, overlayViews
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(id, forKey: .id)
        try container.encode(type, forKey: .type)
        try container.encode(props, forKey: .props)
        try container.encodeIfPresent(children, forKey: .children)
        try container.encodeIfPresent(modifiers, forKey: .modifiers)
        try container.encodeIfPresent(backgroundViews, forKey: .backgroundViews)
    }

    enum ViewType: String, Codable {
        // Layout
        case vstack = "VStack"
        case hstack = "HStack"
        case zstack = "ZStack"
        case spacer = "Spacer"
        case divider = "Divider"

        // Text & Input
        case text = "Text"
        case textField = "TextField"
        case secureField = "SecureField"

        // Controls
        case button = "Button"
        case toggle = "Toggle"
        case slider = "Slider"
        case picker = "Picker"
        case datePicker = "DatePicker"
        case stepper = "Stepper"
        case colorPicker = "ColorPicker"

        // Indicators
        case progressView = "ProgressView"
        case label = "Label"
        case link = "Link"
        case image = "Image"
        case video = "Video"

        // Shapes
        case rectangle = "Rectangle"
        case roundedRectangle = "RoundedRectangle"
        case circle = "Circle"
        case ellipse = "Ellipse"
        case capsule = "Capsule"

        // Lists & Collections
        case list = "List"
        case scrollView = "ScrollView"
        case forEach = "ForEach"
        case section = "Section"
        case group = "Group"

        // Navigation
        case navigationStack = "NavigationStack"
        case navigationLink = "NavigationLink"
        case disclosureGroup = "DisclosureGroup"

        // Charts
        case chart = "Chart"
        case lineMark = "LineMark"
        case barMark = "BarMark"
        case areaMark = "AreaMark"
        case pointMark = "PointMark"
        case ruleMark = "RuleMark"
        case rectMark = "RectMark"
        case sectorMark = "SectorMark"
    }

    struct Props: Codable, Equatable {
        init() {}  // Empty initializer

        // Common
        var label: String?
        var icon: String?  // SF Symbol name

        // Text
        var content: String?
        var textStyles: TextStyles?

        // TextField / SecureField
        var placeholder: String?
        var text: String?
        var textFieldStyles: TextFieldStyles?

        // Button
        var buttonStyles: ButtonStyles?

        // Toggle
        var isOn: Bool?
        var toggleStyles: ToggleStyles?

        // Slider
        var value: Double?
        var minValue: Double?
        var maxValue: Double?
        var step: Double?
        var sliderStyles: SliderStyles?

        // Picker
        var selection: String?
        var options: [PickerOption]?
        var pickerStyles: PickerStyles?

        // ProgressView
        var progress: Double?  // 0.0 to 1.0, nil for indeterminate
        var progressStyles: ProgressStyles?

        // Image
        var sourceType: String?  // "url", "file", "data"
        var sourceValue: String? // URL string, file path, or base64-encoded data
        var systemName: String?  // SF Symbol name (for SFSymbol class)
        var imageStyles: ImageStyles?

        // Video
        var videoSettings: VideoSettings?

        // Link
        var url: String?

        // Stack
        var spacing: CGFloat?
        var alignment: String?

        // Shapes
        var cornerRadius: CGFloat?
        var trimFrom: Double?
        var trimTo: Double?
        var rotation: Double?

        // Spacer
        var minLength: CGFloat?

        // ScrollView
        var axes: String?  // "horizontal", "vertical", "both"
        var showsIndicators: Bool?

        // Section
        var header: String?
        var footer: String?

        // NavigationLink
        var destination: String?  // View ID or label

        // DisclosureGroup
        var isExpanded: Bool?

        // Drag and Drop
        var onDrop: Bool?

        // Charts
        var chartData: ChartData?
        var xAxis: ChartAxisConfig?
        var yAxis: ChartAxisConfig?
        var legend: ChartLegendConfig?
        var chartBackground: String?
        var plotBackground: String?

        // Mark props (for chart marks)
        var x: PlottableField?
        var y: PlottableField?
        var yStart: PlottableField?
        var xStart: PlottableField?
        var xEnd: PlottableField?
        var yEnd: PlottableField?
        var angle: PlottableField?
        var angleStart: PlottableField?
        var foregroundStyle: PlottableField?
        var symbolField: PlottableField?
        var symbol: String?
        var symbolSize: CGFloat?
        var interpolation: String?
        var stacking: String?
        var lineWidth: CGFloat?
        var innerRadius: CGFloat?
        var outerRadius: CGFloat?
        var barWidth: CGFloat?
        var barHeight: CGFloat?
        var opacity: Double?
    }

    struct PickerOption: Codable, Equatable, Hashable {
        var value: String
        var label: String
    }

    // MARK: - Chart Types

    /// Columnar data format for efficient chart data transmission
    /// Note: columns are JSON-encoded to work around MessagePack limitations
    struct ChartData: Codable, Equatable {
        var columnsJson: String  // JSON-encoded columns dict
        var rowCount: Int

        /// Parsed columns dictionary (lazy parsed from JSON)
        func parseColumns() -> [String: [Any]] {
            guard let data = columnsJson.data(using: .utf8),
                  let json = try? JSONSerialization.jsonObject(with: data) as? [String: [Any]] else {
                return [:]
            }
            return json
        }
    }

    /// Chart axis configuration
    struct ChartAxisConfig: Codable, Equatable {
        var position: String?
        var label: String?
        var gridLines: Bool?
        var hidden: Bool?
        var format: String?
        var labelColor: String?
        var gridColor: String?
    }

    /// Chart legend configuration
    struct ChartLegendConfig: Codable, Equatable {
        var position: String?
        var hidden: Bool?
        var title: String?
    }

    /// Field reference for plottable values
    struct PlottableField: Codable, Equatable {
        var field: String?      // Column name reference
        var type: String?       // "quantitative", "nominal", "temporal"
        var label: String?      // Display label
    }

    /// Button-specific styling options
    struct ButtonStyles: Codable, Equatable {
        var role: String?           // "destructive", "cancel"
        var style: String?          // "bordered", "borderedProminent", "borderless", "plain"
        var borderShape: String?    // "automatic", "capsule", "roundedRectangle", "circle"
        var cornerRadius: CGFloat?  // For roundedRectangle shape
        var controlSize: String?    // "mini", "small", "regular", "large", "extraLarge"
        var tint: String?           // Color name or hex
        var disabled: Bool?
        var labelStyle: String?     // "automatic", "iconOnly", "titleOnly", "titleAndIcon"
    }

    /// TextField styling options
    struct TextFieldStyles: Codable, Equatable {
        var style: String?          // "automatic", "plain", "roundedBorder", "squareBorder"
        var disabled: Bool?
        var focused: Bool?
        var autocapitalization: String?  // "none", "words", "sentences", "characters"
        var autocorrection: Bool?
        var keyboardType: String?   // "default", "email", "number", "phone", "url"
        var submitLabel: String?    // "done", "go", "search", "send", "next", "continue"
    }

    /// Toggle styling options
    struct ToggleStyles: Codable, Equatable {
        var style: String?          // "automatic", "switch", "button", "checkbox"
        var tint: String?
        var disabled: Bool?
    }

    /// Slider styling options
    struct SliderStyles: Codable, Equatable {
        var tint: String?
        var disabled: Bool?
    }

    /// Picker styling options
    struct PickerStyles: Codable, Equatable {
        var style: String?          // "automatic", "menu", "segmented", "wheel", "inline"
        var disabled: Bool?
    }

    /// ProgressView styling options
    struct ProgressStyles: Codable, Equatable {
        var style: String?          // "automatic", "linear", "circular"
        var tint: String?
    }

    /// Image styling options
    struct ImageStyles: Codable, Equatable {
        var resizable: Bool?
        var scaledToFit: Bool?
        var scaledToFill: Bool?
        var antialiased: Bool?          // Whether to apply antialiasing (default true)
        var blur: CGFloat?              // Blur radius to apply
        // SF Symbol specific
        var symbolWeight: String?       // "ultraLight" to "black"
        var symbolScale: String?        // "small", "medium", "large"
        var symbolRenderingMode: String? // "monochrome", "hierarchical", "palette", "multicolor"
    }

    /// Video settings
    struct VideoSettings: Codable, Equatable {
        var autoplay: Bool?
        var loop: Bool?
        var muted: Bool?
        var controls: Bool?
        var gravity: String?  // "resizeAspect", "resizeAspectFill", "resize"
    }

    /// Text-specific styling options
    struct TextStyles: Codable, Equatable {
        // Font styling
        var bold: Bool?
        var italic: Bool?
        var monospaced: Bool?
        var monospacedDigit: Bool?

        // Decorations
        var strikethrough: Bool?
        var strikethroughColor: String?
        var underline: Bool?
        var underlineColor: String?

        // Spacing
        var kerning: CGFloat?
        var tracking: CGFloat?
        var baselineOffset: CGFloat?

        // Layout
        var lineLimit: Int?
        var truncationMode: String?
        var minimumScaleFactor: CGFloat?
        var allowsTightening: Bool?

        // Case transformation
        var textCase: String?
    }

    struct ViewModifier: Codable, Equatable {
        let type: ModifierType
        let args: ModifierArgs

        enum ModifierType: String, Codable, Equatable {
            case frame
            case padding
            case background
            case foregroundColor
            case fill
            case stroke
            case font
            case cornerRadius
            case opacity
            case clipShape
            case shadow
            case overlay
            case border
            case animation
            case contentTransition
            case transition
            case blendMode
            case scale
        }

        struct ModifierArgs: Codable, Equatable {
            // Frame
            var width: CGFloat?
            var height: CGFloat?
            var maxWidth: String?  // "infinity" for .infinity
            var maxHeight: String?
            var minWidth: CGFloat?
            var minHeight: CGFloat?

            // Padding
            var value: CGFloat?
            var top: CGFloat?
            var leading: CGFloat?
            var bottom: CGFloat?
            var trailing: CGFloat?
            var horizontal: CGFloat?
            var vertical: CGFloat?

            // Colors
            var color: String?

            // Stroke
            var lineWidth: CGFloat?

            // Font
            var fontName: String?
            var fontSize: CGFloat?
            var fontWeight: String?
            var fontPath: String?  // Path to custom font file

            // Opacity
            var opacity: Double?

            // Animation
            var animationType: String?
            var animationDuration: Double?
            var animationDelay: Double?
            var springResponse: Double?
            var springDamping: Double?

            // ClipShape
            var shape: String?  // "capsule", "circle", "roundedRectangle"
            var cornerRadius: CGFloat?

            // Shadow
            var shadowColor: String?
            var shadowRadius: CGFloat?
            var shadowX: CGFloat?
            var shadowY: CGFloat?

            // Border
            var borderColor: String?
            var borderWidth: CGFloat?

            // Transitions
            var transitionType: String?

            // Blend mode
            var mode: String?

            // Scale
            var scale: CGFloat?
        }
    }
}

// Color parsing
extension Color {
    init(nibColor: String) {
        // Check for opacity suffix (e.g., "red:0.8" or "#FF5733:0.5")
        if let colonIndex = nibColor.lastIndex(of: ":") {
            let colorPart = String(nibColor[..<colonIndex])
            let opacityPart = String(nibColor[nibColor.index(after: colonIndex)...])

            if let opacity = Double(opacityPart) {
                // Parse the color part and apply opacity
                let baseColor = Color.parseBaseColor(colorPart)
                self = baseColor.opacity(opacity)
                return
            }
        }

        // No opacity suffix, parse as regular color
        self = Color.parseBaseColor(nibColor)
    }

    /// Parse a color string without opacity suffix
    private static func parseBaseColor(_ colorString: String) -> Color {
        switch colorString.lowercased() {
        // Basic colors
        case "red": return .red
        case "blue": return .blue
        case "green": return .green
        case "yellow": return .yellow
        case "orange": return .orange
        case "purple": return .purple
        case "pink": return .pink
        case "white": return .white
        case "black": return .black
        case "gray", "grey": return .gray
        case "clear": return .clear

        // Extended colors
        case "indigo": return .indigo
        case "cyan": return .cyan
        case "mint": return .mint
        case "teal": return .teal
        case "brown": return .brown

        // Semantic colors
        case "primary": return .primary
        case "secondary": return .secondary
        case "accentcolor", "accent": return .accentColor

        default:
            // Try hex color
            if colorString.hasPrefix("#") {
                return Color(hex: colorString)
            } else {
                return .primary
            }
        }
    }

    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)

        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }

        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}

// Alignment parsing
extension HorizontalAlignment {
    init(nibAlignment: String?) {
        switch nibAlignment?.lowercased() {
        case "leading": self = .leading
        case "trailing": self = .trailing
        case "center", .none: self = .center
        default: self = .center
        }
    }
}

extension VerticalAlignment {
    init(nibAlignment: String?) {
        switch nibAlignment?.lowercased() {
        case "top": self = .top
        case "bottom": self = .bottom
        case "center", .none: self = .center
        default: self = .center
        }
    }
}

extension Alignment {
    init(nibAlignment: String?) {
        switch nibAlignment?.lowercased() {
        case "topLeading": self = .topLeading
        case "top": self = .top
        case "topTrailing": self = .topTrailing
        case "leading": self = .leading
        case "trailing": self = .trailing
        case "bottomLeading": self = .bottomLeading
        case "bottom": self = .bottom
        case "bottomTrailing": self = .bottomTrailing
        case "center", .none: self = .center
        default: self = .center
        }
    }
}

// MARK: - NSColor parsing (for menu items)

import AppKit

extension NSColor {
    /// Create NSColor from nib color string (named color, hex, or with opacity suffix)
    static func fromNibColor(_ nibColor: String) -> NSColor {
        // Check for opacity suffix (e.g., "red:0.8" or "#FF5733:0.5")
        var colorString = nibColor
        var opacity: CGFloat = 1.0

        if let colonIndex = nibColor.lastIndex(of: ":") {
            let colorPart = String(nibColor[..<colonIndex])
            let opacityPart = String(nibColor[nibColor.index(after: colonIndex)...])
            if let op = Double(opacityPart) {
                colorString = colorPart
                opacity = CGFloat(op)
            }
        }

        let baseColor = parseBaseColor(colorString)
        return opacity < 1.0 ? baseColor.withAlphaComponent(opacity) : baseColor
    }

    private static func parseBaseColor(_ colorString: String) -> NSColor {
        switch colorString.lowercased() {
        case "red": return .systemRed
        case "blue": return .systemBlue
        case "green": return .systemGreen
        case "yellow": return .systemYellow
        case "orange": return .systemOrange
        case "purple": return .systemPurple
        case "pink": return .systemPink
        case "white": return .white
        case "black": return .black
        case "gray", "grey": return .systemGray
        case "clear": return .clear
        case "indigo": return .systemIndigo
        case "cyan": return .cyan
        case "mint": return .systemMint
        case "teal": return .systemTeal
        case "brown": return .systemBrown
        case "primary": return .labelColor
        case "secondary": return .secondaryLabelColor
        case "accentcolor", "accent": return .controlAccentColor
        default:
            if colorString.hasPrefix("#") {
                return NSColor.fromHex(colorString)
            }
            return .labelColor
        }
    }

    static func fromHex(_ hex: String) -> NSColor {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)

        let a, r, g, b: UInt64
        switch hex.count {
        case 3:
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6:
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8:
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }

        return NSColor(
            red: CGFloat(r) / 255,
            green: CGFloat(g) / 255,
            blue: CGFloat(b) / 255,
            alpha: CGFloat(a) / 255
        )
    }
}

// MARK: - NSImage helpers for SF Symbols

extension NSImage {
    /// Apply a tint color to an SF Symbol image
    func withTintColor(_ color: NSColor) -> NSImage {
        let config = NSImage.SymbolConfiguration(paletteColors: [color])
        return self.withSymbolConfiguration(config) ?? self
    }
}
