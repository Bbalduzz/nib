import SwiftUI
import AppKit

// MARK: - ShareLink Builder

extension DynamicView {
    @ViewBuilder
    func buildShareLink() -> some View {
        let items = node.props.items ?? []
        let label = node.props.label
        let icon = node.props.icon
        let hasCustomContent = node.children != nil && !node.children!.isEmpty

        if #available(macOS 13.0, *) {
            if items.count == 1, let item = items.first {
                if hasCustomContent, let children = node.children, let firstChild = children.first {
                    // Custom view label
                    ShareLink(item: item) {
                        DynamicView(node: firstChild, onEvent: onEvent)
                    }
                } else if let labelText = label {
                    if let iconName = icon {
                        ShareLink(item: item) {
                            Label(labelText, systemImage: iconName)
                        }
                    } else {
                        ShareLink(item: item) {
                            Text(labelText)
                        }
                    }
                } else {
                    ShareLink(item: item)
                }
            } else {
                // Multiple items - share as array of strings
                if hasCustomContent, let children = node.children, let firstChild = children.first {
                    // Custom view label
                    ShareLink(items: items) {
                        DynamicView(node: firstChild, onEvent: onEvent)
                    }
                } else if let labelText = label {
                    if let iconName = icon {
                        ShareLink(items: items) {
                            Label(labelText, systemImage: iconName)
                        }
                    } else {
                        ShareLink(items: items) {
                            Text(labelText)
                        }
                    }
                } else {
                    ShareLink(items: items)
                }
            }
        } else {
            // Fallback for older macOS
            if hasCustomContent, let children = node.children, let firstChild = children.first {
                Button(action: {
                    let picker = NSSharingServicePicker(items: items)
                    if let contentView = NSApp.keyWindow?.contentView {
                        picker.show(relativeTo: .zero, of: contentView, preferredEdge: .minY)
                    }
                }) {
                    DynamicView(node: firstChild, onEvent: onEvent)
                }
            } else {
                Button(label ?? "Share") {
                    let picker = NSSharingServicePicker(items: items)
                    if let contentView = NSApp.keyWindow?.contentView {
                        picker.show(relativeTo: .zero, of: contentView, preferredEdge: .minY)
                    }
                }
            }
        }
    }
}
