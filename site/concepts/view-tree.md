# View Tree

Every Nib UI is a tree of views. A root view contains children, which contain more children, forming a hierarchy that describes your entire interface. This tree is serialized and sent to Swift for rendering.

## The View Base Class

All UI elements in Nib inherit from the `View` base class. Each view has:

- A **type** (`_type`) -- the SwiftUI view it maps to (e.g., `"Text"`, `"VStack"`, `"Button"`).
- **Properties** (`_get_props()`) -- view-specific data like text content, slider value, or toggle state.
- **Modifiers** (`_modifiers`) -- a list of styling instructions (padding, color, font, etc.).
- **Children** -- other views nested inside containers.
- An **ID** (`_id`) -- a position-based identifier assigned during tree traversal.

```python
import nib

# A simple view tree
root = nib.VStack(
    controls=[
        nib.Text("Hello", font=nib.Font.TITLE),
        nib.HStack(
            controls=[
                nib.Button("OK", action=confirm),
                nib.Button("Cancel", action=cancel),
            ],
            spacing=8,
        ),
    ],
    spacing=12,
    padding=16,
)

app.build(root)
```

## View Categories

Nib provides views across several categories:

**Controls** -- Interactive and display elements: `Text`, `Button`, `TextField`, `SecureField`, `Toggle`, `Slider`, `Picker`, `DatePicker`, `ColorPicker`, `ProgressView`, `Gauge`, `Label`, `Link`, `Image`, `Video`, `Markdown`, `Map`, `WebView`, `Table`, `TextEditor`, `ShareLink`, `CameraPreview`.

**Layout containers** -- Views that arrange children: `VStack`, `HStack`, `ZStack`, `ScrollView`, `List`, `Section`, `Form`, `Group`, `Spacer`, `Divider`, `NavigationStack`, `NavigationLink`, `DisclosureGroup`, `Grid`, `LazyVGrid`, `LazyHGrid`.

**Shapes** -- Geometric primitives: `Rectangle`, `Circle`, `Ellipse`, `Capsule`, `Path`. Also gradient fills: `LinearGradient`, `RadialGradient`, `AngularGradient`, `EllipticalGradient`.

**Charts** -- Data visualization: `Chart`, `LineMark`, `BarMark`, `AreaMark`, `PointMark`, `RuleMark`, `RectMark`, `SectorMark`.

**Effects** -- Visual effects: `VisualEffectBlur`.

**Canvas** -- Core Graphics drawing surface: `Canvas` with drawing commands from `nib.draw`.

## Children: `controls=` and `content=`

Container views use the `controls=` parameter for their list of children:

```python
nib.VStack(
    controls=[
        nib.Text("Item 1"),
        nib.Text("Item 2"),
        nib.Text("Item 3"),
    ],
    spacing=4,
)
```

Single-child wrapper views (like `Button`, `Link`, `Toggle`) use the `content=` parameter:

```python
# Button with custom content
nib.Button(
    content=nib.HStack(
        controls=[
            nib.SFSymbol("star.fill"),
            nib.Text("Favorite"),
        ],
        spacing=4,
    ),
    action=toggle_favorite,
)
```

!!! info "controls vs content"
    `controls=` is for containers that hold multiple children (stacks, lists, grids). `content=` is for views that wrap a single child view. Some views like `Button` accept both a `label` string for simple cases and `content` for custom layouts.

## Position-Based IDs

Every view gets a position-based ID during tree traversal. The root view is `"0"`. Its first child is `"0.0"`, the second child is `"0.1"`, and so on. Nested children continue the pattern: `"0.1.2"` is the third child of the second child of the root.

```
VStack "0"
  +-- Text "0.0"         ("Hello")
  +-- HStack "0.1"
        +-- Button "0.1.0"  ("OK")
        +-- Button "0.1.1"  ("Cancel")
```

These IDs serve two purposes:

1. **Stable identity** -- Swift uses IDs to match old and new views during re-renders, enabling smooth transitions and state preservation.
2. **Event routing** -- When Swift sends an event (e.g., a button tap), it includes the node ID so Python can look up and call the correct callback.

IDs are assigned automatically by `App._collect_actions()` during each render. You never need to set them manually.

## Flat Node Serialization

When the view tree is sent to Swift, it is serialized as a **flat list of nodes** rather than a nested tree structure. Each node carries a `parentId` and `childIds` instead of nested children. This design was chosen to prevent stack overflow in the Swift runtime when decoding deeply nested trees.

```python
# Conceptual flat node structure (internal, not user-facing)
[
    {"id": "0",   "type": "VStack",  "parentId": None, "childIds": ["0.0", "0.1"]},
    {"id": "0.0", "type": "Text",    "parentId": "0",  "childIds": None},
    {"id": "0.1", "type": "HStack",  "parentId": "0",  "childIds": ["0.1.0", "0.1.1"]},
    {"id": "0.1.0", "type": "Button", "parentId": "0.1", "childIds": None},
    {"id": "0.1.1", "type": "Button", "parentId": "0.1", "childIds": None},
]
```

The `to_flat_list()` method on `View` performs this serialization iteratively using an explicit stack, avoiding Python recursion limits as well.

## Depth Limit

View trees are limited to a maximum depth of **100 levels**. If your tree exceeds this, Nib raises a `NibDepthError`:

```
NibDepthError: View tree exceeds maximum depth of 100 (current: 101).
Simplify your view hierarchy or check for unintended nesting.
```

This limit exists to protect against:

- Accidental infinite nesting (e.g., a view including itself).
- Stack overflow in the Swift runtime during rendering.
- Performance degradation from excessively deep layouts.

In practice, menu bar app UIs rarely exceed 10-20 levels of nesting.

!!! tip "Flattening deep hierarchies"
    If you are dynamically generating views and hitting the depth limit, restructure your layout. Use `ScrollView` with a flat `VStack` instead of deeply nested groups. Use `List` for large collections instead of nesting stacks.

## Visibility

Any view can be hidden by setting `visible=False`:

```python
error_message = nib.Text(
    "Something went wrong",
    foreground_color=nib.Color.RED,
    visible=False,
)

def show_error():
    error_message.visible = True

def hide_error():
    error_message.visible = False
```

When `visible=False`, the view is completely removed from the serialized tree. It does not take up layout space. This is different from `opacity=0`, which hides the view visually but still reserves its space in the layout.

## Background and Overlay Views

Any view can have a `background` or `overlay` that is itself a view. These are serialized as separate nodes in the flat list, linked by `backgroundId` and `overlayId`:

```python
nib.VStack(
    controls=[nib.Text("Content")],
    background=nib.Rectangle(
        corner_radius=12,
        fill="#1a1a2e",
        stroke="#2a2a4e",
        stroke_width=1,
    ),
    padding=16,
)
```

The background view is rendered behind the main view. The overlay view is rendered on top.

## Serialization Format

Each node in the flat list contains:

| Field | Type | Description |
|---|---|---|
| `id` | string | Position-based identifier |
| `type` | string | SwiftUI view type name |
| `props` | dict | View-specific properties |
| `modifiers` | list or null | Styling modifiers |
| `parentId` | string or null | ID of parent node |
| `childIds` | list or null | IDs of child nodes |
| `backgroundId` | string or null | ID of background view node |
| `overlayId` | string or null | ID of overlay view node |
| `animationContext` | dict or null | Per-view animation configuration |
