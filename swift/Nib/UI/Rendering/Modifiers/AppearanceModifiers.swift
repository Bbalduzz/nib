import SwiftUI

// MARK: - Appearance Modifiers

extension View {
    @ViewBuilder
    func applyBackground(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let colorName = args.color {
            self.background(Color(nibColor: colorName))
        } else {
            self
        }
    }

    @ViewBuilder
    func applyForegroundColor(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let colorName = args.color {
            self.foregroundColor(Color(nibColor: colorName))
        } else {
            self
        }
    }

    @ViewBuilder
    func applyFill(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let colorName = args.color {
            // For shapes - uses foregroundColor as SwiftUI handles fill via foreground
            self.foregroundColor(Color(nibColor: colorName))
        } else {
            self
        }
    }

    @ViewBuilder
    func applyStroke(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let colorName = args.color {
            // Simplified stroke - proper stroke requires shape-specific handling
            self.foregroundColor(Color(nibColor: colorName))
        } else {
            self
        }
    }

    @ViewBuilder
    func applyOpacity(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let opacity = args.opacity {
            self.opacity(opacity)
        } else {
            self
        }
    }
}
