import SwiftUI
import MarkdownUI

// MARK: - Text View Builders

extension DynamicView {
    @ViewBuilder
    func buildText() -> some View {
        // Check for attributed strings first
        if let attributedStrings = node.props.attributedStrings, !attributedStrings.isEmpty {
            let _ = debugPrint("[TextBuilder] Building attributed text with \(attributedStrings.count) segments: \(attributedStrings.map { $0.content })")
            buildAttributedText(attributedStrings)
                .applyTextViewModifiers(node.props.textStyles)
        } else {
            let _ = debugPrint("[TextBuilder] Building plain text: '\(node.props.content ?? "(nil)")'")
            let baseText = Text(node.props.content ?? "")
            baseText.applyTextStyles(node.props.textStyles)
        }
    }

    /// Build rich text from attributed string segments
    private func buildAttributedText(_ segments: [AttributedStringItem]) -> Text {
        segments.reduce(Text("")) { result, segment in
            result + buildStyledTextSegment(segment)
        }
    }

    /// Build a single styled text segment
    private func buildStyledTextSegment(_ segment: AttributedStringItem) -> Text {
        var text = Text(segment.content)

        guard let styles = segment.styles else {
            return text
        }

        // Apply font
        if let fontConfig = styles.font {
            if let fontName = fontConfig.fontName {
                text = text.font(
                    Font.nib(
                        name: fontName,
                        size: fontConfig.fontSize,
                        weight: fontConfig.fontWeight,
                        path: fontConfig.fontPath
                    )
                )
            } else if let fontSize = fontConfig.fontSize {
                // Size without name = system font
                let weight = Font.Weight.nib(fontConfig.fontWeight)
                text = text.font(.system(size: fontSize, weight: weight))
            }
        }

        // Apply color
        if let colorName = styles.color {
            text = text.foregroundColor(Color(nibColor: colorName))
        }

        // Apply text styling
        if styles.bold == true {
            text = text.bold()
        }
        if styles.italic == true {
            text = text.italic()
        }
        if #available(macOS 13.3, *) {
            if styles.monospaced == true {
                text = text.monospaced()
            }
        }
        if styles.monospacedDigit == true {
            text = text.monospacedDigit()
        }

        // Apply decorations
        if styles.strikethrough == true {
            if let colorName = styles.strikethroughColor {
                text = text.strikethrough(true, color: Color(nibColor: colorName))
            } else {
                text = text.strikethrough()
            }
        }
        if styles.underline == true {
            if let colorName = styles.underlineColor {
                text = text.underline(true, color: Color(nibColor: colorName))
            } else {
                text = text.underline()
            }
        }

        // Apply spacing
        if let kerning = styles.kerning {
            text = text.kerning(kerning)
        }
        if let tracking = styles.tracking {
            text = text.tracking(tracking)
        }
        if let baselineOffset = styles.baselineOffset {
            text = text.baselineOffset(baselineOffset)
        }

        return text
    }

    @ViewBuilder
    func buildLabel() -> some View {
        // Check for custom content
        if let children = node.children, !children.isEmpty {
            // Custom label with title and/or icon views
            Label {
                // Find title child (or use first child)
                if let titleChild = children.first(where: { ($0.props.label == nil) || true }) {
                    DynamicView(node: titleChild, onEvent: onEvent)
                }
            } icon: {
                // Find icon child if there are multiple children
                if children.count > 1 {
                    DynamicView(node: children[1], onEvent: onEvent)
                } else {
                    EmptyView()
                }
            }
        } else if let icon = node.props.icon {
            Label(node.props.label ?? "", systemImage: icon)
        } else {
            Label(node.props.label ?? "", systemImage: "questionmark")
        }
    }

    @ViewBuilder
    func buildMarkdown() -> some View {
        let content = node.props.content ?? ""
        let themeName = node.props.theme

        Markdown(content)
            .applyMarkdownTheme(themeName)
    }
}

// MARK: - Markdown Theme

extension View {
    @ViewBuilder
    func applyMarkdownTheme(_ themeName: String?) -> some View {
        if let name = themeName {
            switch name.lowercased() {
            case "github":
                self.markdownTheme(.gitHub)
            case "docc":
                self.markdownTheme(.docC)
            case "basic":
                self.markdownTheme(.basic)
            default:
                self
            }
        } else {
            self
        }
    }
}

// MARK: - Text Styling

extension Text {
    @ViewBuilder
    func applyTextStyles(_ styles: ViewNode.TextStyles?) -> some View {
        if let styles = styles {
            applyTextStylesInternal(styles)
        } else {
            self
        }
    }

    private func applyTextStylesInternal(_ styles: ViewNode.TextStyles) -> some View {
        var text = self

        // Font styling
        if styles.bold == true {
            text = text.bold()
        }
        if styles.italic == true {
            text = text.italic()
        }
        if styles.monospaced == true {
            if #available(macOS 13.3, *) {
                text = text.monospaced()
            }
        }
        if styles.monospacedDigit == true {
            text = text.monospacedDigit()
        }

        // Decorations
        if styles.strikethrough == true {
            if let colorName = styles.strikethroughColor {
                text = text.strikethrough(true, color: Color(nibColor: colorName))
            } else {
                text = text.strikethrough()
            }
        }
        if styles.underline == true {
            if let colorName = styles.underlineColor {
                text = text.underline(true, color: Color(nibColor: colorName))
            } else {
                text = text.underline()
            }
        }

        // Spacing
        if let kerning = styles.kerning {
            text = text.kerning(kerning)
        }
        if let tracking = styles.tracking {
            text = text.tracking(tracking)
        }
        if let baselineOffset = styles.baselineOffset {
            text = text.baselineOffset(baselineOffset)
        }

        // Apply view-level text modifiers
        return text.applyTextViewModifiers(styles)
    }
}

// MARK: - Text View Modifiers

extension View {
    @ViewBuilder
    func applyTextViewModifiers(_ styles: ViewNode.TextStyles?) -> some View {
        if let styles = styles {
            self
                .modifier(TextLayoutModifier(styles: styles))
                .modifier(TextCaseModifier(styles: styles))
        } else {
            self
        }
    }
}

struct TextLayoutModifier: ViewModifier {
    let styles: ViewNode.TextStyles

    func body(content: Content) -> some View {
        content
            .applyLineLimit(styles.lineLimit)
            .applyTruncationMode(styles.truncationMode)
            .applyMinimumScaleFactor(styles.minimumScaleFactor)
            .applyAllowsTightening(styles.allowsTightening)
    }
}

// MARK: - Text Layout Helpers

private extension View {
    @ViewBuilder
    func applyLineLimit(_ limit: Int?) -> some View {
        if let limit = limit {
            self.lineLimit(limit)
        } else {
            self
        }
    }

    @ViewBuilder
    func applyTruncationMode(_ mode: String?) -> some View {
        if let mode = mode {
            self.truncationMode(Text.TruncationMode.nib(mode))
        } else {
            self
        }
    }

    @ViewBuilder
    func applyMinimumScaleFactor(_ factor: CGFloat?) -> some View {
        if let factor = factor {
            self.minimumScaleFactor(factor)
        } else {
            self
        }
    }

    @ViewBuilder
    func applyAllowsTightening(_ allow: Bool?) -> some View {
        if allow == true {
            self.allowsTightening(true)
        } else {
            self
        }
    }
}

struct TextCaseModifier: ViewModifier {
    let styles: ViewNode.TextStyles

    func body(content: Content) -> some View {
        if let textCase = styles.textCase {
            content.textCase(Text.Case.nib(textCase))
        } else {
            content
        }
    }
}

// MARK: - Text Type Conversions

extension Text.TruncationMode {
    static func nib(_ value: String) -> Text.TruncationMode {
        switch value.lowercased() {
        case "head": return .head
        case "middle": return .middle
        case "tail": return .tail
        default: return .tail
        }
    }
}

extension Text.Case {
    static func nib(_ value: String) -> Text.Case? {
        switch value.lowercased() {
        case "uppercase": return .uppercase
        case "lowercase": return .lowercase
        default: return nil
        }
    }
}
