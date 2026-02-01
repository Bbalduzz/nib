import SwiftUI

struct NibLogoShape: Shape {
    /// thanks claude :)))
    func path(in rect: CGRect) -> Path {
        let w = rect.width
        let h = rect.height

        // Scale factors based on original viewBox (349 x 447)
        let scaleX = w / 349.0
        let scaleY = h / 447.0

        var path = Path()

        // MARK: - Pentagon/Nib Shape (top)
        // Transformed from original path with matrix(4.166667,0,0,4.166667,659.17,1283.32)
        // then translated by (-699.83, -967.92)

        path.move(to: CGPoint(x: 3.08 * scaleX, y: 159.35 * scaleY))

        path.addLine(to: CGPoint(x: 49.67 * scaleX, y: 305.03 * scaleY))

        path.addCurve(
            to: CGPoint(x: 99.52 * scaleX, y: 341.24 * scaleY),
            control1: CGPoint(x: 56.53 * scaleX, y: 328.42 * scaleY),
            control2: CGPoint(x: 74.29 * scaleX, y: 341.24 * scaleY)
        )

        path.addLine(to: CGPoint(x: 248.85 * scaleX, y: 341.24 * scaleY))

        path.addCurve(
            to: CGPoint(x: 298.69 * scaleX, y: 305.03 * scaleY),
            control1: CGPoint(x: 274.08 * scaleX, y: 341.24 * scaleY),
            control2: CGPoint(x: 291.17 * scaleX, y: 328.42 * scaleY)
        )

        path.addLine(to: CGPoint(x: 345.29 * scaleX, y: 159.35 * scaleY))

        path.addCurve(
            to: CGPoint(x: 326.77 * scaleX, y: 100.56 * scaleY),
            control1: CGPoint(x: 352.82 * scaleX, y: 135.35 * scaleY),
            control2: CGPoint(x: 346.51 * scaleX, y: 115.20 * scaleY)
        )

        path.addLine(to: CGPoint(x: 205.31 * scaleX, y: 11.45 * scaleY))

        path.addCurve(
            to: CGPoint(x: 143.06 * scaleX, y: 11.45 * scaleY),
            control1: CGPoint(x: 184.77 * scaleX, y: -3.81 * scaleY),
            control2: CGPoint(x: 163.60 * scaleX, y: -3.81 * scaleY)
        )

        path.addLine(to: CGPoint(x: 21.59 * scaleX, y: 100.56 * scaleY))

        path.addCurve(
            to: CGPoint(x: 3.08 * scaleX, y: 159.35 * scaleY),
            control1: CGPoint(x: 1.86 * scaleX, y: 115.20 * scaleY),
            control2: CGPoint(x: -4.45 * scaleX, y: 135.35 * scaleY)
        )

        path.closeSubpath()

        // MARK: - Rounded Rectangle (bottom)
        // Transformed from original with matrix(1.091787,0,0,1,-87.30,-32)
        // then translated by (-699.83, -967.92)

        let rectLeft = 61.18 * scaleX
        let rectRight = 287.18 * scaleX
        let rectTop = 357.08 * scaleY
        let rectBottom = 446.08 * scaleY
        let cornerRadius = 22.0 * min(scaleX, scaleY)

        path.move(to: CGPoint(x: rectRight, y: rectTop + cornerRadius))

        // Right edge going down
        path.addLine(to: CGPoint(x: rectRight, y: rectBottom - cornerRadius))

        // Bottom-right corner
        path.addCurve(
            to: CGPoint(x: rectRight - cornerRadius, y: rectBottom),
            control1: CGPoint(x: rectRight, y: rectBottom - cornerRadius * 0.45),
            control2: CGPoint(x: rectRight - cornerRadius * 0.45, y: rectBottom)
        )

        // Bottom edge going left
        path.addLine(to: CGPoint(x: rectLeft + cornerRadius, y: rectBottom))

        // Bottom-left corner
        path.addCurve(
            to: CGPoint(x: rectLeft, y: rectBottom - cornerRadius),
            control1: CGPoint(x: rectLeft + cornerRadius * 0.45, y: rectBottom),
            control2: CGPoint(x: rectLeft, y: rectBottom - cornerRadius * 0.45)
        )

        // Left edge going up
        path.addLine(to: CGPoint(x: rectLeft, y: rectTop + cornerRadius))

        // Top-left corner
        path.addCurve(
            to: CGPoint(x: rectLeft + cornerRadius, y: rectTop),
            control1: CGPoint(x: rectLeft, y: rectTop + cornerRadius * 0.45),
            control2: CGPoint(x: rectLeft + cornerRadius * 0.45, y: rectTop)
        )

        // Top edge going right
        path.addLine(to: CGPoint(x: rectRight - cornerRadius, y: rectTop))

        // Top-right corner
        path.addCurve(
            to: CGPoint(x: rectRight, y: rectTop + cornerRadius),
            control1: CGPoint(x: rectRight - cornerRadius * 0.45, y: rectTop),
            control2: CGPoint(x: rectRight, y: rectTop + cornerRadius * 0.45)
        )

        path.closeSubpath()

        return path
    }

    func asNSImage(size: NSSize, color: NSColor = .white) -> NSImage {
        let image = NSImage(size: size, flipped: true) { rect in
            guard let context = NSGraphicsContext.current?.cgContext else { return false }

            let path = self.path(in: rect)
            context.addPath(path.cgPath)
            context.setFillColor(color.cgColor)
            context.fillPath()

            return true
        }
        image.isTemplate = true
        return image
    }
}
