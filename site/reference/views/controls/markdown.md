# Markdown

![Markdown control](../../../assets/img/controls/markdown.png)

A view that renders CommonMark/GitHub Flavored Markdown text natively. Supports headings, bold, italic, strikethrough, inline code, fenced code blocks, links, lists, blockquotes, task lists, tables, and images. The `content` property is reactive -- changing it triggers an immediate UI update.

## Constructor

```python
nib.Markdown(
    content,
    theme=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `content` | `str` | *(required)* | The Markdown string to render. |
| `theme` | `str` | `None` | Optional theme name. Options: `"basic"` (default), `"gitHub"`, `"docC"`. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `foreground_color`, `opacity`, `width`, `height`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `content` | `str` | Get or set the Markdown text. Setting triggers a UI update. |
| `theme` | `str` | Get or set the rendering theme. Setting triggers a UI update. |

## Examples

### Basic markdown rendering

```python
import nib

def main(app: nib.App):
    app.build(
        nib.Markdown(
            """
# Welcome

This is **bold** and *italic* text.

- Item one
- Item two
- Item three

> A blockquote for emphasis.
            """,
            padding=16,
        )
    )

nib.run(main)
```

### Markdown with GitHub theme

```python
import nib

def main(app: nib.App):
    app.build(
        nib.Markdown(
            """
# Project README

## Installation

```bash
pip install mypackage
```

## Usage

| Feature | Status |
|---------|--------|
| Auth    | Done   |
| API     | WIP    |

See the [docs](https://docs.example.com) for more.
            """,
            theme="gitHub",
            padding=16,
            width=400,
        )
    )

nib.run(main)
```

### Reactive markdown content

```python
import nib

def main(app: nib.App):
    md = nib.Markdown("# Counter: 0", padding=16)
    count = [0]

    def increment():
        count[0] += 1
        md.content = f"# Counter: {count[0]}\n\nClicked **{count[0]}** times."

    app.build(
        nib.VStack(controls=[
            md,
            nib.Button("Increment", action=increment),
        ], spacing=8, padding=16)
    )

nib.run(main)
```
