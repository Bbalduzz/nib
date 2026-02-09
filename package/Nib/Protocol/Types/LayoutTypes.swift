import Foundation
import SwiftUI

// MARK: - Layout Types

extension ViewNode {
    // Grid item specification
    struct GridItemSpec: Codable, Equatable {
        var size: String?  // "fixed", "flexible", "adaptive"
        var value: CGFloat?
        var maximum: CGFloat?
        var spacing: CGFloat?
        var alignment: String?
    }

    // Table column specification
    struct TableColumnSpec: Codable, Equatable {
        var id: String
        var title: String
        var alignment: String?
        var sortable: Bool?
        var width: ColumnWidthSpec?

        struct ColumnWidthSpec: Codable, Equatable {
            var type: String    // "fixed" or "range"
            var value: CGFloat? // for fixed
            var min: CGFloat?   // for range
            var ideal: CGFloat? // for range
            var max: CGFloat?   // for range
        }
    }
}
