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
    /// Build view with type erasure to avoid massive union type signature.
    /// AnyView is the right choice for dynamic views - faster init, simpler types.
    func buildView(for node: ViewNode) -> AnyView {
        switch node.type {
        // Layout
        case .vstack:
            return AnyView(buildVStack())
        case .hstack:
            return AnyView(buildHStack())
        case .zstack:
            return AnyView(buildZStack())
        case .spacer:
            return AnyView(buildSpacer())
        case .divider:
            return AnyView(Divider())

        // Text & Input
        case .text:
            return AnyView(buildText())
        case .textField:
            return AnyView(buildTextField())
        case .secureField:
            return AnyView(buildSecureField())

        // Controls
        case .button:
            return AnyView(buildButton())
        case .toggle:
            return AnyView(buildToggle())
        case .slider:
            return AnyView(buildSlider())
        case .picker:
            return AnyView(buildPicker())
        case .datePicker:
            return AnyView(buildDatePicker())
        case .stepper:
            return AnyView(buildStepper())
        case .colorPicker:
            return AnyView(buildColorPicker())

        // Indicators
        case .progressView:
            return AnyView(buildProgressView())
        case .label:
            return AnyView(buildLabel())
        case .link:
            return AnyView(buildLink())
        case .image:
            return AnyView(buildImage())
        case .video:
            return AnyView(buildVideo())
        case .markdown:
            return AnyView(buildMarkdown())

        // Shapes (transparent by default unless fill specified)
        case .shape:
            return AnyView(EmptyView())
        case .rectangle:
            return AnyView(buildRectangle())
        case .roundedRectangle:
            return AnyView(buildRoundedRectangle())
        case .circle:
            return AnyView(buildCircle())
        case .ellipse:
            return AnyView(buildEllipse())
        case .capsule:
            return AnyView(buildCapsule())

        // Gradients
        case .linearGradient:
            return AnyView(buildLinearGradient())
        case .radialGradient:
            return AnyView(buildRadialGradient())
        case .angularGradient:
            return AnyView(buildAngularGradient())
        case .ellipticalGradient:
            return AnyView(buildEllipticalGradient())

        // Lists & Collections
        case .list:
            return AnyView(buildList())
        case .scrollView:
            return AnyView(buildScrollView())
        case .forEach:
            return AnyView(buildForEach())
        case .section:
            return AnyView(buildSection())
        case .group:
            return AnyView(buildGroup())
        case .form:
            return AnyView(buildForm())

        // Navigation
        case .navigationStack:
            return AnyView(buildNavigationStack())
        case .navigationLink:
            return AnyView(buildNavigationLink())
        case .disclosureGroup:
            return AnyView(buildDisclosureGroup())

        // Charts
        case .chart:
            return AnyView(buildChart())
        case .lineMark, .barMark, .areaMark, .pointMark, .ruleMark, .rectMark, .sectorMark:
            return AnyView(EmptyView())

        // Map
        case .map:
            return AnyView(buildMap())

        // Grid layouts
        case .grid:
            return AnyView(buildGrid())
        case .gridRow:
            return AnyView(buildGridRow())
        case .lazyVGrid:
            return AnyView(buildLazyVGrid())
        case .lazyHGrid:
            return AnyView(buildLazyHGrid())

        // New controls
        case .gauge:
            return AnyView(buildGauge())
        case .textEditor:
            return AnyView(buildTextEditor())
        case .table:
            return AnyView(buildTable())
        case .shareLink:
            return AnyView(buildShareLink())

        // Effects
        case .visualEffectBlur:
            return AnyView(buildVisualEffectBlur())

        // Camera
        case .cameraPreview:
            return AnyView(buildCameraPreview())

        // Canvas (Core Graphics drawing)
        case .canvas:
            return AnyView(buildCanvas())

        // WebView
        case .webView:
            return AnyView(buildWebView())
        }
    }
}
