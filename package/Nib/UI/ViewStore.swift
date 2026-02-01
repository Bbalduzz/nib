import SwiftUI
import Observation

// MARK: - Granular View Store (macOS 14+)

/// Observable store for the view tree with granular change tracking.
/// Uses @Observable (Swift 5.9+) for fine-grained reactivity - only views
/// that access changed properties will re-render.
@Observable
final class ViewStore {
    /// Root node of the view tree (the `node` property for compatibility)
    var node: ViewNode? {
        didSet {
            rebuildCache()
        }
    }

    /// Node cache for O(1) lookup by ID
    private var nodeCache: [String: ViewNode] = [:]

    /// Event callback to send events back to Python
    var onEvent: ((String, String) -> Void)?

    // MARK: - Full Tree Operations

    /// Set the entire view tree (initial render or major changes)
    func setRoot(_ newNode: ViewNode?) {
        node = newNode
    }

    /// Alias for rootNode for internal use
    var rootNode: ViewNode? {
        node
    }

    // MARK: - Granular Updates

    /// Update a specific node's props without full tree re-render
    func updateNodeProps(_ nodeId: String, props: ViewNode.Props) {
        guard var cachedNode = nodeCache[nodeId] else {
            debugPrint("ViewStore: Node not found for props update: \(nodeId)")
            return
        }
        cachedNode.props = props
        nodeCache[nodeId] = cachedNode

        // Update in tree if it's the root
        if node?.id == nodeId {
            node?.props = props
        }
    }

    /// Update a specific node's modifiers
    func updateNodeModifiers(_ nodeId: String, modifiers: [ViewNode.ViewModifier]) {
        guard var cachedNode = nodeCache[nodeId] else {
            debugPrint("ViewStore: Node not found for modifiers update: \(nodeId)")
            return
        }
        cachedNode.modifiers = modifiers
        nodeCache[nodeId] = cachedNode

        // Update in tree if it's the root
        if node?.id == nodeId {
            node?.modifiers = modifiers
        }
    }

    /// Get a node by ID from the cache
    func node(for id: String) -> ViewNode? {
        nodeCache[id]
    }

    /// Check if a node exists in the tree
    func hasNode(_ id: String) -> Bool {
        nodeCache[id] != nil
    }

    // MARK: - Cache Management

    /// Rebuild the entire cache from the root node
    private func rebuildCache() {
        nodeCache.removeAll(keepingCapacity: true)
        if let root = node {
            cacheNode(root)
        }
    }

    /// Recursively cache a node and its children
    private func cacheNode(_ nodeToCache: ViewNode) {
        nodeCache[nodeToCache.id] = nodeToCache
        nodeToCache.children?.forEach { cacheNode($0) }
        nodeToCache.backgroundViews?.forEach { cacheNode($0) }
    }

    // MARK: - Tree Statistics

    /// Total number of nodes in the tree
    var nodeCount: Int {
        nodeCache.count
    }

    /// Get all node IDs
    var allNodeIds: [String] {
        Array(nodeCache.keys)
    }
}

// MARK: - Legacy Compatibility

/// Type alias for backward compatibility with existing code
/// that uses ObservableObject pattern
@available(*, deprecated, message: "Use ViewStore directly with @Observable")
typealias LegacyViewStore = ViewStore
