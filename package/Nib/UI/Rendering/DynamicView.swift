import SwiftUI
import UniformTypeIdentifiers
import Charts

/// Dynamic SwiftUI view that renders from a ViewNode tree
struct DynamicView: View {
    let node: ViewNode
    let onEvent: (String, String) -> Void

    var body: some View {
        buildView(for: node)
            .applyModifiers(node.modifiers)
            .applyAnimationContext(node.animationContext, nodeHash: node.hashValue)
            .applyBackgroundView(node.backgroundView, onEvent: onEvent)
            .applyOverlayView(node.overlayView, onEvent: onEvent)
            .applyInteractionHandlers(
                onDrop: node.props.onDrop,
                onHover: node.props.onHover,
                onClick: node.props.onClick,
                tooltip: node.props.tooltip,
                nodeId: node.id,
                onEvent: onEvent
            )
    }

    /// Recursively build child views
    @ViewBuilder
    var childViews: some View {
        if let children = node.children {
            ForEach(children) { child in
                DynamicView(node: child, onEvent: onEvent)
            }
        }
    }
}

// MARK: - View Building

extension DynamicView {
    @ViewBuilder
    func buildView(for node: ViewNode) -> some View {
        switch node.type {
        // Layout
        case .vstack:
            buildVStack()
        case .hstack:
            buildHStack()
        case .zstack:
            buildZStack()
        case .spacer:
            buildSpacer()
        case .divider:
            Divider()

        // Text & Input
        case .text:
            buildText()
        case .textField:
            buildTextField()
        case .secureField:
            buildSecureField()

        // Controls
        case .button:
            buildButton()
        case .toggle:
            buildToggle()
        case .slider:
            buildSlider()
        case .picker:
            buildPicker()
        case .datePicker:
            buildDatePicker()
        case .stepper:
            buildStepper()
        case .colorPicker:
            buildColorPicker()

        // Indicators
        case .progressView:
            buildProgressView()
        case .label:
            buildLabel()
        case .link:
            buildLink()
        case .image:
            buildImage()
        case .video:
            buildVideo()
        case .markdown:
            buildMarkdown()

        // Shapes (transparent by default unless fill specified)
        case .shape:
            // TODO: Enable when Shape primitive is fully implemented
            EmptyView()
        case .rectangle:
            buildRectangle()
        case .roundedRectangle:
            buildRoundedRectangle()
        case .circle:
            buildCircle()
        case .ellipse:
            buildEllipse()
        case .capsule:
            buildCapsule()

        // Gradients
        case .linearGradient:
            buildLinearGradient()
        case .radialGradient:
            buildRadialGradient()
        case .angularGradient:
            buildAngularGradient()
        case .ellipticalGradient:
            buildEllipticalGradient()

        // Lists & Collections
        case .list:
            buildList()
        case .scrollView:
            buildScrollView()
        case .forEach:
            buildForEach()
        case .section:
            buildSection()
        case .group:
            buildGroup()
        case .form:
            buildForm()

        // Navigation
        case .navigationStack:
            buildNavigationStack()
        case .navigationLink:
            buildNavigationLink()
        case .disclosureGroup:
            buildDisclosureGroup()

        // Charts
        case .chart:
            buildChart()
        case .lineMark, .barMark, .areaMark, .pointMark, .ruleMark, .rectMark, .sectorMark:
            // Marks are rendered by the parent Chart view, not directly
            EmptyView()

        // Map
        case .map:
            buildMap()

        // Grid layouts
        case .grid:
            buildGrid()
        case .gridRow:
            buildGridRow()
        case .lazyVGrid:
            buildLazyVGrid()
        case .lazyHGrid:
            buildLazyHGrid()

        // New controls
        case .gauge:
            buildGauge()
        case .textEditor:
            buildTextEditor()
        case .table:
            buildTable()
        case .shareLink:
            buildShareLink()

        // Effects
        case .visualEffectBlur:
            buildVisualEffectBlur()

        // Camera
        case .cameraPreview:
            buildCameraPreview()

        // Canvas (Core Graphics drawing)
        case .canvas:
            buildCanvas()

        // WebView
        case .webView:
            buildWebView()
        }
    }
}
