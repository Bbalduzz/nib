import AppKit

/// Manages global and local hotkey registration and handling
class HotkeyManager {
    private var globalMonitor: Any?
    private var localMonitor: Any?
    private var registeredHotkeys: Set<String> = []
    private var onHotkeyTriggered: ((String) -> Void)?

    func setHotkeyHandler(_ handler: @escaping (String) -> Void) {
        onHotkeyTriggered = handler
    }

    func updateHotkeys(_ hotkeys: [String]) {
        let newHotkeys = Set(hotkeys)
        guard newHotkeys != registeredHotkeys else { return }

        registeredHotkeys = newHotkeys

        // Remove existing monitors
        if let monitor = globalMonitor {
            NSEvent.removeMonitor(monitor)
            globalMonitor = nil
        }
        if let monitor = localMonitor {
            NSEvent.removeMonitor(monitor)
            localMonitor = nil
        }

        guard !hotkeys.isEmpty else { return }

        // Add local key monitor (works when app has focus, no permissions needed)
        localMonitor = NSEvent.addLocalMonitorForEvents(matching: .keyDown) { [weak self] event in
            if self?.handleKeyEvent(event) == true {
                return nil  // Consume the event
            }
            return event  // Pass through unhandled events
        }

        // Add global key monitor (works when app doesn't have focus, requires Accessibility permission)
        globalMonitor = NSEvent.addGlobalMonitorForEvents(matching: .keyDown) { [weak self] event in
            _ = self?.handleKeyEvent(event)
        }

        debugPrint("Registered hotkeys:", hotkeys)
    }

    @discardableResult
    private func handleKeyEvent(_ event: NSEvent) -> Bool {
        var parts: [String] = []

        if event.modifierFlags.contains(.command) { parts.append("cmd") }
        if event.modifierFlags.contains(.shift) { parts.append("shift") }
        if event.modifierFlags.contains(.option) { parts.append("opt") }
        if event.modifierFlags.contains(.control) { parts.append("ctrl") }

        if let chars = event.charactersIgnoringModifiers?.lowercased() {
            parts.append(chars)
        }

        let hotkeyString = parts.joined(separator: "+")

        if registeredHotkeys.contains(hotkeyString) {
            debugPrint("Hotkey triggered:", hotkeyString)
            onHotkeyTriggered?(hotkeyString)
            return true
        }
        return false
    }

    func cleanup() {
        if let monitor = globalMonitor {
            NSEvent.removeMonitor(monitor)
            globalMonitor = nil
        }
        if let monitor = localMonitor {
            NSEvent.removeMonitor(monitor)
            localMonitor = nil
        }
    }

    deinit {
        cleanup()
    }
}
