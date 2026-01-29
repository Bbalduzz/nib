import SwiftUI

// MARK: - Layout Modifiers

extension View {
    @ViewBuilder
    func applyFrame(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        self
            .frame(
                minWidth: args.minWidth,
                maxWidth: args.maxWidth == "infinity" ? .infinity : args.width.map { CGFloat($0) },
                minHeight: args.minHeight,
                maxHeight: args.maxHeight == "infinity" ? .infinity : args.height.map { CGFloat($0) }
            )
            .frame(
                width: args.maxWidth == nil ? args.width : nil,
                height: args.maxHeight == nil ? args.height : nil
            )
    }

    @ViewBuilder
    func applyPadding(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let value = args.value {
            self.padding(value)
        } else if args.horizontal != nil || args.vertical != nil {
            self
                .padding(.horizontal, args.horizontal ?? 0)
                .padding(.vertical, args.vertical ?? 0)
        } else {
            self.padding(EdgeInsets(
                top: args.top ?? 0,
                leading: args.leading ?? 0,
                bottom: args.bottom ?? 0,
                trailing: args.trailing ?? 0
            ))
        }
    }

    /// Apply margin (outer padding, applied after background)
    /// Margin uses the same implementation as padding but is positioned differently in the modifier chain
    @ViewBuilder
    func applyMargin(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let value = args.value {
            self.padding(value)
        } else if args.horizontal != nil || args.vertical != nil {
            self
                .padding(.horizontal, args.horizontal ?? 0)
                .padding(.vertical, args.vertical ?? 0)
        } else {
            self.padding(EdgeInsets(
                top: args.top ?? 0,
                leading: args.leading ?? 0,
                bottom: args.bottom ?? 0,
                trailing: args.trailing ?? 0
            ))
        }
    }

    @ViewBuilder
    func applyCornerRadius(_ args: ViewNode.ViewModifier.ModifierArgs) -> some View {
        if let radius = args.value {
            self.cornerRadius(radius)
        } else {
            self
        }
    }
}
