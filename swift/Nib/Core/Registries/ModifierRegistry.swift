import SwiftUI

// MARK: - Modifier Registry

/// Type alias for modifier handler functions
typealias ModifierHandler = (AnyView, ViewNode.ViewModifier.ModifierArgs) -> AnyView

/// Central registry for custom modifiers - supports third-party modifier extensions.
final class NibModifierRegistry {
    static let shared = NibModifierRegistry()

    /// Registered custom modifier handlers
    private var handlers: [String: ModifierHandler] = [:]

    /// Registered namespaces
    private(set) var namespaces: Set<String> = ["nib"]

    private init() {}

    // MARK: - Registration

    /// Register a custom modifier handler
    func register(type: String, handler: @escaping ModifierHandler) {
        handlers[type] = handler
    }

    /// Register a namespaced modifier handler (for plugins)
    func register(type: String, namespace: String, handler: @escaping ModifierHandler) {
        let qualifiedType = "\(namespace):\(type)"
        handlers[qualifiedType] = handler
        namespaces.insert(namespace)
    }

    // MARK: - Lookup

    /// Check if a custom modifier is registered
    func hasHandler(for type: String) -> Bool {
        handlers[type] != nil || handlers["nib:\(type)"] != nil
    }

    /// Apply a custom modifier if registered
    /// Returns nil if no handler is registered for this type
    func apply(_ type: String, to view: AnyView, args: ViewNode.ViewModifier.ModifierArgs) -> AnyView? {
        if let handler = handlers[type] {
            return handler(view, args)
        }
        if let handler = handlers["nib:\(type)"] {
            return handler(view, args)
        }
        return nil
    }

    // MARK: - Introspection

    /// Get all registered modifier types
    var registeredTypes: [String] {
        Array(handlers.keys).sorted()
    }
}
