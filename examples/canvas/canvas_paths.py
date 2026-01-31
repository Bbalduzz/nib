import nib
from nib.draw import (
    ArcTo,
    BezierPath,
    Close,
    CubicTo,
    LineTo,
    MoveTo,
    Oval,
    PathArc,
    PathRect,
    QuadraticTo,
    SubPath,
)


def main(app: nib.App):
    app.title = "Canvas Demo"
    app.width = 200
    app.height = 250

    canvas = nib.Canvas(width=200, height=250)
    canvas.draw(
        [
            # Pink shape using typed elements
            BezierPath(
                elements=[
                    MoveTo(25, 125),
                    QuadraticTo(cp1x=50, cp1y=25, x=135, y=35),
                    QuadraticTo(cp1x=75, cp1y=115, x=135, y=215),
                    QuadraticTo(cp1x=50, cp1y=225, x=25, y=125),
                    Close(),
                ],
                fill=nib.Color.BLUE,
            ),
            # Blue shape
            BezierPath(
                elements=[
                    MoveTo(85, 125),
                    QuadraticTo(cp1x=120, cp1y=85, x=165, y=75),
                    QuadraticTo(cp1x=120, cp1y=115, x=165, y=175),
                    QuadraticTo(cp1x=120, cp1y=165, x=85, y=125),
                    Close(),
                ],
                fill=nib.Color.PINK,
                opacity=0.5,
            ),
        ]
    )

    app.build(canvas)


nib.run(main)
