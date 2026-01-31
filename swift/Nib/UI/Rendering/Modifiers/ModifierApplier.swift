import SwiftUI
import UniformTypeIdentifiers

// MARK: - Background View Application

extension View {
    /// Apply a background view (any View) instead of just a color
    @ViewBuilder
    func applyBackgroundView(_ backgroundNode: ViewNode?, onEvent: @escaping (String, String) -> Void) -> some View {
        if let bgNode = backgroundNode {
            self.background {
                DynamicView(node: bgNode, onEvent: onEvent)
            }
        } else {
            self
        }
    }

    /// Apply an overlay view (any View)
    @ViewBuilder
    func applyOverlayView(_ overlayNode: ViewNode?, onEvent: @escaping (String, String) -> Void) -> some View {
        if let ovNode = overlayNode {
            self.overlay {
                DynamicView(node: ovNode, onEvent: onEvent)
            }
        } else {
            self
        }
    }
}

// MARK: - Modifier Application

/// Iterative modifier chain using AnyView to avoid exponential type checking
/// For dynamic modifier application, type erasure is acceptable and necessary for fast compilation
struct NibModifierChain: ViewModifier {
    let modifiers: [ViewNode.ViewModifier]

    func body(content: Content) -> some View {
        var result = AnyView(content)
        for modifier in modifiers {
            result = AnyView(result.applySingleModifier(modifier))
        }
        return result
    }
}

extension View {
    /// Apply an array of Nib modifiers to a view (type-preserving)
    @ViewBuilder
    func applyModifiers(_ modifiers: [ViewNode.ViewModifier]?) -> some View {
        if let modifiers = modifiers, !modifiers.isEmpty {
            self.modifier(NibModifierChain(modifiers: modifiers))
        } else {
            self
        }
    }

    /// Apply a single Nib modifier to a view
    @ViewBuilder
    func applySingleModifier(_ modifier: ViewNode.ViewModifier) -> some View {
        switch modifier.type {
        // Layout
        case .frame:
            applyFrame(modifier.args)
        case .padding:
            applyPadding(modifier.args)
        case .margin:
            applyMargin(modifier.args)
        case .cornerRadius:
            applyCornerRadius(modifier.args)
        case .clipShape:
            applyClipShape(modifier.args)
        case .offset:
            applyOffset(modifier.args)

        // Appearance
        case .background:
            applyBackground(modifier.args)
        case .foregroundColor:
            applyForegroundColor(modifier.args)
        case .fill:
            applyFill(modifier.args)
        case .stroke:
            applyStroke(modifier.args)
        case .opacity:
            applyOpacity(modifier.args)
        case .shadow:
            applyShadow(modifier.args)
        case .overlay:
            applyOverlay(modifier.args)
        case .border:
            applyBorder(modifier.args)

        // Typography
        case .font:
            applyFont(modifier.args)

        // Animation
        case .animation:
            applyAnimation(modifier.args)

        // Transitions
        case .contentTransition:
            applyContentTransition(modifier.args)
        case .transition:
            applyTransition(modifier.args)
        case .blendMode:
            applyBlendMode(modifier.args)
        case .scale:
            applyScale(modifier.args)
        }
    }
}

// MARK: - Transform Modifiers

extension View {
    @ViewBuilder
    func applyScale(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let scale = args.scale {
            self.scaleEffect(scale)
        } else {
            self
        }
    }
}

// MARK: - New Modifiers

extension View {
    @ViewBuilder
    func applyClipShape(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let shape = args.shape {
            switch shape.lowercased() {
            case "capsule":
                self.clipShape(Capsule())
            case "circle":
                self.clipShape(Circle())
            case "roundedrectangle":
                let radius = args.cornerRadius ?? 10
                self.clipShape(RoundedRectangle(cornerRadius: radius))
            default:
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    func applyShadow(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        let color = args.shadowColor.map { Color(nibColor: $0) } ?? Color.black.opacity(0.2)
        let radius = args.shadowRadius ?? 4
        let x = args.shadowX ?? 0
        let y = args.shadowY ?? 2

        self.shadow(color: color, radius: radius, x: x, y: y)
    }

    @ViewBuilder
    func applyOverlay(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let colorName = args.color {
            let color = Color(nibColor: colorName)
            if let shape = args.shape {
                switch shape.lowercased() {
                case "capsule":
                    self.overlay(Capsule().stroke(color, lineWidth: args.lineWidth ?? 1))
                case "circle":
                    self.overlay(Circle().stroke(color, lineWidth: args.lineWidth ?? 1))
                case "roundedrectangle":
                    let radius = args.cornerRadius ?? 10
                    self.overlay(RoundedRectangle(cornerRadius: radius).stroke(color, lineWidth: args.lineWidth ?? 1))
                default:
                    self.overlay(color)
                }
            } else {
                self.overlay(color)
            }
        } else {
            self
        }
    }

    @ViewBuilder
    func applyBorder(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        let color = args.borderColor.map { Color(nibColor: $0) } ?? Color.gray
        let width = args.borderWidth ?? 1

        if let shape = args.shape {
            switch shape.lowercased() {
            case "capsule":
                self.overlay(Capsule().stroke(color, lineWidth: width))
            case "circle":
                self.overlay(Circle().stroke(color, lineWidth: width))
            case "roundedrectangle":
                let radius = args.cornerRadius ?? 10
                self.overlay(RoundedRectangle(cornerRadius: radius).stroke(color, lineWidth: width))
            default:
                self.border(color, width: width)
            }
        } else {
            self.border(color, width: width)
        }
    }
}

// MARK: - Drag and Drop

extension View {
    @ViewBuilder
    func applyDropZone(enabled: Bool, nodeId: String, onEvent: @escaping (String, String) -> Void) -> some View {
        if enabled {
            self.onDrop(of: [.fileURL, .url, .text], isTargeted: nil) { providers in
                handleDrop(providers: providers, nodeId: nodeId, onEvent: onEvent)
                return true
            }
        } else {
            self
        }
    }
}

private func handleDrop(providers: [NSItemProvider], nodeId: String, onEvent: @escaping (String, String) -> Void) {
    var paths: [String] = []
    let group = DispatchGroup()

    for provider in providers {
        // Try file URL first
        if provider.hasItemConformingToTypeIdentifier(UTType.fileURL.identifier) {
            group.enter()
            provider.loadItem(forTypeIdentifier: UTType.fileURL.identifier, options: nil) { item, error in
                defer { group.leave() }
                if let data = item as? Data,
                   let url = URL(dataRepresentation: data, relativeTo: nil) {
                    paths.append(url.path)
                } else if let url = item as? URL {
                    paths.append(url.path)
                }
            }
        }
        // Try regular URL
        else if provider.hasItemConformingToTypeIdentifier(UTType.url.identifier) {
            group.enter()
            provider.loadItem(forTypeIdentifier: UTType.url.identifier, options: nil) { item, error in
                defer { group.leave() }
                if let url = item as? URL {
                    paths.append(url.absoluteString)
                }
            }
        }
        // Try text
        else if provider.hasItemConformingToTypeIdentifier(UTType.text.identifier) {
            group.enter()
            provider.loadItem(forTypeIdentifier: UTType.text.identifier, options: nil) { item, error in
                defer { group.leave() }
                if let text = item as? String {
                    paths.append(text)
                }
            }
        }
    }

    group.notify(queue: .main) {
        if !paths.isEmpty {
            let pathsString = paths.joined(separator: "\n")
            onEvent(nodeId, "drop:\(pathsString)")
        }
    }
}
