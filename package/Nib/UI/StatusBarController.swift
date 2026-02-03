import AppKit
import SwiftUI

class StatusBarController: NSObject, NSPopoverDelegate {
    private var statusItem: NSStatusItem
    private var popover: NSPopover
    private var viewStore = ViewStore()
    private var eventHandler: ((String, String) -> Void)?
    private var rightClickMenu: NSMenu?
    private var menuItems: [NibMessage.MenuItemConfig] = []
    private var iconHostingView: NSHostingView<AnyView>?
    private var hasPrewarmed = false

    override init() {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        popover = NSPopover()
        popover.behavior = .transient
        popover.animates = true

        super.init()

        popover.delegate = self

        if let button = statusItem.button {
            button.image = NibLogoShape().asNSImage(size: NSSize(width: 15, height: 18))
            button.action = #selector(handleStatusBarClick)
            button.target = self
            button.sendAction(on: [.leftMouseUp, .rightMouseUp])
        }

        // Set up the hosting controller once with the observable store
        let hostingView = NSHostingController(
            rootView: PopoverContentView(store: viewStore)
        )
        popover.contentViewController = hostingView
        // Default size - will be updated by updateWindowSize if specified
        popover.contentSize = NSSize(width: 300, height: 400)

        // NOTE: Prewarm is now deferred until after first content arrives
        // This allows the app to start quickly - prewarm happens in background
    }

    /// Pre-warm SwiftUI rendering to eliminate first-click delay
    /// Called after first content arrives, with a small delay to not block
    private func prewarmPopoverIfNeeded() {
        guard !hasPrewarmed else { return }
        hasPrewarmed = true

        // Delay slightly so the main thread can finish other work first
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) { [weak self] in
            self?.doPrewarm()
        }
    }

    private func doPrewarm() {
        guard let button = statusItem.button else { return }

        // Briefly show popover off-screen to trigger SwiftUI initialization
        popover.animates = false
        popover.show(relativeTo: button.bounds, of: button, preferredEdge: .minY)
        popover.performClose(nil)
        popover.animates = true
        debugPrint("Popover prewarmed")
    }

    func updateWindowSize(width: CGFloat?, height: CGFloat?) {
        if let w = width, let h = height {
            popover.contentSize = NSSize(width: w, height: h)
        } else if let w = width {
            popover.contentSize = NSSize(width: w, height: popover.contentSize.height)
        } else if let h = height {
            popover.contentSize = NSSize(width: popover.contentSize.width, height: h)
        }
    }

    func updateStatusBar(icon: NibMessage.MenuIconConfig?, title: String?) {
        guard let button = statusItem.button else { return }

        // Remove existing hosting view if any
        iconHostingView?.removeFromSuperview()
        iconHostingView = nil

        if let iconConfig = icon {
            switch iconConfig {
            case .view(let viewNode):
                // Embed live SwiftUI view
                button.image = nil
                let swiftUIView = DynamicView(
                    node: viewNode,
                    onEvent: { [weak self] nodeId, event in
                        self?.emitEvent(nodeId: nodeId, event: event)
                    })
                let hostingView = NSHostingView(rootView: AnyView(swiftUIView))

                // Let the view determine its own size
                let fittingSize = hostingView.fittingSize
                let height: CGFloat = 22  // Menu bar height
                let width = max(fittingSize.width, 22)  // Minimum width

                // Update status item length to fit content
                statusItem.length = width

                hostingView.frame = NSRect(x: 0, y: 0, width: width, height: height)
                button.addSubview(hostingView)
                button.frame = hostingView.frame
                iconHostingView = hostingView

            default:
                // SF Symbol or config - use image
                statusItem.length = NSStatusItem.variableLength  // Reset to variable
                button.image = createMenuImage(from: iconConfig)
                if title != nil {
                    button.imagePosition = .imageLeading
                }
            }
        } else {
            statusItem.length = NSStatusItem.variableLength  // Reset to variable
            button.image = nil
        }

        button.title = title ?? ""
    }

    func updateContent(_ node: ViewNode?) {
        debugPrint("StatusBarController.updateContent called, node:", node?.type.rawValue ?? "nil")

        // Extract animation from node tree (Python-defined)
        if let animation = extractAnimation(from: node) {
            withAnimation(animation) {
                viewStore.node = node
            }
        } else {
            viewStore.node = node
        }
        debugPrint("ViewStore updated")

        // Prewarm popover after first content arrives (deferred, non-blocking)
        if node != nil {
            prewarmPopoverIfNeeded()
        }
    }

    /// Recursively extract animation configuration from a node tree
    private func extractAnimation(from node: ViewNode?) -> Animation? {
        guard let node = node else { return nil }

        // Check this node's modifiers
        if let modifiers = node.modifiers {
            for modifier in modifiers {
                if modifier.type == .animation {
                    return Animation.nib(
                        type: modifier.args.animationType ?? "default",
                        duration: modifier.args.animationDuration,
                        delay: modifier.args.animationDelay,
                        response: modifier.args.springResponse,
                        damping: modifier.args.springDamping
                    )
                }
            }
        }

        // Check children recursively
        if let children = node.children {
            for child in children {
                if let animation = extractAnimation(from: child) {
                    return animation
                }
            }
        }

        return nil
    }

    func applyPatches(_ patches: [NibMessage.Patch]) {
        debugPrint("applyPatches called with", patches.count, "patches")
        guard var currentNode = viewStore.node else {
            debugPrint("No current node to patch")
            return
        }

        // Apply each patch
        for patch in patches {
            debugPrint("Applying patch:", patch.op, "to:", patch.id, "props:", patch.props ?? [:])
            currentNode = applyPatch(patch, to: currentNode)
        }

        // Update with animation
        if let animation = extractAnimation(from: currentNode) {
            withAnimation(animation) {
                viewStore.node = currentNode
            }
        } else {
            viewStore.node = currentNode
        }
        debugPrint("Patches applied")
    }

    private func applyPatch(_ patch: NibMessage.Patch, to node: ViewNode) -> ViewNode {
        // If this is the target node
        if node.id == patch.id {
            switch patch.op {
            case "replace":
                return patch.node ?? node
            case "props":
                var updated = node
                if let newProps = patch.props {
                    updated.props = mergeProps(node.props, with: newProps)
                }
                return updated
            case "modifiers":
                var updated = node
                updated.modifiers = patch.modifiers
                return updated
            case "remove":
                // Return a placeholder that will be filtered out
                var updated = node
                updated.id = "__removed__"
                return updated
            default:
                return node
            }
        }

        // Recurse into children
        if let children = node.children {
            // First pass: update existing children recursively
            var updatedChildren = children.compactMap { child -> ViewNode? in
                let updated = applyPatch(patch, to: child)
                return updated.id == "__removed__" ? nil : updated
            }

            // Handle insert at specific position
            if patch.op == "insert", let newNode = patch.node {
                let targetParentId = String(patch.id.dropLast(2))  // Remove ".X" suffix
                if targetParentId == node.id {
                    if let insertIndex = extractIndex(from: patch.id, parentId: node.id),
                        insertIndex <= updatedChildren.count
                    {
                        updatedChildren.insert(newNode, at: insertIndex)
                    } else {
                        updatedChildren.append(newNode)
                    }
                }
            }

            var updated = node
            updated.children = updatedChildren
            return updated
        }

        return node
    }

    private func mergeProps(_ existing: ViewNode.Props, with updates: [String: AnyCodable])
        -> ViewNode.Props
    {
        var props = existing
        for (key, value) in updates {
            switch key {
            // Text
            case "content":
                props.content = value.value as? String

            // TextField / SecureField
            case "text":
                props.text = value.value as? String
            case "placeholder":
                props.placeholder = value.value as? String

            // Toggle
            case "isOn":
                props.isOn = value.value as? Bool

            // Slider
            case "value":
                props.value = value.value as? Double
            case "minValue":
                props.minValue = value.value as? Double
            case "maxValue":
                props.maxValue = value.value as? Double
            case "step":
                props.step = value.value as? Double

            // ProgressView
            case "progress":
                props.progress = value.value as? Double

            // Common
            case "label":
                props.label = value.value as? String
            case "icon":
                props.icon = value.value as? String

            // Stack
            case "spacing":
                if let doubleVal = value.value as? Double {
                    props.spacing = CGFloat(doubleVal)
                } else if let intVal = value.value as? Int {
                    props.spacing = CGFloat(intVal)
                }
            case "alignment":
                props.alignment = value.value as? String

            // Picker
            case "selection":
                props.selection = value.value as? String

            // DisclosureGroup
            case "isExpanded":
                props.isExpanded = value.value as? Bool

            // Shapes
            case "cornerRadius":
                if let doubleVal = value.value as? Double {
                    props.cornerRadius = CGFloat(doubleVal)
                } else if let intVal = value.value as? Int {
                    props.cornerRadius = CGFloat(intVal)
                }

            // Image
            case "sourceType":
                props.sourceType = value.value as? String
            case "sourceValue":
                props.sourceValue = value.value as? String
            case "systemName":
                props.systemName = value.value as? String

            // Link
            case "url":
                props.url = value.value as? String

            default:
                debugPrint("mergeProps: unhandled key '\(key)'")
            }
        }
        return props
    }

    private func extractIndex(from id: String, parentId: String) -> Int? {
        let suffix = String(id.dropFirst(parentId.count + 1))  // Remove "parentId."
        return Int(suffix.split(separator: ".").first ?? "")
    }

    func setEventHandler(_ handler: @escaping (String, String) -> Void) {
        log.info("setEventHandler called")
        eventHandler = handler
        viewStore.onEvent = { [weak self] nodeId, event in
            self?.emitEvent(nodeId: nodeId, event: event)
        }
    }

    private func emitEvent(nodeId: String, event: String) {
        log.info("emitEvent: \(event) for node: \(nodeId), handler is \(eventHandler == nil ? "nil" : "set")")
        eventHandler?(nodeId, event)
        log.info("emitEvent completed")
    }

    // MARK: - NSPopoverDelegate

    func popoverDidClose(_ notification: Notification) {
        debugPrint("Popover closed")
        emitEvent(nodeId: "_app", event: "disappear")
    }

    @objc private func handleStatusBarClick() {
        guard let event = NSApp.currentEvent else {
            togglePopover()
            return
        }

        if event.type == .rightMouseUp {
            showRightClickMenu()
        } else {
            togglePopover()
        }
    }

    private func togglePopover() {
        if popover.isShown {
            popover.performClose(nil)
        } else if let button = statusItem.button {
            popover.show(relativeTo: button.bounds, of: button, preferredEdge: .minY)
            // Make the popover window key to enable keyboard input (Cmd+V, etc.)
            NSApp.activate(ignoringOtherApps: true)
            popover.contentViewController?.view.window?.makeKeyAndOrderFront(nil)
            // Notify Python that the popover appeared
            emitEvent(nodeId: "_app", event: "appear")
        }
    }

    // MARK: - Right-Click Menu

    func updateMenu(_ items: [NibMessage.MenuItemConfig]) {
        log.info("updateMenu called with \(items.count) items")
        menuItems = items
        buildMenu()
    }

    private func buildMenu() {
        log.info("buildMenu called, building \(menuItems.count) items")
        rightClickMenu = buildSubmenu(from: menuItems)
        log.info("rightClickMenu built: \(rightClickMenu?.items.count ?? 0) items")
    }

    private func buildSubmenu(from items: [NibMessage.MenuItemConfig]) -> NSMenu {
        let menu = NSMenu()

        for item in items {
            if item.divider == true {
                menu.addItem(NSMenuItem.separator())
            } else {
                // Parse shortcut into key equivalent and modifiers
                let (keyEquiv, modifiers) = parseShortcut(item.shortcut)

                let menuItem = NSMenuItem(
                    title: item.title ?? "",
                    action: item.children?.isEmpty == false ? nil : #selector(menuItemClicked(_:)),
                    keyEquivalent: keyEquiv
                )
                menuItem.keyEquivalentModifierMask = modifiers
                menuItem.target = self
                menuItem.representedObject = item.id

                // Custom content view (replaces title/icon)
                if let content = item.content {
                    let hostingView = NSHostingView(
                        rootView: MenuItemContentView(node: content) { [weak self] in
                            self?.emitEvent(nodeId: item.id, event: "menu:tap")
                        }
                    )
                    let height = item.height ?? 22
                    hostingView.frame = NSRect(x: 0, y: 0, width: 200, height: height)
                    menuItem.view = hostingView
                } else {
                    // Standard icon
                    if let iconConfig = item.icon {
                        menuItem.image = createMenuImage(from: iconConfig)
                    }
                }

                // State (checkmark) - only for non-custom items
                if item.content == nil, let state = item.state {
                    switch state {
                    case "on": menuItem.state = .on
                    case "mixed": menuItem.state = .mixed
                    default: menuItem.state = .off
                    }
                }

                // Badge (macOS 14+) - only for non-custom items
                if item.content == nil {
                    if #available(macOS 14.0, *) {
                        if let badge = item.badge {
                            menuItem.badge = NSMenuItemBadge(string: badge)
                        }
                    }
                }

                // Enabled state
                if item.enabled == false {
                    menuItem.isEnabled = false
                }

                // Recursively build submenu if children exist
                if let children = item.children, !children.isEmpty {
                    menuItem.submenu = buildSubmenu(from: children)
                }

                menu.addItem(menuItem)
            }
        }

        return menu
    }

    /// Parse shortcut string like "cmd+shift+n" into key equivalent and modifier mask
    private func parseShortcut(_ shortcut: String?) -> (String, NSEvent.ModifierFlags) {
        guard let shortcut = shortcut else { return ("", []) }

        var modifiers: NSEvent.ModifierFlags = []
        var keyEquivalent = ""

        let parts = shortcut.lowercased().split(separator: "+")
        for part in parts {
            switch part {
            case "cmd", "command": modifiers.insert(.command)
            case "shift": modifiers.insert(.shift)
            case "opt", "option", "alt": modifiers.insert(.option)
            case "ctrl", "control": modifiers.insert(.control)
            default: keyEquivalent = String(part)
            }
        }

        return (keyEquivalent, modifiers)
    }

    /// Create NSImage from menu icon configuration
    private func createMenuImage(from iconConfig: NibMessage.MenuIconConfig) -> NSImage? {
        switch iconConfig {
        case .name(let name):
            return NSImage(systemSymbolName: name, accessibilityDescription: name)

        case .view:
            // View icons are handled separately in updateStatusBar via NSHostingView
            return nil

        case .config(let config):
            // Create base image
            guard
                var image = NSImage(
                    systemSymbolName: config.name, accessibilityDescription: config.name)
            else {
                return nil
            }

            // Build and apply symbol configuration
            var symbolConfig = NSImage.SymbolConfiguration(scale: .medium)

            // Weight
            if let weight = config.weight {
                let fontWeight: NSFont.Weight
                switch weight {
                case "ultralight": fontWeight = .ultraLight
                case "thin": fontWeight = .thin
                case "light": fontWeight = .light
                case "regular": fontWeight = .regular
                case "medium": fontWeight = .medium
                case "semibold": fontWeight = .semibold
                case "bold": fontWeight = .bold
                case "heavy": fontWeight = .heavy
                case "black": fontWeight = .black
                default: fontWeight = .regular
                }
                symbolConfig = symbolConfig.applying(.init(pointSize: 0, weight: fontWeight))
            }

            // Scale
            if let scale = config.scale {
                let imageScale: NSImage.SymbolScale
                switch scale {
                case "small": imageScale = .small
                case "large": imageScale = .large
                default: imageScale = .medium
                }
                symbolConfig = symbolConfig.applying(.init(scale: imageScale))
            }

            // Apply base configuration (weight, scale)
            image = image.withSymbolConfiguration(symbolConfig) ?? image

            // Rendering mode and color
            if let renderingMode = config.renderingMode {
                switch renderingMode {
                case "hierarchical":
                    if let colorStr = config.color {
                        let color = NSColor.fromNibColor(colorStr)
                        let hierarchicalConfig = NSImage.SymbolConfiguration(
                            hierarchicalColor: color)
                        image = image.withSymbolConfiguration(hierarchicalConfig) ?? image
                    } else {
                        let hierarchicalConfig = NSImage.SymbolConfiguration(
                            hierarchicalColor: .labelColor)
                        image = image.withSymbolConfiguration(hierarchicalConfig) ?? image
                    }
                case "palette":
                    if let colorStr = config.color {
                        let color = NSColor.fromNibColor(colorStr)
                        let paletteConfig = NSImage.SymbolConfiguration(paletteColors: [
                            color, color.withAlphaComponent(0.5),
                        ])
                        image = image.withSymbolConfiguration(paletteConfig) ?? image
                    }
                case "multicolor":
                    let multicolorConfig = NSImage.SymbolConfiguration.preferringMulticolor()
                    image = image.withSymbolConfiguration(multicolorConfig) ?? image
                default:  // "monochrome"
                    if let colorStr = config.color {
                        let color = NSColor.fromNibColor(colorStr)
                        image = image.withTintColor(color)
                    }
                }
            } else if let colorStr = config.color {
                // No rendering mode specified, just apply color
                let color = NSColor.fromNibColor(colorStr)
                image = image.withTintColor(color)
            }

            return image
        }
    }

    private func showRightClickMenu() {
        log.info("showRightClickMenu called, menuItems: \(menuItems.count), rightClickMenu: \(rightClickMenu?.items.count ?? -1)")
        guard let menu = rightClickMenu, !menuItems.isEmpty else {
            log.info("showRightClickMenu: guard failed - menu is nil or empty")
            return
        }

        if let button = statusItem.button {
            menu.popUp(positioning: nil, at: NSPoint(x: 0, y: button.bounds.height + 5), in: button)
        }
    }

    @objc private func menuItemClicked(_ sender: NSMenuItem) {
        log.info("menuItemClicked called, title: \(sender.title)")
        if let itemId = sender.representedObject as? String {
            log.info("menuItemClicked emitting event for id: \(itemId)")
            emitEvent(nodeId: itemId, event: "menu:tap")
        } else {
            log.info("menuItemClicked: no representedObject found")
        }
    }

    func handleAction(nodeId: String, action: String, params: [String: AnyCodable]?) {
        debugPrint("StatusBarController.handleAction - nodeId:", nodeId, "action:", action)
        ViewActionRegistry.shared.performAction(nodeId: nodeId, action: action, params: params)
    }
}

struct PopoverContentView: View {
    var store: ViewStore  // @Observable tracks access automatically

    var body: some View {
        Group {
            if let node = store.node {
                DynamicView(
                    node: node,
                    onEvent: { nodeId, event in
                        store.onEvent?(nodeId, event)
                    })
            } else {
                VStack {
                    NibLogoShape()
                        .frame(width: 80, height: 102)
                    Text("Nib")
                        .font(.title2)
                        .foregroundColor(.secondary)
                    Text("Waiting for content...")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
        }
        .frame(minWidth: 200, minHeight: 100)
    }
}

/// Wrapper for custom menu item content
struct MenuItemContentView: View {
    let node: ViewNode
    let onTap: () -> Void

    var body: some View {
        DynamicView(node: node, onEvent: { _, _ in })
            .contentShape(Rectangle())
            .onTapGesture {
                onTap()
                NSApp.sendAction(#selector(NSMenu.cancelTracking), to: nil, from: nil)
            }
    }
}
