"""Canvas image drawing example.

Demonstrates loading and displaying images on a Canvas.
"""

import nib
from pathlib import Path


def main(app: nib.App):
    app.title = "Canvas Image"
    app.width = 400
    app.height = 300

    canvas = nib.Canvas(width=400, height=300, background_color="#1a1a1a")

    # Load image from file (simplest approach - no dependencies)
    image_path = Path(__file__).parent / "sample.jpg"

    if image_path.exists():
        with open(image_path, "rb") as f:
            image_data = f.read()

        canvas.draw([
            nib.draw.Image(data=image_data, x=20, y=20, width=360, height=260),
        ])
    else:
        # No image available - show placeholder with shapes
        canvas.draw([
            nib.draw.Rect(x=20, y=20, width=360, height=260, fill="#333333", corner_radius=8),
            nib.draw.Text(
                content="Place sample.jpg in examples/",
                x=200, y=150,
                fill="#888888",
                font={"size": 14},
                alignment="center",
            ),
        ])

    app.build(
        nib.VStack(
            controls=[canvas],
            padding=16,
        )
    )


nib.run(main)
