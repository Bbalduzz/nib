import SwiftUI

// MARK: - Animation Modifiers

extension View {
    @ViewBuilder
    func applyAnimation(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        // Animation is now handled by withAnimation at the ViewStore level
        // This modifier is a no-op; the animation config is extracted and used there
        self
    }

    /// Apply per-view animation context for reactive animations.
    /// When a view has an animationContext, all its property changes animate with this config.
    /// The animation is applied using the node's hash as a value, so it triggers when
    /// the view's content changes.
    @ViewBuilder
    func applyAnimationContext(_ context: ViewNode.AnimationContext?, nodeHash: Int) -> some View {
        if let ctx = context {
            let animation = Animation.nib(
                type: ctx.animationType ?? "default",
                duration: ctx.animationDuration,
                delay: ctx.animationDelay,
                response: ctx.springResponse,
                damping: ctx.springDamping
            )
            // Apply animation using node hash as trigger value
            // This ensures animation fires when the view's content changes
            self.animation(animation, value: nodeHash)
        } else {
            self
        }
    }
}

// MARK: - Animation Helpers

extension Animation {
    /// Create an animation from Nib animation specification
    /// - Parameters:
    ///   - type: Animation type ("linear", "easeIn", "easeOut", "easeInOut", "spring")
    ///   - duration: Animation duration in seconds
    ///   - delay: Animation delay in seconds
    ///   - response: Spring response (for spring animations)
    ///   - damping: Spring damping fraction (for spring animations)
    static func nib(
        type: String,
        duration: Double?,
        delay: Double?,
        response: Double?,
        damping: Double?
    ) -> Animation {
        let dur = duration ?? 0.3

        var animation: Animation

        switch type.lowercased() {
        case "linear":
            animation = .linear(duration: dur)
        case "easein":
            animation = .easeIn(duration: dur)
        case "easeout":
            animation = .easeOut(duration: dur)
        case "easeinout":
            animation = .easeInOut(duration: dur)
        case "spring":
            let springResponse = response ?? 0.3
            let springDamping = damping ?? 0.7
            animation = .spring(response: springResponse, dampingFraction: springDamping)
        default:
            animation = .default
        }

        // Apply delay if specified
        if let delaySeconds = delay, delaySeconds > 0 {
            animation = animation.delay(delaySeconds)
        }

        return animation
    }
}

