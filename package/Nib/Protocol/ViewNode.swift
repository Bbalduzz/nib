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
    var contextMenuViews: [ViewNode]?
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
        lhs.contextMenuViews == rhs.contextMenuViews &&
        lhs.slot == rhs.slot &&
        lhs.animationContext == rhs.animationContext
    }

    // MARK: - Hashable
    func hash(into hasher: inout Hasher) {
        hasher.combine(id)
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

    // Direct memberwise initializer (for tree reconstruction from flat nodes)
    init(
        id: String,
        type: ViewType,
        props: Props,
        children: [ViewNode]?,
        modifiers: [ViewModifier]?,
        backgroundViews: [ViewNode]?,
        overlayViews: [ViewNode]?,
        contextMenuViews: [ViewNode]? = nil,
        slot: String?,
        animationContext: AnimationContext?
    ) {
        self.id = id
        self.type = type
        self.props = props
        self.children = children
        self.modifiers = modifiers
        self.backgroundViews = backgroundViews
        self.overlayViews = overlayViews
        self.contextMenuViews = contextMenuViews
        self.slot = slot
        self.animationContext = animationContext
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
        contextMenuViews = try container.decodeIfPresent([ViewNode].self, forKey: .contextMenuViews)
    }

    private enum CodingKeys: String, CodingKey {
        case id, type, props, children, modifiers, backgroundView, backgroundViews, overlayView, overlayViews, contextMenuViews, slot, animationContext
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(id, forKey: .id)
        try container.encode(type, forKey: .type)
        try container.encode(props, forKey: .props)
        try container.encodeIfPresent(children, forKey: .children)
        try container.encodeIfPresent(modifiers, forKey: .modifiers)
        try container.encodeIfPresent(backgroundViews, forKey: .backgroundViews)
        try container.encodeIfPresent(contextMenuViews, forKey: .contextMenuViews)
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
        var numColumns: Int?
        var rowIds: [String]?
        var tableSelection: [String]?
        var tableSortColumn: String?
        var tableSortAscending: Bool?

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

// MARK: - Flat Node for Iterative Decoding

/// A flat representation of a ViewNode, decoded without recursion.
/// Each node stores ID references to children instead of nested nodes,
/// preventing stack overflow during MessagePack decoding.
struct FlatViewNode: Codable {
    let id: String
    let type: ViewNode.ViewType
    var props: ViewNode.Props
    var modifiers: [ViewNode.ViewModifier]?
    var slot: String?
    var animationContext: ViewNode.AnimationContext?

    // Flat references (no recursion)
    var parentId: String?
    var childIds: [String]?
    var backgroundId: String?
    var overlayId: String?
    var contextMenuIds: [String]?
}

// MARK: - Iterative Tree Reconstruction

extension ViewNode {
    /// Reconstruct a nested ViewNode tree from a flat node list.
    /// Uses iterative bottom-up construction (no recursion, O(n) time).
    static func fromFlatNodes(_ flatNodes: [FlatViewNode], rootId: String) -> ViewNode? {
        guard !flatNodes.isEmpty else { return nil }

        // Build lookup
        var flatMap: [String: FlatViewNode] = [:]
        flatMap.reserveCapacity(flatNodes.count)
        for node in flatNodes {
            flatMap[node.id] = node
        }

        // Sort by depth (deeper first). Depth = number of "." in ID.
        // This ensures children are built before their parents.
        let sorted = flatNodes.sorted { a, b in
            let depthA = a.id.filter { $0 == "." }.count
            let depthB = b.id.filter { $0 == "." }.count
            return depthA > depthB
        }

        // Build ViewNodes bottom-up
        var viewNodeMap: [String: ViewNode] = [:]
        viewNodeMap.reserveCapacity(flatNodes.count)

        for flat in sorted {
            // Resolve children (order preserved from childIds)
            let children: [ViewNode]? = flat.childIds?.compactMap { viewNodeMap[$0] }

            // Resolve background view
            let backgroundViews: [ViewNode]?
            if let bgId = flat.backgroundId, let bgNode = viewNodeMap[bgId] {
                backgroundViews = [bgNode]
            } else {
                backgroundViews = nil
            }

            // Resolve overlay view
            let overlayViews: [ViewNode]?
            if let ovId = flat.overlayId, let ovNode = viewNodeMap[ovId] {
                overlayViews = [ovNode]
            } else {
                overlayViews = nil
            }

            // Resolve context menu views
            let contextMenuViews: [ViewNode]?
            if let ctxIds = flat.contextMenuIds {
                let resolved = ctxIds.compactMap { viewNodeMap[$0] }
                contextMenuViews = resolved.isEmpty ? nil : resolved
            } else {
                contextMenuViews = nil
            }

            let node = ViewNode(
                id: flat.id,
                type: flat.type,
                props: flat.props,
                children: (children?.isEmpty ?? true) ? nil : children,
                modifiers: flat.modifiers,
                backgroundViews: backgroundViews,
                overlayViews: overlayViews,
                contextMenuViews: contextMenuViews,
                slot: flat.slot,
                animationContext: flat.animationContext
            )

            viewNodeMap[node.id] = node
        }

        return viewNodeMap[rootId]
    }
}
