"""Demo of custom Shape primitive.

Shows how to create custom shapes using path operations.
"""

import math

import nib


class NibLogoShape(nib.Shape):
    """The Nib logo as a custom shape."""

    view_box = (349, 447)

    def build_path(self, path: nib.Path) -> nib.Path:
        # Pentagon/nib shape (top)
        path.move_to(3.08, 159.35)
        path.line_to(49.67, 305.03)
        path.curve_to(99.52, 341.24, control1=(56.53, 328.42), control2=(74.29, 341.24))
        path.line_to(248.85, 341.24)
        path.curve_to(
            298.69, 305.03, control1=(274.08, 341.24), control2=(291.17, 328.42)
        )
        path.line_to(345.29, 159.35)
        path.curve_to(
            326.77, 100.56, control1=(352.82, 135.35), control2=(346.51, 115.20)
        )
        path.line_to(205.31, 11.45)
        path.curve_to(143.06, 11.45, control1=(184.77, -3.81), control2=(163.60, -3.81))
        path.line_to(21.59, 100.56)
        path.curve_to(3.08, 159.35, control1=(1.86, 115.20), control2=(-4.45, 135.35))
        path.close()

        # Rounded rectangle (bottom)
        path.add_rounded_rect(61.18, 357.08, 226, 89, corner_radius=22)

        return path


class Star(nib.Shape):
    """A 5-pointed star."""

    view_box = (100, 100)

    def build_path(self, path: nib.Path) -> nib.Path:
        cx, cy = 50, 50
        outer_r, inner_r = 45, 20

        for i in range(10):
            angle = math.pi / 2 + i * math.pi / 5
            r = outer_r if i % 2 == 0 else inner_r
            x = cx + r * math.cos(angle)
            y = cy - r * math.sin(angle)

            if i == 0:
                path.move_to(x, y)
            else:
                path.line_to(x, y)

        path.close()
        return path


class Heart(nib.Shape):
    """A heart shape using bezier curves."""

    view_box = (100, 100)

    def build_path(self, path: nib.Path) -> nib.Path:
        path.move_to(50, 85)
        path.curve_to(15, 55, control1=(20, 85), control2=(15, 70))
        path.curve_to(50, 20, control1=(15, 35), control2=(35, 20))
        path.curve_to(85, 55, control1=(65, 20), control2=(85, 35))
        path.curve_to(50, 85, control1=(85, 70), control2=(80, 85))
        path.close()
        return path


def main(app: nib.App):
    app.title = "Shapes"
    app.icon = nib.SFSymbol("star.fill")
    app.width = 350
    app.height = 450

    app.build(
        nib.ScrollView(
            controls=[
                nib.Text("Custom Shapes", font=nib.Font.title),
                nib.Divider(),
                # Row 1: Nib Logo
                nib.HStack(
                    controls=[
                        nib.Text("Nib Logo:", font=nib.Font.headline),
                        nib.Spacer(),
                        NibLogoShape(
                            fill=nib.LinearGradient(
                                colors=["#3B82F6", "#6366F1"],
                                start=(0, 0),
                                end=(1, 1),
                                width=60,
                                height=80,
                            )
                        ),
                    ],
                    padding={"horizontal": 16},
                ),
                # Row 2: Star
                nib.HStack(
                    controls=[
                        nib.Text("Star:", font=nib.Font.headline),
                        nib.Spacer(),
                        Star(fill="#F59E0B", width=60, height=60),
                    ],
                    padding={"horizontal": 16},
                ),
                # Row 3: Heart
                nib.HStack(
                    controls=[
                        nib.Text("Blob:", font=nib.Font.headline),
                        nib.Spacer(),
                        Heart(fill="#EF4444", width=60, height=60),
                    ],
                    padding={"horizontal": 16},
                ),
                # Row 4: Inline triangle
                nib.HStack(
                    controls=[
                        nib.Text("Triangle:", font=nib.Font.headline),
                        nib.Spacer(),
                        nib.Shape(
                            path=(
                                nib.Path()
                                .move_to(50, 0)
                                .line_to(100, 100)
                                .line_to(0, 100)
                                .close()
                            ),
                            fill="#10B981",
                            view_box=(100, 100),
                            width=60,
                            height=60,
                        ),
                    ],
                    padding={"horizontal": 16},
                ),
                # Row 5: With stroke
                nib.HStack(
                    controls=[
                        nib.Text("With Stroke:", font=nib.Font.headline),
                        nib.Spacer(),
                        nib.Shape(
                            path=(
                                nib.Path().add_rounded_rect(
                                    5, 5, 90, 90, corner_radius=15
                                )
                            ),
                            fill="#8B5CF6",
                            stroke="#FFFFFF",
                            stroke_width=3,
                            view_box=(100, 100),
                            width=60,
                            height=60,
                        ),
                    ],
                    padding={"horizontal": 16},
                ),
                nib.Spacer(),
            ],
            # spacing=16,
            padding=16,
        )
    )


nib.run(main)
