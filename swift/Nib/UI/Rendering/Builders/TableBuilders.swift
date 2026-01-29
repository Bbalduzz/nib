import SwiftUI

// MARK: - Table Builder

extension DynamicView {
    @ViewBuilder
    func buildTable() -> some View {
        let columns = node.props.tableColumns ?? []
        let rowsJson = node.props.tableRowsJson ?? "[]"
        let rowIdKey = node.props.rowIdKey ?? "id"

        if #available(macOS 12.0, *) {
            TableWrapper(
                nodeId: node.id,
                columns: columns,
                rowsJson: rowsJson,
                rowIdKey: rowIdKey,
                onEvent: onEvent
            )
        } else {
            Text("Table requires macOS 12+")
        }
    }
}

// MARK: - Table Wrapper

@available(macOS 12.0, *)
struct TableWrapper: View {
    let nodeId: String
    let columns: [ViewNode.TableColumnSpec]
    let rowsJson: String
    let rowIdKey: String
    let onEvent: (String, String) -> Void

    @State private var selection: Set<String> = []

    private var items: [TableRowItem] {
        let rows = parseRows()
        return rows.enumerated().map { index, row -> TableRowItem in
            let id = (row[rowIdKey] as? String) ?? String(index)
            return TableRowItem(id: id, data: row)
        }
    }

    var body: some View {
        tableContent
            .onChange(of: selection) { _, newValue in
                let ids = newValue.joined(separator: ",")
                onEvent(nodeId, "selection:\(ids)")
            }
    }

    @ViewBuilder
    private var tableContent: some View {
        // Simple list-based table view for compatibility
        List(items, selection: $selection) { item in
            HStack {
                ForEach(columns, id: \.id) { column in
                    Text(stringValue(item.data[column.key]))
                        .frame(maxWidth: .infinity, alignment: parseAlignment(column.alignment))
                }
            }
        }
    }

    private func parseAlignment(_ alignment: String?) -> Alignment {
        switch alignment {
        case "trailing": return .trailing
        case "center": return .center
        default: return .leading
        }
    }

    private func parseRows() -> [[String: Any]] {
        guard let data = rowsJson.data(using: .utf8),
              let rows = try? JSONSerialization.jsonObject(with: data) as? [[String: Any]] else {
            return []
        }
        return rows
    }

    private func stringValue(_ value: Any?) -> String {
        switch value {
        case let s as String: return s
        case let i as Int: return String(i)
        case let d as Double: return String(d)
        case let b as Bool: return b ? "true" : "false"
        default: return ""
        }
    }
}

// MARK: - Table Row Item

struct TableRowItem: Identifiable, Hashable {
    let id: String
    let data: [String: Any]

    func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }

    static func == (lhs: TableRowItem, rhs: TableRowItem) -> Bool {
        lhs.id == rhs.id
    }
}
