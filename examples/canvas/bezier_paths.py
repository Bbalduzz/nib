"""Bezier path drawing example.

Demonstrates the Flet-style path API with typed path elements.
"""

import nib
from nib.draw import (
    BezierPath,
    MoveTo,
    LineTo,
    QuadraticTo,
    CubicTo,
    Close,
    Oval,
    PathRect,
)


def main(app: nib.App):
    app.title = "Bezier Paths"
    app.width = 300
    app.height = 350

    canvas = nib.Canvas(width=300, height=350, background_color="#1a1a1a")

    canvas.draw([
        # Leaf shape using quadratic beziers (like Flet example)
        BezierPath(
            elements=[
                MoveTo(25, 125),
                QuadraticTo(cp1x=50, cp1y=25, x=135, y=35),
                QuadraticTo(cp1x=75, cp1y=115, x=135, y=215),
                QuadraticTo(cp1x=50, cp1y=225, x=25, y=125),
                Close(),
            ],
            fill="#F06292",
        ),
        # Overlapping shape with transparency
        BezierPath(
            elements=[
                MoveTo(85, 125),
                QuadraticTo(cp1x=120, cp1y=85, x=165, y=75),
                QuadraticTo(cp1x=120, cp1y=115, x=165, y=175),
                QuadraticTo(cp1x=120, cp1y=165, x=85, y=125),
                Close(),
            ],
            fill="#42A5F5",
            opacity=0.7,
        ),

        # Heart shape using cubic beziers
        BezierPath(
            elements=[
                MoveTo(230, 80),
                CubicTo(cp1x=230, cp1y=50, cp2x=200, cp2y=50, x=200, y=80),
                CubicTo(cp1x=200, cp1y=110, cp2x=230, cp2y=130, x=230, y=160),
                CubicTo(cp1x=230, cp1y=130, cp2x=260, cp2y=110, x=260, y=80),
                CubicTo(cp1x=260, cp1y=50, cp2x=230, cp2y=50, x=230, y=80),
                Close(),
            ],
            fill="#EF5350",
        ),

        # Star using lines
        BezierPath(
            elements=[
                MoveTo(230, 200),
                LineTo(240, 230),
                LineTo(270, 230),
                LineTo(245, 250),
                LineTo(255, 280),
                LineTo(230, 260),
                LineTo(205, 280),
                LineTo(215, 250),
                LineTo(190, 230),
                LineTo(220, 230),
                Close(),
            ],
            fill="#FFD54F",
        ),

        # Rounded rectangle and oval
        BezierPath(
            elements=[
                PathRect(x=20, y=260, width=80, height=40, border_radius=10),
            ],
            fill="#66BB6A",
        ),
        BezierPath(
            elements=[
                Oval(x=110, y=260, width=60, height=40),
            ],
            fill="#AB47BC",
        ),
    ])

    app.build(
        nib.VStack(
            controls=[
                canvas,
            ],
            padding=16,
        )
    )


nib.run(main)
