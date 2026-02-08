# Gauge

![Gauge control](../../../assets/img/controls/gauge.png)

A view that displays a value within a bounded range, ideal for showing battery levels, CPU usage, memory consumption, or any bounded numeric measurement. Gauge supports multiple visual styles and accepts either strings or custom views for its labels.

## Constructor

```python
nib.Gauge(
    value=0.0,
    min_value=0.0,
    max_value=1.0,
    label=None,
    current_value_label=None,
    min_value_label=None,
    max_value_label=None,
    style=GaugeStyle.AUTOMATIC,
    tint=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `float` | `0.0` | Current gauge value. |
| `min_value` | `float` | `0.0` | Minimum value of the range. |
| `max_value` | `float` | `1.0` | Maximum value of the range. |
| `label` | `str \| View` | `None` | Label describing the gauge. Accepts a plain string or a custom `View`. |
| `current_value_label` | `str \| View` | `None` | Label showing the current value. Accepts a plain string or a custom `View`. |
| `min_value_label` | `str \| View` | `None` | Label for the minimum end of the range. Accepts a plain string or a custom `View`. |
| `max_value_label` | `str \| View` | `None` | Label for the maximum end of the range. Accepts a plain string or a custom `View`. |
| `style` | `str` | `GaugeStyle.AUTOMATIC` | Gauge style. Options: `GaugeStyle.AUTOMATIC`, `GaugeStyle.LINEAR_CAPACITY`, `GaugeStyle.CIRCULAR_CAPACITY`, `GaugeStyle.ACCESSORY_LINEAR`, `GaugeStyle.ACCESSORY_LINEAR_CAPACITY`, `GaugeStyle.ACCESSORY_CIRCULAR`, `GaugeStyle.ACCESSORY_CIRCULAR_CAPACITY`. |
| `tint` | `Color \| str` | `None` | Tint color for the gauge fill. Accepts a `Color` enum or hex string. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `opacity`, `width`, `height`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `value` | `float` | Get or set the current gauge value. Triggers a UI update. |
| `label` | `str \| View` | Get or set the gauge label. |
| `current_value_label` | `str \| View` | Get or set the current value label. |
| `min_value_label` | `str \| View` | Get or set the minimum value label. |
| `max_value_label` | `str \| View` | Get or set the maximum value label. |
| `style` | `str` | Get or set the gauge style. |
| `tint` | `Color \| str` | Get or set the tint color. |

## Examples

### Simple battery gauge

```python
import nib

def main(app: nib.App):
    app.build(
        nib.Gauge(
            value=0.75,
            label="Battery",
            current_value_label="75%",
            style=nib.GaugeStyle.LINEAR_CAPACITY,
            tint=nib.Color.GREEN,
            padding=16,
        )
    )

nib.run(main)
```

### Circular gauge with view labels

```python
import nib

def main(app: nib.App):
    cpu_usage = 62

    app.build(
        nib.Gauge(
            value=cpu_usage / 100,
            label=nib.Label("CPU", icon="cpu"),
            current_value_label=nib.Text(f"{cpu_usage}%",
                                          font=nib.Font.HEADLINE),
            min_value_label=nib.Image(system_name="tortoise"),
            max_value_label=nib.Image(system_name="hare"),
            style=nib.GaugeStyle.ACCESSORY_CIRCULAR,
            tint=nib.Color.BLUE,
            padding=16,
        )
    )

nib.run(main)
```

### Download progress gauge

```python
import nib

def main(app: nib.App):
    progress = 0.4

    app.build(
        nib.Gauge(
            value=progress,
            label="Download",
            current_value_label=f"{int(progress * 100)}%",
            min_value_label="0%",
            max_value_label="100%",
            style=nib.GaugeStyle.LINEAR_CAPACITY,
            tint=nib.Color.BLUE,
            padding=16,
            width=250,
        )
    )

nib.run(main)
```
