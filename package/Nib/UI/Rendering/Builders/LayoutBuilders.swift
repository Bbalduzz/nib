import SwiftUI

// MARK: - Layout View Builders

extension DynamicView {
    @ViewBuilder
    func buildVStack() -> some View {
        VStack(
            alignment: HorizontalAlignment(nibAlignment: node.props.alignment),
            spacing: node.props.spacing
        ) {
            childViews
        }
    }

    @ViewBuilder
    func buildHStack() -> some View {
        HStack(
            alignment: VerticalAlignment(nibAlignment: node.props.alignment),
            spacing: node.props.spacing
        ) {
            childViews
        }
    }

    @ViewBuilder
    func buildZStack() -> some View {
        ZStack(alignment: Alignment(nibAlignment: node.props.alignment)) {
            childViews
        }
    }

    @ViewBuilder
    func buildSpacer() -> some View {
        if let minLength = node.props.minLength {
            Spacer(minLength: minLength)
        } else {
            Spacer()
        }
    }
}

// MARK: - List & Collection Builders

extension DynamicView {
    @ViewBuilder
    func buildList() -> some View {
        List {
            childViews
        }
    }

    @ViewBuilder
    func buildScrollView() -> some View {
        let axes = scrollAxes(from: node.props.axes)
        let showsIndicators = node.props.showsIndicators ?? true

        ScrollView(axes, showsIndicators: showsIndicators) {
            if axes == .horizontal {
                HStack { childViews }
            } else {
                VStack { childViews }
            }
        }
    }

    @ViewBuilder
    func buildForEach() -> some View {
        // ForEach requires children - iterate through them
        ForEach(node.children ?? []) { child in
            DynamicView(node: child, onEvent: onEvent)
        }
    }

    @ViewBuilder
    func buildSection() -> some View {
        Section {
            childViews
        } header: {
            if let header = node.props.header {
                Text(header)
            }
        } footer: {
            if let footer = node.props.footer {
                Text(footer)
            }
        }
    }

    @ViewBuilder
    func buildGroup() -> some View {
        Group {
            childViews
        }
    }

    @ViewBuilder
    func buildForm() -> some View {
        let style = node.props.formStyle ?? "columns"

        switch style.lowercased() {
        case "grouped":
            Form {
                childViews
            }
            .formStyle(.grouped)
        case "columns":
            Form {
                childViews
            }
            .formStyle(.columns)
        default:
            // automatic - let system decide
            Form {
                childViews
            }
        }
    }

    private func scrollAxes(from axes: String?) -> Axis.Set {
        switch axes?.lowercased() {
        case "horizontal":
            return .horizontal
        case "both":
            return [.horizontal, .vertical]
        default:
            return .vertical
        }
    }
}

// MARK: - Navigation Builders

extension DynamicView {
    @ViewBuilder
    func buildNavigationStack() -> some View {
        NavigationStack {
            VStack {
                childViews
            }
        }
    }

    @ViewBuilder
    func buildNavigationLink() -> some View {
        NavigationLink {
            if let children = node.children, !children.isEmpty {
                VStack {
                    ForEach(children) { child in
                        DynamicView(node: child, onEvent: onEvent)
                    }
                }
            } else {
                Text(node.props.destination ?? "")
            }
        } label: {
            Text(node.props.label ?? "")
        }
    }

    @ViewBuilder
    func buildDisclosureGroup() -> some View {
        let children = node.children ?? []
        StatefulDisclosureGroup(
            label: node.props.label ?? "",
            isExpanded: node.props.isExpanded ?? false,
            nodeId: node.id,
            onEvent: onEvent
        ) {
            ForEach(children) { child in
                DynamicView(node: child, onEvent: onEvent)
            }
        }
    }
}
