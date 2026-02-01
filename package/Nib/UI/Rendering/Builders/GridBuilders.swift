import SwiftUI

// MARK: - Grid Builder

extension DynamicView {
    @ViewBuilder
    func buildGrid() -> some View {
        let alignment = Alignment(nibAlignment: node.props.alignment)
        let hSpacing = node.props.horizontalSpacing
        let vSpacing = node.props.verticalSpacing

        Grid(alignment: alignment, horizontalSpacing: hSpacing, verticalSpacing: vSpacing) {
            if let children = node.children {
                ForEach(children, id: \.id) { child in
                    DynamicView(node: child, onEvent: onEvent)
                }
            }
        }
    }

    @ViewBuilder
    func buildGridRow() -> some View {
        let alignment = VerticalAlignment(nibAlignment: node.props.alignment)

        GridRow(alignment: alignment) {
            if let children = node.children {
                ForEach(children, id: \.id) { child in
                    DynamicView(node: child, onEvent: onEvent)
                }
            }
        }
    }

    @ViewBuilder
    func buildLazyVGrid() -> some View {
        let columns = parseGridItems(node.props.columns)
        let spacing = node.props.spacing
        let alignment = HorizontalAlignment(nibAlignment: node.props.alignment)
        let pinnedViews = parsePinnedViews(node.props.pinnedViews)

        LazyVGrid(columns: columns, alignment: alignment, spacing: spacing, pinnedViews: pinnedViews) {
            if let children = node.children {
                ForEach(children, id: \.id) { child in
                    DynamicView(node: child, onEvent: onEvent)
                }
            }
        }
    }

    @ViewBuilder
    func buildLazyHGrid() -> some View {
        let rows = parseGridItems(node.props.rows)
        let spacing = node.props.spacing
        let alignment = VerticalAlignment(nibAlignment: node.props.alignment)
        let pinnedViews = parsePinnedViews(node.props.pinnedViews)

        LazyHGrid(rows: rows, alignment: alignment, spacing: spacing, pinnedViews: pinnedViews) {
            if let children = node.children {
                ForEach(children, id: \.id) { child in
                    DynamicView(node: child, onEvent: onEvent)
                }
            }
        }
    }

    private func parseGridItems(_ specs: [ViewNode.GridItemSpec]?) -> [GridItem] {
        guard let specs = specs else {
            return [GridItem(.flexible())]
        }

        return specs.map { spec in
            let size: GridItem.Size
            switch spec.size {
            case "fixed":
                size = .fixed(spec.value ?? 100)
            case "adaptive":
                if let max = spec.maximum {
                    size = .adaptive(minimum: spec.value ?? 80, maximum: max)
                } else {
                    size = .adaptive(minimum: spec.value ?? 80)
                }
            case "flexible":
                fallthrough
            default:
                if let max = spec.maximum {
                    size = .flexible(minimum: spec.value ?? 10, maximum: max)
                } else {
                    size = .flexible(minimum: spec.value ?? 10)
                }
            }

            var item = GridItem(size, spacing: spec.spacing)
            if let alignmentStr = spec.alignment {
                item.alignment = Alignment(nibAlignment: alignmentStr)
            }
            return item
        }
    }

    private func parsePinnedViews(_ views: [String]?) -> PinnedScrollableViews {
        guard let views = views else { return [] }

        var result: PinnedScrollableViews = []
        for view in views {
            switch view.lowercased() {
            case "header", "sectionheaders":
                result.insert(.sectionHeaders)
            case "footer", "sectionfooters":
                result.insert(.sectionFooters)
            default:
                break
            }
        }
        return result
    }
}
