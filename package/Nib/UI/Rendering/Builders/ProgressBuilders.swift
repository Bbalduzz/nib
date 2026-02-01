import SwiftUI

// MARK: - Progress View Builders

extension DynamicView {
    @ViewBuilder
    func buildProgressView() -> some View {
        let styles = node.props.progressStyles

        Group {
            if let progress = node.props.progress {
                if let label = node.props.label {
                    ProgressView(label, value: progress)
                } else {
                    ProgressView(value: progress)
                }
            } else {
                if let label = node.props.label {
                    ProgressView(label)
                } else {
                    ProgressView()
                }
            }
        }
        .applyProgressStyles(styles)
    }
}

// MARK: - ProgressView Styling

extension View {
    @ViewBuilder
    func applyProgressStyles(_ styles: ViewNode.ProgressStyles?) -> some View {
        if let styles = styles {
            self
                .applyProgressStyle(styles)
                .applyProgressTint(styles.tint)
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyProgressStyle(_ styles: ViewNode.ProgressStyles) -> some View {
        if let style = styles.style {
            switch style.lowercased() {
            case "linear":
                self.progressViewStyle(.linear)
            case "circular":
                self.progressViewStyle(.circular)
            default:
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyProgressTint(_ tint: String?) -> some View {
        if let tint = tint {
            self.tint(Color(nibColor: tint))
        } else {
            self
        }
    }
}
