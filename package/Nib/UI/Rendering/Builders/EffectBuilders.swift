import SwiftUI
import AppKit

// MARK: - Visual Effect Blur Builder

extension DynamicView {
    @ViewBuilder
    func buildVisualEffectBlur() -> some View {
        let material = node.props.material ?? "popover"
        let blendingMode = node.props.blendingMode ?? "behindWindow"
        let isEmphasized = node.props.isEmphasized ?? false
        let cornerRadius = node.props.cornerRadius

        VisualEffectBlurView(
            material: parseMaterial(material),
            blendingMode: parseBlendingMode(blendingMode),
            isEmphasized: isEmphasized,
            cornerRadius: cornerRadius
        )
    }

    private func parseMaterial(_ material: String) -> NSVisualEffectView.Material {
        switch material {
        case "headerView": return .headerView
        case "menu": return .menu
        case "popover": return .popover
        case "sidebar": return .sidebar
        case "fullScreenUI": return .fullScreenUI
        case "hud": return .hudWindow
        case "sheet": return .sheet
        case "windowBackground": return .windowBackground
        case "contentBackground": return .contentBackground
        case "underWindowBackground": return .underWindowBackground
        case "underPageBackground": return .underPageBackground
        case "titlebar": return .titlebar
        case "selection": return .selection
        case "tooltip": return .popover  // tooltip not available, use popover
        case "ultraThin": return .hudWindow
        case "thin": return .popover
        case "regular": return .contentBackground
        case "thick": return .sidebar
        case "ultraThick": return .headerView
        default: return .popover
        }
    }

    private func parseBlendingMode(_ mode: String) -> NSVisualEffectView.BlendingMode {
        switch mode {
        case "behindWindow": return .behindWindow
        case "withinWindow": return .withinWindow
        default: return .behindWindow
        }
    }
}

// MARK: - Visual Effect Blur View

struct VisualEffectBlurView: NSViewRepresentable {
    let material: NSVisualEffectView.Material
    let blendingMode: NSVisualEffectView.BlendingMode
    let isEmphasized: Bool
    let cornerRadius: CGFloat?

    func makeNSView(context: Context) -> NSVisualEffectView {
        let view = NSVisualEffectView()
        view.material = material
        view.blendingMode = blendingMode
        view.isEmphasized = isEmphasized
        view.state = .active
        if let radius = cornerRadius {
            view.wantsLayer = true
            view.layer?.cornerRadius = radius
            view.layer?.masksToBounds = true
        }
        return view
    }

    func updateNSView(_ nsView: NSVisualEffectView, context: Context) {
        nsView.material = material
        nsView.blendingMode = blendingMode
        nsView.isEmphasized = isEmphasized
        if let radius = cornerRadius {
            nsView.wantsLayer = true
            nsView.layer?.cornerRadius = radius
            nsView.layer?.masksToBounds = true
        }
    }
}
