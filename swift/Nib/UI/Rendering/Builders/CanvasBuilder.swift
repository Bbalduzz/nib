import SwiftUI
import AppKit

// MARK: - Canvas View Builder

extension DynamicView {
    @ViewBuilder
    func buildCanvas() -> some View {
        let canvasWidth = node.props.canvasWidth ?? 100
        let canvasHeight = node.props.canvasHeight ?? 100
        let commands = node.props.commands ?? []
        let backgroundColor = node.props.backgroundColor
        let gesturesEnabled = node.props.canvasGestures ?? false

        CanvasNSViewRepresentable(
            nodeId: node.id,
            canvasWidth: CGFloat(canvasWidth),
            canvasHeight: CGFloat(canvasHeight),
            commands: commands,
            backgroundColor: backgroundColor.flatMap { NSColor.fromHex($0) },
            gesturesEnabled: gesturesEnabled,
            onEvent: onEvent
        )
        .frame(width: CGFloat(canvasWidth), height: CGFloat(canvasHeight))
    }
}

// MARK: - Canvas NSViewRepresentable

struct CanvasNSViewRepresentable: NSViewRepresentable {
    let nodeId: String
    let canvasWidth: CGFloat
    let canvasHeight: CGFloat
    let commands: [DrawCommand]
    let backgroundColor: NSColor?
    let gesturesEnabled: Bool
    let onEvent: (String, String) -> Void

    func makeNSView(context: Context) -> CanvasNSView {
        let view = CanvasNSView()
        view.wantsLayer = true
        view.layer?.drawsAsynchronously = true  // GPU acceleration
        view.canvasSize = CGSize(width: canvasWidth, height: canvasHeight)
        view.commands = commands
        view.backgroundColor = backgroundColor
        view.nodeId = nodeId
        view.gesturesEnabled = gesturesEnabled
        view.onEvent = onEvent
        return view
    }

    func updateNSView(_ nsView: CanvasNSView, context: Context) {
        nsView.canvasSize = CGSize(width: canvasWidth, height: canvasHeight)
        nsView.commands = commands
        nsView.backgroundColor = backgroundColor
        nsView.nodeId = nodeId
        nsView.gesturesEnabled = gesturesEnabled
        nsView.onEvent = onEvent
        nsView.setNeedsDisplay(nsView.bounds)
    }
}

// MARK: - Canvas NSView

class CanvasNSView: NSView {
    var canvasSize: CGSize = CGSize(width: 100, height: 100)
    var commands: [DrawCommand] = []
    var backgroundColor: NSColor?
    var nodeId: String = ""
    var gesturesEnabled: Bool = false
    var onEvent: ((String, String) -> Void)?

    // Tracking area for mouse events
    private var trackingArea: NSTrackingArea?

    override var isFlipped: Bool { true }  // Use top-left origin like most graphics systems

    override var acceptsFirstResponder: Bool { gesturesEnabled }

    override func updateTrackingAreas() {
        super.updateTrackingAreas()

        if let existing = trackingArea {
            removeTrackingArea(existing)
        }

        if gesturesEnabled {
            trackingArea = NSTrackingArea(
                rect: bounds,
                options: [.activeInKeyWindow, .mouseMoved, .mouseEnteredAndExited],
                owner: self,
                userInfo: nil
            )
            addTrackingArea(trackingArea!)
        }
    }

    // MARK: - Mouse Events

    override func mouseDown(with event: NSEvent) {
        guard gesturesEnabled else { return }
        let point = convert(event.locationInWindow, from: nil)
        onEvent?(nodeId, "pan:start:\(point.x),\(point.y)")
    }

    override func mouseDragged(with event: NSEvent) {
        guard gesturesEnabled else { return }
        let point = convert(event.locationInWindow, from: nil)
        onEvent?(nodeId, "pan:update:\(point.x),\(point.y)")
    }

    override func mouseUp(with event: NSEvent) {
        guard gesturesEnabled else { return }
        let point = convert(event.locationInWindow, from: nil)
        onEvent?(nodeId, "pan:end:\(point.x),\(point.y)")
    }

    override func mouseMoved(with event: NSEvent) {
        guard gesturesEnabled else { return }
        let point = convert(event.locationInWindow, from: nil)
        onEvent?(nodeId, "hover:\(point.x),\(point.y)")
    }

    // MARK: - Canvas Capture

    func captureImage() -> Data? {
        guard let bitmapRep = bitmapImageRepForCachingDisplay(in: bounds) else { return nil }
        cacheDisplay(in: bounds, to: bitmapRep)
        return bitmapRep.representation(using: .png, properties: [:])
    }

    // MARK: - Drawing

    override func draw(_ dirtyRect: NSRect) {
        guard let ctx = NSGraphicsContext.current?.cgContext else { return }

        // Clear and fill background
        ctx.clear(bounds)
        if let bg = backgroundColor {
            ctx.setFillColor(bg.cgColor)
            ctx.fill(bounds)
        }

        // Draw all commands
        for cmd in commands {
            drawCommand(cmd, in: ctx)
        }
    }

    private func drawCommand(_ cmd: DrawCommand, in ctx: CGContext) {
        ctx.saveGState()

        // Apply opacity if specified
        if let opacity = cmd.opacity, opacity < 1.0 {
            ctx.setAlpha(CGFloat(opacity))
        }

        // Apply blend mode if specified
        if let blendMode = cmd.blendMode {
            ctx.setBlendMode(cgBlendMode(from: blendMode))
        }

        switch cmd.type {
        case "rect":
            drawRect(cmd, in: ctx)
        case "circle":
            drawCircle(cmd, in: ctx)
        case "ellipse":
            drawEllipse(cmd, in: ctx)
        case "line":
            drawLine(cmd, in: ctx)
        case "arc":
            drawArc(cmd, in: ctx)
        case "path":
            drawPath(cmd, in: ctx)
        case "bezierPath":
            drawBezierPath(cmd, in: ctx)
        case "image":
            drawImage(cmd, in: ctx)
        case "text":
            drawText(cmd, in: ctx)
        case "points":
            drawPoints(cmd, in: ctx)
        case "shadow":
            drawShadow(cmd, in: ctx)
        case "fill":
            drawFill(cmd, in: ctx)
        case "colorFill":
            drawColorFill(cmd, in: ctx)
        default:
            break
        }

        ctx.restoreGState()
    }

    // MARK: - Shape Drawing

    private func drawRect(_ cmd: DrawCommand, in ctx: CGContext) {
        guard let x = cmd.x, let y = cmd.y,
              let w = cmd.width, let h = cmd.height else { return }

        let rect = CGRect(x: x, y: y, width: w, height: h)
        let path: CGPath

        if let cr = cmd.cornerRadius, cr > 0 {
            path = CGPath(roundedRect: rect, cornerWidth: CGFloat(cr), cornerHeight: CGFloat(cr), transform: nil)
        } else {
            path = CGPath(rect: rect, transform: nil)
        }

        fillAndStroke(path: path, cmd: cmd, in: ctx)
    }

    private func drawCircle(_ cmd: DrawCommand, in ctx: CGContext) {
        guard let cx = cmd.cx, let cy = cmd.cy, let r = cmd.radius else { return }

        let rect = CGRect(x: cx - r, y: cy - r, width: r * 2, height: r * 2)
        let path = CGPath(ellipseIn: rect, transform: nil)

        fillAndStroke(path: path, cmd: cmd, in: ctx)
    }

    private func drawEllipse(_ cmd: DrawCommand, in ctx: CGContext) {
        guard let cx = cmd.cx, let cy = cmd.cy,
              let rx = cmd.rx, let ry = cmd.ry else { return }

        let rect = CGRect(x: cx - rx, y: cy - ry, width: rx * 2, height: ry * 2)
        let path = CGPath(ellipseIn: rect, transform: nil)

        fillAndStroke(path: path, cmd: cmd, in: ctx)
    }

    private func drawLine(_ cmd: DrawCommand, in ctx: CGContext) {
        guard let x1 = cmd.x1, let y1 = cmd.y1,
              let x2 = cmd.x2, let y2 = cmd.y2 else { return }

        if let strokeHex = cmd.stroke {
            let color = NSColor.fromHex(strokeHex)
            ctx.setStrokeColor(color.cgColor)
        }

        ctx.setLineWidth(CGFloat(cmd.strokeWidth ?? 1))

        // Set line cap
        if let lineCap = cmd.lineCap {
            switch lineCap {
            case "round": ctx.setLineCap(.round)
            case "square": ctx.setLineCap(.square)
            default: ctx.setLineCap(.butt)
            }
        }

        ctx.move(to: CGPoint(x: x1, y: y1))
        ctx.addLine(to: CGPoint(x: x2, y: y2))
        ctx.strokePath()
    }

    private func drawArc(_ cmd: DrawCommand, in ctx: CGContext) {
        guard let cx = cmd.cx, let cy = cmd.cy,
              let r = cmd.radius,
              let startAngle = cmd.startAngle,
              let endAngle = cmd.endAngle else { return }

        let clockwise = cmd.clockwise ?? true

        let path = CGMutablePath()
        path.addArc(
            center: CGPoint(x: cx, y: cy),
            radius: CGFloat(r),
            startAngle: CGFloat(startAngle),
            endAngle: CGFloat(endAngle),
            clockwise: !clockwise  // CGPath uses opposite convention
        )

        fillAndStroke(path: path, cmd: cmd, in: ctx)
    }

    private func drawPath(_ cmd: DrawCommand, in ctx: CGContext) {
        guard let points = cmd.points, points.count >= 2 else { return }

        let path = CGMutablePath()

        for (index, point) in points.enumerated() {
            guard point.count >= 2 else { continue }
            let cgPoint = CGPoint(x: point[0], y: point[1])

            if index == 0 {
                path.move(to: cgPoint)
            } else {
                path.addLine(to: cgPoint)
            }
        }

        if cmd.closed == true {
            path.closeSubpath()
        }

        // Set line join
        if let lineJoin = cmd.lineJoin {
            switch lineJoin {
            case "round": ctx.setLineJoin(.round)
            case "bevel": ctx.setLineJoin(.bevel)
            default: ctx.setLineJoin(.miter)
            }
        }

        fillAndStroke(path: path, cmd: cmd, in: ctx)
    }

    private func drawBezierPath(_ cmd: DrawCommand, in ctx: CGContext) {
        let path = CGMutablePath()

        // Use new elements format if available
        if let elements = cmd.elements, !elements.isEmpty {
            addPathElements(elements, to: path)
        }
        // Fall back to legacy commands format
        else if let commands = cmd.commands, !commands.isEmpty {
            for command in commands {
                switch command {
                case .move(let values):
                    guard values.count >= 2 else { continue }
                    path.move(to: CGPoint(x: values[0], y: values[1]))
                case .line(let values):
                    guard values.count >= 2 else { continue }
                    path.addLine(to: CGPoint(x: values[0], y: values[1]))
                case .curve(let values):
                    guard values.count >= 6 else { continue }
                    path.addCurve(
                        to: CGPoint(x: values[4], y: values[5]),
                        control1: CGPoint(x: values[0], y: values[1]),
                        control2: CGPoint(x: values[2], y: values[3])
                    )
                case .quad(let values):
                    guard values.count >= 4 else { continue }
                    path.addQuadCurve(
                        to: CGPoint(x: values[2], y: values[3]),
                        control: CGPoint(x: values[0], y: values[1])
                    )
                case .close:
                    path.closeSubpath()
                }
            }
        } else {
            return
        }

        fillAndStroke(path: path, cmd: cmd, in: ctx)
    }

    private func addPathElements(_ elements: [PathElement], to path: CGMutablePath) {
        for element in elements {
            switch element.type {
            case "moveTo":
                guard let x = element.x, let y = element.y else { continue }
                path.move(to: CGPoint(x: x, y: y))

            case "lineTo":
                guard let x = element.x, let y = element.y else { continue }
                path.addLine(to: CGPoint(x: x, y: y))

            case "close":
                path.closeSubpath()

            case "cubicTo":
                guard let cp1x = element.cp1x, let cp1y = element.cp1y,
                      let cp2x = element.cp2x, let cp2y = element.cp2y,
                      let x = element.x, let y = element.y else { continue }
                path.addCurve(
                    to: CGPoint(x: x, y: y),
                    control1: CGPoint(x: cp1x, y: cp1y),
                    control2: CGPoint(x: cp2x, y: cp2y)
                )

            case "quadraticTo":
                guard let cp1x = element.cp1x, let cp1y = element.cp1y,
                      let x = element.x, let y = element.y else { continue }
                let weight = element.w ?? 1.0

                if abs(weight - 1.0) < 0.001 {
                    // Standard quadratic bezier
                    path.addQuadCurve(to: CGPoint(x: x, y: y), control: CGPoint(x: cp1x, y: cp1y))
                } else {
                    // Rational quadratic (conic) - approximate with cubic bezier
                    // For weighted quadratic beziers, we convert to cubic
                    addConicCurve(to: path, cp: CGPoint(x: cp1x, y: cp1y),
                                  end: CGPoint(x: x, y: y), weight: weight)
                }

            case "arc":
                guard let x = element.x, let y = element.y,
                      let width = element.width, let height = element.height,
                      let startAngle = element.startAngle,
                      let sweepAngle = element.sweepAngle else { continue }

                let rect = CGRect(x: x, y: y, width: width, height: height)
                let center = CGPoint(x: rect.midX, y: rect.midY)
                let radiusX = width / 2
                let radiusY = height / 2

                // Handle elliptical arc by scaling
                if abs(radiusX - radiusY) < 0.001 {
                    // Circular arc
                    path.addArc(
                        center: center,
                        radius: CGFloat(radiusX),
                        startAngle: CGFloat(startAngle),
                        endAngle: CGFloat(startAngle + sweepAngle),
                        clockwise: sweepAngle < 0
                    )
                } else {
                    // Elliptical arc - use transform
                    var transform = CGAffineTransform.identity
                    transform = transform.translatedBy(x: center.x, y: center.y)
                    transform = transform.scaledBy(x: 1, y: CGFloat(radiusY / radiusX))
                    transform = transform.translatedBy(x: -center.x, y: -center.y)

                    path.addArc(
                        center: center,
                        radius: CGFloat(radiusX),
                        startAngle: CGFloat(startAngle),
                        endAngle: CGFloat(startAngle + sweepAngle),
                        clockwise: sweepAngle < 0,
                        transform: transform
                    )
                }

            case "arcTo":
                guard let x = element.x, let y = element.y,
                      let radius = element.radius else { continue }
                let rotation = element.rotation ?? 0
                let largeArc = element.largeArc ?? false
                let clockwise = element.clockwise ?? true

                // SVG-style arc to point
                addSVGArc(to: path, endX: x, endY: y, radius: radius,
                          rotation: rotation, largeArc: largeArc, clockwise: clockwise)

            case "oval":
                guard let x = element.x, let y = element.y,
                      let width = element.width, let height = element.height else { continue }
                path.addEllipse(in: CGRect(x: x, y: y, width: width, height: height))

            case "rect":
                guard let x = element.x, let y = element.y,
                      let width = element.width, let height = element.height else { continue }

                if let borderRadius = element.borderRadius, borderRadius > 0 {
                    path.addRoundedRect(
                        in: CGRect(x: x, y: y, width: width, height: height),
                        cornerWidth: CGFloat(borderRadius),
                        cornerHeight: CGFloat(borderRadius)
                    )
                } else {
                    path.addRect(CGRect(x: x, y: y, width: width, height: height))
                }

            case "subPath":
                guard let x = element.x, let y = element.y,
                      let subElements = element.elements else { continue }

                // Create sub-path with offset
                let subPath = CGMutablePath()
                addPathElements(subElements, to: subPath)

                var transform = CGAffineTransform(translationX: CGFloat(x), y: CGFloat(y))
                if let transformedPath = subPath.copy(using: &transform) {
                    path.addPath(transformedPath)
                }

            default:
                break
            }
        }
    }

    /// Add a conic (rational quadratic) curve approximated as cubic bezier
    private func addConicCurve(to path: CGMutablePath, cp: CGPoint, end: CGPoint, weight: Double) {
        guard !path.isEmpty else { return }
        let currentPoint = path.currentPoint

        // For conic sections with weight != 1, we approximate using cubic bezier
        // This is a standard conversion formula
        let w = CGFloat(weight)
        let start = currentPoint

        // Convert rational quadratic to cubic bezier control points
        // Using de Casteljau subdivision for weighted curves
        let cp1 = CGPoint(
            x: start.x + (2.0 / 3.0) * w * (cp.x - start.x),
            y: start.y + (2.0 / 3.0) * w * (cp.y - start.y)
        )
        let cp2 = CGPoint(
            x: end.x + (2.0 / 3.0) * w * (cp.x - end.x),
            y: end.y + (2.0 / 3.0) * w * (cp.y - end.y)
        )

        path.addCurve(to: end, control1: cp1, control2: cp2)
    }

    /// Add an SVG-style arc (endpoint parameterization)
    private func addSVGArc(to path: CGMutablePath, endX: Double, endY: Double,
                           radius: Double, rotation: Double, largeArc: Bool, clockwise: Bool) {
        if path.isEmpty {
            path.move(to: CGPoint(x: endX, y: endY))
            return
        }
        let currentPoint = path.currentPoint

        let rx = CGFloat(radius)
        let ry = CGFloat(radius)
        let x1 = currentPoint.x
        let y1 = currentPoint.y
        let x2 = CGFloat(endX)
        let y2 = CGFloat(endY)

        // If radius is 0 or points are the same, draw a line
        if radius == 0 || (abs(x1 - x2) < 0.001 && abs(y1 - y2) < 0.001) {
            path.addLine(to: CGPoint(x: x2, y: y2))
            return
        }

        // Rotation in radians
        let phi = CGFloat(rotation) * .pi / 180

        // Step 1: Compute (x1', y1')
        let cosPhi = cos(phi)
        let sinPhi = sin(phi)
        let dx = (x1 - x2) / 2
        let dy = (y1 - y2) / 2
        let x1p = cosPhi * dx + sinPhi * dy
        let y1p = -sinPhi * dx + cosPhi * dy

        // Correct radii if needed
        var rxSq = rx * rx
        var rySq = ry * ry
        let x1pSq = x1p * x1p
        let y1pSq = y1p * y1p

        let lambda = x1pSq / rxSq + y1pSq / rySq
        var rxCorrected = rx
        var ryCorrected = ry
        if lambda > 1 {
            let sqrtLambda = sqrt(lambda)
            rxCorrected = sqrtLambda * rx
            ryCorrected = sqrtLambda * ry
            rxSq = rxCorrected * rxCorrected
            rySq = ryCorrected * ryCorrected
        }

        // Step 2: Compute (cx', cy')
        var sq = (rxSq * rySq - rxSq * y1pSq - rySq * x1pSq) / (rxSq * y1pSq + rySq * x1pSq)
        sq = max(0, sq)
        let coef = (largeArc != clockwise ? 1 : -1) * sqrt(sq)
        let cxp = coef * rxCorrected * y1p / ryCorrected
        let cyp = -coef * ryCorrected * x1p / rxCorrected

        // Step 3: Compute (cx, cy) from (cx', cy')
        let cx = cosPhi * cxp - sinPhi * cyp + (x1 + x2) / 2
        let cy = sinPhi * cxp + cosPhi * cyp + (y1 + y2) / 2

        // Step 4: Compute angles
        func angle(ux: CGFloat, uy: CGFloat, vx: CGFloat, vy: CGFloat) -> CGFloat {
            let dot = ux * vx + uy * vy
            let len = sqrt(ux * ux + uy * uy) * sqrt(vx * vx + vy * vy)
            var ang = acos(max(-1, min(1, dot / len)))
            if ux * vy - uy * vx < 0 {
                ang = -ang
            }
            return ang
        }

        let theta1 = angle(ux: 1, uy: 0,
                          vx: (x1p - cxp) / rxCorrected,
                          vy: (y1p - cyp) / ryCorrected)

        var dtheta = angle(
            ux: (x1p - cxp) / rxCorrected,
            uy: (y1p - cyp) / ryCorrected,
            vx: (-x1p - cxp) / rxCorrected,
            vy: (-y1p - cyp) / ryCorrected
        )

        if !clockwise && dtheta > 0 {
            dtheta -= 2 * .pi
        } else if clockwise && dtheta < 0 {
            dtheta += 2 * .pi
        }

        // Draw the arc using Core Graphics
        var transform = CGAffineTransform.identity
        transform = transform.translatedBy(x: cx, y: cy)
        transform = transform.rotated(by: phi)
        transform = transform.scaledBy(x: rxCorrected, y: ryCorrected)

        path.addArc(
            center: .zero,
            radius: 1,
            startAngle: theta1,
            endAngle: theta1 + dtheta,
            clockwise: !clockwise,
            transform: transform
        )
    }

    // MARK: - Image Drawing

    private func drawImage(_ cmd: DrawCommand, in ctx: CGContext) {
        // Raw bytes from MessagePack bin type - no base64 decoding needed
        guard let imageData = cmd.data,
              let image = NSImage(data: imageData),
              let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil)
        else { return }

        let x = CGFloat(cmd.x ?? 0)
        let y = CGFloat(cmd.y ?? 0)
        let w = CGFloat(cmd.width ?? Double(cgImage.width))
        let h = CGFloat(cmd.height ?? Double(cgImage.height))

        // CGContext draws images with origin at bottom-left, but we're flipped
        // so we need to flip the image drawing
        ctx.saveGState()
        ctx.translateBy(x: x, y: y + h)
        ctx.scaleBy(x: 1, y: -1)
        ctx.draw(cgImage, in: CGRect(x: 0, y: 0, width: w, height: h))
        ctx.restoreGState()
    }

    // MARK: - Text Drawing

    private func drawText(_ cmd: DrawCommand, in ctx: CGContext) {
        guard let content = cmd.content else { return }

        let x = CGFloat(cmd.x ?? 0)
        let y = CGFloat(cmd.y ?? 0)

        // Build font
        var font = NSFont.systemFont(ofSize: 14)
        if let fontConfig = cmd.font {
            let size = CGFloat(fontConfig.size ?? 14.0)
            if let weight = fontConfig.weight {
                font = NSFont.systemFont(ofSize: size, weight: fontWeight(from: weight))
            } else {
                font = NSFont.systemFont(ofSize: size)
            }
        }

        // Build attributes
        var attributes: [NSAttributedString.Key: Any] = [
            .font: font
        ]

        if let fill = cmd.fill, let colorHex = fill.colorValue {
            let color = NSColor.fromHex(colorHex)
            attributes[.foregroundColor] = color
        }

        // Handle alignment
        let paragraphStyle = NSMutableParagraphStyle()
        switch cmd.alignment {
        case "center": paragraphStyle.alignment = .center
        case "right": paragraphStyle.alignment = .right
        default: paragraphStyle.alignment = .left
        }
        attributes[.paragraphStyle] = paragraphStyle

        // Draw text
        let string = NSAttributedString(string: content, attributes: attributes)
        string.draw(at: CGPoint(x: x, y: y))
    }

    // MARK: - New Primitives

    private func drawPoints(_ cmd: DrawCommand, in ctx: CGContext) {
        guard let points = cmd.points, !points.isEmpty else { return }

        let strokeColor = cmd.stroke.map { NSColor.fromHex($0) } ?? NSColor.black
        ctx.setStrokeColor(strokeColor.cgColor)
        ctx.setFillColor(strokeColor.cgColor)
        ctx.setLineWidth(CGFloat(cmd.strokeWidth ?? 2))

        // Set line cap
        let cap = cmd.effectiveLineCap ?? "round"
        switch cap {
        case "round": ctx.setLineCap(.round)
        case "square": ctx.setLineCap(.square)
        default: ctx.setLineCap(.butt)
        }

        let mode = cmd.pointMode ?? "points"

        switch mode {
        case "points":
            // Draw each point as a small circle
            let radius = CGFloat(cmd.strokeWidth ?? 2) / 2
            for point in points where point.count >= 2 {
                let rect = CGRect(x: point[0] - radius, y: point[1] - radius, width: radius * 2, height: radius * 2)
                ctx.fillEllipse(in: rect)
            }
        case "lines":
            // Draw lines between pairs of points
            var i = 0
            while i + 1 < points.count {
                let p1 = points[i]
                let p2 = points[i + 1]
                if p1.count >= 2 && p2.count >= 2 {
                    ctx.move(to: CGPoint(x: p1[0], y: p1[1]))
                    ctx.addLine(to: CGPoint(x: p2[0], y: p2[1]))
                }
                i += 2
            }
            ctx.strokePath()
        case "polygon":
            // Draw connected line segments
            if let first = points.first, first.count >= 2 {
                ctx.move(to: CGPoint(x: first[0], y: first[1]))
                for point in points.dropFirst() where point.count >= 2 {
                    ctx.addLine(to: CGPoint(x: point[0], y: point[1]))
                }
                ctx.strokePath()
            }
        default:
            break
        }
    }

    private func drawShadow(_ cmd: DrawCommand, in ctx: CGContext) {
        guard let points = cmd.points, !points.isEmpty else { return }

        let elevation = CGFloat(cmd.elevation ?? 5)
        let shadowColor = cmd.color.map { NSColor.fromHex($0) } ?? NSColor.black
        let opacity = CGFloat(cmd.opacity ?? 0.3)

        // Build path from points
        let path = CGMutablePath()
        if let first = points.first, first.count >= 2 {
            path.move(to: CGPoint(x: first[0], y: first[1]))
            for point in points.dropFirst() where point.count >= 2 {
                path.addLine(to: CGPoint(x: point[0], y: point[1]))
            }
            path.closeSubpath()
        }

        // Draw shadow
        ctx.setShadow(
            offset: CGSize(width: 0, height: elevation / 2),
            blur: elevation,
            color: shadowColor.withAlphaComponent(opacity).cgColor
        )
        ctx.addPath(path)
        ctx.setFillColor(NSColor.clear.cgColor)
        ctx.fillPath()
    }

    private func drawFill(_ cmd: DrawCommand, in ctx: CGContext) {
        let rect = bounds

        if let fill = cmd.fill {
            switch fill {
            case .color(let hex):
                let color = NSColor.fromHex(hex)
                ctx.setFillColor(color.cgColor)
                ctx.fill(rect)
            case .gradient(let gradient):
                fillWithGradient(gradient, in: rect, ctx: ctx)
            }
        }
    }

    private func drawColorFill(_ cmd: DrawCommand, in ctx: CGContext) {
        guard let colorHex = cmd.color else { return }

        let color = NSColor.fromHex(colorHex)

        if let blendMode = cmd.blendMode {
            ctx.setBlendMode(cgBlendMode(from: blendMode))
        }

        ctx.setFillColor(color.cgColor)
        ctx.fill(bounds)
    }

    // MARK: - Helpers

    private func fillAndStroke(path: CGPath, cmd: DrawCommand, in ctx: CGContext) {
        ctx.addPath(path)

        if let fill = cmd.fill {
            switch fill {
            case .color(let hex):
                let fillColor = NSColor.fromHex(hex)
                ctx.setFillColor(fillColor.cgColor)
                ctx.fillPath()
            case .gradient(let gradient):
                ctx.saveGState()
                ctx.addPath(path)
                ctx.clip()
                fillWithGradient(gradient, in: path.boundingBox, ctx: ctx)
                ctx.restoreGState()
            }
            ctx.addPath(path)  // Re-add path for stroke
        }

        if let strokeHex = cmd.stroke {
            let strokeColor = NSColor.fromHex(strokeHex)
            ctx.setStrokeColor(strokeColor.cgColor)
            ctx.setLineWidth(CGFloat(cmd.strokeWidth ?? 1))
            ctx.strokePath()
        }
    }

    private func fillWithGradient(_ gradient: GradientConfig, in rect: CGRect, ctx: CGContext) {
        let colors = gradient.colors.map { NSColor.fromHex($0).cgColor }
        guard let cgGradient = CGGradient(
            colorsSpace: CGColorSpaceCreateDeviceRGB(),
            colors: colors as CFArray,
            locations: gradient.stops?.map { CGFloat($0) }
        ) else { return }

        switch gradient.type {
        case "linear":
            let start = gradient.start ?? [0, 0]
            let end = gradient.end ?? [rect.width, rect.height]
            ctx.drawLinearGradient(
                cgGradient,
                start: CGPoint(x: start[0], y: start[1]),
                end: CGPoint(x: end[0], y: end[1]),
                options: [.drawsBeforeStartLocation, .drawsAfterEndLocation]
            )
        case "radial":
            let center = gradient.center ?? [rect.midX, rect.midY]
            let radius = CGFloat(gradient.radius ?? Double(min(rect.width, rect.height) / 2))
            let focus = gradient.focus ?? center
            ctx.drawRadialGradient(
                cgGradient,
                startCenter: CGPoint(x: focus[0], y: focus[1]),
                startRadius: 0,
                endCenter: CGPoint(x: center[0], y: center[1]),
                endRadius: radius,
                options: [.drawsBeforeStartLocation, .drawsAfterEndLocation]
            )
        case "sweep":
            // Sweep/conic gradients require manual drawing
            drawSweepGradient(gradient, in: rect, ctx: ctx)
        default:
            break
        }
    }

    private func drawSweepGradient(_ gradient: GradientConfig, in rect: CGRect, ctx: CGContext) {
        let center = gradient.center ?? [Double(rect.midX), Double(rect.midY)]
        let centerPoint = CGPoint(x: center[0], y: center[1])
        let radius = max(rect.width, rect.height)
        let startAngle = CGFloat(gradient.startAngle ?? 0)
        let endAngle = CGFloat(gradient.endAngle ?? .pi * 2)

        let colors = gradient.colors.map { NSColor.fromHex($0) }
        let stops = gradient.stops ?? colors.enumerated().map { CGFloat($0.offset) / CGFloat(colors.count - 1) }

        // Draw sweep gradient as many thin pie slices
        let segments = 360
        let angleStep = (endAngle - startAngle) / CGFloat(segments)

        for i in 0..<segments {
            let angle = startAngle + CGFloat(i) * angleStep
            let t = CGFloat(i) / CGFloat(segments)

            // Interpolate color
            let color = interpolateColor(colors: colors, stops: stops.map { Double($0) }, t: Double(t))

            ctx.setFillColor(color.cgColor)

            let path = CGMutablePath()
            path.move(to: centerPoint)
            path.addArc(center: centerPoint, radius: radius, startAngle: angle, endAngle: angle + angleStep, clockwise: false)
            path.closeSubpath()

            ctx.addPath(path)
            ctx.fillPath()
        }
    }

    private func interpolateColor(colors: [NSColor], stops: [Double], t: Double) -> NSColor {
        guard colors.count >= 2 else { return colors.first ?? .black }

        // Find the two colors to interpolate between
        var i = 0
        while i < stops.count - 1 && stops[i + 1] < t {
            i += 1
        }
        i = min(i, colors.count - 2)

        let t0 = stops[i]
        let t1 = stops[min(i + 1, stops.count - 1)]
        let localT = t1 > t0 ? (t - t0) / (t1 - t0) : 0

        let c1 = colors[i]
        let c2 = colors[min(i + 1, colors.count - 1)]

        var r1: CGFloat = 0, g1: CGFloat = 0, b1: CGFloat = 0, a1: CGFloat = 0
        var r2: CGFloat = 0, g2: CGFloat = 0, b2: CGFloat = 0, a2: CGFloat = 0

        c1.getRed(&r1, green: &g1, blue: &b1, alpha: &a1)
        c2.getRed(&r2, green: &g2, blue: &b2, alpha: &a2)

        let lt = CGFloat(localT)
        return NSColor(
            red: r1 + (r2 - r1) * lt,
            green: g1 + (g2 - g1) * lt,
            blue: b1 + (b2 - b1) * lt,
            alpha: a1 + (a2 - a1) * lt
        )
    }

    private func cgBlendMode(from string: String) -> CGBlendMode {
        switch string {
        case "multiply": return .multiply
        case "screen": return .screen
        case "overlay": return .overlay
        case "darken": return .darken
        case "lighten": return .lighten
        case "colorDodge": return .colorDodge
        case "colorBurn": return .colorBurn
        case "softLight": return .softLight
        case "hardLight": return .hardLight
        case "difference": return .difference
        case "exclusion": return .exclusion
        case "hue": return .hue
        case "saturation": return .saturation
        case "color": return .color
        case "luminosity": return .luminosity
        case "clear": return .clear
        case "copy": return .copy
        case "sourceIn": return .sourceIn
        case "sourceOut": return .sourceOut
        case "sourceAtop": return .sourceAtop
        case "destinationOver": return .destinationOver
        case "destinationIn": return .destinationIn
        case "destinationOut": return .destinationOut
        case "destinationAtop": return .destinationAtop
        case "xor": return .xor
        case "plusDarker": return .plusDarker
        case "plusLighter": return .plusLighter
        default: return .normal
        }
    }

    private func fontWeight(from string: String) -> NSFont.Weight {
        switch string.lowercased() {
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
