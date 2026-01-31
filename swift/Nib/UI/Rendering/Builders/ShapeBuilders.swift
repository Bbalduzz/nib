import SwiftUI

// MARK: - Shape View Builders

extension DynamicView {
    /// Get the fill color from modifiers, or nil if not specified
    private var fillColor: Color? {
        guard let modifiers = node.modifiers else { return nil }
        for modifier in modifiers {
            if modifier.type == .fill, let colorName = modifier.args.color {
                return Color(nibColor: colorName)
            }
        }
        return nil
    }

    /// Get fill modifier args (for gradient detection)
    private var fillModifierArgs: ViewNode.ViewModifier.ModifierArgs? {
        guard let modifiers = node.modifiers else { return nil }
        for modifier in modifiers {
            if modifier.type == .fill {
                return modifier.args
            }
        }
        return nil
    }

    /// Build gradient from modifier args
    private func gradientFromArgs(_ args: ViewNode.ViewModifier.ModifierArgs) -> Gradient {
        // Handle stops - Python sends [[position, colorString], ...]
        // But we also need to handle the simpler case
        if let colors = args.colors {
            let swiftColors = colors.map { Color(nibColor: $0) }
            return Gradient(colors: swiftColors)
        }
        return Gradient(colors: [.clear])
    }

    /// Convert [x, y] array to UnitPoint (for modifiers)
    private func unitPointFromArgs(_ array: [Double]?, default defaultPoint: UnitPoint) -> UnitPoint {
        guard let arr = array, arr.count >= 2 else { return defaultPoint }
        return UnitPoint(x: arr[0], y: arr[1])
    }

    @ViewBuilder
    func buildRoundedRectangle() -> some View {
        if let args = fillModifierArgs, let gradientType = args.gradientType {
            let grad = gradientFromArgs(args)
            switch gradientType {
            case "LinearGradient":
                let start = unitPointFromArgs(args.startPoint, default: UnitPoint(x: 0.5, y: 0))
                let end = unitPointFromArgs(args.endPoint, default: UnitPoint(x: 0.5, y: 1))
                RoundedRectangle(cornerRadius: node.props.cornerRadius ?? 10)
                    .fill(LinearGradient(gradient: grad, startPoint: start, endPoint: end))
            case "RadialGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                RoundedRectangle(cornerRadius: node.props.cornerRadius ?? 10)
                    .fill(RadialGradient(gradient: grad, center: center, startRadius: args.startRadius ?? 0, endRadius: args.endRadius ?? 100))
            case "AngularGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                RoundedRectangle(cornerRadius: node.props.cornerRadius ?? 10)
                    .fill(AngularGradient(gradient: grad, center: center, startAngle: .degrees(args.startAngle ?? 0), endAngle: .degrees(args.endAngle ?? 360)))
            case "EllipticalGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                RoundedRectangle(cornerRadius: node.props.cornerRadius ?? 10)
                    .fill(EllipticalGradient(gradient: grad, center: center, startRadiusFraction: args.startRadiusFraction ?? 0, endRadiusFraction: args.endRadiusFraction ?? 0.5))
            default:
                RoundedRectangle(cornerRadius: node.props.cornerRadius ?? 10)
                    .fill(fillColor ?? Color.clear)
            }
        } else {
            RoundedRectangle(cornerRadius: node.props.cornerRadius ?? 10)
                .fill(fillColor ?? Color.clear)
        }
    }

    @ViewBuilder
    func buildCircle() -> some View {
        let trimFrom = node.props.trimFrom ?? 0.0
        let trimTo = node.props.trimTo ?? 1.0
        let rotation = node.props.rotation ?? 0.0

        if trimFrom != 0.0 || trimTo != 1.0 {
            // Trimmed circle (arc) - typically for progress rings, use stroke style
            Circle()
                .trim(from: trimFrom, to: trimTo)
                .stroke(style: StrokeStyle(lineWidth: 1))
                .rotationEffect(.degrees(rotation - 90))  // -90 to start from top
        } else if let args = fillModifierArgs, let gradientType = args.gradientType {
            let grad = gradientFromArgs(args)
            switch gradientType {
            case "LinearGradient":
                let start = unitPointFromArgs(args.startPoint, default: UnitPoint(x: 0.5, y: 0))
                let end = unitPointFromArgs(args.endPoint, default: UnitPoint(x: 0.5, y: 1))
                Circle().fill(LinearGradient(gradient: grad, startPoint: start, endPoint: end)).rotationEffect(.degrees(rotation))
            case "RadialGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                Circle().fill(RadialGradient(gradient: grad, center: center, startRadius: args.startRadius ?? 0, endRadius: args.endRadius ?? 100)).rotationEffect(.degrees(rotation))
            case "AngularGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                Circle().fill(AngularGradient(gradient: grad, center: center, startAngle: .degrees(args.startAngle ?? 0), endAngle: .degrees(args.endAngle ?? 360))).rotationEffect(.degrees(rotation))
            case "EllipticalGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                Circle().fill(EllipticalGradient(gradient: grad, center: center, startRadiusFraction: args.startRadiusFraction ?? 0, endRadiusFraction: args.endRadiusFraction ?? 0.5)).rotationEffect(.degrees(rotation))
            default:
                Circle().fill(fillColor ?? Color.clear).rotationEffect(.degrees(rotation))
            }
        } else {
            Circle()
                .fill(fillColor ?? Color.clear)
                .rotationEffect(.degrees(rotation))
        }
    }

    @ViewBuilder
    func buildRectangle() -> some View {
        if let args = fillModifierArgs, let gradientType = args.gradientType {
            let grad = gradientFromArgs(args)
            switch gradientType {
            case "LinearGradient":
                let start = unitPointFromArgs(args.startPoint, default: UnitPoint(x: 0.5, y: 0))
                let end = unitPointFromArgs(args.endPoint, default: UnitPoint(x: 0.5, y: 1))
                Rectangle().fill(LinearGradient(gradient: grad, startPoint: start, endPoint: end))
            case "RadialGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                Rectangle().fill(RadialGradient(gradient: grad, center: center, startRadius: args.startRadius ?? 0, endRadius: args.endRadius ?? 100))
            case "AngularGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                Rectangle().fill(AngularGradient(gradient: grad, center: center, startAngle: .degrees(args.startAngle ?? 0), endAngle: .degrees(args.endAngle ?? 360)))
            case "EllipticalGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                Rectangle().fill(EllipticalGradient(gradient: grad, center: center, startRadiusFraction: args.startRadiusFraction ?? 0, endRadiusFraction: args.endRadiusFraction ?? 0.5))
            default:
                Rectangle().fill(fillColor ?? Color.clear)
            }
        } else {
            Rectangle().fill(fillColor ?? Color.clear)
        }
    }

    @ViewBuilder
    func buildEllipse() -> some View {
        if let args = fillModifierArgs, let gradientType = args.gradientType {
            let grad = gradientFromArgs(args)
            switch gradientType {
            case "LinearGradient":
                let start = unitPointFromArgs(args.startPoint, default: UnitPoint(x: 0.5, y: 0))
                let end = unitPointFromArgs(args.endPoint, default: UnitPoint(x: 0.5, y: 1))
                Ellipse().fill(LinearGradient(gradient: grad, startPoint: start, endPoint: end))
            case "RadialGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                Ellipse().fill(RadialGradient(gradient: grad, center: center, startRadius: args.startRadius ?? 0, endRadius: args.endRadius ?? 100))
            case "AngularGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                Ellipse().fill(AngularGradient(gradient: grad, center: center, startAngle: .degrees(args.startAngle ?? 0), endAngle: .degrees(args.endAngle ?? 360)))
            case "EllipticalGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                Ellipse().fill(EllipticalGradient(gradient: grad, center: center, startRadiusFraction: args.startRadiusFraction ?? 0, endRadiusFraction: args.endRadiusFraction ?? 0.5))
            default:
                Ellipse().fill(fillColor ?? Color.clear)
            }
        } else {
            Ellipse().fill(fillColor ?? Color.clear)
        }
    }

    @ViewBuilder
    func buildCapsule() -> some View {
        if let args = fillModifierArgs, let gradientType = args.gradientType {
            let grad = gradientFromArgs(args)
            switch gradientType {
            case "LinearGradient":
                let start = unitPointFromArgs(args.startPoint, default: UnitPoint(x: 0.5, y: 0))
                let end = unitPointFromArgs(args.endPoint, default: UnitPoint(x: 0.5, y: 1))
                Capsule().fill(LinearGradient(gradient: grad, startPoint: start, endPoint: end))
            case "RadialGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                Capsule().fill(RadialGradient(gradient: grad, center: center, startRadius: args.startRadius ?? 0, endRadius: args.endRadius ?? 100))
            case "AngularGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                Capsule().fill(AngularGradient(gradient: grad, center: center, startAngle: .degrees(args.startAngle ?? 0), endAngle: .degrees(args.endAngle ?? 360)))
            case "EllipticalGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                Capsule().fill(EllipticalGradient(gradient: grad, center: center, startRadiusFraction: args.startRadiusFraction ?? 0, endRadiusFraction: args.endRadiusFraction ?? 0.5))
            default:
                Capsule().fill(fillColor ?? Color.clear)
            }
        } else {
            Capsule().fill(fillColor ?? Color.clear)
        }
    }

    // MARK: - Gradient Builders

    /// Convert colors array or stops to SwiftUI Gradient
    private var gradient: Gradient {
        if let stops = node.props.stops {
            let swiftStops = stops.map { stop in
                Gradient.Stop(color: Color(nibColor: stop.color), location: stop.position)
            }
            return Gradient(stops: swiftStops)
        } else if let colors = node.props.colors {
            let swiftColors = colors.map { Color(nibColor: $0) }
            return Gradient(colors: swiftColors)
        }
        return Gradient(colors: [.clear])
    }

    /// Convert [x, y] array to UnitPoint
    private func unitPoint(from array: [Double]?, default defaultPoint: UnitPoint) -> UnitPoint {
        guard let arr = array, arr.count >= 2 else { return defaultPoint }
        return UnitPoint(x: arr[0], y: arr[1])
    }

    @ViewBuilder
    func buildLinearGradient() -> some View {
        let start = unitPoint(from: node.props.startPoint, default: UnitPoint(x: 0.5, y: 0))
        let end = unitPoint(from: node.props.endPoint, default: UnitPoint(x: 0.5, y: 1))

        LinearGradient(gradient: gradient, startPoint: start, endPoint: end)
    }

    @ViewBuilder
    func buildRadialGradient() -> some View {
        let center = unitPoint(from: node.props.center, default: .center)
        let startRadius = node.props.startRadius ?? 0
        let endRadius = node.props.endRadius ?? 100

        RadialGradient(
            gradient: gradient,
            center: center,
            startRadius: startRadius,
            endRadius: endRadius
        )
    }

    @ViewBuilder
    func buildAngularGradient() -> some View {
        let center = unitPoint(from: node.props.center, default: .center)
        let startAngle = Angle(degrees: node.props.startAngle ?? 0)
        let endAngle = Angle(degrees: node.props.endAngle ?? 360)

        AngularGradient(
            gradient: gradient,
            center: center,
            startAngle: startAngle,
            endAngle: endAngle
        )
    }

    @ViewBuilder
    func buildEllipticalGradient() -> some View {
        let center = unitPoint(from: node.props.center, default: .center)
        let startFraction = node.props.startRadiusFraction ?? 0
        let endFraction = node.props.endRadiusFraction ?? 0.5

        EllipticalGradient(
            gradient: gradient,
            center: center,
            startRadiusFraction: startFraction,
            endRadiusFraction: endFraction
        )
    }
}
