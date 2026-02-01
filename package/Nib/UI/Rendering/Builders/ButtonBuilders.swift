import SwiftUI

// MARK: - Button View Builders

extension DynamicView {
    @ViewBuilder
    func buildButton() -> some View {
        let styles = node.props.buttonStyles

        // Build button - supports custom content via children or simple label/icon
        let button = Button(role: ButtonRole.nib(styles?.role), action: {
            onEvent(node.id, "tap")
        }) {
            // Check if custom content is provided via children
            if let children = node.children, !children.isEmpty {
                // Render custom content
                ForEach(children) { child in
                    DynamicView(node: child, onEvent: onEvent)
                }
            } else if let icon = node.props.icon {
                // Simple label with icon
                Label(node.props.label ?? "", systemImage: icon)
            } else {
                // Simple text label
                Text(node.props.label ?? "")
            }
        }

        // Apply button styling
        button.applyButtonStyles(styles)
    }

    @ViewBuilder
    func buildToggle() -> some View {
        // Check for custom content
        if let children = node.children, !children.isEmpty {
            StatefulToggleWithContent(
                isOn: node.props.isOn ?? false,
                styles: node.props.toggleStyles,
                nodeId: node.id,
                onEvent: onEvent
            ) {
                ForEach(children) { child in
                    DynamicView(node: child, onEvent: onEvent)
                }
            }
        } else {
            StatefulToggle(
                label: node.props.label ?? "",
                isOn: node.props.isOn ?? false,
                styles: node.props.toggleStyles,
                nodeId: node.id,
                onEvent: onEvent
            )
        }
    }
}

// MARK: - Button Styling

extension View {
    @ViewBuilder
    func applyButtonStyles(_ styles: ViewNode.ButtonStyles?) -> some View {
        if let styles = styles {
            self
                .applyButtonStyle(styles)
                .applyButtonBorderShape(styles)
                .applyControlSize(styles)
                .applyButtonTint(styles)
                .applyLabelStyle(styles)
                .applyButtonDisabled(styles)
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyButtonStyle(_ styles: ViewNode.ButtonStyles) -> some View {
        if let style = styles.style {
            switch style.lowercased() {
            case "bordered":
                self.buttonStyle(.bordered)
            case "borderedprominent":
                self.buttonStyle(.borderedProminent)
            case "borderless":
                self.buttonStyle(.borderless)
            case "plain":
                self.buttonStyle(.plain)
            case "link":
                self.buttonStyle(.link)
            default:
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyButtonBorderShape(_ styles: ViewNode.ButtonStyles) -> some View {
        if #available(macOS 14.0, *) {
            if let shape = styles.borderShape {
                switch shape.lowercased() {
                case "capsule":
                    self.buttonBorderShape(.capsule)
                case "roundedrectangle":
                    if let radius = styles.cornerRadius {
                        self.buttonBorderShape(.roundedRectangle(radius: radius))
                    } else {
                        self.buttonBorderShape(.roundedRectangle)
                    }
                case "circle":
                    self.buttonBorderShape(.circle)
                default:
                    self
                }
            } else {
                self
            }
        } else {
            // buttonBorderShape requires macOS 14.0+
            self
        }
    }

    @ViewBuilder
    private func applyControlSize(_ styles: ViewNode.ButtonStyles) -> some View {
        if let size = styles.controlSize {
            switch size.lowercased() {
            case "mini":
                self.controlSize(.mini)
            case "small":
                self.controlSize(.small)
            case "regular":
                self.controlSize(.regular)
            case "large":
                self.controlSize(.large)
            case "extralarge":
                if #available(macOS 14.0, *) {
                    self.controlSize(.extraLarge)
                } else {
                    self
                }
            default:
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyButtonTint(_ styles: ViewNode.ButtonStyles) -> some View {
        if let tint = styles.tint {
            self.tint(Color(nibColor: tint))
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyLabelStyle(_ styles: ViewNode.ButtonStyles) -> some View {
        if let style = styles.labelStyle {
            switch style.lowercased() {
            case "icononly":
                self.labelStyle(.iconOnly)
            case "titleonly":
                self.labelStyle(.titleOnly)
            case "titleandicon":
                self.labelStyle(.titleAndIcon)
            default:
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyButtonDisabled(_ styles: ViewNode.ButtonStyles) -> some View {
        if styles.disabled == true {
            self.disabled(true)
        } else {
            self
        }
    }
}

// MARK: - Toggle Styling

extension View {
    @ViewBuilder
    func applyToggleStyles(_ styles: ViewNode.ToggleStyles?) -> some View {
        if let styles = styles {
            self
                .applyToggleStyle(styles)
                .applyToggleTint(styles.tint)
                .applyToggleDisabled(styles.disabled)
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyToggleStyle(_ styles: ViewNode.ToggleStyles) -> some View {
        if let style = styles.style {
            switch style.lowercased() {
            case "switch":
                self.toggleStyle(.switch)
            case "button":
                self.toggleStyle(.button)
            case "checkbox":
                self.toggleStyle(.checkbox)
            default:
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyToggleTint(_ tint: String?) -> some View {
        if let tint = tint {
            self.tint(Color(nibColor: tint))
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyToggleDisabled(_ disabled: Bool?) -> some View {
        if disabled == true {
            self.disabled(true)
        } else {
            self
        }
    }
}

// MARK: - Type Conversions

extension ButtonRole {
    static func nib(_ value: String?) -> ButtonRole? {
        switch value?.lowercased() {
        case "destructive": return .destructive
        case "cancel": return .cancel
        default: return nil
        }
    }
}
