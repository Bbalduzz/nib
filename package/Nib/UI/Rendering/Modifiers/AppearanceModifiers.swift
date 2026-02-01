import SwiftUI

// MARK: - Appearance Modifiers

extension View {
    /// Build a Gradient from modifier args
    private func gradientFromModifierArgs(_ args: ViewNode.ViewModifier.ModifierArgs) -> Gradient {
        if let colors = args.colors {
            let swiftColors = colors.map { Color(nibColor: $0) }
            return Gradient(colors: swiftColors)
        }
        return Gradient(colors: [.clear])
    }

    /// Convert [x, y] array to UnitPoint
    private func unitPointFromModifierArgs(_ array: [Double]?, default defaultPoint: UnitPoint) -> UnitPoint {
        guard let arr = array, arr.count >= 2 else { return defaultPoint }
        return UnitPoint(x: arr[0], y: arr[1])
    }

    @ViewBuilder
    func applyBackground(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let gradientType = args.gradientType {
            let grad = gradientFromModifierArgs(args)
            switch gradientType {
            case "LinearGradient":
                let start = unitPointFromModifierArgs(args.startPoint, default: UnitPoint(x: 0.5, y: 0))
                let end = unitPointFromModifierArgs(args.endPoint, default: UnitPoint(x: 0.5, y: 1))
                self.background(LinearGradient(gradient: grad, startPoint: start, endPoint: end))
            case "RadialGradient":
                let center = unitPointFromModifierArgs(args.center, default: .center)
                self.background(RadialGradient(gradient: grad, center: center, startRadius: args.startRadius ?? 0, endRadius: args.endRadius ?? 100))
            case "AngularGradient":
                let center = unitPointFromModifierArgs(args.center, default: .center)
                self.background(AngularGradient(gradient: grad, center: center, startAngle: .degrees(args.startAngle ?? 0), endAngle: .degrees(args.endAngle ?? 360)))
            case "EllipticalGradient":
                let center = unitPointFromModifierArgs(args.center, default: .center)
                self.background(EllipticalGradient(gradient: grad, center: center, startRadiusFraction: args.startRadiusFraction ?? 0, endRadiusFraction: args.endRadiusFraction ?? 0.5))
            default:
                self
            }
        } else if let colorName = args.color {
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
