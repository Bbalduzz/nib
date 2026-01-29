import AppKit
import SwiftUI
import ServiceManagement

class AppDelegate: NSObject, NSApplicationDelegate {
    var statusBarController: StatusBarController?
    var socketServer: SocketServer?
    var hotkeyManager = HotkeyManager()
    var pythonProcess: Process?

    func applicationDidFinishLaunching(_ notification: Notification) {
        clearLog()
        debugPrint("Nib runtime starting...")

        // Add Edit menu for standard commands (Cmd+V paste, etc.)
        setupEditMenu()

        // Handle launch at login registration (for bundled apps)
        registerLaunchAtLoginIfNeeded()

        // Initialize status bar
        statusBarController = StatusBarController()

        // Set up hotkey handler
        hotkeyManager.setHotkeyHandler { [weak self] hotkeyString in
            self?.socketServer?.sendEvent(nodeId: "hotkey", event: "hotkey:\(hotkeyString)")
        }

        // Check if we're running as a bundled app with embedded Python
        if isBundledApp() {
            debugPrint("Running in bundled mode - launching embedded Python")
            launchEmbeddedPython()
        } else {
            // Development mode: Python launches us, we just start the socket server
            debugPrint("Running in development mode - waiting for Python connection")
            startSocketServer()
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
        let bundlePath = Bundle.main.bundlePath
        let pythonPath = (bundlePath as NSString)
            .appendingPathComponent("Contents/MacOS/python/bin/python3")
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
        let pythonDir = "\(bundlePath)/Contents/MacOS/python"
        let pythonBin = "\(pythonDir)/bin/python3"
        let appDir = "\(bundlePath)/Contents/Resources/app"
        let vendorDir = "\(appDir)/vendor"
        let mainScript = "\(appDir)/main.py"

        // Verify Python exists
        guard FileManager.default.fileExists(atPath: pythonBin) else {
            showLaunchError("Python interpreter not found at: \(pythonBin)")
            return
        }

        // Verify main script exists
        guard FileManager.default.fileExists(atPath: mainScript) else {
            showLaunchError("Main script not found at: \(mainScript)")
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
        env["PYTHONDONTWRITEBYTECODE"] = "1"  // Don't create .pyc files in bundle
        env["PYTHONHOME"] = pythonDir
        // Set LC_ALL for proper encoding
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
                debugPrint("Notification - title:", payload.title)
                self?.sendNotification(payload)

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

    // MARK: - Service Routing

    private func handleService(_ payload: NibMessage.ServicePayload) {
        let sendResponse: (NibServiceResponse) -> Void = { [weak self] response in
            self?.socketServer?.sendServiceResponse(response)
        }

        switch payload.service {
        case "battery":
            if payload.action == "status" {
                BatteryService.handleStatus(requestId: payload.requestId, sendResponse: sendResponse)
            } else {
                debugPrint("Unknown battery action:", payload.action)
            }
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
