import Foundation
import SwiftUI
import AppKit

// MARK: - SwiftUI Color Parsing

extension Color {
    init(nibColor: String) {
        // Check for opacity suffix (e.g., "red:0.8" or "#FF5733:0.5")
        if let colonIndex = nibColor.lastIndex(of: ":") {
            let colorPart = String(nibColor[..<colonIndex])
            let opacityPart = String(nibColor[nibColor.index(after: colonIndex)...])

            if let opacity = Double(opacityPart) {
                // Parse the color part and apply opacity
                let baseColor = Color.parseBaseColor(colorPart)
                self = baseColor.opacity(opacity)
                return
            }
        }

        // No opacity suffix, parse as regular color
        self = Color.parseBaseColor(nibColor)
    }

    /// Parse a color string without opacity suffix
    private static func parseBaseColor(_ colorString: String) -> Color {
        switch colorString.lowercased() {
        // Basic colors
        case "red": return .red
        case "blue": return .blue
        case "green": return .green
        case "yellow": return .yellow
        case "orange": return .orange
        case "purple": return .purple
        case "pink": return .pink
        case "white": return .white
        case "black": return .black
        case "gray", "grey": return .gray
        case "clear": return .clear

        // Extended colors
        case "indigo": return .indigo
        case "cyan": return .cyan
        case "mint": return .mint
        case "teal": return .teal
        case "brown": return .brown

        // Semantic colors
        case "primary": return .primary
        case "secondary": return .secondary
        case "accentcolor", "accent": return .accentColor

        default:
            // Try hex color
            if colorString.hasPrefix("#") {
                return Color(hex: colorString)
            } else {
                return .primary
            }
        }
    }

    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)

        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }

        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}

// MARK: - Alignment Parsing

extension HorizontalAlignment {
    init(nibAlignment: String?) {
        switch nibAlignment?.lowercased() {
        case "leading": self = .leading
        case "trailing": self = .trailing
        case "center", .none: self = .center
        default: self = .center
        }
    }
}

extension VerticalAlignment {
    init(nibAlignment: String?) {
        switch nibAlignment?.lowercased() {
        case "top": self = .top
        case "bottom": self = .bottom
        case "center", .none: self = .center
        default: self = .center
        }
    }
}

extension Alignment {
    init(nibAlignment: String?) {
        switch nibAlignment?.lowercased() {
        case "topLeading": self = .topLeading
        case "top": self = .top
        case "topTrailing": self = .topTrailing
        case "leading": self = .leading
        case "trailing": self = .trailing
        case "bottomLeading": self = .bottomLeading
        case "bottom": self = .bottom
        case "bottomTrailing": self = .bottomTrailing
        case "center", .none: self = .center
        default: self = .center
        }
    }
}

// MARK: - NSColor Parsing (for menu items)

extension NSColor {
    /// Create NSColor from nib color string (named color, hex, or with opacity suffix)
    static func fromNibColor(_ nibColor: String) -> NSColor {
        // Check for opacity suffix (e.g., "red:0.8" or "#FF5733:0.5")
        var colorString = nibColor
        var opacity: CGFloat = 1.0

        if let colonIndex = nibColor.lastIndex(of: ":") {
            let colorPart = String(nibColor[..<colonIndex])
            let opacityPart = String(nibColor[nibColor.index(after: colonIndex)...])
            if let op = Double(opacityPart) {
                colorString = colorPart
                opacity = CGFloat(op)
            }
        }

        let baseColor = parseBaseColor(colorString)
        return opacity < 1.0 ? baseColor.withAlphaComponent(opacity) : baseColor
    }

    private static func parseBaseColor(_ colorString: String) -> NSColor {
        switch colorString.lowercased() {
        case "red": return .systemRed
        case "blue": return .systemBlue
        case "green": return .systemGreen
        case "yellow": return .systemYellow
        case "orange": return .systemOrange
        case "purple": return .systemPurple
        case "pink": return .systemPink
        case "white": return .white
        case "black": return .black
        case "gray", "grey": return .systemGray
        case "clear": return .clear
        case "indigo": return .systemIndigo
        case "cyan": return .cyan
        case "mint": return .systemMint
        case "teal": return .systemTeal
        case "brown": return .systemBrown
        case "primary": return .labelColor
        case "secondary": return .secondaryLabelColor
        case "accentcolor", "accent": return .controlAccentColor
        default:
            if colorString.hasPrefix("#") {
                return NSColor.fromHex(colorString)
            }
            return .labelColor
        }
    }

    static func fromHex(_ hex: String) -> NSColor {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)

        let a, r, g, b: UInt64
        switch hex.count {
        case 3:
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6:
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8:
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }

        return NSColor(
            red: CGFloat(r) / 255,
            green: CGFloat(g) / 255,
            blue: CGFloat(b) / 255,
            alpha: CGFloat(a) / 255
        )
    }
}

// MARK: - NSImage helpers for SF Symbols

extension NSImage {
    /// Apply a tint color to an SF Symbol image
    func withTintColor(_ color: NSColor) -> NSImage {
        let config = NSImage.SymbolConfiguration(paletteColors: [color])
        return self.withSymbolConfiguration(config) ?? self
    }
}
