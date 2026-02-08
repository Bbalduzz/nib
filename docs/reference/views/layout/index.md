# Layout

Layout views arrange child views in structured compositions. They control positioning, spacing, alignment, scrolling, and navigation. All layout views inherit from `View` and accept common modifiers such as `width`, `height`, `padding`, `background`, `foreground_color`, `opacity`, `corner_radius`, `font`, `animation`, and more as constructor parameters.

## Stacks

| View | Description |
|------|-------------|
| [VStack](vstack.md) | Arranges children vertically from top to bottom with optional spacing and horizontal alignment. |
| [HStack](hstack.md) | Arranges children horizontally from leading to trailing with optional spacing and vertical alignment. |
| [ZStack](zstack.md) | Overlays children on top of each other along the z-axis for layered compositions. |

## Containers

| View | Description |
|------|-------------|
| [ScrollView](scrollview.md) | A scrollable container that supports vertical, horizontal, or bidirectional scrolling. |
| [List](list.md) | A scrollable column of rows with native list styling and section support. |
| [Section](section.md) | Groups related content with optional header and footer text, typically within a List or Form. |
| [Form](form.md) | A container for grouping data-entry controls with automatic two-column layout on macOS. |
| [Group](group.md) | A transparent container that groups views without adding visual structure. |

## Spacing

| View | Description |
|------|-------------|
| [Spacer](spacer.md) | Flexible space that expands to fill available room within a stack layout. |

## Grids

| View | Description |
|------|-------------|
| [Grid & GridRow](grid.md) | A fixed grid layout with explicit row and column structure. |
| [LazyVGrid & LazyHGrid](lazy-grid.md) | Lazily loaded grid layouts that grow vertically or horizontally. |

## Navigation

| View | Description |
|------|-------------|
| [NavigationStack & NavigationLink](navigation.md) | Hierarchical drill-down navigation with a managed view stack. |
| [DisclosureGroup](disclosure-group.md) | A collapsible section that shows or hides content on demand. |
