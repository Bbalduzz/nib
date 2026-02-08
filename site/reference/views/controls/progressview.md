# ProgressView

![ProgressView control](../../../assets/img/controls/progressview.png)

A view that shows the progress of an ongoing task. When `value` is `None`, an indeterminate spinner is displayed. When `value` is provided, a determinate progress bar shows the completion percentage as `value / total`.

## Constructor

```python
nib.ProgressView(
    value=None,
    total=1.0,
    label="",
    style=None,
    tint=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `float \| None` | `None` | Current progress value. When `None`, displays an indeterminate spinner. When set, shows a progress bar filled to `value / total`. |
| `total` | `float` | `1.0` | Maximum value representing 100% completion. Set to `100` for percentage values or the actual total for counts. |
| `label` | `str` | `""` | Optional text label displayed alongside the progress indicator. |
| `style` | `ProgressStyle \| str` | `None` | Visual style. Options: `ProgressStyle.automatic`, `ProgressStyle.linear` (horizontal bar), `ProgressStyle.circular` (ring indicator). |
| `tint` | `Color \| str` | `None` | Tint color for the progress indicator fill. Accepts a `Color` enum, hex string, or RGB tuple. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `opacity`, `width`, `height`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `value` | `float \| None` | Get or set the progress value. Set to `None` for indeterminate mode. Triggers a UI update. |
| `progress` | `float \| None` | Get or set the progress as a fraction (0.0 to 1.0). Internally converts using `total`. |
| `total` | `float` | Get or set the total value. Triggers a UI update. |
| `label` | `str` | Get or set the progress label. Triggers a UI update. |

## Examples

### Indeterminate loading spinner

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(controls=[
            nib.ProgressView(),
            nib.Text("Loading..."),
        ], spacing=8, padding=16)
    )

nib.run(main)
```

### Determinate download progress

```python
import nib
import threading, time

def main(app: nib.App):
    progress = nib.ProgressView(
        value=0,
        total=100,
        label="Downloading...",
        style=nib.ProgressStyle.linear,
        tint=nib.Color.BLUE,
        width=250,
    )

    def simulate_download():
        for i in range(101):
            progress.value = i
            progress.label = f"Downloading... {i}%"
            time.sleep(0.05)
        progress.label = "Complete!"

    threading.Thread(target=simulate_download, daemon=True).start()

    app.build(
        nib.VStack(controls=[progress], padding=20)
    )

nib.run(main)
```

### Circular progress indicator

```python
import nib

def main(app: nib.App):
    app.build(
        nib.HStack(controls=[
            nib.ProgressView(
                value=3,
                total=10,
                style=nib.ProgressStyle.circular,
                tint=nib.Color.GREEN,
            ),
            nib.Text("3 of 10 tasks complete"),
        ], spacing=12, padding=16)
    )

nib.run(main)
```
