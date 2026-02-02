"""Gradient Demo - Test all gradient types in nib."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

import nib


def main(app: nib.App):
    app.title = "Gradients"
    app.icon = nib.SFSymbol("paintpalette.fill")
    app.width = 320
    app.height = 400
    app.menu = [
        nib.MenuItem("Quit", action=app.quit),
    ]

    app.build(
        nib.ScrollView(
            [
                nib.VStack(
                    controls=[
                        nib.Text("Gradient Demo", font=nib.Font.title),
                        nib.Spacer(min_length=16),
                        # Linear Gradient
                        nib.Text("LinearGradient", font=nib.Font.headline),
                        nib.Rectangle(
                            corner_radius=12,
                            width=280,
                            height=60,
                            background=nib.LinearGradient(
                                colors=["#FF6B6B", "#4ECDC4"],
                                start=(0, 0),
                                end=(1, 1),
                            ),
                        ),
                        nib.Spacer(min_length=16),
                        # Linear with stops
                        nib.Text("LinearGradient (stops)", font=nib.Font.headline),
                        nib.Rectangle(
                            corner_radius=12,
                            width=280,
                            height=60,
                            background=nib.LinearGradient(
                                stops=[
                                    (0.0, "#FF0000"),
                                    (0.5, "#FFFF00"),
                                    (1.0, "#00FF00"),
                                ],
                                start=(0, 0.5),
                                end=(1, 0.5),
                            ),
                        ),
                        nib.Spacer(min_length=16),
                        # Radial Gradient
                        nib.Text("RadialGradient", font=nib.Font.headline),
                        nib.Circle(
                            width=120,
                            height=120,
                            background=nib.RadialGradient(
                                colors=["#FFFFFF", "#6B5B95"],
                                center=(0.5, 0.5),
                                start_radius=0,
                                end_radius=60,
                            ),
                        ),
                        nib.Spacer(min_length=16),
                        # Angular Gradient
                        nib.Text("AngularGradient", font=nib.Font.headline),
                        nib.Circle(
                            width=120,
                            height=120,
                            background=nib.AngularGradient(
                                colors=[
                                    "#FF0000",
                                    "#FF7F00",
                                    "#FFFF00",
                                    "#00FF00",
                                    "#0000FF",
                                    "#8B00FF",
                                    "#FF0000",
                                ],
                                center=(0.5, 0.5),
                            ),
                        ),
                        nib.Spacer(min_length=16),
                        # Elliptical Gradient
                        nib.Text("EllipticalGradient", font=nib.Font.headline),
                        nib.Circle(
                            # corner_radius=12,
                            width=280,
                            height=80,
                            background=nib.EllipticalGradient(
                                colors=["#FFFFFF", "#2C3E50"],
                                center=(0.5, 0.5),
                                start_radius_fraction=0,
                                end_radius_fraction=0.8,
                            ),
                        ),
                        nib.Spacer(min_length=20),
                    ],
                    spacing=4,
                    padding=20,
                )
            ]
        )
    )


nib.run(main)
