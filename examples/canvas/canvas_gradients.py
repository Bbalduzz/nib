"""Canvas Gradients Demo - Demonstrating gradient fills with nib types.

This example shows how Canvas drawing primitives integrate with nib types:
- nib.Color for fill and stroke colors
- nib.Font for text styling
- nib.BlendMode for compositing
- nib.HorizontalAlignment for text alignment
"""

import nib


def main(app: nib.App):
    app.title = "Gradients"
    app.icon = nib.SFSymbol("paintpalette.fill")
    app.width = 450
    app.height = 380

    canvas = nib.Canvas(
        width=430,
        height=320,
        background_color=nib.Color(hex="#1a1a2e"),
    )

    # Custom colors using nib.Color
    coral = nib.Color(hex="#FF6B6B")
    teal = nib.Color(hex="#4ECDC4")
    yellow = nib.Color(hex="#FFE66D")

    # Draw gradient shapes
    canvas.draw([
        # Linear gradient rectangle - colors can be nib.Color or hex strings
        nib.draw.Rect(
            x=20, y=20, width=120, height=80,
            corner_radius=10,
            fill=nib.draw.LinearGradient(
                start=(20, 20),
                end=(140, 100),
                colors=[coral, teal],  # Using nib.Color
            ),
        ),

        # Radial gradient circle
        nib.draw.Circle(
            cx=220, cy=60, radius=50,
            fill=nib.draw.RadialGradient(
                center=(220, 60),
                radius=50,
                colors=[yellow, coral],
            ),
        ),

        # Sweep gradient circle
        nib.draw.Circle(
            cx=360, cy=60, radius=50,
            fill=nib.draw.SweepGradient(
                center=(360, 60),
                colors=[coral, teal, yellow, coral],
            ),
        ),

        # Multi-stop linear gradient - mix hex and nib.Color
        nib.draw.Rect(
            x=20, y=130, width=390, height=40,
            corner_radius=8,
            fill=nib.draw.LinearGradient(
                start=(20, 150),
                end=(410, 150),
                colors=[coral, yellow, teal, "#45B7D1", "#96CEB4"],
                stops=[0.0, 0.25, 0.5, 0.75, 1.0],
            ),
        ),

        # Points demo - stroke accepts nib.Color
        nib.draw.Points(
            points=[(30, 210), (80, 230), (130, 200), (180, 240), (230, 210)],
            point_mode=nib.draw.PointMode.POLYGON,
            stroke=teal,
            stroke_width=3,
        ),

        # Scatter points
        nib.draw.Points(
            points=[
                (280, 200), (300, 220), (320, 190), (340, 230),
                (360, 210), (380, 195), (400, 225),
            ],
            point_mode=nib.draw.PointMode.POINTS,
            stroke=yellow,
            stroke_width=8,
        ),

        # Labels - using nib.Font and nib.Color
        nib.draw.Text("Linear", x=55, y=105,
                      fill=nib.Color.WHITE,
                      font=nib.Font.system(12)),
        nib.draw.Text("Radial", x=195, y=115,
                      fill=nib.Color.WHITE,
                      font=nib.Font.system(12)),
        nib.draw.Text("Sweep", x=335, y=115,
                      fill=nib.Color.WHITE,
                      font=nib.Font.system(12)),
        nib.draw.Text("Multi-stop Gradient", x=20, y=175,
                      fill=nib.Color.WHITE,
                      font=nib.Font.system(12)),
        nib.draw.Text("Polygon Points", x=20, y=260,
                      fill=nib.Color.WHITE,
                      font=nib.Font.system(12)),
        nib.draw.Text("Scatter Points", x=280, y=260,
                      fill=nib.Color.WHITE,
                      font=nib.Font.system(12)),

        # Fill demo with blend mode - using nib.BlendMode
        nib.draw.Rect(
            x=20, y=280, width=100, height=30,
            fill=nib.draw.LinearGradient(
                start=(20, 280),
                end=(120, 310),
                colors=[coral, teal],
            ),
            blend_mode=nib.BlendMode.SCREEN,  # Using nib.BlendMode
        ),

        nib.draw.Text("Blend: Screen", x=130, y=295,
                      fill=nib.Color.GRAY,
                      font=nib.Font.system(10)),
    ])

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Canvas Gradients Demo", font=nib.Font.HEADLINE),
                canvas,
            ],
            spacing=10,
            padding=10,
        )
    )


nib.run(main)
