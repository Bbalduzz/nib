import SwiftUI

// MARK: - View Builder Registry

/// Central registry for view builders - supports both built-in and third-party types.
/// Uses singleton pattern for global access.
final class NibViewBuilderRegistry {
    static let shared = NibViewBuilderRegistry()

    /// Registered builders indexed by view type
    private var builders: [String: AnyNibViewBuilder] = [:]

    /// Registered namespaces (for plugin isolation)
    private(set) var namespaces: Set<String> = ["nib"]

    private init() {}

    // MARK: - Registration

    /// Register a view builder for a specific type
    func register<B: NibViewBuilder>(_ builder: B) {
        builders[B.viewType] = AnyNibViewBuilder(builder)
    }

    /// Register a namespaced builder (for third-party plugins)
    func register<B: NibViewBuilder>(_ builder: B, namespace: String) {
        let qualifiedType = "\(namespace):\(B.viewType)"
        builders[qualifiedType] = AnyNibViewBuilder(builder)
        namespaces.insert(namespace)
    }

    /// Register a type-erased builder directly
    func register(_ builder: AnyNibViewBuilder) {
        builders[builder.viewType] = builder
    }

    /// Register a type-erased builder with namespace
    func register(_ builder: AnyNibViewBuilder, namespace: String) {
        let qualifiedType = "\(namespace):\(builder.viewType)"
        builders[qualifiedType] = AnyNibViewBuilder(
            viewType: qualifiedType,
            build: { node, context in builder.build(node: node, context: context) }
        )
        namespaces.insert(namespace)
    }

    // MARK: - Lookup

    /// Get builder for a view type
    func builder(for viewType: String) -> AnyNibViewBuilder? {
        // Direct lookup first
        if let builder = builders[viewType] {
            return builder
        }

        // Try with default namespace
        if let builder = builders["nib:\(viewType)"] {
            return builder
        }

        return nil
    }

    /// Check if a builder is registered for the given type
    func hasBuilder(for viewType: String) -> Bool {
        builder(for: viewType) != nil
    }

    /// Build a view, returning placeholder for unknown types
    func build(node: ViewNode, context: NibRenderContext) -> AnyView {
        if let builder = builder(for: node.type.rawValue) {
            return builder.build(node: node, context: context)
        }

        // Unknown type - return debug placeholder in DEBUG, empty in RELEASE
        #if DEBUG
        return AnyView(
            Text("Unknown view type: \(node.type.rawValue)")
                .foregroundColor(.red)
                .font(.caption)
        )
        #else
        return AnyView(EmptyView())
        #endif
    }

    // MARK: - Introspection

    /// Get all registered view types
    var registeredTypes: [String] {
        Array(builders.keys).sorted()
    }

    /// Get all registered view types for a specific namespace
    func registeredTypes(in namespace: String) -> [String] {
        let prefix = "\(namespace):"
        return builders.keys
            .filter { $0.hasPrefix(prefix) }
            .map { String($0.dropFirst(prefix.count)) }
            .sorted()
    }
}

