"""Canvas Demo - Core Graphics drawing in nib.

This example demonstrates the Canvas view with declarative drawing commands.
"""

import nib


def main(app: nib.App):
    app.title = "Canvas"
    app.icon = nib.SFSymbol("paintbrush.pointed")
    app.width = 420
    app.height = 380

    # Create canvas with initial drawing
    canvas = nib.Canvas(width=400, height=320, background_color="#1a1a1a")

    canvas.draw(
        [
            # Rectangle with rounded corners
            nib.draw.Rect(
                x=20, y=20, width=120, height=80, fill="#3498db", corner_radius=10
            ),
            # Circle
            nib.draw.Circle(cx=320, cy=60, radius=40, fill="#e74c3c"),
            # Ellipse with stroke
            nib.draw.Ellipse(
                cx=80,
                cy=180,
                rx=50,
                ry=30,
                fill="#9b59b6",
                stroke="#ffffff",
                stroke_width=2,
            ),
            # Horizontal line
            nib.draw.Line(
                x1=20, y1=260, x2=380, y2=260, stroke="#2ecc71", stroke_width=3
            ),
            # Vertical line
            nib.draw.Line(
                x1=200,
                y1=120,
                x2=200,
                y2=240,
                stroke="#f39c12",
                stroke_width=2,
                line_cap="round",
            ),
            # Triangle (closed path)
            nib.draw.Path(
                points=[(300, 180), (350, 240), (250, 240)], fill="#1abc9c", closed=True
            ),
            # Another circle
            nib.draw.Circle(
                cx=200,
                cy=160,
                radius=25,
                fill="#ff6b6b",
                stroke="#ffffff",
                stroke_width=3,
            ),
            # Text label
            nib.draw.Text("Canvas Demo - Core Graphics", x=20, y=290, fill="#ffffff"),
            nib.draw.BezierPath(
                commands=[
                    {"move": [25, 125]},
                    {
                        "quad": [50, 25, 135, 35]
                    },  # QuadraticTo(cp1x=50, cp1y=25, x=135, y=35)
                    {
                        "quad": [75, 115, 135, 215]
                    },  # QuadraticTo(cp1x=75, cp1y=115, x=135, y=215)
                    {
                        "quad": [50, 225, 25, 125]
                    },  # QuadraticTo(cp1x=50, cp1y=225, x=25, y=125)
                    {"close": True},
                ],
                fill="#F06292",  # Pink 400
            ),
            # Second shape (blue, semi-transparent)
            nib.draw.BezierPath(
                commands=[
                    {"move": [85, 125]},
                    {"quad": [120, 85, 165, 75]},
                    {"quad": [120, 115, 165, 175]},
                    {"quad": [120, 165, 85, 125]},
                    {"close": True},
                ],
                fill="#42A5F5",  # Blue 400
                opacity=0.5,
            ),
        ]
    )

    # Redraw button to test reactive updates
    counter = 0

    def redraw():
        nonlocal counter
        counter += 1
        colors = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6"]
        color = colors[counter % len(colors)]

        canvas.draw(
            [
                nib.draw.Rect(x=20, y=20, width=360, height=240, fill="#1a1a1a"),
                nib.draw.Circle(cx=200, cy=140, radius=80, fill=color),
                nib.draw.Text(f"Click count: {counter}", x=20, y=290, fill="#ffffff"),
            ]
        )

    app.build(
        nib.VStack(
            controls=[canvas],
            spacing=10,
            padding=10,
        )
    )


nib.run(main)
