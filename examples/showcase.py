"""
Showcase example for Nib.

Demonstrates all the available views and controls using the new function-based API.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

import nib


def main(app: nib.App):
    app.title = "Showcase"
    app.icon = nib.SFSymbol("sparkles")
    app.menu = [nib.MenuItem("Quit", action=app.quit)]

    # State controls (mutable)
    text_input = nib.TextField(placeholder="Enter text...", value="")
    slider_label = nib.Text("50%")

    # Event handlers
    def on_text_change(value: str):
        print(f"Text changed: {value}")

    def on_toggle_change(value: bool):
        print(f"Toggle changed: {value}")

    def on_slider_change(value: float):
        slider_label.content = f"{int(value * 100)}%"

    def on_picker_change(value: str):
        print(f"Picker changed: {value}")

    def on_button():
        print("Button clicked!")

    # Build UI
    app.build(
        nib.ScrollView(
            controls=[
                nib.VStack(
                    controls=[
                        # Header
                        nib.Text("Nib Showcase", font=nib.Font.largeTitle, bold=True),
                        nib.Text(
                            "All available views and controls",
                            font=nib.Font.subheadline,
                            foreground_color=nib.Color.secondary,
                        ),
                        nib.Divider(),
                        nib.Spacer(min_length=10),
                        # Text Styles Section
                        nib.VStack(
                            controls=[
                                nib.Text("Text Styles", font=nib.Font.headline),
                                nib.HStack(
                                    controls=[
                                        nib.Text("Bold", bold=True),
                                        nib.Text("Italic", italic=True),
                                        nib.Text("Strike", strikethrough=True),
                                        nib.Text("Underline", underline=True),
                                    ],
                                    spacing=10,
                                ),
                                nib.Text(
                                    "Monospaced Text",
                                    monospaced=True,
                                    foreground_color=nib.Color.blue,
                                ),
                            ],
                            spacing=6,
                            alignment=nib.HorizontalAlignment.leading,
                        ),
                        nib.Spacer(min_length=20),
                        # Input Controls Section
                        nib.VStack(
                            controls=[
                                nib.Text("Input Controls", font=nib.Font.headline),
                                text_input,
                                nib.Toggle(
                                    "Enable notifications",
                                    is_on=False,
                                    on_change=on_toggle_change,
                                ),
                                nib.HStack(
                                    controls=[
                                        nib.Text("Volume:"),
                                        nib.Slider(
                                            value=0.5,
                                            min_value=0,
                                            max_value=1,
                                            on_change=on_slider_change,
                                        ),
                                        slider_label,
                                    ],
                                    spacing=10,
                                ),
                                nib.Picker(
                                    label="Select option",
                                    selection="option1",
                                    options=[
                                        ("option1", "Option 1"),
                                        ("option2", "Option 2"),
                                        ("option3", "Option 3"),
                                    ],
                                    on_change=on_picker_change,
                                ),
                            ],
                            spacing=10,
                            alignment=nib.HorizontalAlignment.leading,
                        ),
                        nib.Spacer(min_length=20),
                        # Buttons Section
                        nib.VStack(
                            controls=[
                                nib.Text("Buttons", font=nib.Font.headline),
                                nib.HStack(
                                    controls=[
                                        nib.Button("Default", action=on_button),
                                        nib.Button(
                                            "Bordered",
                                            action=on_button,
                                            style=nib.ButtonStyle.bordered,
                                        ),
                                        nib.Button(
                                            "Prominent",
                                            action=on_button,
                                            style=nib.ButtonStyle.borderedProminent,
                                        ),
                                    ],
                                    spacing=8,
                                ),
                                nib.HStack(
                                    controls=[
                                        nib.Button(
                                            content=nib.HStack(
                                                controls=[
                                                    nib.SFSymbol("star.fill"),
                                                    nib.Text("With Icon"),
                                                ],
                                                spacing=4,
                                            ),
                                            action=on_button,
                                        ),
                                        nib.Button(
                                            "Destructive",
                                            action=on_button,
                                            role=nib.ButtonRole.destructive,
                                        ),
                                    ],
                                    spacing=8,
                                ),
                            ],
                            spacing=8,
                            alignment=nib.HorizontalAlignment.leading,
                        ),
                        nib.Spacer(min_length=20),
                        # Indicators Section
                        nib.VStack(
                            controls=[
                                nib.Text("Indicators", font=nib.Font.headline),
                                nib.HStack(
                                    controls=[
                                        nib.Label(
                                            "Downloads", icon="arrow.down.circle"
                                        ),
                                        nib.Spacer(),
                                        nib.ProgressView(value=0.7),
                                    ],
                                    spacing=10,
                                ),
                                nib.HStack(
                                    controls=[
                                        nib.SFSymbol("gear", font=nib.Font.title2),
                                        nib.SFSymbol(
                                            "star.fill",
                                            font=nib.Font.title2,
                                            foreground_color=nib.Color.yellow,
                                        ),
                                        nib.SFSymbol(
                                            "heart.fill",
                                            font=nib.Font.title2,
                                            foreground_color=nib.Color.red,
                                        ),
                                    ],
                                    spacing=15,
                                ),
                                nib.Link(
                                    "Visit Anthropic", url="https://www.anthropic.com"
                                ),
                            ],
                            spacing=10,
                            alignment=nib.HorizontalAlignment.leading,
                        ),
                        nib.Spacer(min_length=20),
                        # Shapes Section
                        nib.VStack(
                            controls=[
                                nib.Text("Shapes", font=nib.Font.headline),
                                nib.HStack(
                                    controls=[
                                        nib.Circle(
                                            fill=nib.Color.red, width=30, height=30
                                        ),
                                        nib.Rectangle(
                                            fill=nib.Color.green, width=30, height=30
                                        ),
                                        nib.RoundedRectangle(
                                            corner_radius=8,
                                            fill=nib.Color.blue,
                                            width=40,
                                            height=30,
                                        ),
                                        nib.Capsule(
                                            fill=nib.Color.purple, width=50, height=25
                                        ),
                                        nib.Ellipse(
                                            fill=nib.Color.orange, width=40, height=25
                                        ),
                                    ],
                                    spacing=10,
                                ),
                            ],
                            spacing=8,
                            alignment=nib.HorizontalAlignment.leading,
                        ),
                        nib.Spacer(min_length=20),
                        # Background & Overlay Section
                        nib.VStack(
                            controls=[
                                nib.Text(
                                    "Background & Overlay", font=nib.Font.headline
                                ),
                                nib.HStack(
                                    controls=[
                                        # Background view example
                                        nib.Text(
                                            "With Background",
                                            padding=12,
                                            background=nib.RoundedRectangle(
                                                corner_radius=8,
                                                fill="#3B82F6",
                                            ),
                                            foreground_color=nib.Color.white,
                                        ),
                                        # Overlay view example
                                        nib.Text(
                                            "With Overlay",
                                            padding=12,
                                            background=nib.RoundedRectangle(
                                                corner_radius=8,
                                                fill="#1F2937",
                                            ),
                                            overlay=nib.RoundedRectangle(
                                                corner_radius=8,
                                                stroke_color="#10B981",
                                                stroke_width=2,
                                            ),
                                            foreground_color=nib.Color.white,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                            ],
                            spacing=8,
                            alignment=nib.HorizontalAlignment.leading,
                        ),
                        nib.Spacer(min_length=20),
                        # Advanced Text Section
                        nib.VStack(
                            controls=[
                                nib.Text("Advanced Text", font=nib.Font.headline),
                                nib.HStack(
                                    controls=[
                                        # Monospaced digits for numbers
                                        nib.Text(
                                            "111,111",
                                            monospaced_digit=True,
                                            font=nib.Font.title2,
                                        ),
                                        nib.Text(
                                            "← Monospaced Digits",
                                            foreground_color=nib.Color.secondary,
                                        ),
                                    ],
                                    spacing=8,
                                ),
                                nib.HStack(
                                    controls=[
                                        # Monospaced digits for numbers
                                        nib.Text(
                                            "111,111",
                                            font=nib.Font.title2,
                                        ),
                                        nib.Text(
                                            "← Not Monospaced Digits",
                                            foreground_color=nib.Color.secondary,
                                        ),
                                    ],
                                    spacing=8,
                                ),
                            ],
                            spacing=10,
                            alignment=nib.HorizontalAlignment.leading,
                        ),
                        nib.Spacer(min_length=20),
                        # Images Section
                        nib.VStack(
                            controls=[
                                nib.Text("Images", font=nib.Font.headline),
                                nib.HStack(
                                    controls=[
                                        # URL image with aspect fit
                                        nib.Image(
                                            src="/Users/edoardobalducci/Downloads/original-19f4a0f6c05e0336fba7760d82b682fa.png",
                                            label="Random image",
                                            width=60,
                                            height=60,
                                            aspect_ratio=nib.ContentMode.FIT,
                                            corner_radius=8,
                                        ),
                                        # URL image with circle clip
                                        nib.Image(
                                            src="https://picsum.photos/101/101",
                                            label="Avatar",
                                            width=60,
                                            height=60,
                                            aspect_ratio=nib.ContentMode.FILL,
                                            clip_shape=nib.Circle(),
                                        ),
                                        # URL image with blur effect
                                        nib.Image(
                                            src="https://picsum.photos/102/102",
                                            label="Blurred image",
                                            width=60,
                                            height=60,
                                            aspect_ratio=nib.ContentMode.FILL,
                                            blur=3,
                                            corner_radius=8,
                                        ),
                                    ],
                                    spacing=12,
                                ),
                                nib.Text(
                                    "Fit • Circle Clip • Blur",
                                    font=nib.Font.caption,
                                    foreground_color=nib.Color.secondary,
                                ),
                            ],
                            spacing=10,
                            alignment=nib.HorizontalAlignment.leading,
                        ),
                        nib.Spacer(min_length=20),
                        # Visual Effects Section
                        nib.VStack(
                            controls=[
                                nib.Text("Visual Effects", font=nib.Font.headline),
                                nib.HStack(
                                    controls=[
                                        # Shadow
                                        nib.Text(
                                            "Shadow",
                                            padding=10,
                                            background=nib.Color.green,
                                            corner_radius=8,
                                            shadow_color="#000000",
                                            shadow_radius=4,
                                            shadow_y=2,
                                        ),
                                        # Border
                                        nib.Text(
                                            "Border",
                                            padding=10,
                                            border_color=nib.Color.blue,
                                            border_width=2,
                                            corner_radius=8,
                                        ),
                                        # Clip shape
                                        nib.Text(
                                            "Clipped",
                                            padding=10,
                                            background=nib.Color.purple,
                                            foreground_color=nib.Color.white,
                                            clip_shape="capsule",
                                        ),
                                    ],
                                    spacing=10,
                                ),
                            ],
                            spacing=8,
                            alignment=nib.HorizontalAlignment.leading,
                        ),
                        nib.Spacer(min_length=20),
                        # Disclosure Group
                        nib.DisclosureGroup(
                            "Advanced Options",
                            controls=[
                                nib.Toggle("Enable feature A", is_on=True),
                                nib.Toggle("Enable feature B", is_on=False),
                                nib.Slider(value=0.7, min_value=0, max_value=1),
                            ],
                        ),
                    ],
                    spacing=8,
                    padding=20,
                ),
            ],
            axes="vertical",
        )
    )


nib.run(main)
