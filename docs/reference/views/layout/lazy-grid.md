# LazyVGrid & LazyHGrid

Lazily loaded grid layouts that grow in one direction. `LazyVGrid` creates a grid that grows vertically with columns defined by `GridItem` specifications. `LazyHGrid` creates a grid that grows horizontally with rows defined by `GridItem` specifications. Views are loaded lazily as they become visible.

## Constructor

```python
nib.LazyVGrid(
    columns=None,
    controls=None,
    spacing=None,
    alignment=None,
    pinned_views=None,
    **modifiers,
)
```

```python
nib.LazyHGrid(
    rows=None,
    controls=None,
    spacing=None,
    alignment=None,
    pinned_views=None,
    **modifiers,
)
```

## Parameters

### LazyVGrid

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `columns` | `list[GridItem]` | required | Column specifications that define the grid layout. |
| `controls` | `list[View]` | `None` | Child views to arrange in the grid. |
| `spacing` | `float` | `None` | Vertical spacing in points between rows. |
| `alignment` | `str` | `None` | Horizontal alignment of grid content. |
| `pinned_views` | `list[str]` | `None` | Views to pin to top/bottom. Options: `"header"`, `"footer"`. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `width`, `height`, etc. |

### LazyHGrid

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `rows` | `list[GridItem]` | required | Row specifications that define the grid layout. |
| `controls` | `list[View]` | `None` | Child views to arrange in the grid. |
| `spacing` | `float` | `None` | Horizontal spacing in points between columns. |
| `alignment` | `str` | `None` | Vertical alignment of grid content. |
| `pinned_views` | `list[str]` | `None` | Views to pin to leading/trailing. Options: `"header"`, `"footer"`. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `width`, `height`, etc. |

## GridItem

`GridItem` defines the sizing strategy for a column (in LazyVGrid) or row (in LazyHGrid).

```python
nib.GridItem(
    size=GridItemSize.FLEXIBLE,
    value=None,
    maximum=None,
    spacing=None,
    alignment=None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `size` | `GridItemSize` | `FLEXIBLE` | Sizing strategy: `FIXED`, `FLEXIBLE`, or `ADAPTIVE`. |
| `value` | `float` | `None` | Size value whose meaning depends on the sizing strategy (see below). |
| `maximum` | `float` | `None` | Maximum size for flexible items. |
| `spacing` | `float` | `None` | Spacing after this column or row. |
| `alignment` | `str` | `None` | Alignment within this column or row. |

### Sizing Strategies

| Strategy | Behavior | `value` meaning |
|----------|----------|-----------------|
| `GridItemSize.FIXED` | Exact size, does not grow or shrink. | Exact size in points. |
| `GridItemSize.FLEXIBLE` | Expands to fill available space. | Minimum size in points. |
| `GridItemSize.ADAPTIVE` | Fits as many items as possible. | Minimum item size in points. |

### Convenience Constructors

```python
from nib import fixed, flexible, adaptive

fixed(size, spacing=None)       # Fixed-size column/row
flexible(minimum=10, maximum=None, spacing=None)  # Flexible column/row
adaptive(minimum, maximum=None, spacing=None)      # Adaptive column/row
```

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `controls` | `list[View]` | Get or set the child views. Setting triggers a UI update. |
| `columns` | `list[GridItem]` | (LazyVGrid) Get or set column specifications. Setting triggers a UI update. |
| `rows` | `list[GridItem]` | (LazyHGrid) Get or set row specifications. Setting triggers a UI update. |

## Examples

### Three-column grid

```python
import nib

def main(app: nib.App):
    app.build(
        nib.LazyVGrid(
            columns=[
                nib.GridItem(nib.GridItemSize.FLEXIBLE),
                nib.GridItem(nib.GridItemSize.FLEXIBLE),
                nib.GridItem(nib.GridItemSize.FLEXIBLE),
            ],
            controls=[
                nib.Rectangle(
                    corner_radius=8,
                    fill=f"#{i * 30 + 40:02x}{i * 20 + 60:02x}FF",
                    height=80,
                )
                for i in range(9)
            ],
            spacing=10,
            padding=16,
        )
    )

nib.run(main)
```

### Adaptive grid

The grid automatically fits as many columns as possible, each at least 100 points wide.

```python
import nib

def main(app: nib.App):
    items = [f"Item {i}" for i in range(12)]

    app.build(
        nib.LazyVGrid(
            columns=[nib.adaptive(100)],
            controls=[
                nib.Text(
                    item,
                    padding=12,
                    background="#2a2a2a",
                    corner_radius=8,
                )
                for item in items
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```

### Horizontal grid with fixed rows

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ScrollView(
            controls=[
                nib.LazyHGrid(
                    rows=[
                        nib.GridItem(nib.GridItemSize.FIXED, 50),
                        nib.GridItem(nib.GridItemSize.FIXED, 50),
                    ],
                    controls=[
                        nib.Text(f"Cell {i}", padding=8, background="#333333", corner_radius=4)
                        for i in range(20)
                    ],
                    spacing=10,
                ),
            ],
            axes="horizontal",
            padding=16,
        )
    )

nib.run(main)
```
