"""
Font demo for Nib.

Demonstrates font support including:
- System fonts (SF Pro, SF Compact Rounded, etc.)
- Custom fonts from local files
- Custom fonts from URLs
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

from nib import (
    App,
    Color,
    Divider,
    Font,
    HStack,
    MenuItem,
    ScrollView,
    Spacer,
    Text,
    VStack,
)


def font_sample(text: str, font: Font, label: str) -> VStack:
    """Create a font sample with label."""
    return VStack(
        controls=[
            Text(text, font=font),
            Text(label, font=Font.system(10), foreground_color=Color.SECONDARY),
        ],
        spacing=2,
    )


def main(app: App):
    app.title = "Font Demo"
    app.icon = "textformat"
    app.width = 400
    app.height = 550
    app.fonts = {
        "Iosevka": "/Users/edoardobalducci/Documents/work/notit-dev/src/assets/fonts/Iosevka/Iosevka-Regular.ttf",
    }
    app.menu = [
        MenuItem("Quit", action=app.quit),
    ]

    app.build(
        ScrollView(
            controls=[
                VStack(
                    controls=[
                        # Header
                        Text("Font Demo", font=Font.largeTitle),
                        Text(
                            "Typography options in Nib",
                            font=Font.subheadline,
                            foreground_color=Color.SECONDARY,
                        ),
                        Spacer(min_length=10),
                        Divider(),
                        Spacer(min_length=10),
                        # System Text Styles
                        Text("System Text Styles", font=Font.HEADLINE),
                        Spacer(min_length=5),
                        font_sample("Large Title", Font.LARGE_TITLE, "Font.largeTitle"),
                        font_sample("Title", Font.TITLE, "Font.title"),
                        font_sample("Title 2", Font.TITLE2, "Font.title2"),
                        font_sample("Title 3", Font.TITLE3, "Font.title3"),
                        font_sample("Headline", Font.HEADLINE, "Font.headline"),
                        font_sample(
                            "Subheadline", Font.SUBHEADLINE, "Font.subheadline"
                        ),
                        font_sample("Body", Font.BODY, "Font.body"),
                        font_sample("Callout", Font.CALLOUT, "Font.callout"),
                        font_sample("Caption", Font.CAPTION, "Font.caption"),
                        font_sample("Footnote", Font.FOOTNOTE, "Font.footnote"),
                        Spacer(min_length=15),
                        Divider(),
                        Spacer(min_length=10),
                        # System Fonts
                        Text("System Fonts", font=Font.headline),
                        Text(
                            "Use installed macOS fonts by name",
                            font=Font.caption,
                            foreground_color=Color.SECONDARY,
                        ),
                        Spacer(min_length=5),
                        font_sample(
                            "SF Pro Display",
                            Font.custom("SF Pro Display", size=16),
                            'Font.custom("SF Pro Display", 16)',
                        ),
                        font_sample(
                            "SF Compact Rounded",
                            Font.custom("SF Compact Rounded", size=16),
                            'Font.custom("SF Compact Rounded", 16)',
                        ),
                        font_sample(
                            "SF Mono",
                            Font.custom("SF Mono", size=14),
                            'Font.custom("SF Mono", 14)',
                        ),
                        font_sample(
                            "Helvetica Neue",
                            Font.custom("Helvetica Neue", size=16),
                            'Font.custom("Helvetica Neue", 16)',
                        ),
                        font_sample(
                            "Bradley Hand",
                            Font.custom("Bradley Hand", size=18),
                            'Font.custom("Bradley Hand", 18)',
                        ),
                        font_sample(
                            "Iosevka",
                            Font.custom("Iosevka", size=18),
                            'Font.custom("Iosevka", 18)',
                        ),
                        Spacer(min_length=15),
                        Divider(),
                        Spacer(min_length=10),
                        # Custom Sizes
                        Text("Custom Sizes", font=Font.headline),
                        Spacer(min_length=5),
                        HStack(
                            controls=[
                                Text("10pt", font=Font.system(10)),
                                Text("14pt", font=Font.system(14)),
                                Text("18pt", font=Font.system(18)),
                                Text("24pt", font=Font.system(24)),
                            ],
                            spacing=15,
                        ),
                        Spacer(min_length=15),
                        Divider(),
                        Spacer(min_length=10),
                        # Font Weights
                        Text("Font Weights", font=Font.headline),
                        Spacer(min_length=5),
                        font_sample(
                            "Ultra Light",
                            Font.system(16, weight="ultraLight"),
                            'Font.system(16, weight="ultraLight")',
                        ),
                        font_sample(
                            "Light",
                            Font.system(16, weight="light"),
                            'Font.system(16, weight="light")',
                        ),
                        font_sample(
                            "Regular",
                            Font.system(16, weight="regular"),
                            'Font.system(16, weight="regular")',
                        ),
                        font_sample(
                            "Medium",
                            Font.system(16, weight="medium"),
                            'Font.system(16, weight="medium")',
                        ),
                        font_sample(
                            "Semibold",
                            Font.system(16, weight="semibold"),
                            'Font.system(16, weight="semibold")',
                        ),
                        font_sample(
                            "Bold",
                            Font.system(16, weight="bold"),
                            'Font.system(16, weight="bold")',
                        ),
                        font_sample(
                            "Heavy",
                            Font.system(16, weight="heavy"),
                            'Font.system(16, weight="heavy")',
                        ),
                        font_sample(
                            "Black",
                            Font.system(16, weight="black"),
                            'Font.system(16, weight="black")',
                        ),
                        Spacer(min_length=20),
                        # Usage instructions
                        Divider(),
                        Spacer(min_length=10),
                        Text("Custom Fonts", font=Font.headline),
                        Text(
                            "Register fonts via app.fonts:",
                            font=Font.caption,
                            foreground_color=Color.SECONDARY,
                        ),
                        Spacer(min_length=5),
                        VStack(
                            controls=[
                                Text(
                                    "app.fonts = {",
                                    font=Font.custom("SF Mono", size=11),
                                    foreground_color=Color.CYAN,
                                ),
                                Text(
                                    '    "MyFont": "/path/to/font.ttf",',
                                    font=Font.custom("SF Mono", size=11),
                                    foreground_color=Color.CYAN,
                                ),
                                Text(
                                    '    "WebFont": "https://...",',
                                    font=Font.custom("SF Mono", size=11),
                                    foreground_color=Color.CYAN,
                                ),
                                Text(
                                    "}",
                                    font=Font.custom("SF Mono", size=11),
                                    foreground_color=Color.CYAN,
                                ),
                            ],
                            spacing=2,
                            padding={"horizontal": 10, "vertical": 8},
                            background=Color.BLACK.with_opacity(0.3),
                            corner_radius=6,
                        ),
                        Spacer(min_length=20),
                    ],
                    spacing=6,
                    padding=20,
                ),
            ],
        )
    )


if __name__ == "__main__":
    from nib import run

    run(main)
