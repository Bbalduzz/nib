import Foundation

// MARK: - Utility Types

extension ViewNode {
    struct PickerOption: Codable, Equatable, Hashable {
        var value: String
        var label: String
    }

    /// Gradient stop with position and color
    struct GradientStop: Codable, Equatable {
        var position: Double   // 0.0 to 1.0
        var color: String      // Color string

        // Custom decoder to handle array format [position, color]
        // Position can be Int or Double from MessagePack
        init(from decoder: Decoder) throws {
            var container = try decoder.unkeyedContainer()

            // Decode position - handle both Int and Double using NumericValue wrapper
            let numValue = try container.decode(NumericValue.self)
            position = numValue.doubleValue

            color = try container.decode(String.self)
        }

        func encode(to encoder: Encoder) throws {
            var container = encoder.unkeyedContainer()
            try container.encode(position)
            try container.encode(color)
        }
    }

    /// Helper to decode numeric values that might be Int or Double
    struct NumericValue: Codable {
        let doubleValue: Double

        init(from decoder: Decoder) throws {
            let container = try decoder.singleValueContainer()
            if let d = try? container.decode(Double.self) {
                doubleValue = d
            } else if let i = try? container.decode(Int.self) {
                doubleValue = Double(i)
            } else {
                throw DecodingError.typeMismatch(Double.self, DecodingError.Context(
                    codingPath: decoder.codingPath,
                    debugDescription: "Expected numeric value"
                ))
            }
        }

        func encode(to encoder: Encoder) throws {
            var container = encoder.singleValueContainer()
            try container.encode(doubleValue)
        }
    }
}
