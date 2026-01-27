import SwiftUI

// MARK: - Content Transition Modifiers

extension View {
    /// Apply a content transition modifier for animating content changes
    @ViewBuilder
    func applyContentTransition(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let transitionType = args.transitionType {
            self.contentTransition(ContentTransition.nib(transitionType))
        } else {
            self
        }
    }

    /// Apply a view transition modifier for appearance/disappearance
    @ViewBuilder
    func applyTransition(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let transitionType = args.transitionType {
            self.transition(AnyTransition.nib(transitionType))
        } else {
            self
        }
    }

    /// Apply a blend mode modifier
    @ViewBuilder
    func applyBlendMode(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let mode = args.mode {
            self.blendMode(BlendMode.nib(mode))
        } else {
            self
        }
    }
}

// MARK: - ContentTransition Extension

extension ContentTransition {
    /// Create a ContentTransition from a string type
    static func nib(_ type: String) -> ContentTransition {
        switch type.lowercased() {
        case "identity":
            return .identity
        case "interpolate":
            return .interpolate
        case "numerictext":
            return .numericText(countsDown: false)
        case "numerictextdown":
            return .numericText(countsDown: true)
        case "opacity":
            return .opacity
        default:
            return .identity
        }
    }
}

// MARK: - AnyTransition Extension

extension AnyTransition {
    /// Create an AnyTransition from a string type
    static func nib(_ type: String) -> AnyTransition {
        switch type.lowercased() {
        case "identity":
            return .identity
        case "opacity":
            return .opacity
        case "scale":
            return .scale
        case "slide":
            return .slide
        case "moveleading":
            return .move(edge: .leading)
        case "movetrailing":
            return .move(edge: .trailing)
        case "movetop":
            return .move(edge: .top)
        case "movebottom":
            return .move(edge: .bottom)
        case "push":
            return .push(from: .leading)
        default:
            return .identity
        }
    }
}

// MARK: - BlendMode Extension

extension BlendMode {
    /// Create a BlendMode from a string
    static func nib(_ mode: String) -> BlendMode {
        switch mode.lowercased() {
        case "normal":
            return .normal
        case "multiply":
            return .multiply
        case "screen":
            return .screen
        case "overlay":
            return .overlay
        case "darken":
            return .darken
        case "lighten":
            return .lighten
        case "colordodge":
            return .colorDodge
        case "colorburn":
            return .colorBurn
        case "softlight":
            return .softLight
        case "hardlight":
            return .hardLight
        case "difference":
            return .difference
        case "exclusion":
            return .exclusion
        case "hue":
            return .hue
        case "saturation":
            return .saturation
        case "color":
            return .color
        case "luminosity":
            return .luminosity
        default:
            return .normal
        }
    }
}
