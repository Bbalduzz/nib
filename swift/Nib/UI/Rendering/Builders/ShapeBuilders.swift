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
}
