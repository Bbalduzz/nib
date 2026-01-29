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

    @ViewBuilder
    func buildRoundedRectangle() -> some View {
        RoundedRectangle(cornerRadius: node.props.cornerRadius ?? 10)
            .fill(fillColor ?? Color.clear)
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
        } else {
            Circle()
                .fill(fillColor ?? Color.clear)
                .rotationEffect(.degrees(rotation))
        }
    }

    @ViewBuilder
    func buildRectangle() -> some View {
        Rectangle()
            .fill(fillColor ?? Color.clear)
    }

    @ViewBuilder
    func buildEllipse() -> some View {
        Ellipse()
            .fill(fillColor ?? Color.clear)
    }

    @ViewBuilder
    func buildCapsule() -> some View {
        Capsule()
            .fill(fillColor ?? Color.clear)
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
