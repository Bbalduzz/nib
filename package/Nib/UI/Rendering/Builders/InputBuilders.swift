import SwiftUI

// MARK: - Input Control Builders

extension DynamicView {
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
    func buildGauge() -> some View {
        let value = node.props.value ?? 0
        let minValue = node.props.minValue ?? 0
        let maxValue = node.props.maxValue ?? 1
        let labelText = node.props.label ?? ""
        let currentValueLabelText = node.props.currentValueLabel
        let minValueLabelText = node.props.minValueLabel
        let maxValueLabelText = node.props.maxValueLabel
        let style = node.props.gaugeStyle ?? "automatic"
        let tintColor = node.props.tint.map { Color(nibColor: $0) }

        // Check for view-based labels in children
        let labelView = node.child(forSlot: "label")
        let currentValueView = node.child(forSlot: "currentValue")
        let minValueView = node.child(forSlot: "minValue")
        let maxValueView = node.child(forSlot: "maxValue")

        let gaugeView = Gauge(value: value, in: minValue...maxValue) {
            // Label
            if let labelNode = labelView {
                DynamicView(node: labelNode, onEvent: onEvent)
            } else if !labelText.isEmpty {
                Text(labelText)
            }
        } currentValueLabel: {
            // Current value label
            if let cvNode = currentValueView {
                DynamicView(node: cvNode, onEvent: onEvent)
            } else if let cvl = currentValueLabelText {
                Text(cvl)
            }
        } minimumValueLabel: {
            // Min value label
            if let mvNode = minValueView {
                DynamicView(node: mvNode, onEvent: onEvent)
            } else if let mvl = minValueLabelText {
                Text(mvl)
            }
        } maximumValueLabel: {
            // Max value label
            if let mvNode = maxValueView {
                DynamicView(node: mvNode, onEvent: onEvent)
            } else if let mvl = maxValueLabelText {
                Text(mvl)
            }
        }

        let styledGauge = applyGaugeStyle(gaugeView, style: style)

        if let tint = tintColor {
            styledGauge.tint(tint)
        } else {
            styledGauge
        }
    }

    @ViewBuilder
    private func applyGaugeStyle<G: View>(_ gauge: G, style: String) -> some View {
        switch style {
        case "linearCapacity":
            gauge.gaugeStyle(.linearCapacity)
        case "circularCapacity":
            gauge.gaugeStyle(.accessoryCircularCapacity)
        case "accessoryLinear":
            gauge.gaugeStyle(.accessoryLinear)
        case "accessoryLinearCapacity":
            gauge.gaugeStyle(.accessoryLinearCapacity)
        case "accessoryCircular":
            gauge.gaugeStyle(.accessoryCircular)
        case "accessoryCircularCapacity":
            gauge.gaugeStyle(.accessoryCircularCapacity)
        default:
            gauge.gaugeStyle(.automatic)
        }
    }

    @ViewBuilder
    func buildTextEditor() -> some View {
        let text = node.props.text ?? ""
        let placeholder = node.props.placeholder
        let styles = node.props.textEditorStyles

        // Legacy fallback props
        let legacyLineLimit = node.props.lineLimit
        let legacyScrollsDisabled = node.props.scrollsDisabled ?? false
        let legacyContentBackgroundHidden = node.props.contentBackgroundHidden ?? false
        let legacyContentBackground = node.props.contentBackground

        TextEditorWrapper(
            nodeId: node.id,
            text: text,
            placeholder: placeholder,
            styles: styles,
            legacyLineLimit: legacyLineLimit,
            legacyScrollsDisabled: legacyScrollsDisabled,
            legacyContentBackgroundHidden: legacyContentBackgroundHidden,
            legacyContentBackground: legacyContentBackground,
            onEvent: onEvent
        )
    }
}

// MARK: - TextEditor Wrapper

struct TextEditorWrapper: View {
    let nodeId: String
    let text: String
    let placeholder: String?
    let styles: ViewNode.TextEditorStyles?
    let legacyLineLimit: Int?
    let legacyScrollsDisabled: Bool
    let legacyContentBackgroundHidden: Bool
    let legacyContentBackground: String?
    let onEvent: (String, String) -> Void

    @State private var localText: String

    init(nodeId: String, text: String, placeholder: String?, styles: ViewNode.TextEditorStyles?, legacyLineLimit: Int?, legacyScrollsDisabled: Bool, legacyContentBackgroundHidden: Bool, legacyContentBackground: String?, onEvent: @escaping (String, String) -> Void) {
        self.nodeId = nodeId
        self.text = text
        self.placeholder = placeholder
        self.styles = styles
        self.legacyLineLimit = legacyLineLimit
        self.legacyScrollsDisabled = legacyScrollsDisabled
        self.legacyContentBackgroundHidden = legacyContentBackgroundHidden
        self.legacyContentBackground = legacyContentBackground
        self.onEvent = onEvent
        self._localText = State(initialValue: text)
    }

    var body: some View {
        let base = TextEditor(text: $localText)
            .onChange(of: text) { _, newValue in
                // Sync local state when prop changes from Python
                if localText != newValue {
                    localText = newValue
                }
            }
            .onChange(of: localText) { _, newValue in
                onEvent(nodeId, "change:\(newValue)")
            }

        let v1 = applyFont(to: base)
        let v2 = applyForegroundColor(to: v1)
        let v3 = applyLineSpacing(to: v2)
        let v4 = applyTextAlignment(to: v3)
        let v5 = applyLineLimit(to: v4)
        let v6 = applyScrollDisabled(to: v5)
        let v7 = applyAutocorrectionDisabled(to: v6)
        let v8 = applyBackground(to: v7)
        let v9 = applyEditorStyle(to: v8)
        let v10 = applyFindNavigator(to: v9)

        return v10
    }

    // MARK: - Style Appliers

    @ViewBuilder
    private func applyFont(to view: some View) -> some View {
        if let fontSpec = styles?.font, let fontName = fontSpec.fontName {
            view.font(Font.nib(name: fontName, size: fontSpec.fontSize, weight: fontSpec.fontWeight, path: fontSpec.fontPath))
        } else {
            view
        }
    }

    @ViewBuilder
    private func applyForegroundColor(to view: some View) -> some View {
        if let colorStr = styles?.foregroundColor {
            view.foregroundStyle(Color(nibColor: colorStr))
        } else {
            view
        }
    }

    @ViewBuilder
    private func applyLineSpacing(to view: some View) -> some View {
        if let spacing = styles?.lineSpacing {
            view.lineSpacing(spacing)
        } else {
            view
        }
    }

    @ViewBuilder
    private func applyTextAlignment(to view: some View) -> some View {
        if let alignment = styles?.textAlignment {
            switch alignment.lowercased() {
            case "center":
                view.multilineTextAlignment(.center)
            case "trailing":
                view.multilineTextAlignment(.trailing)
            default:
                view.multilineTextAlignment(.leading)
            }
        } else {
            view
        }
    }

    @ViewBuilder
    private func applyLineLimit(to view: some View) -> some View {
        if let limit = styles?.lineLimit ?? legacyLineLimit {
            view.lineLimit(limit)
        } else {
            view
        }
    }

    @ViewBuilder
    private func applyScrollDisabled(to view: some View) -> some View {
        let disabled = styles?.scrollsDisabled ?? legacyScrollsDisabled
        if disabled {
            view.scrollDisabled(true)
        } else {
            view
        }
    }

    @ViewBuilder
    private func applyAutocorrectionDisabled(to view: some View) -> some View {
        if styles?.autocorrectionDisabled == true {
            view.autocorrectionDisabled(true)
        } else {
            view
        }
    }

    @ViewBuilder
    private func applyBackground(to view: some View) -> some View {
        if #available(macOS 14.0, *) {
            let bgHidden = styles?.contentBackgroundHidden ?? legacyContentBackgroundHidden
            let bgColor = styles?.backgroundColor ?? legacyContentBackground

            if bgHidden {
                view.scrollContentBackground(.hidden)
            } else if let color = bgColor {
                view
                    .scrollContentBackground(.hidden)
                    .background(Color(nibColor: color))
            } else {
                view
            }
        } else {
            view
        }
    }

    @ViewBuilder
    private func applyEditorStyle(to view: some View) -> some View {
        if #available(macOS 14.0, *) {
            if let style = styles?.editorStyle, style.lowercased() == "plain" {
                view.textEditorStyle(.plain)
            } else {
                view
            }
        } else {
            view
        }
    }

    @ViewBuilder
    private func applyFindNavigator(to view: some View) -> some View {
        // findNavigator is not available on macOS — pass through
        view
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
    func applyDisabledState(_ disabled: Bool?) -> some View {
        if disabled == true {
            self.disabled(true)
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
                .applySliderTint(styles.tint)
                .applyDisabledState(styles.disabled)
        } else {
            self
        }
    }

    @ViewBuilder
    private func applySliderTint(_ tint: String?) -> some View {
        if let tint = tint {
            self.tint(Color(nibColor: tint))
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
