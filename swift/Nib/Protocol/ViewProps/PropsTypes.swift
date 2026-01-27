import Foundation
import SwiftUI

// MARK: - Common Props

/// Props for simple views like Divider, Group
struct CommonProps: Codable, Equatable {
    var label: String?
    var icon: String?
    var onDrop: Bool?

    init(label: String? = nil, icon: String? = nil, onDrop: Bool? = nil) {
        self.label = label
        self.icon = icon
        self.onDrop = onDrop
    }
}

// MARK: - Text Props

struct TextProps: Codable, Equatable {
    var content: String?
    var textStyles: ViewNode.TextStyles?
}

// MARK: - Button Props

struct ButtonProps: Codable, Equatable {
    var label: String?
    var icon: String?
    var buttonStyles: ViewNode.ButtonStyles?
}

// MARK: - Stack Props

struct StackProps: Codable, Equatable {
    var spacing: CGFloat?
    var alignment: String?
}

// MARK: - TextField Props

struct TextFieldProps: Codable, Equatable {
    var placeholder: String?
    var text: String?
    var textFieldStyles: ViewNode.TextFieldStyles?
}

// MARK: - SecureField Props

struct SecureFieldProps: Codable, Equatable {
    var placeholder: String?
    var text: String?
    var textFieldStyles: ViewNode.TextFieldStyles?
}

// MARK: - Toggle Props

struct ToggleProps: Codable, Equatable {
    var label: String?
    var isOn: Bool?
    var toggleStyles: ViewNode.ToggleStyles?
}

// MARK: - Slider Props

struct SliderProps: Codable, Equatable {
    var value: Double?
    var minValue: Double?
    var maxValue: Double?
    var step: Double?
    var sliderStyles: ViewNode.SliderStyles?
}

// MARK: - Picker Props

struct PickerProps: Codable, Equatable {
    var label: String?
    var selection: String?
    var options: [ViewNode.PickerOption]?
    var pickerStyles: ViewNode.PickerStyles?
}

// MARK: - ProgressView Props

struct ProgressProps: Codable, Equatable {
    var label: String?
    var progress: Double?  // 0.0 to 1.0, nil for indeterminate
    var progressStyles: ViewNode.ProgressStyles?
}

// MARK: - Image Props

struct ImageProps: Codable, Equatable {
    var sourceType: String?  // "url", "file", "data"
    var sourceValue: String? // URL string, file path, or base64-encoded data
    var label: String?       // Accessibility label
    var imageStyles: ViewNode.ImageStyles?
}

// MARK: - Label Props

struct LabelProps: Codable, Equatable {
    var label: String?
    var icon: String?
}

// MARK: - Link Props

struct LinkProps: Codable, Equatable {
    var label: String?
    var url: String?
}

// MARK: - Shape Props

struct ShapeProps: Codable, Equatable {
    var cornerRadius: CGFloat?
    var trimFrom: Double?
    var trimTo: Double?
    var rotation: Double?
}

// MARK: - Spacer Props

struct SpacerProps: Codable, Equatable {
    var minLength: CGFloat?
}

// MARK: - ScrollView Props

struct ScrollViewProps: Codable, Equatable {
    var axes: String?  // "horizontal", "vertical", "both"
    var showsIndicators: Bool?
}

// MARK: - Section Props

struct SectionProps: Codable, Equatable {
    var header: String?
    var footer: String?
}

// MARK: - Navigation Props

struct NavigationProps: Codable, Equatable {
    var label: String?
    var destination: String?
}

// MARK: - DisclosureGroup Props

struct DisclosureGroupProps: Codable, Equatable {
    var label: String?
    var isExpanded: Bool?
}
