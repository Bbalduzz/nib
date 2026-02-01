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
        let lineLimit = node.props.lineLimit
        let scrollsDisabled = node.props.scrollsDisabled ?? false
        let textStyles = node.props.textStyles
        let contentBackgroundHidden = node.props.contentBackgroundHidden ?? false
        let contentBackground = node.props.contentBackground

        TextEditorWrapper(
            nodeId: node.id,
            text: text,
            placeholder: placeholder,
            lineLimit: lineLimit,
            scrollsDisabled: scrollsDisabled,
            textStyles: textStyles,
            contentBackgroundHidden: contentBackgroundHidden,
            contentBackground: contentBackground,
            onEvent: onEvent
        )
    }
}

// MARK: - TextEditor Wrapper

struct TextEditorWrapper: View {
    let nodeId: String
    let text: String
    let placeholder: String?
    let lineLimit: Int?
    let scrollsDisabled: Bool
    let textStyles: ViewNode.TextStyles?
    let contentBackgroundHidden: Bool
    let contentBackground: String?
    let onEvent: (String, String) -> Void

    @State private var localText: String

    init(nodeId: String, text: String, placeholder: String?, lineLimit: Int?, scrollsDisabled: Bool, textStyles: ViewNode.TextStyles?, contentBackgroundHidden: Bool, contentBackground: String?, onEvent: @escaping (String, String) -> Void) {
        self.nodeId = nodeId
        self.text = text
        self.placeholder = placeholder
        self.lineLimit = lineLimit
        self.scrollsDisabled = scrollsDisabled
        self.textStyles = textStyles
        self.contentBackgroundHidden = contentBackgroundHidden
        self.contentBackground = contentBackground
        self.onEvent = onEvent
        self._localText = State(initialValue: text)
    }

    var body: some View {
        let editor = TextEditor(text: $localText)
            .onChange(of: localText) { _, newValue in
                onEvent(nodeId, "change:\(newValue)")
            }

        // Apply modifiers and return
        return applyAllModifiers(to: editor)
    }

    @ViewBuilder
    private func applyAllModifiers(to editor: some View) -> some View {
        // Start with base modifiers
        let withScroll = applyScrollModifier(to: editor)
        let withBackground = applyBackgroundModifier(to: withScroll)
        let withStyle = applyStyleModifier(to: withBackground)
        withStyle
    }

    @ViewBuilder
    private func applyScrollModifier(to view: some View) -> some View {
        if scrollsDisabled {
            view.scrollDisabled(true)
        } else {
            view
        }
    }

    @ViewBuilder
    private func applyBackgroundModifier(to view: some View) -> some View {
        if #available(macOS 14.0, *) {
            if contentBackgroundHidden {
                // Hide default background, make transparent
                view.scrollContentBackground(.hidden)
            } else if let bgColor = contentBackground {
                // Hide default and apply custom color
                view
                    .scrollContentBackground(.hidden)
                    .background(Color(nibColor: bgColor))
            } else {
                view
            }
        } else {
            // Fallback for older macOS - can't easily hide TextEditor background
            view
        }
    }

    @ViewBuilder
    private func applyStyleModifier(to view: some View) -> some View {
        if let styles = textStyles, styles.monospaced == true {
            if #available(macOS 13.3, *) {
                view.monospaced()
            } else {
                view
            }
        } else {
            view
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
