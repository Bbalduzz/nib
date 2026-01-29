import Foundation
import SwiftUI

// MARK: - View Modifier Types

extension ViewNode {
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

            // Transitions
            var transitionType: String?

            // Blend mode
            var mode: String?

            // Scale
            var scale: CGFloat?
        }
    }
}
