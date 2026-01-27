import SwiftUI

// MARK: - Control View Builders

extension DynamicView {
    @ViewBuilder
    func buildText() -> some View {
        let baseText = Text(node.props.content ?? "")
        baseText.applyTextStyles(node.props.textStyles)
    }

    @ViewBuilder
    func buildButton() -> some View {
        let styles = node.props.buttonStyles

        // Build button - supports custom content via children or simple label/icon
        let button = Button(role: ButtonRole.nib(styles?.role), action: {
            onEvent(node.id, "tap")
        }) {
            // Check if custom content is provided via children
            if let children = node.children, !children.isEmpty {
                // Render custom content
                ForEach(children) { child in
                    DynamicView(node: child, onEvent: onEvent)
                }
            } else if let icon = node.props.icon {
                // Simple label with icon
                Label(node.props.label ?? "", systemImage: icon)
            } else {
                // Simple text label
                Text(node.props.label ?? "")
            }
        }

        // Apply button styling
        button.applyButtonStyles(styles)
    }

    @ViewBuilder
    func buildTextField() -> some View {
        StatefulTextField(
            placeholder: node.props.placeholder ?? "",
            initialText: node.props.text ?? "",
            styles: node.props.textFieldStyles,
            nodeId: node.id,
            onEvent: onEvent
        )
    }

    @ViewBuilder
    func buildSecureField() -> some View {
        StatefulSecureField(
            placeholder: node.props.placeholder ?? "",
            initialText: node.props.text ?? "",
            styles: node.props.textFieldStyles,
            nodeId: node.id,
            onEvent: onEvent
        )
    }

    @ViewBuilder
    func buildToggle() -> some View {
        // Check for custom content
        if let children = node.children, !children.isEmpty {
            StatefulToggleWithContent(
                isOn: node.props.isOn ?? false,
                styles: node.props.toggleStyles,
                nodeId: node.id,
                onEvent: onEvent
            ) {
                ForEach(children) { child in
                    DynamicView(node: child, onEvent: onEvent)
                }
            }
        } else {
            StatefulToggle(
                label: node.props.label ?? "",
                isOn: node.props.isOn ?? false,
                styles: node.props.toggleStyles,
                nodeId: node.id,
                onEvent: onEvent
            )
        }
    }

    @ViewBuilder
    func buildSlider() -> some View {
        StatefulSlider(
            value: node.props.value ?? 0,
            range: (node.props.minValue ?? 0)...(node.props.maxValue ?? 1),
            step: node.props.step,
            styles: node.props.sliderStyles,
            nodeId: node.id,
            onEvent: onEvent
        )
    }

    @ViewBuilder
    func buildPicker() -> some View {
        StatefulPicker(
            label: node.props.label ?? "",
            selection: node.props.selection ?? "",
            options: node.props.options ?? [],
            styles: node.props.pickerStyles,
            nodeId: node.id,
            onEvent: onEvent
        )
    }

    @ViewBuilder
    func buildDatePicker() -> some View {
        // Placeholder for DatePicker
        Text("DatePicker: Not implemented")
    }

    @ViewBuilder
    func buildStepper() -> some View {
        // Placeholder for Stepper
        Text("Stepper: Not implemented")
    }

    @ViewBuilder
    func buildColorPicker() -> some View {
        // Placeholder for ColorPicker
        Text("ColorPicker: Not implemented")
    }

    @ViewBuilder
    func buildProgressView() -> some View {
        let styles = node.props.progressStyles

        Group {
            if let progress = node.props.progress {
                if let label = node.props.label {
                    ProgressView(label, value: progress)
                } else {
                    ProgressView(value: progress)
                }
            } else {
                if let label = node.props.label {
                    ProgressView(label)
                } else {
                    ProgressView()
                }
            }
        }
        .applyProgressStyles(styles)
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
    func buildLink() -> some View {
        if let urlString = node.props.url, let url = URL(string: urlString) {
            // Check for custom content
            if let children = node.children, !children.isEmpty {
                Link(destination: url) {
                    ForEach(children) { child in
                        DynamicView(node: child, onEvent: onEvent)
                    }
                }
            } else {
                Link(node.props.label ?? urlString, destination: url)
            }
        } else {
            Text(node.props.label ?? "Invalid URL")
        }
    }

    @ViewBuilder
    func buildImage() -> some View {
        let styles = node.props.imageStyles
        let sourceType = node.props.sourceType
        let sourceValue = node.props.sourceValue
        let systemName = node.props.systemName

        Group {
            // SF Symbol (used by SFSymbol class)
            if let symbolName = systemName {
                Image(systemName: symbolName)
                    .applySFSymbolStyles(styles)
            }
            // URL image
            else if sourceType == "url", let urlString = sourceValue, let url = URL(string: urlString) {
                AsyncImage(url: url) { phase in
                    switch phase {
                    case .empty:
                        ProgressView()
                    case .success(let image):
                        image
                            .applyAsyncImageStyles(styles)
                    case .failure:
                        Image(systemName: "photo")
                            .foregroundColor(.secondary)
                    @unknown default:
                        Image(systemName: "photo")
                    }
                }
            }
            // File image
            else if sourceType == "file", let path = sourceValue, let nsImage = NSImage(contentsOfFile: path) {
                Image(nsImage: nsImage)
                    .applyImageStyles(styles)
            }
            // Base64 data image
            else if sourceType == "data",
                    let base64String = sourceValue,
                    let data = Data(base64Encoded: base64String),
                    let nsImage = NSImage(data: data) {
                Image(nsImage: nsImage)
                    .applyImageStyles(styles)
            }
            // Fallback
            else {
                Image(systemName: "photo")
                    .foregroundColor(.secondary)
            }
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

// MARK: - Text Layout Helpers (avoid AnyView for faster compilation)

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

// MARK: - Button Styling

extension View {
    @ViewBuilder
    func applyButtonStyles(_ styles: ViewNode.ButtonStyles?) -> some View {
        if let styles = styles {
            self
                .applyButtonStyle(styles)
                .applyButtonBorderShape(styles)
                .applyControlSize(styles)
                .applyTint(styles)
                .applyLabelStyle(styles)
                .applyDisabled(styles)
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyButtonStyle(_ styles: ViewNode.ButtonStyles) -> some View {
        if let style = styles.style {
            switch style.lowercased() {
            case "bordered":
                self.buttonStyle(.bordered)
            case "borderedprominent":
                self.buttonStyle(.borderedProminent)
            case "borderless":
                self.buttonStyle(.borderless)
            case "plain":
                self.buttonStyle(.plain)
            case "link":
                self.buttonStyle(.link)
            default:
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyButtonBorderShape(_ styles: ViewNode.ButtonStyles) -> some View {
        if #available(macOS 14.0, *) {
            if let shape = styles.borderShape {
                switch shape.lowercased() {
                case "capsule":
                    self.buttonBorderShape(.capsule)
                case "roundedrectangle":
                    if let radius = styles.cornerRadius {
                        self.buttonBorderShape(.roundedRectangle(radius: radius))
                    } else {
                        self.buttonBorderShape(.roundedRectangle)
                    }
                case "circle":
                    self.buttonBorderShape(.circle)
                default:
                    self
                }
            } else {
                self
            }
        } else {
            // buttonBorderShape requires macOS 14.0+
            self
        }
    }

    @ViewBuilder
    private func applyControlSize(_ styles: ViewNode.ButtonStyles) -> some View {
        if let size = styles.controlSize {
            switch size.lowercased() {
            case "mini":
                self.controlSize(.mini)
            case "small":
                self.controlSize(.small)
            case "regular":
                self.controlSize(.regular)
            case "large":
                self.controlSize(.large)
            case "extralarge":
                if #available(macOS 14.0, *) {
                    self.controlSize(.extraLarge)
                } else {
                    self
                }
            default:
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyTint(_ styles: ViewNode.ButtonStyles) -> some View {
        if let tint = styles.tint {
            self.tint(Color(nibColor: tint))
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyLabelStyle(_ styles: ViewNode.ButtonStyles) -> some View {
        if let style = styles.labelStyle {
            switch style.lowercased() {
            case "icononly":
                self.labelStyle(.iconOnly)
            case "titleonly":
                self.labelStyle(.titleOnly)
            case "titleandicon":
                self.labelStyle(.titleAndIcon)
            default:
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyDisabled(_ styles: ViewNode.ButtonStyles) -> some View {
        if styles.disabled == true {
            self.disabled(true)
        } else {
            self
        }
    }
}

// MARK: - Type Conversions

extension ButtonRole {
    static func nib(_ value: String?) -> ButtonRole? {
        switch value?.lowercased() {
        case "destructive": return .destructive
        case "cancel": return .cancel
        default: return nil
        }
    }
}

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

// MARK: - TextField Styling

extension View {
    @ViewBuilder
    func applyTextFieldStyles(_ styles: ViewNode.TextFieldStyles?) -> some View {
        if let styles = styles {
            self
                .applyTextFieldStyle(styles)
                .applyDisabledState(styles.disabled)
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyTextFieldStyle(_ styles: ViewNode.TextFieldStyles) -> some View {
        if let style = styles.style {
            switch style.lowercased() {
            case "plain":
                self.textFieldStyle(.plain)
            case "roundedborder":
                self.textFieldStyle(.roundedBorder)
            case "squareborder":
                if #available(macOS 14.0, *) {
                    self.textFieldStyle(.squareBorder)
                } else {
                    self.textFieldStyle(.roundedBorder)
                }
            default:
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyDisabledState(_ disabled: Bool?) -> some View {
        if disabled == true {
            self.disabled(true)
        } else {
            self
        }
    }
}

// MARK: - Toggle Styling

extension View {
    @ViewBuilder
    func applyToggleStyles(_ styles: ViewNode.ToggleStyles?) -> some View {
        if let styles = styles {
            self
                .applyToggleStyle(styles)
                .applyTint(styles.tint)
                .applyDisabledState(styles.disabled)
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyToggleStyle(_ styles: ViewNode.ToggleStyles) -> some View {
        if let style = styles.style {
            switch style.lowercased() {
            case "switch":
                self.toggleStyle(.switch)
            case "button":
                self.toggleStyle(.button)
            case "checkbox":
                self.toggleStyle(.checkbox)
            default:
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyTint(_ tint: String?) -> some View {
        if let tint = tint {
            self.tint(Color(nibColor: tint))
        } else {
            self
        }
    }
}

// MARK: - Slider Styling

extension View {
    @ViewBuilder
    func applySliderStyles(_ styles: ViewNode.SliderStyles?) -> some View {
        if let styles = styles {
            self
                .applyTint(styles.tint)
                .applyDisabledState(styles.disabled)
        } else {
            self
        }
    }
}

// MARK: - Picker Styling

extension View {
    @ViewBuilder
    func applyPickerStyles(_ styles: ViewNode.PickerStyles?) -> some View {
        if let styles = styles {
            self
                .applyPickerStyle(styles)
                .applyDisabledState(styles.disabled)
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyPickerStyle(_ styles: ViewNode.PickerStyles) -> some View {
        if let style = styles.style {
            switch style.lowercased() {
            case "menu":
                self.pickerStyle(.menu)
            case "segmented":
                self.pickerStyle(.segmented)
            case "inline":
                self.pickerStyle(.inline)
            case "radiogroup":
                self.pickerStyle(.radioGroup)
            default:
                self
            }
        } else {
            self
        }
    }
}

// MARK: - ProgressView Styling

extension View {
    @ViewBuilder
    func applyProgressStyles(_ styles: ViewNode.ProgressStyles?) -> some View {
        if let styles = styles {
            self
                .applyProgressStyle(styles)
                .applyTint(styles.tint)
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyProgressStyle(_ styles: ViewNode.ProgressStyles) -> some View {
        if let style = styles.style {
            switch style.lowercased() {
            case "linear":
                self.progressViewStyle(.linear)
            case "circular":
                self.progressViewStyle(.circular)
            default:
                self
            }
        } else {
            self
        }
    }
}

// MARK: - Image Styling

extension View {
    @ViewBuilder
    func applyImageStyles(_ styles: ViewNode.ImageStyles?) -> some View {
        if let styles = styles {
            self
                .applyResizable(styles)
                .applyScaling(styles)
                .applyAntialiased(styles)
                .applyBlur(styles)
        } else {
            self
        }
    }

    /// Apply SF Symbol-specific styles
    @ViewBuilder
    func applySFSymbolStyles(_ styles: ViewNode.ImageStyles?) -> some View {
        if let styles = styles {
            self
                .applySymbolRenderingMode(styles)
                .applySymbolConfiguration(styles)
        } else {
            self
        }
    }

    @ViewBuilder
    private func applySymbolRenderingMode(_ styles: ViewNode.ImageStyles) -> some View {
        if let mode = styles.symbolRenderingMode {
            switch mode.lowercased() {
            case "monochrome":
                self.symbolRenderingMode(.monochrome)
            case "hierarchical":
                self.symbolRenderingMode(.hierarchical)
            case "palette":
                self.symbolRenderingMode(.palette)
            case "multicolor":
                self.symbolRenderingMode(.multicolor)
            default:
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applySymbolConfiguration(_ styles: ViewNode.ImageStyles) -> some View {
        if let scale = styles.symbolScale, let s = Image.Scale.nib(scale) {
            self.imageScale(s)
                .fontWeight(Font.Weight.nib(styles.symbolWeight) ?? .regular)
        } else if let weight = styles.symbolWeight, let w = Font.Weight.nib(weight) {
            self.fontWeight(w)
        } else {
            self
        }
    }

    /// Apply styles to an AsyncImage result (SwiftUI Image from async loading)
    @ViewBuilder
    func applyAsyncImageStyles(_ styles: ViewNode.ImageStyles?) -> some View {
        if let styles = styles {
            applyAsyncImageStylesInternal(styles)
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyAsyncImageStylesInternal(_ styles: ViewNode.ImageStyles) -> some View {
        // For async images, we need to handle resizable differently
        if let image = self as? SwiftUI.Image {
            let resizedImage = styles.resizable == true ? image.resizable(resizingMode: .stretch) : image

            let scaledImage: some View = {
                if styles.scaledToFit == true {
                    return AnyView(resizedImage.scaledToFit())
                } else if styles.scaledToFill == true {
                    return AnyView(resizedImage.scaledToFill())
                } else {
                    return AnyView(resizedImage)
                }
            }()

            scaledImage
                .applyAntialiased(styles)
                .applyBlur(styles)
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyResizable(_ styles: ViewNode.ImageStyles) -> some View {
        if styles.resizable == true {
            if let image = self as? Image {
                AnyView(image.resizable(resizingMode: .stretch))
            } else {
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyScaling(_ styles: ViewNode.ImageStyles) -> some View {
        if styles.scaledToFit == true {
            self.scaledToFit()
        } else if styles.scaledToFill == true {
            self.scaledToFill()
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyAntialiased(_ styles: ViewNode.ImageStyles) -> some View {
        if styles.antialiased == false {
            if let image = self as? Image {
                AnyView(image.interpolation(.none))
            } else {
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyBlur(_ styles: ViewNode.ImageStyles) -> some View {
        if let blur = styles.blur, blur > 0 {
            self.blur(radius: blur)
        } else {
            self
        }
    }
}

// MARK: - Additional Type Conversions

extension Font.Weight {
    static func nib(_ value: String?) -> Font.Weight? {
        switch value?.lowercased() {
        case "ultralight": return .ultraLight
        case "thin": return .thin
        case "light": return .light
        case "regular": return .regular
        case "medium": return .medium
        case "semibold": return .semibold
        case "bold": return .bold
        case "heavy": return .heavy
        case "black": return .black
        default: return nil
        }
    }
}

extension Image.Scale {
    static func nib(_ value: String?) -> Image.Scale? {
        switch value?.lowercased() {
        case "small": return .small
        case "medium": return .medium
        case "large": return .large
        default: return nil
        }
    }
}

