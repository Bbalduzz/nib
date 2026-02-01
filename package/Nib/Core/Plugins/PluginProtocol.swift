import Foundation

// MARK: - Plugin Protocol

/// Protocol that third-party plugins must implement to extend Nib.
/// Plugins can provide custom view builders and modifier handlers.
protocol NibPlugin {
    /// Unique namespace for this plugin (e.g., "charts", "markdown")
    /// Used to qualify view types and prevent conflicts
    var namespace: String { get }

    /// Version string for compatibility checking
    var version: String { get }

    /// View builders provided by this plugin
    var viewBuilders: [AnyNibViewBuilder] { get }

    /// Modifier handlers provided by this plugin (optional)
    var modifierHandlers: [String: ModifierHandler] { get }

    /// Called when the plugin is loaded and registered
    func onLoad()

    /// Called when the plugin is unloaded
    func onUnload()
}

// MARK: - Default Implementations

extension NibPlugin {
    /// Default: no custom modifier handlers
    var modifierHandlers: [String: ModifierHandler] { [:] }

    /// Default: no-op on load
    func onLoad() {}

    /// Default: no-op on unload
    func onUnload() {}
}

// MARK: - Plugin Errors

enum NibPluginError: Error, LocalizedError {
    case invalidBundle
    case namespaceConflict(String)
    case incompatibleVersion(required: String, found: String)
    case loadFailed(String)

    var errorDescription: String? {
        switch self {
        case .invalidBundle:
            return "Invalid plugin bundle - missing or invalid principal class"
        case .namespaceConflict(let namespace):
            return "Plugin namespace '\(namespace)' is already registered"
        case .incompatibleVersion(let required, let found):
            return "Incompatible plugin version: requires \(required), found \(found)"
        case .loadFailed(let reason):
            return "Plugin load failed: \(reason)"
        }
    }
}
