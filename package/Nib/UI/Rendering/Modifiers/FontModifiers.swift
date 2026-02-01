import AppKit
import SwiftUI

// MARK: - Font Modifiers

extension View {
    @ViewBuilder
    func applyFont(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let fontName = args.fontName {
            self.font(Font.nib(name: fontName, size: args.fontSize, weight: args.fontWeight, path: args.fontPath))
        } else if let size = args.fontSize {
            self.font(.system(size: size, weight: Font.Weight.nib(args.fontWeight)))
        } else {
            self
        }
    }
}

// MARK: - Font Helpers

extension Font {
    /// Create a font from Nib font specification
    /// - Parameters:
    ///   - name: Font name (system font name, custom font family name, or registered font name)
    ///   - size: Font size in points
    ///   - weight: Font weight string
    ///   - path: Optional path to custom font file for runtime loading
    static func nib(name: String, size: CGFloat?, weight: String?, path: String? = nil) -> Font {
        // If a path is provided, try to register the custom font
        if let fontPath = path {
            _ = FontManager.shared.registerFont(at: fontPath)
        }

        // Check for system font names first
        switch name.lowercased() {
        case "largetitle": return .largeTitle
        case "title": return .title
        case "title2": return .title2
        case "title3": return .title3
        case "headline": return .headline
        case "subheadline": return .subheadline
        case "body": return .body
        case "callout": return .callout
        case "caption": return .caption
        case "caption2": return .caption2
        case "footnote": return .footnote
        default:
            // Resolve custom font name (handles app.fonts registered names)
            let resolvedName = FontManager.shared.resolvedFontName(name)

            // Try to load as custom font by name
            if let fontSize = size {
                if let nsFont = NSFont(name: resolvedName, size: fontSize) {
                    // Custom font found
                    return Font(nsFont)
                }
                // Also try the original name (for system fonts like "SF Pro")
                if resolvedName != name, let nsFont = NSFont(name: name, size: fontSize) {
                    return Font(nsFont)
                }
                // Fallback to system font with same size
                return .system(size: fontSize, weight: Weight.nib(weight))
            }
            return .body
        }
    }
}

extension Font.Weight {
    /// Convert Nib weight string to Font.Weight
    static func nib(_ weight: String?) -> Font.Weight {
        switch weight?.lowercased() {
        case "ultralight": return .ultraLight
        case "thin": return .thin
        case "light": return .light
        case "regular": return .regular
        case "medium": return .medium
        case "semibold": return .semibold
        case "bold": return .bold
        case "heavy": return .heavy
        case "black": return .black
        default: return .regular
        }
    }
}
