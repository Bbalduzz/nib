import SwiftUI

// MARK: - Optimized View Dispatcher

/// Optimized view dispatcher that uses a hybrid approach:
/// - Fast path: switch statement for high-frequency built-in types
/// - Slow path: registry lookup for less common or custom types
///
/// This preserves performance for common operations while enabling extensibility.
struct OptimizedViewDispatcher {
    private let registry = NibViewBuilderRegistry.shared

    /// Build a view for the given node using the optimal dispatch path
    @ViewBuilder
    func build(node: ViewNode, context: NibRenderContext) -> some View {
        switch node.type {
        // MARK: Fast Path - High Frequency Types

        // Layout (most common)
        case .vstack:
            buildVStack(node: node, context: context)
        case .hstack:
            buildHStack(node: node, context: context)
        case .zstack:
            buildZStack(node: node, context: context)
        case .spacer:
            buildSpacer(node: node)

        // Text & Controls (high frequency)
        case .text:
            buildText(node: node)
        case .button:
            buildButton(node: node, context: context)

        // MARK: Slow Path - Registry Lookup

        default:
            // Use registry for less common types or custom views
            registry.build(node: node, context: context)
        }
    }

    // MARK: - Fast Path Implementations

    @ViewBuilder
    private func buildVStack(node: ViewNode, context: NibRenderContext) -> some View {
        VStack(
            alignment: HorizontalAlignment(nibAlignment: node.props.alignment),
            spacing: node.props.spacing
        ) {
            context.buildChildren(node.children)
        }
    }

    @ViewBuilder
    private func buildHStack(node: ViewNode, context: NibRenderContext) -> some View {
        HStack(
            alignment: VerticalAlignment(nibAlignment: node.props.alignment),
            spacing: node.props.spacing
        ) {
            context.buildChildren(node.children)
        }
    }

    @ViewBuilder
    private func buildZStack(node: ViewNode, context: NibRenderContext) -> some View {
        ZStack(alignment: Alignment(nibAlignment: node.props.alignment)) {
            context.buildChildren(node.children)
        }
    }

    @ViewBuilder
    private func buildSpacer(node: ViewNode) -> some View {
        if let minLength = node.props.minLength {
            Spacer(minLength: minLength)
        } else {
            Spacer()
        }
    }

    @ViewBuilder
    private func buildText(node: ViewNode) -> some View {
        Text(node.props.content ?? "")
            .applyTextStyles(node.props.textStyles)
    }

    @ViewBuilder
    private func buildButton(node: ViewNode, context: NibRenderContext) -> some View {
        let styles = node.props.buttonStyles

        Button(role: ButtonRole.nib(styles?.role), action: {
            context.onEvent(node.id, "tap")
        }) {
            if let children = node.children, !children.isEmpty {
                ForEach(children) { child in
                    context.buildChild(child)
                }
            } else if let icon = node.props.icon {
                Label(node.props.label ?? "", systemImage: icon)
            } else {
                Text(node.props.label ?? "")
            }
        }
        .applyButtonStyles(styles)
    }
}

// MARK: - Dispatcher Factory

extension OptimizedViewDispatcher {
    /// Create a render context for recursive building
    func makeContext(onEvent: @escaping (String, String) -> Void) -> NibRenderContext {
        NibRenderContext(
            onEvent: onEvent,
            childBuilder: { [self] childNode in
                AnyView(
                    self.build(node: childNode, context: self.makeContext(onEvent: onEvent))
                        .applyModifiers(childNode.modifiers)
                        .applyBackgroundView(childNode.backgroundView, onEvent: onEvent)
                        .applyOverlayView(childNode.overlayView, onEvent: onEvent)
                        .applyInteractionHandlers(
                            onDrop: childNode.props.onDrop,
                            onHover: childNode.props.onHover,
                            onClick: childNode.props.onClick,
                            tooltip: childNode.props.tooltip,
                            nodeId: childNode.id,
                            onEvent: onEvent
                        )
                )
            }
        )
    }
}
