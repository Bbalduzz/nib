import nib


def main(app: nib.App):
    app.title = "Markdown"
    app.icon = nib.SFSymbol("doc.richtext")
    app.width = 350
    app.height = 400

    app.build(
        nib.ScrollView(
            controls=[
                nib.Markdown(
                    content="""\
# Markdown Preview

This is a **bold** and *italic* text example.

## Lists

- First item
- Second item
- Third item

## Code

Inline `code` and a block:

```python
def hello():
    print("Hello, world!")
```

## Links

Visit [example.com](https://example.com) for more.

---

> This is a blockquote.
""",
                ),
            ],
            padding=20,
        )
    )


nib.run(main)
