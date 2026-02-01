import Foundation
import SwiftUI

// MARK: - Type-Discriminated Props

/// Type-discriminated props union - each view type has its own props struct.
/// This replaces the "god struct" pattern with type-safe, per-view props.
///
/// Benefits:
/// - Type safety: Only relevant props are available for each view type
/// - Memory efficiency: Only store what's needed
/// - Better Codable: Cleaner serialization
enum ViewProps: Codable, Equatable {
    case text(TextProps)
    case button(ButtonProps)
    case stack(StackProps)
    case textField(TextFieldProps)
    case secureField(SecureFieldProps)
    case toggle(ToggleProps)
    case slider(SliderProps)
    case picker(PickerProps)
    case progressView(ProgressProps)
    case image(ImageProps)
    case label(LabelProps)
    case link(LinkProps)
    case shape(ShapeProps)
    case spacer(SpacerProps)
    case scrollView(ScrollViewProps)
    case section(SectionProps)
    case navigation(NavigationProps)
    case disclosureGroup(DisclosureGroupProps)
    case common(CommonProps)  // For simple views like Divider, Group

    // MARK: - Coding Keys

    private enum CodingKeys: String, CodingKey {
        case type
        case text, button, stack, textField, secureField
        case toggle, slider, picker, progressView, image
        case label, link, shape, spacer, scrollView
        case section, navigation, disclosureGroup, common
    }

    // MARK: - Decoding

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)

        // Try to decode each type in order of frequency
        if let props = try? container.decode(TextProps.self, forKey: .text) {
            self = .text(props)
        } else if let props = try? container.decode(ButtonProps.self, forKey: .button) {
            self = .button(props)
        } else if let props = try? container.decode(StackProps.self, forKey: .stack) {
            self = .stack(props)
        } else if let props = try? container.decode(TextFieldProps.self, forKey: .textField) {
            self = .textField(props)
        } else if let props = try? container.decode(SecureFieldProps.self, forKey: .secureField) {
            self = .secureField(props)
        } else if let props = try? container.decode(ToggleProps.self, forKey: .toggle) {
            self = .toggle(props)
        } else if let props = try? container.decode(SliderProps.self, forKey: .slider) {
            self = .slider(props)
        } else if let props = try? container.decode(PickerProps.self, forKey: .picker) {
            self = .picker(props)
        } else if let props = try? container.decode(ProgressProps.self, forKey: .progressView) {
            self = .progressView(props)
        } else if let props = try? container.decode(ImageProps.self, forKey: .image) {
            self = .image(props)
        } else if let props = try? container.decode(LabelProps.self, forKey: .label) {
            self = .label(props)
        } else if let props = try? container.decode(LinkProps.self, forKey: .link) {
            self = .link(props)
        } else if let props = try? container.decode(ShapeProps.self, forKey: .shape) {
            self = .shape(props)
        } else if let props = try? container.decode(SpacerProps.self, forKey: .spacer) {
            self = .spacer(props)
        } else if let props = try? container.decode(ScrollViewProps.self, forKey: .scrollView) {
            self = .scrollView(props)
        } else if let props = try? container.decode(SectionProps.self, forKey: .section) {
            self = .section(props)
        } else if let props = try? container.decode(NavigationProps.self, forKey: .navigation) {
            self = .navigation(props)
        } else if let props = try? container.decode(DisclosureGroupProps.self, forKey: .disclosureGroup) {
            self = .disclosureGroup(props)
        } else {
            // Default to common props
            let props = try container.decodeIfPresent(CommonProps.self, forKey: .common) ?? CommonProps()
            self = .common(props)
        }
    }

    // MARK: - Encoding

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)

        switch self {
        case .text(let props):
            try container.encode(props, forKey: .text)
        case .button(let props):
            try container.encode(props, forKey: .button)
        case .stack(let props):
            try container.encode(props, forKey: .stack)
        case .textField(let props):
            try container.encode(props, forKey: .textField)
        case .secureField(let props):
            try container.encode(props, forKey: .secureField)
        case .toggle(let props):
            try container.encode(props, forKey: .toggle)
        case .slider(let props):
            try container.encode(props, forKey: .slider)
        case .picker(let props):
            try container.encode(props, forKey: .picker)
        case .progressView(let props):
            try container.encode(props, forKey: .progressView)
        case .image(let props):
            try container.encode(props, forKey: .image)
        case .label(let props):
            try container.encode(props, forKey: .label)
        case .link(let props):
            try container.encode(props, forKey: .link)
        case .shape(let props):
            try container.encode(props, forKey: .shape)
        case .spacer(let props):
            try container.encode(props, forKey: .spacer)
        case .scrollView(let props):
            try container.encode(props, forKey: .scrollView)
        case .section(let props):
            try container.encode(props, forKey: .section)
        case .navigation(let props):
            try container.encode(props, forKey: .navigation)
        case .disclosureGroup(let props):
            try container.encode(props, forKey: .disclosureGroup)
        case .common(let props):
            try container.encode(props, forKey: .common)
        }
    }
}

// MARK: - Convenience Accessors

extension ViewProps {
    /// Get text props if this is a text view
    var textProps: TextProps? {
        if case .text(let props) = self { return props }
        return nil
    }

    /// Get button props if this is a button view
    var buttonProps: ButtonProps? {
        if case .button(let props) = self { return props }
        return nil
    }

    /// Get stack props if this is a stack view
    var stackProps: StackProps? {
        if case .stack(let props) = self { return props }
        return nil
    }

    /// Get toggle props if this is a toggle view
    var toggleProps: ToggleProps? {
        if case .toggle(let props) = self { return props }
        return nil
    }

    /// Get slider props if this is a slider view
    var sliderProps: SliderProps? {
        if case .slider(let props) = self { return props }
        return nil
    }

    /// Get picker props if this is a picker view
    var pickerProps: PickerProps? {
        if case .picker(let props) = self { return props }
        return nil
    }

    /// Get image props if this is an image view
    var imageProps: ImageProps? {
        if case .image(let props) = self { return props }
        return nil
    }
}
