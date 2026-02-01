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
        var key: String
        var width: CGFloat?
        var minWidth: CGFloat?
        var maxWidth: CGFloat?
        var alignment: String?
    }
}
