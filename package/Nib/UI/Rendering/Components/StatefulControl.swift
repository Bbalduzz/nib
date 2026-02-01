import SwiftUI

// MARK: - Generic Stateful Control Wrapper

/// A generic wrapper for controls that need local state management.
///
/// This wrapper:
/// - Manages @State internally for the control's value
/// - Emits events when the value changes via the onEvent callback
/// - Supports custom event formatting
struct StatefulControl<Value: Equatable, Content: View>: View {
    let initialValue: Value
    let nodeId: String
    let onEvent: (String, String) -> Void
    let eventFormatter: (Value) -> String
    let content: (Binding<Value>) -> Content

    @State private var value: Value

    init(
        initialValue: Value,
        nodeId: String,
        onEvent: @escaping (String, String) -> Void,
        eventFormatter: @escaping (Value) -> String = { "change:\($0)" },
        @ViewBuilder content: @escaping (Binding<Value>) -> Content
    ) {
        self.initialValue = initialValue
        self.nodeId = nodeId
        self.onEvent = onEvent
        self.eventFormatter = eventFormatter
        self.content = content
        self._value = State(initialValue: initialValue)
    }

    var body: some View {
        content($value)
            .onChange(of: value) { _, newValue in
                onEvent(nodeId, eventFormatter(newValue))
            }
    }
}

// MARK: - Specialized Stateful Views

/// TextField with local state that emits change events
struct StatefulTextField: View {
    let placeholder: String
    let initialText: String
    let styles: ViewNode.TextFieldStyles?
    let onEvent: (String, String) -> Void
    let nodeId: String

    @State private var text: String

    init(
        placeholder: String, initialText: String, styles: ViewNode.TextFieldStyles?, nodeId: String,
        onEvent: @escaping (String, String) -> Void
    ) {
        self.placeholder = placeholder
        self.initialText = initialText
        self.styles = styles
        self.nodeId = nodeId
        self.onEvent = onEvent
        self._text = State(initialValue: initialText)
    }

    var body: some View {
        TextField(placeholder, text: $text)
            .onSubmit {
                onEvent(nodeId, "submit:\(text)")
            }
            .onChange(of: text) { _, newValue in
                onEvent(nodeId, "change:\(newValue)")
            }
            .applyTextFieldStyles(styles)
    }
}

/// SecureField with local state that emits change events
struct StatefulSecureField: View {
    let placeholder: String
    let initialText: String
    let styles: ViewNode.TextFieldStyles?
    let onEvent: (String, String) -> Void
    let nodeId: String

    @State private var text: String

    init(
        placeholder: String, initialText: String, styles: ViewNode.TextFieldStyles?, nodeId: String,
        onEvent: @escaping (String, String) -> Void
    ) {
        self.placeholder = placeholder
        self.initialText = initialText
        self.styles = styles
        self.nodeId = nodeId
        self.onEvent = onEvent
        self._text = State(initialValue: initialText)
    }

    var body: some View {
        SecureField(placeholder, text: $text)
            .onSubmit {
                onEvent(nodeId, "submit:\(text)")
            }
            .onChange(of: text) { _, newValue in
                onEvent(nodeId, "change:\(newValue)")
            }
            .applyTextFieldStyles(styles)
    }
}

/// Toggle with local state that emits change events
struct StatefulToggle: View {
    let label: String
    let initialValue: Bool
    let styles: ViewNode.ToggleStyles?
    let onEvent: (String, String) -> Void
    let nodeId: String

    @State private var isOn: Bool

    init(
        label: String, isOn: Bool, styles: ViewNode.ToggleStyles?, nodeId: String,
        onEvent: @escaping (String, String) -> Void
    ) {
        self.label = label
        self.initialValue = isOn
        self.styles = styles
        self.nodeId = nodeId
        self.onEvent = onEvent
        self._isOn = State(initialValue: isOn)
    }

    var body: some View {
        Toggle(label, isOn: $isOn)
            .onChange(of: isOn) { _, newValue in
                onEvent(nodeId, "change:\(newValue)")
            }
            .applyToggleStyles(styles)
    }
}

/// Toggle with custom content label
struct StatefulToggleWithContent<Content: View>: View {
    let initialValue: Bool
    let styles: ViewNode.ToggleStyles?
    let onEvent: (String, String) -> Void
    let nodeId: String
    let content: () -> Content

    @State private var isOn: Bool

    init(
        isOn: Bool, styles: ViewNode.ToggleStyles?, nodeId: String,
        onEvent: @escaping (String, String) -> Void, @ViewBuilder content: @escaping () -> Content
    ) {
        self.initialValue = isOn
        self.styles = styles
        self.nodeId = nodeId
        self.onEvent = onEvent
        self.content = content
        self._isOn = State(initialValue: isOn)
    }

    var body: some View {
        Toggle(isOn: $isOn, label: content)
            .onChange(of: isOn) { _, newValue in
                onEvent(nodeId, "change:\(newValue)")
            }
            .applyToggleStyles(styles)
    }
}

/// Slider with local state that emits change events
struct StatefulSlider: View {
    let initialValue: Double
    let range: ClosedRange<Double>
    let step: Double?
    let styles: ViewNode.SliderStyles?
    let onEvent: (String, String) -> Void
    let nodeId: String

    @State private var value: Double

    init(
        value: Double, range: ClosedRange<Double>, step: Double?, styles: ViewNode.SliderStyles?,
        nodeId: String, onEvent: @escaping (String, String) -> Void
    ) {
        self.initialValue = value
        self.range = range
        self.step = step
        self.styles = styles
        self.nodeId = nodeId
        self.onEvent = onEvent
        self._value = State(initialValue: value)
    }

    var body: some View {
        Group {
            if let step = step {
                Slider(value: $value, in: range, step: step)
            } else {
                Slider(value: $value, in: range)
            }
        }
        .onChange(of: value) { _, newValue in
            onEvent(nodeId, "change:\(newValue)")
        }
        .applySliderStyles(styles)
    }
}

/// Picker with local state that emits change events
struct StatefulPicker: View {
    let label: String
    let initialSelection: String
    let options: [ViewNode.PickerOption]
    let styles: ViewNode.PickerStyles?
    let onEvent: (String, String) -> Void
    let nodeId: String

    @State private var selection: String

    init(
        label: String, selection: String, options: [ViewNode.PickerOption],
        styles: ViewNode.PickerStyles?, nodeId: String, onEvent: @escaping (String, String) -> Void
    ) {
        self.label = label
        self.initialSelection = selection
        self.options = options
        self.styles = styles
        self.nodeId = nodeId
        self.onEvent = onEvent
        self._selection = State(initialValue: selection)
    }

    var body: some View {
        Picker(label, selection: $selection) {
            ForEach(options, id: \.value) { option in
                Text(option.label).tag(option.value)
            }
        }
        .onChange(of: selection) { _, newValue in
            onEvent(nodeId, "change:\(newValue)")
        }
        .applyPickerStyles(styles)
    }
}

/// DisclosureGroup with local state that emits expand/collapse events
struct StatefulDisclosureGroup<Content: View>: View {
    let label: String
    let initialExpanded: Bool
    let onEvent: (String, String) -> Void
    let nodeId: String
    let content: () -> Content

    @State private var isExpanded: Bool

    init(
        label: String, isExpanded: Bool, nodeId: String,
        onEvent: @escaping (String, String) -> Void, @ViewBuilder content: @escaping () -> Content
    ) {
        self.label = label
        self.initialExpanded = isExpanded
        self.nodeId = nodeId
        self.onEvent = onEvent
        self.content = content
        self._isExpanded = State(initialValue: isExpanded)
    }

    var body: some View {
        DisclosureGroup(label, isExpanded: $isExpanded) {
            content()
        }
        .onChange(of: isExpanded) { _, newValue in
            onEvent(nodeId, "expand:\(newValue)")
        }
    }
}

// MARK: - Factory Namespace

/// Namespace for StatefulControl factory methods
enum StatefulControls {
    /// Creates a stateful TextField
    static func textField(
        placeholder: String,
        initialText: String,
        styles: ViewNode.TextFieldStyles?,
        nodeId: String,
        onEvent: @escaping (String, String) -> Void
    ) -> StatefulTextField {
        StatefulTextField(
            placeholder: placeholder, initialText: initialText, styles: styles, nodeId: nodeId,
            onEvent: onEvent)
    }

    /// Creates a stateful SecureField
    static func secureField(
        placeholder: String,
        initialText: String,
        styles: ViewNode.TextFieldStyles?,
        nodeId: String,
        onEvent: @escaping (String, String) -> Void
    ) -> StatefulSecureField {
        StatefulSecureField(
            placeholder: placeholder, initialText: initialText, styles: styles, nodeId: nodeId,
            onEvent: onEvent)
    }

    /// Creates a stateful Toggle
    static func toggle(
        label: String,
        isOn: Bool,
        styles: ViewNode.ToggleStyles?,
        nodeId: String,
        onEvent: @escaping (String, String) -> Void
    ) -> StatefulToggle {
        StatefulToggle(label: label, isOn: isOn, styles: styles, nodeId: nodeId, onEvent: onEvent)
    }

    /// Creates a stateful Slider
    static func slider(
        value: Double,
        range: ClosedRange<Double>,
        step: Double?,
        styles: ViewNode.SliderStyles?,
        nodeId: String,
        onEvent: @escaping (String, String) -> Void
    ) -> StatefulSlider {
        StatefulSlider(
            value: value, range: range, step: step, styles: styles, nodeId: nodeId, onEvent: onEvent
        )
    }

    /// Creates a stateful Picker
    static func picker(
        label: String,
        selection: String,
        options: [ViewNode.PickerOption],
        styles: ViewNode.PickerStyles?,
        nodeId: String,
        onEvent: @escaping (String, String) -> Void
    ) -> StatefulPicker {
        StatefulPicker(
            label: label, selection: selection, options: options, styles: styles, nodeId: nodeId,
            onEvent: onEvent)
    }
}
