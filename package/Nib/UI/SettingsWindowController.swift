import AppKit
import SwiftUI

/// Controller for the Settings window
class SettingsWindowController: NSObject, NSWindowDelegate {
    private var window: NSWindow?
    private var currentPayload: NibMessage.SettingsRenderPayload?
    var onEvent: ((String, String) -> Void)?

    func render(_ payload: NibMessage.SettingsRenderPayload) {
        currentPayload = payload

        if window == nil {
            createWindow(
                width: payload.width ?? 450,
                height: payload.height ?? 350,
                title: payload.title ?? "Settings"
            )
        }

        // Update content
        let contentView = SettingsContentView(
            tabs: payload.tabs,
            onEvent: { [weak self] nodeId, event in
                self?.onEvent?(nodeId, event)
            }
        )
        window?.contentView = NSHostingView(rootView: contentView)
    }

    func show() {
        window?.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
    }

    func close() {
        window?.close()
    }

    private func createWindow(width: CGFloat, height: CGFloat, title: String) {
        let window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: width, height: height),
            styleMask: [.titled, .closable],
            backing: .buffered,
            defer: false
        )
        window.title = title
        window.delegate = self
        window.center()
        window.isReleasedWhenClosed = false
        self.window = window
    }

    // MARK: - NSWindowDelegate

    func windowWillClose(_ notification: Notification) {
        debugPrint("Settings window closed")
    }
}

/// SwiftUI view for settings content with tabs
struct SettingsContentView: View {
    let tabs: [NibMessage.SettingsTabPayload]
    let onEvent: (String, String) -> Void

    @State private var selectedTab = 0

    var body: some View {
        if tabs.count == 1, let content = tabs.first?.content {
            // Single tab - no tab bar needed
            DynamicView(node: content, onEvent: onEvent)
        } else {
            // Multiple tabs
            TabView(selection: $selectedTab) {
                ForEach(Array(tabs.enumerated()), id: \.offset) { index, tab in
                    if let content = tab.content {
                        DynamicView(node: content, onEvent: onEvent)
                            .tabItem {
                                if let icon = tab.icon {
                                    Image(systemName: icon)
                                }
                                Text(tab.title)
                            }
                            .tag(index)
                    }
                }
            }
            .padding()
        }
    }
}
