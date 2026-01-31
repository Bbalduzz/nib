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

    /// Apply a view transition modifier for appearance/disappearance.
    /// Supports simple, asymmetric, combined, and custom keyframe transitions.
    @ViewBuilder
    func applyTransition(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let configType = args.transitionConfigType {
            // Enhanced transition config
            switch configType {
            case "asymmetric":
                let insertion = AnyTransition.nib(args.transitionInsertion ?? "opacity")
                let removal = AnyTransition.nib(args.transitionRemoval ?? "opacity")
                self.transition(.asymmetric(insertion: insertion, removal: removal))

            case "combined":
                let combined = (args.transitionList ?? []).reduce(AnyTransition.identity) { result, type in
                    result.combined(with: AnyTransition.nib(type))
                }
                self.transition(combined)

            case "custom":
                if let keyframes = args.customKeyframes, !keyframes.isEmpty {
                    self.transition(AnyTransition.customKeyframes(keyframes))
                } else {
                    self.transition(.opacity)
                }

            case "simple":
                self.transition(AnyTransition.nib(args.transitionValue ?? "identity"))

            default:
                self.transition(AnyTransition.nib(args.transitionValue ?? "identity"))
            }
        } else if let transitionType = args.transitionType {
            // Backwards compatible simple transition
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

    /// Create a custom keyframe-based transition
    static func customKeyframes(_ keyframes: [ViewNode.CustomKeyframe]) -> AnyTransition {
        let parsed = parseKeyframes(keyframes)
        return .modifier(
            active: CustomKeyframeModifier(keyframes: parsed, progress: 0),
            identity: CustomKeyframeModifier(keyframes: parsed, progress: 1)
        )
    }

    private static func parseKeyframes(_ keyframes: [ViewNode.CustomKeyframe]) -> [CustomKeyframeModifier.Keyframe] {
        return keyframes.map { kf in
            CustomKeyframeModifier.Keyframe(
                progress: kf.progress,
                opacity: kf.modifiers?.opacity,
                scale: kf.modifiers?.scale.map { CGFloat($0) },
                blur: kf.modifiers?.blur.map { CGFloat($0) },
                offsetX: kf.modifiers?.offsetX.map { CGFloat($0) },
                offsetY: kf.modifiers?.offsetY.map { CGFloat($0) }
            )
        }.sorted { $0.progress < $1.progress }
    }
}

// MARK: - Custom Keyframe Transition Modifier

/// A ViewModifier that interpolates between keyframes during transitions.
/// Used by custom transitions to animate opacity, scale, blur, and offset.
struct CustomKeyframeModifier: ViewModifier, Animatable {
    let keyframes: [Keyframe]
    var progress: Double

    var animatableData: Double {
        get { progress }
        set { progress = newValue }
    }

    struct Keyframe {
        let progress: Double
        let opacity: Double?
        let scale: CGFloat?
        let blur: CGFloat?
        let offsetX: CGFloat?
        let offsetY: CGFloat?
    }

    func body(content: Content) -> some View {
        let interpolated = interpolate(at: progress)

        content
            .opacity(interpolated.opacity)
            .scaleEffect(interpolated.scale)
            .blur(radius: interpolated.blur)
            .offset(x: interpolated.offsetX, y: interpolated.offsetY)
    }

    private func interpolate(at progress: Double) -> (opacity: Double, scale: CGFloat, blur: CGFloat, offsetX: CGFloat, offsetY: CGFloat) {
        // Default values
        var opacity: Double = 1.0
        var scale: CGFloat = 1.0
        var blur: CGFloat = 0.0
        var offsetX: CGFloat = 0.0
        var offsetY: CGFloat = 0.0

        guard !keyframes.isEmpty else {
            return (opacity, scale, blur, offsetX, offsetY)
        }

        // Find surrounding keyframes
        var lower = keyframes.first!
        var upper = keyframes.last!

        for i in 0..<keyframes.count - 1 {
            if keyframes[i].progress <= progress && keyframes[i + 1].progress >= progress {
                lower = keyframes[i]
                upper = keyframes[i + 1]
                break
            }
        }

        // Calculate interpolation factor
        let range = upper.progress - lower.progress
        let t = range > 0 ? (progress - lower.progress) / range : 1.0

        // Interpolate each property
        opacity = lerp(lower.opacity ?? 1.0, upper.opacity ?? 1.0, t)
        scale = lerp(lower.scale ?? 1.0, upper.scale ?? 1.0, t)
        blur = lerp(lower.blur ?? 0.0, upper.blur ?? 0.0, t)
        offsetX = lerp(lower.offsetX ?? 0.0, upper.offsetX ?? 0.0, t)
        offsetY = lerp(lower.offsetY ?? 0.0, upper.offsetY ?? 0.0, t)

        return (opacity, scale, blur, offsetX, offsetY)
    }

    private func lerp<T: BinaryFloatingPoint>(_ a: T, _ b: T, _ t: Double) -> T {
        return a + T(t) * (b - a)
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
