import Foundation
import SwiftUI

// MARK: - View Modifier Types

extension ViewNode {
    /// Custom keyframe for transition animations
    struct CustomKeyframe: Codable, Equatable {
        var progress: Double
        var modifiers: KeyframeModifiers?

        struct KeyframeModifiers: Codable, Equatable {
            var opacity: Double?
            var scale: Double?
            var blur: Double?
            var offsetX: Double?
            var offsetY: Double?
        }
    }

    struct ViewModifier: Codable, Equatable {
        let type: ModifierType
        let args: ModifierArgs

        enum ModifierType: String, Codable, Equatable {
            case frame
            case padding
            case margin
            case background
            case foregroundColor
            case fill
            case stroke
            case font
            case cornerRadius
            case opacity
            case clipShape
            case shadow
            case overlay
            case border
            case animation
            case contentTransition
            case transition
            case blendMode
            case scale
            case offset
        }

        struct ModifierArgs: Codable, Equatable {
            // Frame
            var width: CGFloat?
            var height: CGFloat?
            var maxWidth: String?  // "infinity" for .infinity
            var maxHeight: String?
            var minWidth: CGFloat?
            var minHeight: CGFloat?

            // Padding
            var value: CGFloat?
            var top: CGFloat?
            var leading: CGFloat?
            var bottom: CGFloat?
            var trailing: CGFloat?
            var horizontal: CGFloat?
            var vertical: CGFloat?

            // Colors
            var color: String?

            // Stroke
            var lineWidth: CGFloat?

            // Font
            var fontName: String?
            var fontSize: CGFloat?
            var fontWeight: String?
            var fontPath: String?  // Path to custom font file

            // Opacity
            var opacity: Double?

            // Animation
            var animationType: String?
            var animationDuration: Double?
            var animationDelay: Double?
            var springResponse: Double?
            var springDamping: Double?

            // ClipShape
            var shape: String?  // "capsule", "circle", "roundedRectangle"
            var cornerRadius: CGFloat?

            // Shadow
            var shadowColor: String?
            var shadowRadius: CGFloat?
            var shadowX: CGFloat?
            var shadowY: CGFloat?

            // Border
            var borderColor: String?
            var borderWidth: CGFloat?

            // Transitions (simple)
            var transitionType: String?

            // Enhanced transitions (asymmetric, combined, custom)
            var transitionConfigType: String?  // "simple", "asymmetric", "combined", "custom"
            var transitionValue: String?       // For simple config type
            var transitionInsertion: String?   // For asymmetric
            var transitionRemoval: String?     // For asymmetric
            var transitionList: [String]?      // For combined
            var customKeyframes: [CustomKeyframe]?  // For custom transitions

            // Blend mode
            var mode: String?

            // Scale
            var scale: CGFloat?

            // Offset
            var offsetX: CGFloat?
            var offsetY: CGFloat?

            // Gradient support (for fill/background)
            var gradientType: String?  // "LinearGradient", "RadialGradient", etc.
            var colors: [String]?
            var stops: [[Double]]?  // [[position, color_index], ...] - but we use [position, color_string]
            var startPoint: [Double]?
            var endPoint: [Double]?
            var center: [Double]?
            var startRadius: Double?
            var endRadius: Double?
            var startAngle: Double?
            var endAngle: Double?
            var startRadiusFraction: Double?
            var endRadiusFraction: Double?
        }
    }
}
