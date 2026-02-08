import nib


def main(app: nib.App):
    app.title = "Canvas"
    app.icon = nib.SFSymbol("paintbrush")
    app.width = 320
    app.height = 360

    canvas = nib.Canvas(
        width=280,
        height=280,
        background_color="#1a1a2e",
        commands=[
            # Background circles
            nib.draw.Circle(cx=140, cy=140, radius=120, fill="#16213e", opacity=0.8),
            nib.draw.Circle(cx=140, cy=140, radius=80, fill="#0f3460", opacity=0.8),
            nib.draw.Circle(cx=140, cy=140, radius=40, fill="#533483", opacity=0.8),
            # Cross lines
            nib.draw.Line(x1=20, y1=140, x2=260, y2=140, stroke="#e94560", stroke_width=2, opacity=0.5),
            nib.draw.Line(x1=140, y1=20, x2=140, y2=260, stroke="#e94560", stroke_width=2, opacity=0.5),
            # Corner rects
            nib.draw.Rect(x=10, y=10, width=50, height=50, corner_radius=8, fill="#e94560", opacity=0.7),
            nib.draw.Rect(x=220, y=10, width=50, height=50, corner_radius=8, fill="#0f3460", opacity=0.7),
            nib.draw.Rect(x=10, y=220, width=50, height=50, corner_radius=8, fill="#0f3460", opacity=0.7),
            nib.draw.Rect(x=220, y=220, width=50, height=50, corner_radius=8, fill="#e94560", opacity=0.7),
            # Center label
            nib.draw.Text(x=140, y=145, text="Canvas", font_size=20, color="#FFFFFF"),
        ],
    )

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Drawing Canvas", font=nib.Font.HEADLINE),
                canvas,
            ],
            spacing=8,
            padding=20,
        )
    )


nib.run(main)
