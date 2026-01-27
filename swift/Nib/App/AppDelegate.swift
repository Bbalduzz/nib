import AppKit
import SwiftUI
import UniformTypeIdentifiers

class AppDelegate: NSObject, NSApplicationDelegate {
    var statusBarController: StatusBarController?
    var socketServer: SocketServer?
    var globalHotkeyMonitor: Any?
    var registeredHotkeys: Set<String> = []

    func applicationDidFinishLaunching(_ notification: Notification) {
        clearLog()
        debugPrint("Nib runtime starting...")

        // Initialize status bar
        statusBarController = StatusBarController()

        // Get socket path from environment or use default
        let socketPath = ProcessInfo.processInfo.environment["NIB_SOCKET"]
            ?? "/tmp/nib-\(ProcessInfo.processInfo.processIdentifier).sock"

        // Start socket server
        socketServer = SocketServer(path: socketPath)
        socketServer?.onMessage = { [weak self] message in
            self?.handleMessage(message)
        }

        // Wire up event handler
        statusBarController?.setEventHandler { [weak self] nodeId, event in
            self?.socketServer?.sendEvent(nodeId: nodeId, event: event)
        }

        socketServer?.start()

        print("Nib runtime started, socket: \(socketPath)")
    }

    func applicationWillTerminate(_ notification: Notification) {
        socketServer?.stop()
    }

    private func handleMessage(_ message: NibMessage) {
        debugPrint("handleMessage called")
        DispatchQueue.main.async { [weak self] in
            switch message {
            case .render(let payload):
                debugPrint("Rendering - icon:", payload.statusBar?.icon ?? "nil", "title:", payload.statusBar?.title ?? "nil")

                // Register custom fonts before rendering
                if let fonts = payload.fonts {
                    debugPrint("Registering \(fonts.count) custom fonts")
                    FontManager.shared.registerFonts(fonts)
                }

                self?.statusBarController?.updateStatusBar(
                    icon: payload.statusBar?.icon,
                    title: payload.statusBar?.title
                )
                if let window = payload.window {
                    self?.statusBarController?.updateWindowSize(
                        width: window.width,
                        height: window.height
                    )
                }
                if let menu = payload.menu {
                    self?.statusBarController?.updateMenu(menu)
                }
                if let hotkeys = payload.hotkeys {
                    self?.updateHotkeys(hotkeys)
                }
                if let root = payload.root {
                    debugPrint("Updating content with root type:", root.type)
                    self?.statusBarController?.updateContent(root)
                } else {
                    debugPrint("No root view in payload")
                }

            case .patch(let payload):
                debugPrint("Patching - \(payload.patches.count) patches")
                self?.statusBarController?.updateStatusBar(
                    icon: payload.statusBar?.icon,
                    title: payload.statusBar?.title
                )
                if let window = payload.window {
                    self?.statusBarController?.updateWindowSize(
                        width: window.width,
                        height: window.height
                    )
                }
                self?.statusBarController?.applyPatches(payload.patches)

            case .notify(let payload):
                debugPrint("Notification - title:", payload.title)
                self?.sendNotification(payload)

            case .clipboard(let payload):
                debugPrint("Clipboard - action:", payload.action)
                self?.handleClipboard(payload)

            case .fileDialog(let payload):
                debugPrint("FileDialog - action:", payload.action)
                self?.handleFileDialog(payload)

            case .userDefaults(let payload):
                debugPrint("UserDefaults - action:", payload.action)
                self?.handleUserDefaults(payload)

            case .quit:
                debugPrint("Quit message received")
                NSApp.terminate(nil)
            }
        }
    }

    private func sendNotification(_ payload: NibMessage.NotifyPayload) {
        // Use NSUserNotification (deprecated but works without bundle identity issues)
        let notification = NSUserNotification()
        notification.title = payload.title
        if let body = payload.body {
            notification.informativeText = body
        }
        if let subtitle = payload.subtitle {
            notification.subtitle = subtitle
        }
        if payload.sound ?? true {
            notification.soundName = NSUserNotificationDefaultSoundName
        }
        if let identifier = payload.identifier {
            notification.identifier = identifier
        }

        NSUserNotificationCenter.default.deliver(notification)
        debugPrint("Notification sent: \(payload.title)")
    }

    // MARK: - Clipboard

    private func handleClipboard(_ payload: NibMessage.ClipboardPayload) {
        switch payload.action {
        case "write":
            if let content = payload.content {
                NSPasteboard.general.clearContents()
                NSPasteboard.general.setString(content, forType: .string)
                debugPrint("Clipboard write successful")
            }
        case "read":
            let content = NSPasteboard.general.string(forType: .string) ?? ""
            let requestId = payload.requestId ?? ""
            socketServer?.sendEvent(nodeId: requestId, event: "clipboard:\(content)")
            debugPrint("Clipboard read:", content.prefix(50))
        default:
            debugPrint("Unknown clipboard action:", payload.action)
        }
    }

    // MARK: - File Dialog

    private func handleFileDialog(_ payload: NibMessage.FileDialogPayload) {
        switch payload.action {
        case "open":
            let panel = NSOpenPanel()
            panel.title = payload.title ?? "Open File"
            panel.allowsMultipleSelection = payload.multiple ?? false
            panel.canChooseDirectories = false
            panel.canChooseFiles = true

            if let directory = payload.directory {
                panel.directoryURL = URL(fileURLWithPath: directory)
            }

            if let types = payload.types, !types.isEmpty {
                panel.allowedContentTypes = types.compactMap { ext in
                    UTType(filenameExtension: ext)
                }
            }

            let response = panel.runModal()
            if response == .OK {
                let paths = panel.urls.map { $0.path }.joined(separator: "\n")
                socketServer?.sendEvent(nodeId: payload.requestId, event: "fileDialog:\(paths)")
            } else {
                socketServer?.sendEvent(nodeId: payload.requestId, event: "fileDialog:")
            }

        case "save":
            let panel = NSSavePanel()
            panel.title = payload.title ?? "Save File"

            if let directory = payload.directory {
                panel.directoryURL = URL(fileURLWithPath: directory)
            }
            if let defaultName = payload.defaultName {
                panel.nameFieldStringValue = defaultName
            }

            if let types = payload.types, !types.isEmpty {
                panel.allowedContentTypes = types.compactMap { ext in
                    UTType(filenameExtension: ext)
                }
            }

            let response = panel.runModal()
            if response == .OK, let url = panel.url {
                socketServer?.sendEvent(nodeId: payload.requestId, event: "fileDialog:\(url.path)")
            } else {
                socketServer?.sendEvent(nodeId: payload.requestId, event: "fileDialog:")
            }

        default:
            debugPrint("Unknown fileDialog action:", payload.action)
        }
    }

    // MARK: - Global Hotkeys

    private func updateHotkeys(_ hotkeys: [String]) {
        let newHotkeys = Set(hotkeys)
        guard newHotkeys != registeredHotkeys else { return }

        registeredHotkeys = newHotkeys

        // Remove existing monitor
        if let monitor = globalHotkeyMonitor {
            NSEvent.removeMonitor(monitor)
            globalHotkeyMonitor = nil
        }

        guard !hotkeys.isEmpty else { return }

        // Add global key monitor
        globalHotkeyMonitor = NSEvent.addGlobalMonitorForEvents(matching: .keyDown) { [weak self] event in
            self?.handleKeyEvent(event)
        }

        debugPrint("Registered hotkeys:", hotkeys)
    }

    private func handleKeyEvent(_ event: NSEvent) {
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
            socketServer?.sendEvent(nodeId: "hotkey", event: "hotkey:\(hotkeyString)")
        }
    }

    // MARK: - UserDefaults

    private func handleUserDefaults(_ payload: NibMessage.UserDefaultsPayload) {
        let defaults = UserDefaults.standard
        let requestId = payload.requestId ?? ""

        switch payload.action {
        case "get":
            guard let key = payload.key else {
                socketServer?.sendEvent(nodeId: requestId, event: "userDefaults:error:key required")
                return
            }
            let value = defaults.object(forKey: key)
            let response = encodeUserDefaultsValue(value)
            socketServer?.sendEvent(nodeId: requestId, event: "userDefaults:get:\(response)")
            debugPrint("UserDefaults get:", key, "=", response)

        case "set":
            guard let key = payload.key else {
                debugPrint("UserDefaults set: key required")
                return
            }
            if let value = payload.value?.value {
                defaults.set(value, forKey: key)
                debugPrint("UserDefaults set:", key, "=", value)
            } else {
                defaults.removeObject(forKey: key)
                debugPrint("UserDefaults set nil for:", key)
            }

        case "remove":
            guard let key = payload.key else {
                debugPrint("UserDefaults remove: key required")
                return
            }
            defaults.removeObject(forKey: key)
            debugPrint("UserDefaults removed:", key)

        case "clear":
            // Clear all keys with the app's bundle identifier prefix
            let domain = Bundle.main.bundleIdentifier ?? "nib"
            defaults.removePersistentDomain(forName: domain)
            debugPrint("UserDefaults cleared for domain:", domain)

        case "containsKey":
            guard let key = payload.key else {
                socketServer?.sendEvent(nodeId: requestId, event: "userDefaults:containsKey:false")
                return
            }
            let exists = defaults.object(forKey: key) != nil
            socketServer?.sendEvent(nodeId: requestId, event: "userDefaults:containsKey:\(exists)")
            debugPrint("UserDefaults containsKey:", key, "=", exists)

        case "getKeys":
            let prefix = payload.prefix ?? ""
            let allKeys = defaults.dictionaryRepresentation().keys
            let matchingKeys = allKeys.filter { $0.hasPrefix(prefix) }
            let keysString = matchingKeys.joined(separator: "\n")
            socketServer?.sendEvent(nodeId: requestId, event: "userDefaults:getKeys:\(keysString)")
            debugPrint("UserDefaults getKeys with prefix:", prefix, "found:", matchingKeys.count)

        default:
            debugPrint("Unknown userDefaults action:", payload.action)
        }
    }

    private func encodeUserDefaultsValue(_ value: Any?) -> String {
        guard let value = value else { return "null" }

        switch value {
        case let string as String:
            // Escape special characters for safe transmission
            let escaped = string
                .replacingOccurrences(of: "\\", with: "\\\\")
                .replacingOccurrences(of: "\n", with: "\\n")
                .replacingOccurrences(of: ":", with: "\\:")
            return "string:\(escaped)"
        case let number as NSNumber:
            // Check if it's a boolean
            if CFGetTypeID(number) == CFBooleanGetTypeID() {
                return "bool:\(number.boolValue)"
            }
            // Check if it's an integer or floating point
            if floor(number.doubleValue) == number.doubleValue {
                return "int:\(number.intValue)"
            }
            return "float:\(number.doubleValue)"
        case let data as Data:
            return "data:\(data.base64EncodedString())"
        case let array as [Any]:
            // Encode array as JSON
            if let jsonData = try? JSONSerialization.data(withJSONObject: array),
               let jsonString = String(data: jsonData, encoding: .utf8) {
                return "array:\(jsonString)"
            }
            return "null"
        case let dict as [String: Any]:
            // Encode dictionary as JSON
            if let jsonData = try? JSONSerialization.data(withJSONObject: dict),
               let jsonString = String(data: jsonData, encoding: .utf8) {
                return "dict:\(jsonString)"
            }
            return "null"
        default:
            return "null"
        }
    }
}
