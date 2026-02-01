import Foundation

// MARK: - Plugin Loader

/// Manages plugin discovery, loading, and lifecycle.
final class NibPluginLoader {
    static let shared = NibPluginLoader()

    /// Currently loaded plugins indexed by namespace
    private var loadedPlugins: [String: NibPlugin] = [:]

    /// Reference to the registries
    private let viewRegistry = NibViewBuilderRegistry.shared
    private let modifierRegistry = NibModifierRegistry.shared

    private init() {}

    // MARK: - Loading

    /// Register a plugin programmatically
    func registerPlugin(_ plugin: NibPlugin) throws {
        // Check for namespace conflicts
        guard loadedPlugins[plugin.namespace] == nil else {
            throw NibPluginError.namespaceConflict(plugin.namespace)
        }

        // Register view builders
        for builder in plugin.viewBuilders {
            viewRegistry.register(builder, namespace: plugin.namespace)
        }

        // Register modifier handlers
        for (type, handler) in plugin.modifierHandlers {
            modifierRegistry.register(type: type, namespace: plugin.namespace, handler: handler)
        }

        // Notify plugin it's loaded
        plugin.onLoad()

        // Track the plugin
        loadedPlugins[plugin.namespace] = plugin

        debugPrint("Plugin '\(plugin.namespace)' v\(plugin.version) loaded successfully")
    }

    /// Load a plugin from a bundle (for dynamic loading)
    /// Note: Plugin classes must have a required init() initializer
    func loadPlugin(from bundle: Bundle, factory: () -> NibPlugin) throws {
        guard bundle.principalClass is NibPlugin.Type else {
            throw NibPluginError.invalidBundle
        }

        // Create instance using factory and register
        let plugin = factory()
        try registerPlugin(plugin)
    }

    // MARK: - Unloading

    /// Unload a plugin by namespace
    func unloadPlugin(namespace: String) {
        guard let plugin = loadedPlugins[namespace] else { return }

        // Notify plugin it's being unloaded
        plugin.onUnload()

        // Remove from tracking
        loadedPlugins.removeValue(forKey: namespace)

        debugPrint("Plugin '\(namespace)' unloaded")

        // Note: Registry entries remain orphaned but inactive
        // A full cleanup would require tracking which entries belong to which plugin
    }

    // MARK: - Introspection

    /// Check if a plugin is loaded
    func isLoaded(namespace: String) -> Bool {
        loadedPlugins[namespace] != nil
    }

    /// Get all loaded plugin namespaces
    var loadedNamespaces: [String] {
        Array(loadedPlugins.keys).sorted()
    }

    /// Get a loaded plugin by namespace
    func plugin(for namespace: String) -> NibPlugin? {
        loadedPlugins[namespace]
    }
}
