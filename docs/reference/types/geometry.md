# Offset & CornerRadius

Nib provides two geometry dataclasses for positioning views and controlling corner rounding.

---

## Offset

The `Offset` dataclass shifts a view from its natural position by the specified x and y amounts. The view still occupies its original space in the layout but is rendered at the offset position.

### Constructor

```python
Offset(x=0, y=0)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `float` | `0` | Horizontal offset in points. Positive values move right. |
| `y` | `float` | `0` | Vertical offset in points. Positive values move down. |

### Usage

Pass an `Offset` to the `offset` modifier parameter on any view.

```python
import nib

# Shift a view 10 points right and 20 points down
nib.Circle(
    fill=nib.Color.BLUE,
    width=50,
    height=50,
    offset=nib.Offset(10, 20),
)
```

### Example: Overlapping circles in a ZStack

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ZStack(
            controls=[
                nib.Circle(fill=nib.Color.RED, width=60, height=60),
                nib.Circle(
                    fill=nib.Color.BLUE.with_opacity(0.7),
                    width=60,
                    height=60,
                    offset=nib.Offset(25, 0),
                ),
                nib.Circle(
                    fill=nib.Color.GREEN.with_opacity(0.7),
                    width=60,
                    height=60,
                    offset=nib.Offset(12, 22),
                ),
            ],
            padding=40,
        )
    )

nib.run(main)
```

---

## CornerRadius

The `CornerRadius` dataclass configures different radii for each corner of a rectangle. It is used with shape views like `Rectangle`, as well as the `corner_radius` modifier on any view.

### Constructor

```python
CornerRadius(top_left=0, top_right=0, bottom_left=0, bottom_right=0)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `top_left` | `float` | `0` | Radius of the top-left corner in points. |
| `top_right` | `float` | `0` | Radius of the top-right corner in points. |
| `bottom_left` | `float` | `0` | Radius of the bottom-left corner in points. |
| `bottom_right` | `float` | `0` | Radius of the bottom-right corner in points. |

### Factory Methods

#### `CornerRadius.all(radius)`

Create a `CornerRadius` where all four corners have the same radius.

```python
cr = nib.CornerRadius.all(10)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `radius` | `float` | Radius to apply to all corners. |

#### `CornerRadius.only(top_left=0, top_right=0, bottom_left=0, bottom_right=0)`

Create a `CornerRadius` with only the specified corners rounded. Unspecified corners default to zero.

```python
cr = nib.CornerRadius.only(top_left=20, top_right=20)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `top_left` | `float` | `0` | Top-left corner radius. |
| `top_right` | `float` | `0` | Top-right corner radius. |
| `bottom_left` | `float` | `0` | Bottom-left corner radius. |
| `bottom_right` | `float` | `0` | Bottom-right corner radius. |

#### `CornerRadius.horizontal(left=0, right=0)`

Create a horizontally symmetric `CornerRadius`. The left side corners share one radius and the right side corners share another.

```python
cr = nib.CornerRadius.horizontal(left=10, right=20)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `left` | `float` | `0` | Radius for `top_left` and `bottom_left`. |
| `right` | `float` | `0` | Radius for `top_right` and `bottom_right`. |

#### `CornerRadius.vertical(top=0, bottom=0)`

Create a vertically symmetric `CornerRadius`. The top corners share one radius and the bottom corners share another.

```python
cr = nib.CornerRadius.vertical(top=15, bottom=0)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `top` | `float` | `0` | Radius for `top_left` and `top_right`. |
| `bottom` | `float` | `0` | Radius for `bottom_left` and `bottom_right`. |

### Instance Methods

#### `.copy(top_left=None, top_right=None, bottom_left=None, bottom_right=None)`

Return a new `CornerRadius` with specified properties overridden. Unspecified values keep their current value.

```python
base = nib.CornerRadius.all(10)
modified = base.copy(bottom_left=0, bottom_right=0)
# Result: top_left=10, top_right=10, bottom_left=0, bottom_right=0
```

#### `.is_uniform()`

Check if all corners have the same radius. Returns `True` if all four values are equal.

```python
nib.CornerRadius.all(10).is_uniform()  # True
nib.CornerRadius.only(top_left=10).is_uniform()  # False
```

### Examples

#### Card with rounded top corners only

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Card Header", font=nib.Font.HEADLINE, padding=12),
                nib.Divider(),
                nib.Text("Card body content goes here.", padding=12),
            ],
            background=nib.Rectangle(
                corner_radius=nib.CornerRadius.vertical(top=12, bottom=0),
                fill="#2A2A2A",
            ),
            width=280,
        )
    )

nib.run(main)
```

#### Asymmetric tab shape

```python
import nib

tab_shape = nib.CornerRadius.only(top_left=12, top_right=12)
nib.Rectangle(
    corner_radius=tab_shape,
    fill=nib.Color.ACCENT,
    width=100,
    height=36,
)
```
