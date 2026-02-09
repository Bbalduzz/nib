import SwiftUI
import AppKit

// MARK: - Table Builder

extension DynamicView {
    @ViewBuilder
    func buildTable() -> some View {
        NibTableView(
            node: node,
            onEvent: onEvent
        )
    }
}

// MARK: - NSTableView Wrapper

struct NibTableView: NSViewRepresentable {
    let node: ViewNode
    let onEvent: (String, String) -> Void

    func makeNSView(context: Context) -> NSScrollView {
        let scrollView = NSScrollView()
        scrollView.hasVerticalScroller = true
        scrollView.hasHorizontalScroller = false
        scrollView.autohidesScrollers = true
        scrollView.borderType = .noBorder

        let tableView = NSTableView()
        tableView.style = .inset
        tableView.usesAlternatingRowBackgroundColors = true
        tableView.allowsMultipleSelection = true
        tableView.columnAutoresizingStyle = .uniformColumnAutoresizingStyle
        tableView.rowHeight = 28
        tableView.intercellSpacing = NSSize(width: 8, height: 2)
        tableView.headerView = NSTableHeaderView()

        // Configure columns
        configureColumns(tableView: tableView, columns: node.props.tableColumns ?? [])

        // Set data source and delegate
        tableView.dataSource = context.coordinator
        tableView.delegate = context.coordinator

        scrollView.documentView = tableView

        // Apply initial selection
        if let selectedIds = node.props.tableSelection {
            applySelection(tableView: tableView, selectedIds: Set(selectedIds), coordinator: context.coordinator)
        }

        return scrollView
    }

    func updateNSView(_ scrollView: NSScrollView, context: Context) {
        guard let tableView = scrollView.documentView as? NSTableView else { return }
        let coordinator = context.coordinator

        // Update data
        let columns = node.props.tableColumns ?? []
        let numColumns = node.props.numColumns ?? 0
        let rowIds = node.props.rowIds ?? []
        let children = node.children ?? []
        let sortColumn = node.props.tableSortColumn
        let sortAscending = node.props.tableSortAscending ?? true

        coordinator.columns = columns
        coordinator.numColumns = numColumns
        coordinator.rowIds = rowIds
        coordinator.cellNodes = children
        coordinator.nodeId = node.id

        // Update columns if needed
        let existingIds = tableView.tableColumns.map { $0.identifier.rawValue }
        let newIds = columns.map { $0.id }
        if existingIds != newIds {
            // Remove all existing columns
            for col in tableView.tableColumns {
                tableView.removeTableColumn(col)
            }
            configureColumns(tableView: tableView, columns: columns)
        }

        // Update sort indicators
        for tableColumn in tableView.tableColumns {
            if tableColumn.identifier.rawValue == sortColumn {
                tableView.indicatorImage(in: tableColumn)
                tableColumn.sortDescriptorPrototype = NSSortDescriptor(
                    key: tableColumn.identifier.rawValue,
                    ascending: sortAscending
                )
                tableView.setIndicatorImage(
                    NSImage(systemSymbolName: sortAscending ? "chevron.up" : "chevron.down",
                            accessibilityDescription: nil),
                    in: tableColumn
                )
            } else {
                tableView.setIndicatorImage(nil, in: tableColumn)
            }
        }

        // Reload data
        coordinator.isUpdating = true
        tableView.reloadData()

        // Restore selection
        if let selectedIds = node.props.tableSelection {
            applySelection(tableView: tableView, selectedIds: Set(selectedIds), coordinator: coordinator)
        }
        coordinator.isUpdating = false
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(
            nodeId: node.id,
            columns: node.props.tableColumns ?? [],
            numColumns: node.props.numColumns ?? 0,
            rowIds: node.props.rowIds ?? [],
            cellNodes: node.children ?? [],
            onEvent: onEvent
        )
    }

    private func configureColumns(tableView: NSTableView, columns: [ViewNode.TableColumnSpec]) {
        for col in columns {
            let nsCol = NSTableColumn(identifier: NSUserInterfaceItemIdentifier(col.id))
            nsCol.title = col.title
            nsCol.headerToolTip = col.title

            // Apply width
            if let widthSpec = col.width {
                if widthSpec.type == "fixed", let value = widthSpec.value {
                    nsCol.width = value
                    nsCol.minWidth = value
                    nsCol.maxWidth = value
                } else if widthSpec.type == "range" {
                    if let min = widthSpec.min, min > 0 { nsCol.minWidth = min }
                    if let ideal = widthSpec.ideal, ideal > 0 { nsCol.width = ideal }
                    if let max = widthSpec.max, max > 0 { nsCol.maxWidth = max }
                }
            } else {
                nsCol.resizingMask = .autoresizingMask
            }

            // Sort descriptor for sortable columns
            if col.sortable ?? true {
                nsCol.sortDescriptorPrototype = NSSortDescriptor(key: col.id, ascending: true)
            }

            tableView.addTableColumn(nsCol)
        }
    }

    private func applySelection(tableView: NSTableView, selectedIds: Set<String>, coordinator: Coordinator) {
        let indexSet = NSMutableIndexSet()
        for (index, rowId) in coordinator.rowIds.enumerated() {
            if selectedIds.contains(rowId) {
                indexSet.add(index)
            }
        }
        tableView.selectRowIndexes(indexSet as IndexSet, byExtendingSelection: false)
    }
}

// MARK: - Coordinator

extension NibTableView {
    class Coordinator: NSObject, NSTableViewDataSource, NSTableViewDelegate {
        var nodeId: String
        var columns: [ViewNode.TableColumnSpec]
        var numColumns: Int
        var rowIds: [String]
        var cellNodes: [ViewNode]
        let onEvent: (String, String) -> Void
        var isUpdating = false

        // Cache hosting views for cell reuse
        private var hostingViews: [String: NSHostingView<DynamicView>] = [:]

        init(nodeId: String, columns: [ViewNode.TableColumnSpec], numColumns: Int,
             rowIds: [String], cellNodes: [ViewNode],
             onEvent: @escaping (String, String) -> Void) {
            self.nodeId = nodeId
            self.columns = columns
            self.numColumns = numColumns
            self.rowIds = rowIds
            self.cellNodes = cellNodes
            self.onEvent = onEvent
        }

        // MARK: NSTableViewDataSource

        func numberOfRows(in tableView: NSTableView) -> Int {
            return rowIds.count
        }

        func tableView(_ tableView: NSTableView, sortDescriptorsDidChange oldDescriptors: [NSSortDescriptor]) {
            guard let descriptor = tableView.sortDescriptors.first,
                  let key = descriptor.key else { return }
            onEvent(nodeId, "sort:\(key)")
        }

        // MARK: NSTableViewDelegate

        func tableView(_ tableView: NSTableView, viewFor tableColumn: NSTableColumn?, row: Int) -> NSView? {
            guard let colId = tableColumn?.identifier.rawValue,
                  let colIndex = columns.firstIndex(where: { $0.id == colId }) else {
                return nil
            }

            guard numColumns > 0 else { return nil }
            let childIndex = row * numColumns + colIndex
            guard childIndex < cellNodes.count else { return nil }

            let cellNode = cellNodes[childIndex]
            let cellId = "\(row)_\(colIndex)"

            // Create or reuse hosting view
            if let existing = hostingViews[cellId] {
                existing.rootView = DynamicView(node: cellNode, onEvent: onEvent)
                return existing
            }

            let hostingView = NSHostingView(rootView: DynamicView(node: cellNode, onEvent: onEvent))
            hostingViews[cellId] = hostingView
            return hostingView
        }

        func tableView(_ tableView: NSTableView, heightOfRow row: Int) -> CGFloat {
            return 28
        }

        func tableViewSelectionDidChange(_ notification: Notification) {
            guard !isUpdating else { return }
            guard let tableView = notification.object as? NSTableView else { return }

            let selectedIndices = tableView.selectedRowIndexes
            let selectedIds = selectedIndices.compactMap { index -> String? in
                guard index < rowIds.count else { return nil }
                return rowIds[index]
            }
            let idsStr = selectedIds.joined(separator: ",")
            onEvent(nodeId, "selection:\(idsStr)")
        }
    }
}
