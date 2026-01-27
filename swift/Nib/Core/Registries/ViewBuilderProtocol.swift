import SwiftUI

// MARK: - View Builder Protocol

/// Protocol for view builders that can construct SwiftUI views from ViewNode data.
/// Each builder handles a specific view type (e.g., VStack, Button, Text).
protocol NibViewBuilder {
    /// The view type identifier this builder handles (e.g., "VStack", "Button")
    static var viewType: String { get }

    /// Build a SwiftUI view from the given node
    @ViewBuilder
    func build(node: ViewNode, context: NibRenderContext) -> AnyView
}

// MARK: - Render Context

/// Context passed to view builders providing access to shared resources
struct NibRenderContext {
    /// Callback for emitting events back to Python
    let onEvent: (String, String) -> Void

    /// Builds a child node into a view (for recursive rendering)
    let childBuilder: (ViewNode) -> AnyView

    /// Build child views for container types
    @ViewBuilder
    func buildChildren(_ children: [ViewNode]?) -> some View {
        if let children = children {
            ForEach(children) { child in
                childBuilder(child)
            }
        }
    }

    /// Build a single child node
    func buildChild(_ node: ViewNode) -> AnyView {
        childBuilder(node)
    }
}

// MARK: - Type-Erased Builder Wrapper

/// Type-erased wrapper for view builders, allowing storage in heterogeneous collections
struct AnyNibViewBuilder {
    fileprivate let _build: (ViewNode, NibRenderContext) -> AnyView
    let viewType: String

    init<B: NibViewBuilder>(_ builder: B) {
        self.viewType = B.viewType
        self._build = { node, context in
            builder.build(node: node, context: context)
        }
    }

    /// Internal initializer for manual construction (used by registry)
    init(viewType: String, build: @escaping (ViewNode, NibRenderContext) -> AnyView) {
        self.viewType = viewType
        self._build = build
    }

    /// Build a view using the wrapped builder
    func build(node: ViewNode, context: NibRenderContext) -> AnyView {
        _build(node, context)
    }
}
