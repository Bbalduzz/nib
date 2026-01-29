import Foundation
import SwiftUI

// MARK: - Chart Types

extension ViewNode {
    /// Columnar data format for efficient chart data transmission
    /// Note: columns are JSON-encoded to work around MessagePack limitations
    struct ChartData: Codable, Equatable {
        var columnsJson: String  // JSON-encoded columns dict
        var rowCount: Int

        /// Parsed columns dictionary (lazy parsed from JSON)
        func parseColumns() -> [String: [Any]] {
            guard let data = columnsJson.data(using: .utf8),
                  let json = try? JSONSerialization.jsonObject(with: data) as? [String: [Any]] else {
                return [:]
            }
            return json
        }
    }

    /// Chart axis configuration
    struct ChartAxisConfig: Codable, Equatable {
        var position: String?
        var label: String?
        var gridLines: Bool?
        var hidden: Bool?
        var format: String?
        var labelColor: String?
        var gridColor: String?
    }

    /// Chart legend configuration
    struct ChartLegendConfig: Codable, Equatable {
        var position: String?
        var hidden: Bool?
        var title: String?
    }

    /// Field reference for plottable values
    struct PlottableField: Codable, Equatable {
        var field: String?      // Column name reference
        var type: String?       // "quantitative", "nominal", "temporal"
        var label: String?      // Display label
    }
}
