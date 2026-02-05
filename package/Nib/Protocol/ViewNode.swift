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
    // Slot identifier for views used as named children (e.g., Gauge labels)
    var slot: String?
    // Animation context for per-view reactive animations
    var animationContext: AnimationContext?

    // MARK: - Animation Context
    /// Configuration for per-view reactive animations.
    /// When a view has an animationContext, all property changes animate with this config.
    struct AnimationContext: Codable, Equatable, Hashable {
        var animationType: String?
        var animationDuration: Double?
        var animationDelay: Double?
        var springResponse: Double?
        var springDamping: Double?
    }

    // MARK: - Equatable (for SwiftUI diffing optimization)
    static func == (lhs: ViewNode, rhs: ViewNode) -> Bool {
        lhs.id == rhs.id &&
        lhs.type == rhs.type &&
        lhs.props == rhs.props &&
        lhs.children == rhs.children &&
        lhs.modifiers == rhs.modifiers &&
        lhs.backgroundViews == rhs.backgroundViews &&
        lhs.overlayViews == rhs.overlayViews &&
        lhs.slot == rhs.slot &&
        lhs.animationContext == rhs.animationContext
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

    /// Find a child by its slot name
    func child(forSlot slotName: String) -> ViewNode? {
        children?.first { $0.slot == slotName }
    }

    // Custom decoder to handle missing props
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        id = try container.decode(String.self, forKey: .id)
        type = try container.decode(ViewType.self, forKey: .type)
        props = try container.decodeIfPresent(Props.self, forKey: .props) ?? Props()
        children = try container.decodeIfPresent([ViewNode].self, forKey: .children)
        modifiers = try container.decodeIfPresent([ViewModifier].self, forKey: .modifiers)
        slot = try container.decodeIfPresent(String.self, forKey: .slot)
        animationContext = try container.decodeIfPresent(AnimationContext.self, forKey: .animationContext)
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
        case id, type, props, children, modifiers, backgroundView, backgroundViews, overlayView, overlayViews, slot, animationContext
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(id, forKey: .id)
        try container.encode(type, forKey: .type)
        try container.encode(props, forKey: .props)
        try container.encodeIfPresent(children, forKey: .children)
        try container.encodeIfPresent(modifiers, forKey: .modifiers)
        try container.encodeIfPresent(backgroundViews, forKey: .backgroundViews)
        try container.encodeIfPresent(slot, forKey: .slot)
        try container.encodeIfPresent(animationContext, forKey: .animationContext)
    }

    // MARK: - View Type Enum

    enum ViewType: String, Codable {
        // Layout
        case vstack = "VStack"
        case hstack = "HStack"
        case zstack = "ZStack"
        case spacer = "Spacer"
        case divider = "Divider"

        // Grid layouts
        case grid = "Grid"
        case gridRow = "GridRow"
        case lazyVGrid = "LazyVGrid"
        case lazyHGrid = "LazyHGrid"

        // Text & Input
        case text = "Text"
        case textField = "TextField"
        case secureField = "SecureField"
        case textEditor = "TextEditor"

        // Controls
        case button = "Button"
        case toggle = "Toggle"
        case slider = "Slider"
        case picker = "Picker"
        case datePicker = "DatePicker"
        case stepper = "Stepper"
        case colorPicker = "ColorPicker"
        case gauge = "Gauge"
        case shareLink = "ShareLink"

        // Indicators
        case progressView = "ProgressView"
        case label = "Label"
        case link = "Link"
        case image = "Image"
        case video = "Video"
        case markdown = "Markdown"

        // Table
        case table = "Table"

        // Shapes
        case shape = "Shape"
        case rectangle = "Rectangle"
        case roundedRectangle = "RoundedRectangle"
        case circle = "Circle"
        case ellipse = "Ellipse"
        case capsule = "Capsule"

        // Gradients
        case linearGradient = "LinearGradient"
        case radialGradient = "RadialGradient"
        case angularGradient = "AngularGradient"
        case ellipticalGradient = "EllipticalGradient"

        // Effects
        case visualEffectBlur = "VisualEffectBlur"

        // Lists & Collections
        case list = "List"
        case scrollView = "ScrollView"
        case forEach = "ForEach"
        case section = "Section"
        case group = "Group"
        case form = "Form"

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

        // Map
        case map = "Map"

        // Camera
        case cameraPreview = "CameraPreview"

        // Canvas (Core Graphics drawing)
        case canvas = "Canvas"

        // WebView
        case webView = "WebView"
    }

    // MARK: - Props

    struct Props: Codable, Equatable {
        init() {}  // Empty initializer

        // Common
        var label: String?
        var icon: String?  // SF Symbol name

        // Text
        var content: String?
        var attributedStrings: [AttributedStringItem]?
        var textStyles: TextStyles?

        // Markdown
        var theme: String?

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
        var cornerRadii: CornerRadii?  // Per-corner radius for Rectangle
        var trimFrom: Double?
        var trimTo: Double?
        var rotation: Double?

        // Shape stroke (for Rectangle, RoundedRectangle, etc.)
        var stroke: String?
        var strokeWidth: Double?

        // Custom Shape (TODO: enable when Shape primitive is fully implemented)
        // var pathOperations: [PathOperation]?
        // var viewBox: ViewBox?
        // var fill: String?
        // var fillGradient: ShapeGradient?

        // Gradients
        var colors: [String]?              // Simple color array
        var stops: [GradientStop]?         // Explicit stops with positions
        var startPoint: [Double]?          // [x, y] for LinearGradient
        var endPoint: [Double]?            // [x, y] for LinearGradient
        var center: [Double]?              // [x, y] for radial/angular/elliptical
        var startRadius: Double?           // RadialGradient
        var endRadius: Double?             // RadialGradient
        var startAngle: Double?            // AngularGradient (degrees)
        var endAngle: Double?              // AngularGradient (degrees)
        var startRadiusFraction: Double?   // EllipticalGradient
        var endRadiusFraction: Double?     // EllipticalGradient

        // Spacer
        var minLength: CGFloat?

        // ScrollView
        var axes: String?  // "horizontal", "vertical", "both"
        var showsIndicators: Bool?

        // Section
        var header: String?
        var footer: String?

        // Form
        var formStyle: String?

        // NavigationLink
        var destination: String?  // View ID or label

        // DisclosureGroup
        var isExpanded: Bool?

        // Interaction handlers
        var onDrop: Bool?
        var onHover: Bool?
        var onClick: Bool?
        var tooltip: String?

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

        // Map
        var latitude: Double?
        var longitude: Double?
        var zoom: Double?
        var markers: [MapMarkerData]?
        var annotations: [MapAnnotationData]?
        var circles: [MapCircleData]?
        var polylines: [MapPolylineData]?
        var polygons: [MapPolygonData]?
        var mapSettings: MapSettings?

        // Gauge
        var gaugeStyle: String?
        var currentValueLabel: String?
        var minValueLabel: String?
        var maxValueLabel: String?
        var tint: String?

        // TextEditor
        var textEditorStyles: TextEditorStyles?
        // Legacy TextEditor props (deprecated — use textEditorStyles)
        var lineLimit: Int?
        var scrollsDisabled: Bool?
        var contentBackgroundHidden: Bool?
        var contentBackground: String?

        // Grid
        var columns: [GridItemSpec]?
        var rows: [GridItemSpec]?
        var horizontalSpacing: CGFloat?
        var verticalSpacing: CGFloat?
        var pinnedViews: [String]?

        // Table
        var tableColumns: [TableColumnSpec]?
        var tableRowsJson: String?  // JSON-encoded array of row objects
        var rowIdKey: String?

        // ShareLink
        var items: [String]?
        var subject: String?
        var message: String?

        // VisualEffectBlur
        var material: String?
        var blendingMode: String?
        var isEmphasized: Bool?

        // CameraPreview
        var deviceId: String?

        // Canvas
        var canvasWidth: Double?
        var canvasHeight: Double?
        var commands: [DrawCommand]?
        var backgroundColor: String?
        var canvasGestures: Bool?  // Enable pan/hover gestures

        // WebView (reuses url from Link)
        var html: String?
        var baseURL: String?
        var allowsBackForward: Bool?
        var allowsMagnification: Bool?
    }
}
