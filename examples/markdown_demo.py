"""Markdown Demo - Test Markdown rendering in nib."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

import nib


def main(app: nib.App):
    app.title = "Markdown"
    app.icon = nib.SFSymbol("doc.richtext")
    app.width = 400
    app.height = 500
    app.menu = [
        nib.MenuItem("Quit", action=app.quit),
    ]

    markdown_content = """
# Markdown Demo

This is a **bold** and *italic* text example.

## Features

- Lists work great
- With multiple items
  - And nested items too

### Code

Inline `code` and code blocks:

```python
def hello():
    print("Hello, World!")
```

### Links & More

Visit [Nib Documentation](https://github.com/example/nib) for more info.

> Blockquotes are also supported!

---

| Column 1 | Column 2 |
|----------|----------|
| Cell A   | Cell B   |
| Cell C   | Cell D   |

- [x] Task completed
- [ ] Task pending
"""

    app.build(
        nib.ScrollView(
            [
                nib.VStack(
                    controls=[
                        nib.Markdown(markdown_content),
                    ],
                    padding=20,
                )
            ]
        )
    )


nib.run(main)
