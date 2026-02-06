import AppKit
import SwiftUI

/// Controller for the Settings window.
/// Uses NSToolbar for tab switching to match native macOS Settings style.
class SettingsWindowController: NSObject, NSWindowDelegate, NSToolbarDelegate {
    private var window: NSWindow?
    private var currentPayload: NibMessage.SettingsRenderPayload?
    private var selectedTabIndex = 0
    var onEvent: ((String, String) -> Void)?

    // Toolbar item identifiers, one per tab
    private var tabIdentifiers: [NSToolbarItem.Identifier] = []
    private var tabsByIdentifier: [NSToolbarItem.Identifier: NibMessage.SettingsTabPayload] = [:]

    func render(_ payload: NibMessage.SettingsRenderPayload) {
        currentPayload = payload
        selectedTabIndex = 0

        // Build toolbar identifiers from tabs
        tabIdentifiers = payload.tabs.enumerated().map { index, _ in
            NSToolbarItem.Identifier("settingsTab.\(index)")
        }
        tabsByIdentifier = [:]
        for (index, tab) in payload.tabs.enumerated() {
            tabsByIdentifier[tabIdentifiers[index]] = tab
        }

        if window == nil {
            createWindow(
                width: payload.width ?? 450,
                height: payload.height ?? 350,
                title: payload.title ?? "Settings"
            )
        }

        // Set up toolbar if there are multiple tabs
        if payload.tabs.count > 1 {
            setupToolbar()
        }

        updateContent()
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
        window.toolbarStyle = .preference
        window.delegate = self
        window.center()
        window.isReleasedWhenClosed = false
        self.window = window
    }

    private func setupToolbar() {
        let toolbar = NSToolbar(identifier: "SettingsToolbar")
        toolbar.delegate = self
        toolbar.displayMode = .iconAndLabel
        toolbar.allowsUserCustomization = false
        if !tabIdentifiers.isEmpty {
            toolbar.selectedItemIdentifier = tabIdentifiers[selectedTabIndex]
        }
        window?.toolbar = toolbar
        // Show the selected tab title in the window title bar
        if let tabs = currentPayload?.tabs, !tabs.isEmpty {
            window?.title = tabs[selectedTabIndex].title
        }
    }

    private func updateContent() {
        guard let tabs = currentPayload?.tabs else { return }
        let index = min(selectedTabIndex, tabs.count - 1)

        if let content = tabs[index].content {
            let contentView = SettingsTabContentView(
                node: content,
                onEvent: { [weak self] nodeId, event in
                    self?.onEvent?(nodeId, event)
                }
            )
            window?.contentView = NSHostingView(rootView: contentView)
        }

        // Update window title to selected tab name (for multi-tab)
        if tabs.count > 1 {
            window?.title = tabs[index].title
        }
    }

    @objc private func toolbarItemTapped(_ sender: NSToolbarItem) {
        guard let index = tabIdentifiers.firstIndex(of: sender.itemIdentifier) else { return }
        selectedTabIndex = index
        window?.toolbar?.selectedItemIdentifier = sender.itemIdentifier
        updateContent()
    }

    // MARK: - NSToolbarDelegate

    func toolbar(
        _ toolbar: NSToolbar,
        itemForItemIdentifier itemIdentifier: NSToolbarItem.Identifier,
        willBeInsertedIntoToolbar flag: Bool
    ) -> NSToolbarItem? {
        guard let tab = tabsByIdentifier[itemIdentifier] else { return nil }

        let item = NSToolbarItem(itemIdentifier: itemIdentifier)
        item.label = tab.title
        item.target = self
        item.action = #selector(toolbarItemTapped(_:))

        if let iconName = tab.icon, let image = NSImage(systemSymbolName: iconName, accessibilityDescription: tab.title) {
            item.image = image
        } else {
            // Fallback icon
            item.image = NSImage(systemSymbolName: "gearshape", accessibilityDescription: tab.title)
        }

        return item
    }

    func toolbarAllowedItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        return tabIdentifiers
    }

    func toolbarDefaultItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        return tabIdentifiers
    }

    func toolbarSelectableItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        return tabIdentifiers
    }

    // MARK: - NSWindowDelegate

    func windowWillClose(_ notification: Notification) {
        debugPrint("Settings window closed")
    }
}

/// SwiftUI view for a single settings tab's content
struct SettingsTabContentView: View {
    let node: ViewNode
    let onEvent: (String, String) -> Void

    var body: some View {
        DynamicView(node: node, onEvent: onEvent)
            .padding()
    }
}
