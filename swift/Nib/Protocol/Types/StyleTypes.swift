import Foundation
import SwiftUI

// MARK: - Style Types

extension ViewNode {
    /// Button-specific styling options
    struct ButtonStyles: Codable, Equatable {
        var role: String?           // "destructive", "cancel"
        var style: String?          // "bordered", "borderedProminent", "borderless", "plain"
        var borderShape: String?    // "automatic", "capsule", "roundedRectangle", "circle"
        var cornerRadius: CGFloat?  // For roundedRectangle shape
        var controlSize: String?    // "mini", "small", "regular", "large", "extraLarge"
        var tint: String?           // Color name or hex
        var disabled: Bool?
        var labelStyle: String?     // "automatic", "iconOnly", "titleOnly", "titleAndIcon"
    }

    /// TextField styling options
    struct TextFieldStyles: Codable, Equatable {
        var style: String?          // "automatic", "plain", "roundedBorder", "squareBorder"
        var disabled: Bool?
        var focused: Bool?
        var autocapitalization: String?  // "none", "words", "sentences", "characters"
        var autocorrection: Bool?
        var keyboardType: String?   // "default", "email", "number", "phone", "url"
        var submitLabel: String?    // "done", "go", "search", "send", "next", "continue"
    }

    /// Toggle styling options
    struct ToggleStyles: Codable, Equatable {
        var style: String?          // "automatic", "switch", "button", "checkbox"
        var tint: String?
        var disabled: Bool?
    }

    /// Slider styling options
    struct SliderStyles: Codable, Equatable {
        var tint: String?
        var disabled: Bool?
    }

    /// Picker styling options
    struct PickerStyles: Codable, Equatable {
        var style: String?          // "automatic", "menu", "segmented", "wheel", "inline"
        var disabled: Bool?
    }

    /// ProgressView styling options
    struct ProgressStyles: Codable, Equatable {
        var style: String?          // "automatic", "linear", "circular"
        var tint: String?
    }

    /// Image styling options
    struct ImageStyles: Codable, Equatable {
        var resizable: Bool?
        var scaledToFit: Bool?
        var scaledToFill: Bool?
        var antialiased: Bool?          // Whether to apply antialiasing (default true)
        var blur: CGFloat?              // Blur radius to apply
        // SF Symbol specific
        var symbolWeight: String?       // "ultraLight" to "black"
        var symbolScale: String?        // "small", "medium", "large"
        var symbolRenderingMode: String? // "monochrome", "hierarchical", "palette", "multicolor"
    }

    /// Video settings
    struct VideoSettings: Codable, Equatable {
        var autoplay: Bool?
        var loop: Bool?
        var muted: Bool?
        var controls: Bool?
        var gravity: String?  // "resizeAspect", "resizeAspectFill", "resize"
    }

    /// Text-specific styling options
    struct TextStyles: Codable, Equatable {
        // Font styling
        var bold: Bool?
        var italic: Bool?
        var monospaced: Bool?
        var monospacedDigit: Bool?

        // Decorations
        var strikethrough: Bool?
        var strikethroughColor: String?
        var underline: Bool?
        var underlineColor: String?

        // Spacing
        var kerning: CGFloat?
        var tracking: CGFloat?
        var baselineOffset: CGFloat?

        // Layout
        var lineLimit: Int?
        var truncationMode: String?
        var minimumScaleFactor: CGFloat?
        var allowsTightening: Bool?

        // Case transformation
        var textCase: String?
    }
}
