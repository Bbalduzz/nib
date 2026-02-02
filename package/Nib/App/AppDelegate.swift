import AppKit
import SwiftUI
import ServiceManagement
import UserNotifications
import MessagePack

class AppDelegate: NSObject, NSApplicationDelegate, UNUserNotificationCenterDelegate {
    var statusBarController: StatusBarController?
    var socketServer: SocketServer?
    var hotkeyManager = HotkeyManager()
    var pythonProcess: Process?
    private lazy var settingsController = SettingsWindowController()
    private lazy var notificationService = NotificationService()

    func applicationDidFinishLaunching(_ notification: Notification) {
        clearLog()
        debugPrint("Nib runtime starting...")

        // Check if we're running as a bundled app with embedded Python
        if isBundledApp() {
            debugPrint("Running in bundled mode - launching embedded Python")
            // Full initialization for bundled mode
            setupEditMenu()
            registerLaunchAtLoginIfNeeded()
            setupNotifications()
            statusBarController = StatusBarController()
            hotkeyManager.setHotkeyHandler { [weak self] hotkeyString in
                self?.socketServer?.sendEvent(nodeId: "hotkey", event: "hotkey:\(hotkeyString)")
            }
            launchEmbeddedPython()
        } else {
            // Development mode: Start socket server FIRST so Python can connect quickly
            debugPrint("Running in development mode - starting socket server immediately")
            startSocketServer()

            // Then do the rest of initialization (Python can start connecting now)
            setupEditMenu()
            registerLaunchAtLoginIfNeeded()
            setupNotifications()
            statusBarController = StatusBarController()
            hotkeyManager.setHotkeyHandler { [weak self] hotkeyString in
                self?.socketServer?.sendEvent(nodeId: "hotkey", event: "hotkey:\(hotkeyString)")
            }
        }
    }

    // MARK: - Launch at Login

    private func registerLaunchAtLoginIfNeeded() {
        // Check if launch_at_login is enabled in Info.plist
        guard let launchAtLogin = Bundle.main.infoDictionary?["NibLaunchAtLogin"] as? Bool,
              launchAtLogin else {
            return
        }

        // Check if we've already registered (using UserDefaults)
        let registeredKey = "NibLaunchAtLoginRegistered"
        if UserDefaults.standard.bool(forKey: registeredKey) {
            debugPrint("Launch at login already registered")
            return
        }

        // Register with SMAppService (macOS 13+)
        if #available(macOS 13.0, *) {
            do {
                try SMAppService.mainApp.register()
                UserDefaults.standard.set(true, forKey: registeredKey)
                debugPrint("Registered for launch at login")
            } catch {
                debugPrint("Failed to register for launch at login: \(error)")
            }
        } else {
            debugPrint("Launch at login requires macOS 13+")
        }
    }

    func applicationWillTerminate(_ notification: Notification) {
        // Terminate Python process if running
        if let process = pythonProcess, process.isRunning {
            debugPrint("Terminating Python process")
            process.terminate()
        }
        hotkeyManager.cleanup()
        socketServer?.stop()
    }

    // MARK: - Bundled Mode Detection

    private func isBundledApp() -> Bool {
        // Check if we're running inside a .app bundle with embedded Python
        // Python is in Resources (not MacOS) to avoid code signing issues
        let bundlePath = Bundle.main.bundlePath
        let pythonPath = (bundlePath as NSString)
            .appendingPathComponent("Contents/Resources/python/bin/python3")
        return FileManager.default.fileExists(atPath: pythonPath)
    }

    private func startSocketServer() {
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

    // MARK: - Embedded Python Launching

    private func launchEmbeddedPython() {
        let bundle = Bundle.main
        let bundlePath = bundle.bundlePath

        // Paths within bundle
        // Python is in Resources (not MacOS) to avoid code signing issues
        let pythonDir = "\(bundlePath)/Contents/Resources/python"
        let pythonBin = "\(pythonDir)/bin/python3"
        let appDir = "\(bundlePath)/Contents/Resources/app"
        let vendorDir = "\(appDir)/vendor"

        // Check for compiled bytecode first (.pyc), fall back to source (.py)
        let mainPyc = "\(appDir)/main.pyc"
        let mainPy = "\(appDir)/main.py"
        let mainScript = FileManager.default.fileExists(atPath: mainPyc) ? mainPyc : mainPy

        // Verify Python exists
        guard FileManager.default.fileExists(atPath: pythonBin) else {
            showLaunchError("Python interpreter not found at: \(pythonBin)")
            return
        }

        // Verify main script exists
        guard FileManager.default.fileExists(atPath: mainScript) else {
            showLaunchError("Main script not found at: \(mainPy) or \(mainPyc)")
            return
        }

        // Generate socket path
        let socketPath = "/tmp/nib-\(ProcessInfo.processInfo.processIdentifier).sock"

        // Start socket server BEFORE launching Python (to avoid race condition)
        socketServer = SocketServer(path: socketPath)
        socketServer?.onMessage = { [weak self] message in
            self?.handleMessage(message)
        }

        // Wire up event handler
        statusBarController?.setEventHandler { [weak self] nodeId, event in
            self?.socketServer?.sendEvent(nodeId: nodeId, event: event)
        }

        socketServer?.start()
        debugPrint("Socket server started at: \(socketPath)")

        // Set up Python environment
        var env = ProcessInfo.processInfo.environment
        env["NIB_SOCKET"] = socketPath
        env["PYTHONPATH"] = vendorDir
        env["PYTHONDONTWRITEBYTECODE"] = "1"  // dont create .pyc files in bundle
        env["PYTHONHOME"] = pythonDir
        env["LC_ALL"] = "en_US.UTF-8"
        env["LANG"] = "en_US.UTF-8"

        // Launch Python process
        let process = Process()
        process.executableURL = URL(fileURLWithPath: pythonBin)
        process.arguments = [mainScript]
        process.environment = env
        process.currentDirectoryURL = URL(fileURLWithPath: appDir)

        // Capture Python output for debugging
        let outputPipe = Pipe()
        let errorPipe = Pipe()
        process.standardOutput = outputPipe
        process.standardError = errorPipe

        // Read stdout
        outputPipe.fileHandleForReading.readabilityHandler = { handle in
            let data = handle.availableData
            if !data.isEmpty, let output = String(data: data, encoding: .utf8) {
                for line in output.split(separator: "\n") {
                    debugPrint("[Python] \(line)")
                }
            }
        }

        // Read stderr
        errorPipe.fileHandleForReading.readabilityHandler = { handle in
            let data = handle.availableData
            if !data.isEmpty, let output = String(data: data, encoding: .utf8) {
                for line in output.split(separator: "\n") {
                    debugPrint("[Python ERR] \(line)")
                }
            }
        }

        // Handle Python termination
        process.terminationHandler = { [weak self] proc in
            DispatchQueue.main.async {
                let exitCode = proc.terminationStatus
                debugPrint("Python process exited with code: \(exitCode)")

                // Clean up pipe handlers
                outputPipe.fileHandleForReading.readabilityHandler = nil
                errorPipe.fileHandleForReading.readabilityHandler = nil

                if exitCode != 0 {
                    self?.showLaunchError("Python exited with error code: \(exitCode)\nCheck /tmp/nib.log for details")
                }

                // Exit the app when Python exits
                NSApp.terminate(nil)
            }
        }

        do {
            try process.run()
            pythonProcess = process
            debugPrint("Launched Python: \(pythonBin)")
            print("Nib app started (bundled mode)")
        } catch {
            debugPrint("Failed to launch Python: \(error)")
            showLaunchError("Failed to launch Python: \(error.localizedDescription)")
        }
    }

    private func showLaunchError(_ message: String) {
        DispatchQueue.main.async {
            let alert = NSAlert()
            alert.messageText = "Failed to Start Application"
            alert.informativeText = message
            alert.alertStyle = .critical
            alert.addButton(withTitle: "Quit")
            alert.runModal()
            NSApp.terminate(nil)
        }
    }

    // MARK: - Message Handling

    private func handleMessage(_ message: NibMessage) {
        debugPrint("handleMessage called")
        DispatchQueue.main.async { [weak self] in
            switch message {
            case .render(let payload):
                self?.handleRender(payload)

            case .patch(let payload):
                self?.handlePatch(payload)

            case .notify(let payload):
                debugPrint("Notification (legacy) - title:", payload.title)
                self?.sendNotification(payload)

            case .notification(let payload):
                debugPrint("Notification - action:", payload.action)
                self?.notificationService.handle(payload)

            case .clipboard(let payload):
                debugPrint("Clipboard - action:", payload.action)
                ClipboardHandler.handle(payload) { nodeId, event in
                    self?.socketServer?.sendEvent(nodeId: nodeId, event: event)
                }

            case .fileDialog(let payload):
                debugPrint("FileDialog - action:", payload.action)
                FileDialogHandler.handle(payload) { nodeId, event in
                    self?.socketServer?.sendEvent(nodeId: nodeId, event: event)
                }

            case .userDefaults(let payload):
                debugPrint("UserDefaults - action:", payload.action)
                UserDefaultsHandler.handle(payload) { nodeId, event in
                    self?.socketServer?.sendEvent(nodeId: nodeId, event: event)
                }

            case .service(let payload):
                debugPrint("Service - \(payload.service):\(payload.action)")
                self?.handleService(payload)

            case .action(let payload):
                debugPrint("Action - nodeId:", payload.nodeId, "action:", payload.action)
                self?.statusBarController?.handleAction(nodeId: payload.nodeId, action: payload.action, params: payload.params)

            case .settingsRender(let payload):
                debugPrint("Settings render - tabs:", payload.tabs.count)
                self?.settingsController.onEvent = { [weak self] nodeId, event in
                    self?.socketServer?.sendEvent(nodeId: nodeId, event: event)
                }
                self?.settingsController.render(payload)

            case .settingsOpen:
                debugPrint("Settings open")
                self?.settingsController.show()

            case .settingsClose:
                debugPrint("Settings close")
                self?.settingsController.close()

            case .quit:
                debugPrint("Quit message received")
                NSApp.terminate(nil)
            }
        }
    }

    private func handleRender(_ payload: NibMessage.RenderPayload) {
        debugPrint("Rendering - icon:", payload.statusBar?.icon ?? "nil", "title:", payload.statusBar?.title ?? "nil")

        // Register custom fonts before rendering
        if let fonts = payload.fonts {
            debugPrint("Registering \(fonts.count) custom fonts")
            FontManager.shared.registerFonts(fonts)
        }

        statusBarController?.updateStatusBar(
            icon: payload.statusBar?.icon,
            title: payload.statusBar?.title
        )
        if let window = payload.window {
            statusBarController?.updateWindowSize(
                width: window.width,
                height: window.height
            )
        }
        if let menu = payload.menu {
            statusBarController?.updateMenu(menu)
        }
        if let hotkeys = payload.hotkeys {
            hotkeyManager.updateHotkeys(hotkeys)
        }
        if let root = payload.root {
            debugPrint("Updating content with root type:", root.type)
            statusBarController?.updateContent(root)
        } else {
            debugPrint("No root view in payload")
        }
    }

    private func handlePatch(_ payload: NibMessage.PatchPayload) {
        debugPrint("Patching - \(payload.patches.count) patches")
        statusBarController?.updateStatusBar(
            icon: payload.statusBar?.icon,
            title: payload.statusBar?.title
        )
        if let window = payload.window {
            statusBarController?.updateWindowSize(
                width: window.width,
                height: window.height
            )
        }
        statusBarController?.applyPatches(payload.patches)
    }

    // MARK: - Notifications

    /// Whether we're running as the main executable of a proper .app bundle
    /// UserNotifications framework crashes without a proper app bundle
    private lazy var isRunningFromAppBundle: Bool = {
        // We need to check that:
        // 1. Bundle path ends with .app (we are the main app, not something inside it)
        // 2. The executable is in Contents/MacOS/ (standard app bundle structure)
        let bundlePath = Bundle.main.bundlePath
        let executablePath = Bundle.main.executablePath ?? ""

        // Must be .app bundle AND executable must be in Contents/MacOS/
        let isAppBundle = bundlePath.hasSuffix(".app")
        let isMainExecutable = executablePath.contains("/Contents/MacOS/")

        return isAppBundle && isMainExecutable
    }()

    private func setupNotifications() {
        // Configure notification service with callbacks
        notificationService.configure(
            sendResponse: { [weak self] response in
                self?.sendNotificationResponse(response)
            },
            sendEvent: { [weak self] nodeId, event in
                self?.socketServer?.sendEvent(nodeId: nodeId, event: event)
            }
        )

        // Set up notification center (handles app bundle check internally)
        notificationService.setupNotificationCenter()

        // Legacy setup for old notification API
        guard isRunningFromAppBundle else {
            debugPrint("Skipping legacy notification setup (not running from .app bundle - dev mode)")
            return
        }

        let center = UNUserNotificationCenter.current()
        center.delegate = notificationService

        // Request authorization for notifications
        center.requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
            if let error = error {
                debugPrint("Notification authorization error: \(error)")
            } else {
                debugPrint("Notification authorization granted: \(granted)")
            }
        }
    }

    private func sendNotificationResponse(_ response: NotificationService.NotificationResponse) {
        guard let socketServer = socketServer else { return }

        // Build response dictionary
        var responseDict: [String: Any] = [
            "type": response.type
        ]
        if let requestId = response.requestId {
            responseDict["requestId"] = requestId
        }

        var dataDict: [String: Any] = [:]
        if let granted = response.data.granted {
            dataDict["granted"] = granted
        }
        if let success = response.data.success {
            dataDict["success"] = success
        }
        if let error = response.data.error {
            dataDict["error"] = error
        }
        if let notifications = response.data.notifications {
            dataDict["notifications"] = notifications
        }
        if let notification = response.data.notification {
            dataDict["notification"] = notification
        }
        responseDict["data"] = dataDict

        // Send via MessagePack
        do {
            let encoder = MessagePackEncoder()
            let packed = try encoder.encode(AnyCodableDict(responseDict))
            socketServer.sendMessage(packed)
        } catch {
            debugPrint("Failed to encode notification response: \(error)")
        }
    }

    /// Helper struct for encoding arbitrary dictionaries
    private struct AnyCodableDict: Encodable {
        let dict: [String: Any]

        init(_ dict: [String: Any]) {
            self.dict = dict
        }

        func encode(to encoder: Encoder) throws {
            var container = encoder.container(keyedBy: DynamicCodingKey.self)
            for (key, value) in dict {
                let codingKey = DynamicCodingKey(stringValue: key)!
                try encodeValue(value, forKey: codingKey, in: &container)
            }
        }

        private func encodeValue(_ value: Any, forKey key: DynamicCodingKey, in container: inout KeyedEncodingContainer<DynamicCodingKey>) throws {
            switch value {
            case let str as String:
                try container.encode(str, forKey: key)
            case let int as Int:
                try container.encode(int, forKey: key)
            case let double as Double:
                try container.encode(double, forKey: key)
            case let bool as Bool:
                try container.encode(bool, forKey: key)
            case let dict as [String: Any]:
                try container.encode(AnyCodableDict(dict), forKey: key)
            case let array as [[String: Any]]:
                var nested = container.nestedUnkeyedContainer(forKey: key)
                for item in array {
                    try nested.encode(AnyCodableDict(item))
                }
            default:
                break
            }
        }

        private struct DynamicCodingKey: CodingKey {
            var stringValue: String
            var intValue: Int?

            init?(stringValue: String) {
                self.stringValue = stringValue
                self.intValue = nil
            }

            init?(intValue: Int) {
                self.stringValue = String(intValue)
                self.intValue = intValue
            }
        }
    }

    private func sendNotification(_ payload: NibMessage.NotifyPayload) {
        // IMPORTANT: Must check app bundle BEFORE touching UNUserNotificationCenter
        if isRunningFromAppBundle {
            sendNotificationModern(payload)
        } else {
            sendNotificationLegacy(payload)
        }
    }

    private func sendNotificationModern(_ payload: NibMessage.NotifyPayload) {
        let content = UNMutableNotificationContent()
        content.title = payload.title

        if let body = payload.body {
            content.body = body
        }
        if let subtitle = payload.subtitle {
            content.subtitle = subtitle
        }
        if payload.sound ?? true {
            content.sound = .default
        }

        // Use provided identifier or generate a unique one
        let identifier = payload.identifier ?? UUID().uuidString

        // Create request with no trigger (immediate delivery)
        let request = UNNotificationRequest(
            identifier: identifier,
            content: content,
            trigger: nil
        )

        UNUserNotificationCenter.current().add(request) { error in
            if let error = error {
                debugPrint("Failed to send notification: \(error)")
            } else {
                debugPrint("Notification sent: \(payload.title)")
            }
        }
    }

    private func sendNotificationLegacy(_ payload: NibMessage.NotifyPayload) {
        // Use AppleScript for dev mode (no bundle) - avoids deprecated APIs
        let title = payload.title.replacingOccurrences(of: "\"", with: "\\\"")
        let body = (payload.body ?? "").replacingOccurrences(of: "\"", with: "\\\"")
        let subtitle = payload.subtitle?.replacingOccurrences(of: "\"", with: "\\\"")

        var script = "display notification \"\(body)\" with title \"\(title)\""
        if let sub = subtitle {
            script += " subtitle \"\(sub)\""
        }
        if payload.sound ?? true {
            script += " sound name \"default\""
        }

        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/osascript")
        process.arguments = ["-e", script]
        try? process.run()
        debugPrint("Notification sent (AppleScript): \(payload.title)")
    }

    // MARK: - UNUserNotificationCenterDelegate

    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification,
        withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void
    ) {
        // Show notification even when app is in foreground
        completionHandler([.banner, .sound])
    }

    // MARK: - Service Routing

    private func handleService(_ payload: NibMessage.ServicePayload) {
        let sendResponse: (NibServiceResponse) -> Void = { [weak self] response in
            self?.socketServer?.sendServiceResponse(response)
        }

        switch payload.service {
        case "battery":
            BatteryService.handle(payload, sendResponse: sendResponse)
        case "connectivity":
            if payload.action == "status" {
                ConnectivityService.handleStatus(requestId: payload.requestId, sendResponse: sendResponse)
            } else {
                debugPrint("Unknown connectivity action:", payload.action)
            }
        case "screen":
            ScreenService.handle(payload, sendResponse: sendResponse)
        case "keychain":
            KeychainService.handle(payload, sendResponse: sendResponse)
        case "camera":
            CameraService.shared.handle(payload, sendResponse: sendResponse)
        case "launchAtLogin":
            log.info("Routing to LaunchAtLoginService: \(payload.action)")
            LaunchAtLoginService.handle(payload, sendResponse: sendResponse)
        default:
            debugPrint("Unknown service:", payload.service)
        }
    }

    // MARK: - Edit Menu (for Cmd+V paste support in TextFields)

    private func setupEditMenu() {
        let editMenu = NSMenu(title: "Edit")

        editMenu.addItem(withTitle: "Undo", action: Selector(("undo:")), keyEquivalent: "z")
        editMenu.addItem(withTitle: "Redo", action: Selector(("redo:")), keyEquivalent: "Z")
        editMenu.addItem(NSMenuItem.separator())
        editMenu.addItem(withTitle: "Cut", action: #selector(NSText.cut(_:)), keyEquivalent: "x")
        editMenu.addItem(withTitle: "Copy", action: #selector(NSText.copy(_:)), keyEquivalent: "c")
        editMenu.addItem(withTitle: "Paste", action: #selector(NSText.paste(_:)), keyEquivalent: "v")
        editMenu.addItem(withTitle: "Select All", action: #selector(NSText.selectAll(_:)), keyEquivalent: "a")

        let editMenuItem = NSMenuItem(title: "Edit", action: nil, keyEquivalent: "")
        editMenuItem.submenu = editMenu

        // Insert Edit menu after the app menu (index 1)
        if NSApp.mainMenu == nil {
            NSApp.mainMenu = NSMenu()
        }
        if let mainMenu = NSApp.mainMenu {
            if mainMenu.items.count > 0 {
                mainMenu.insertItem(editMenuItem, at: 1)
            } else {
                mainMenu.addItem(editMenuItem)
            }
        }
    }
}
