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
        // Delegate to buildRectangle - both Rectangle and RoundedRectangle now use the same logic
        buildRectangle()
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

    /// Get the corner radii for rectangle shapes
    private var rectangleCornerRadii: RectangleCornerRadii {
        // Per-corner radii takes precedence
        if let radii = node.props.cornerRadii {
            return RectangleCornerRadii(
                topLeading: radii.topLeading,
                bottomLeading: radii.bottomLeading,
                bottomTrailing: radii.bottomTrailing,
                topTrailing: radii.topTrailing
            )
        }
        // Fall back to uniform corner radius
        if let radius = node.props.cornerRadius {
            return RectangleCornerRadii(
                topLeading: radius,
                bottomLeading: radius,
                bottomTrailing: radius,
                topTrailing: radius
            )
        }
        // Default: no rounding
        return RectangleCornerRadii(
            topLeading: 0,
            bottomLeading: 0,
            bottomTrailing: 0,
            topTrailing: 0
        )
    }

    @ViewBuilder
    func buildRectangle() -> some View {
        let radii = rectangleCornerRadii
        let strokeColor = node.props.stroke.map { Color(nibColor: $0) }
        let strokeWidth = node.props.strokeWidth ?? 1.0

        if let args = fillModifierArgs, let gradientType = args.gradientType {
            let grad = gradientFromArgs(args)
            switch gradientType {
            case "LinearGradient":
                let start = unitPointFromArgs(args.startPoint, default: UnitPoint(x: 0.5, y: 0))
                let end = unitPointFromArgs(args.endPoint, default: UnitPoint(x: 0.5, y: 1))
                buildRectangleWithFill(radii: radii, fill: LinearGradient(gradient: grad, startPoint: start, endPoint: end), strokeColor: strokeColor, strokeWidth: strokeWidth)
            case "RadialGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                buildRectangleWithFill(radii: radii, fill: RadialGradient(gradient: grad, center: center, startRadius: args.startRadius ?? 0, endRadius: args.endRadius ?? 100), strokeColor: strokeColor, strokeWidth: strokeWidth)
            case "AngularGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                buildRectangleWithFill(radii: radii, fill: AngularGradient(gradient: grad, center: center, startAngle: .degrees(args.startAngle ?? 0), endAngle: .degrees(args.endAngle ?? 360)), strokeColor: strokeColor, strokeWidth: strokeWidth)
            case "EllipticalGradient":
                let center = unitPointFromArgs(args.center, default: .center)
                buildRectangleWithFill(radii: radii, fill: EllipticalGradient(gradient: grad, center: center, startRadiusFraction: args.startRadiusFraction ?? 0, endRadiusFraction: args.endRadiusFraction ?? 0.5), strokeColor: strokeColor, strokeWidth: strokeWidth)
            default:
                buildRectangleWithFill(radii: radii, fill: fillColor ?? Color.clear, strokeColor: strokeColor, strokeWidth: strokeWidth)
            }
        } else {
            buildRectangleWithFill(radii: radii, fill: fillColor ?? Color.clear, strokeColor: strokeColor, strokeWidth: strokeWidth)
        }
    }

    @ViewBuilder
    private func buildRectangleWithFill<F: ShapeStyle>(radii: RectangleCornerRadii, fill: F, strokeColor: Color?, strokeWidth: Double) -> some View {
        // Note: Can't chain .fill() and .stroke() on a Shape directly - use overlay
        if let strokeColor = strokeColor {
            UnevenRoundedRectangle(cornerRadii: radii)
                .fill(fill)
                .overlay(
                    UnevenRoundedRectangle(cornerRadii: radii)
                        .stroke(strokeColor, lineWidth: CGFloat(strokeWidth))
                )
        } else {
            UnevenRoundedRectangle(cornerRadii: radii)
                .fill(fill)
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

    // MARK: - Custom Shape Builder
    // TODO: Enable when Shape primitive is fully implemented
    /*
    @ViewBuilder
    func buildShape() -> some View {
        let operations = node.props.pathOperations ?? []
        let viewBox = node.props.viewBox
        let strokeColor = node.props.stroke.map { Color(nibColor: $0) }
        let strokeWidth = node.props.strokeWidth ?? 1.0

        // Check for gradient fill first
        if let gradientConfig = node.props.fillGradient {
            let shape = CustomShape(operations: operations, viewBox: viewBox)
            buildShapeWithGradient(shape: shape, gradient: gradientConfig, strokeColor: strokeColor, strokeWidth: strokeWidth)
        } else {
            // Simple color fill
            let shapeFillColor: Color? = {
                if let fill = node.props.fill {
                    return Color(nibColor: fill)
                }
                return fillColor
            }()

            if let strokeColor = strokeColor {
                CustomShape(operations: operations, viewBox: viewBox)
                    .fill(shapeFillColor ?? Color.clear)
                    .stroke(strokeColor, lineWidth: CGFloat(strokeWidth))
            } else {
                CustomShape(operations: operations, viewBox: viewBox)
                    .fill(shapeFillColor ?? Color.clear)
            }
        }
    }
    */

    /*
    @ViewBuilder
    private func buildShapeWithGradient<S: Shape>(shape: S, gradient: ShapeGradient, strokeColor: Color?, strokeWidth: Double) -> some View {
        let grad = shapeGradient(from: gradient)

        switch gradient.type {
        case "LinearGradient":
            let start = shapeUnitPoint(from: gradient.startPoint, default: UnitPoint(x: 0.5, y: 0))
            let end = shapeUnitPoint(from: gradient.endPoint, default: UnitPoint(x: 0.5, y: 1))
            if let strokeColor = strokeColor {
                shape.fill(LinearGradient(gradient: grad, startPoint: start, endPoint: end))
                    .stroke(strokeColor, lineWidth: CGFloat(strokeWidth))
            } else {
                shape.fill(LinearGradient(gradient: grad, startPoint: start, endPoint: end))
            }

        case "RadialGradient":
            let center = shapeUnitPoint(from: gradient.center, default: .center)
            let startRadius = gradient.startRadius ?? 0
            let endRadius = gradient.endRadius ?? 100
            if let strokeColor = strokeColor {
                shape.fill(RadialGradient(gradient: grad, center: center, startRadius: startRadius, endRadius: endRadius))
                    .stroke(strokeColor, lineWidth: CGFloat(strokeWidth))
            } else {
                shape.fill(RadialGradient(gradient: grad, center: center, startRadius: startRadius, endRadius: endRadius))
            }

        case "AngularGradient":
            let center = shapeUnitPoint(from: gradient.center, default: .center)
            let startAngle = Angle(degrees: gradient.startAngle ?? 0)
            let endAngle = Angle(degrees: gradient.endAngle ?? 360)
            if let strokeColor = strokeColor {
                shape.fill(AngularGradient(gradient: grad, center: center, startAngle: startAngle, endAngle: endAngle))
                    .stroke(strokeColor, lineWidth: CGFloat(strokeWidth))
            } else {
                shape.fill(AngularGradient(gradient: grad, center: center, startAngle: startAngle, endAngle: endAngle))
            }

        case "EllipticalGradient":
            let center = shapeUnitPoint(from: gradient.center, default: .center)
            let startFraction = gradient.startRadiusFraction ?? 0
            let endFraction = gradient.endRadiusFraction ?? 0.5
            if let strokeColor = strokeColor {
                shape.fill(EllipticalGradient(gradient: grad, center: center, startRadiusFraction: startFraction, endRadiusFraction: endFraction))
                    .stroke(strokeColor, lineWidth: CGFloat(strokeWidth))
            } else {
                shape.fill(EllipticalGradient(gradient: grad, center: center, startRadiusFraction: startFraction, endRadiusFraction: endFraction))
            }

        default:
            shape.fill(Color.clear)
        }
    }

    private func shapeGradient(from config: ShapeGradient) -> Gradient {
        if let colors = config.colors {
            let swiftColors = colors.map { Color(nibColor: $0) }
            return Gradient(colors: swiftColors)
        }
        return Gradient(colors: [.clear])
    }

    private func shapeUnitPoint(from array: [Double]?, default defaultPoint: UnitPoint) -> UnitPoint {
        guard let arr = array, arr.count >= 2 else { return defaultPoint }
        return UnitPoint(x: arr[0], y: arr[1])
    }
    */
}

// MARK: - Custom Shape
// TODO: Enable when Shape primitive is fully implemented
/*
/// A SwiftUI Shape that renders from path operations.
/// Supports scaling via viewBox to fit any size.
struct CustomShape: Shape {
    let operations: [PathOperation]
    let viewBox: ViewBox?

    func path(in rect: CGRect) -> Path {
        var path = Path()

        // Calculate scaling if viewBox is provided
        let scaleX: CGFloat
        let scaleY: CGFloat
        let offsetX: CGFloat
        let offsetY: CGFloat

        if let vb = viewBox {
            let scale = min(rect.width / CGFloat(vb.w), rect.height / CGFloat(vb.h))
            scaleX = scale
            scaleY = scale
            offsetX = (rect.width - CGFloat(vb.w) * scale) / 2 + rect.minX
            offsetY = (rect.height - CGFloat(vb.h) * scale) / 2 + rect.minY
        } else {
            scaleX = 1
            scaleY = 1
            offsetX = rect.minX
            offsetY = rect.minY
        }

        func point(_ x: Double, _ y: Double) -> CGPoint {
            CGPoint(x: CGFloat(x) * scaleX + offsetX, y: CGFloat(y) * scaleY + offsetY)
        }

        for op in operations {
            switch op.op {
            case "move":
                if let x = op.x, let y = op.y {
                    path.move(to: point(x, y))
                }

            case "line":
                if let x = op.x, let y = op.y {
                    path.addLine(to: point(x, y))
                }

            case "curve":
                if let x = op.x, let y = op.y,
                   let c1x = op.c1x, let c1y = op.c1y,
                   let c2x = op.c2x, let c2y = op.c2y {
                    path.addCurve(
                        to: point(x, y),
                        control1: point(c1x, c1y),
                        control2: point(c2x, c2y)
                    )
                }

            case "quad":
                if let x = op.x, let y = op.y,
                   let cx = op.cx, let cy = op.cy {
                    path.addQuadCurve(to: point(x, y), control: point(cx, cy))
                }

            case "arc":
                if let cx = op.cx, let cy = op.cy,
                   let radius = op.radius,
                   let start = op.startAngle,
                   let end = op.endAngle {
                    let clockwise = op.clockwise ?? true
                    path.addArc(
                        center: point(cx, cy),
                        radius: CGFloat(radius) * scaleX,
                        startAngle: .radians(start),
                        endAngle: .radians(end),
                        clockwise: !clockwise  // SwiftUI uses opposite convention
                    )
                }

            case "close":
                path.closeSubpath()

            case "rect":
                if let x = op.x, let y = op.y, let w = op.w, let h = op.h {
                    path.addRect(CGRect(
                        x: CGFloat(x) * scaleX + offsetX,
                        y: CGFloat(y) * scaleY + offsetY,
                        width: CGFloat(w) * scaleX,
                        height: CGFloat(h) * scaleY
                    ))
                }

            case "roundedRect":
                if let x = op.x, let y = op.y, let w = op.w, let h = op.h {
                    let cr = op.cornerRadius ?? 0
                    path.addRoundedRect(
                        in: CGRect(
                            x: CGFloat(x) * scaleX + offsetX,
                            y: CGFloat(y) * scaleY + offsetY,
                            width: CGFloat(w) * scaleX,
                            height: CGFloat(h) * scaleY
                        ),
                        cornerSize: CGSize(
                            width: CGFloat(cr) * scaleX,
                            height: CGFloat(cr) * scaleY
                        )
                    )
                }

            case "ellipse":
                if let x = op.x, let y = op.y, let w = op.w, let h = op.h {
                    path.addEllipse(in: CGRect(
                        x: CGFloat(x) * scaleX + offsetX,
                        y: CGFloat(y) * scaleY + offsetY,
                        width: CGFloat(w) * scaleX,
                        height: CGFloat(h) * scaleY
                    ))
                }

            case "circle":
                if let cx = op.cx, let cy = op.cy, let r = op.r {
                    let scaledR = CGFloat(r) * scaleX
                    path.addEllipse(in: CGRect(
                        x: CGFloat(cx) * scaleX + offsetX - scaledR,
                        y: CGFloat(cy) * scaleY + offsetY - scaledR,
                        width: scaledR * 2,
                        height: scaledR * 2
                    ))
                }

            default:
                break
            }
        }

        return path
    }
}
*/
