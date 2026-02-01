import Foundation

/// Protocol for views that can handle actions
protocol ActionHandler: AnyObject {
    func handleAction(_ action: String, params: [String: AnyCodable]?)
}

/// Global registry for view action handlers.
/// Views register themselves when created and can receive actions from Python.
class ViewActionRegistry {
    static let shared = ViewActionRegistry()

    private var handlers: [String: ActionHandler] = [:]
    private let lock = NSLock()

    private init() {}

    /// Register an action handler for a node ID
    func register(nodeId: String, handler: ActionHandler) {
        lock.lock()
        defer { lock.unlock() }
        handlers[nodeId] = handler
        debugPrint("ViewActionRegistry: registered handler for", nodeId)
    }

    /// Unregister an action handler
    func unregister(nodeId: String) {
        lock.lock()
        defer { lock.unlock() }
        handlers.removeValue(forKey: nodeId)
        debugPrint("ViewActionRegistry: unregistered handler for", nodeId)
    }

    /// Perform an action on the registered handler
    func performAction(nodeId: String, action: String, params: [String: AnyCodable]?) {
        lock.lock()
        let handler = handlers[nodeId]
        lock.unlock()

        if let handler = handler {
            debugPrint("ViewActionRegistry: performing action", action, "on", nodeId)
            DispatchQueue.main.async {
                handler.handleAction(action, params: params)
            }
        } else {
            debugPrint("ViewActionRegistry: no handler found for", nodeId)
        }
    }
}
