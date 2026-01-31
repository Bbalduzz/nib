"""
Color demo for Nib.

Demonstrates the Color class with hex values, named colors, and opacity.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

from nib import (
    App,
    Color,
    Font,
    FontWeight,
    HStack,
    MenuItem,
    RoundedRectangle,
    ScrollView,
    Spacer,
    Text,
    VStack,
)


def color_swatch(color: Color, name: str) -> VStack:
    """Create a color swatch with label."""
    return VStack(
        controls=[
            RoundedRectangle(
                corner_radius=8,
                fill=color,
                width=60,
                height=40,
            ),
            Text(
                name,
                font=Font.system(10),
                foreground_color=Color.SECONDARY,
            ),
        ],
        spacing=4,
    )


def main(app: App):
    app.title = "Colors"
    app.icon = "paintpalette.fill"
    app.width = 420
    app.height = 500
    app.menu = [
        MenuItem("Quit", action=app.quit),
    ]

    app.build(
        ScrollView(
            shows_indicators=False,
            controls=[
                VStack(
                    controls=[
                        # Header
                        Text(
                            "Color Demo",
                            font=Font.system(size=26, weight=FontWeight.semibold),
                            foreground_color=Color.PRIMARY,
                        ),
                        Text(
                            "All available colors in Nib",
                            font=Font.subheadline,
                            foreground_color=Color.SECONDARY,
                        ),
                        Spacer(min_length=10),
                        # Divider(),
                        # Basic Colors
                        Text(
                            "Basic Colors",
                            font=Font.headline,
                            foreground_color=Color.PRIMARY,
                        ),
                        HStack(
                            controls=[
                                color_swatch(Color.RED, "RED"),
                                color_swatch(Color.ORANGE, "ORANGE"),
                                color_swatch(Color.YELLOW, "YELLOW"),
                                color_swatch(Color.GREEN, "GREEN"),
                                color_swatch(Color.BLUE, "BLUE"),
                            ],
                            spacing=12,
                        ),
                        HStack(
                            controls=[
                                color_swatch(Color.PURPLE, "PURPLE"),
                                color_swatch(Color.PINK, "PINK"),
                                color_swatch(Color.WHITE, "WHITE"),
                                color_swatch(Color.BLACK, "BLACK"),
                                color_swatch(Color.GRAY, "GRAY"),
                            ],
                            spacing=12,
                        ),
                        Spacer(min_length=15),
                        # Extended Colors
                        Text(
                            "Extended Colors",
                            font=Font.headline,
                            foreground_color=Color.PRIMARY,
                        ),
                        HStack(
                            controls=[
                                color_swatch(Color.INDIGO, "INDIGO"),
                                color_swatch(Color.CYAN, "CYAN"),
                                color_swatch(Color.MINT, "MINT"),
                                color_swatch(Color.TEAL, "TEAL"),
                                color_swatch(Color.BROWN, "BROWN"),
                            ],
                            spacing=12,
                        ),
                        Spacer(min_length=15),
                        # Semantic Colors
                        Text(
                            "Semantic Colors",
                            font=Font.headline,
                            foreground_color=Color.PRIMARY,
                        ),
                        HStack(
                            controls=[
                                color_swatch(Color.PRIMARY, "PRIMARY"),
                                color_swatch(Color.SECONDARY, "SECONDARY"),
                                color_swatch(Color.ACCENT, "ACCENT"),
                                color_swatch(Color.CLEAR, "CLEAR"),
                            ],
                            spacing=12,
                        ),
                        Spacer(min_length=15),
                        # Hex Colors
                        Text(
                            "Hex Colors",
                            font=Font.headline,
                            foreground_color=Color.PRIMARY,
                        ),
                        HStack(
                            controls=[
                                color_swatch(Color(hex="#FF6B6B"), "#FF6B6B"),
                                color_swatch(Color(hex="#4ECDC4"), "#4ECDC4"),
                                color_swatch(Color(hex="#45B7D1"), "#45B7D1"),
                                color_swatch(Color(hex="#96CEB4"), "#96CEB4"),
                                color_swatch(Color(hex="#FFEAA7"), "#FFEAA7"),
                            ],
                            spacing=12,
                        ),
                        Spacer(min_length=15),
                        # Opacity Examples
                        Text(
                            "With Opacity",
                            font=Font.headline,
                            foreground_color=Color.PRIMARY,
                        ),
                        HStack(
                            controls=[
                                color_swatch(Color.BLUE.with_opacity(1.0), "100%"),
                                color_swatch(Color.BLUE.with_opacity(0.8), "80%"),
                                color_swatch(Color.BLUE.with_opacity(0.6), "60%"),
                                color_swatch(Color.BLUE.with_opacity(0.4), "40%"),
                                color_swatch(Color.BLUE.with_opacity(0.2), "20%"),
                            ],
                            spacing=12,
                        ),
                        Spacer(min_length=15),
                        # Gradient-like effect with hex + opacity
                        Text(
                            "Hex + Opacity",
                            font=Font.headline,
                            foreground_color=Color.PRIMARY,
                        ),
                        HStack(
                            controls=[
                                color_swatch(
                                    Color(hex="#FF6B6B").with_opacity(1.0), "100%"
                                ),
                                color_swatch(
                                    Color(hex="#FF6B6B").with_opacity(0.75), "75%"
                                ),
                                color_swatch(
                                    Color(hex="#FF6B6B").with_opacity(0.5), "50%"
                                ),
                                color_swatch(
                                    Color(hex="#FF6B6B").with_opacity(0.25), "25%"
                                ),
                            ],
                            spacing=12,
                        ),
                        Spacer(min_length=20),
                    ],
                    spacing=8,
                    padding=20,
                ),
            ],
        )
    )


if __name__ == "__main__":
    from nib import run

    run(main)
