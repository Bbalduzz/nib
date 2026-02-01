"""
Positioning Example - Demonstrates offset and absolute positioning in nib.

This example shows:
1. Using offset for relative positioning
2. Using ZStack alignment for corner positioning
3. Using Spacers for manual absolute positioning
"""

import nib


def main(app: nib.App):
    app.title = "Positioning"
    app.icon = nib.SFSymbol("arrow.up.left.and.arrow.down.right")
    app.width = 350
    app.height = 450

    app.build(
        nib.ScrollView(
            [
                nib.VStack(
                    controls=[
                        # Section 1: Offset (relative positioning)
                        nib.Text(
                            "1. Offset (relative positioning)", font=nib.Font.HEADLINE
                        ),
                        nib.Text(
                            "Offset moves a view from its natural position",
                            font=nib.Font.CAPTION,
                            foreground_color=nib.Color.SECONDARY,
                        ),
                        nib.ZStack(
                            controls=[
                                # Background
                                nib.RoundedRectangle(
                                    fill=nib.Color.SECONDARY.with_opacity(0.1),
                                    corner_radius=8,
                                ),
                                # Original position (gray)
                                nib.Circle(
                                    fill=nib.Color.GRAY.with_opacity(0.3),
                                    width=30,
                                    height=30,
                                ),
                                # Offset by (20, 20) - moves right and down
                                nib.Circle(
                                    fill=nib.Color.BLUE,
                                    width=30,
                                    height=30,
                                    offset=nib.Offset(20, 20),
                                ),
                                nib.Text(
                                    "offset=(20, 20)",
                                    font=nib.Font.CAPTION,
                                    offset=nib.Offset(20, 40),
                                ),
                            ],
                            height=100,
                        ),
                        nib.Divider(),
                        # Section 2: ZStack alignment
                        nib.Text("2. ZStack Alignment", font=nib.Font.HEADLINE),
                        nib.Text(
                            "Use alignment to position in corners",
                            font=nib.Font.CAPTION,
                            foreground_color=nib.Color.SECONDARY,
                        ),
                        nib.ZStack(
                            controls=[
                                nib.RoundedRectangle(
                                    fill=nib.Color.SECONDARY.with_opacity(0.1),
                                    corner_radius=8,
                                ),
                                # This circle will be in top-right corner
                                nib.Circle(
                                    fill=nib.Color.RED,
                                    width=20,
                                    height=20,
                                ),
                                nib.Text(
                                    "topTrailing",
                                    font=nib.Font.CAPTION,
                                    offset=nib.Offset(-30, 15),
                                ),
                            ],
                            alignment=nib.Alignment.TOP_TRAILING,  # or nib.Alignment.TOP_TRAILING
                            height=80,
                            padding=8,
                        ),
                        nib.Divider(),
                        # Section 3: Manual positioning with Spacers
                        nib.Text(
                            "3. Spacers for Absolute Positioning",
                            font=nib.Font.HEADLINE,
                        ),
                        nib.Text(
                            "Use Spacers to push content to corners",
                            font=nib.Font.CAPTION,
                            foreground_color=nib.Color.SECONDARY,
                        ),
                        nib.ZStack(
                            controls=[
                                nib.RoundedRectangle(
                                    fill=nib.Color.SECONDARY.with_opacity(0.1),
                                    corner_radius=8,
                                ),
                                # Top-right: HStack with Spacer pushing content right,
                                # wrapped in VStack with Spacer pushing to top
                                nib.VStack(
                                    controls=[
                                        nib.HStack(
                                            controls=[
                                                nib.Spacer(),
                                                nib.Circle(
                                                    fill=nib.Color.GREEN,
                                                    width=20,
                                                    height=20,
                                                ),
                                            ],
                                        ),
                                        nib.Spacer(),
                                    ],
                                    padding=8,
                                ),
                                # Bottom-left: opposite pattern
                                nib.VStack(
                                    controls=[
                                        nib.Spacer(),
                                        nib.HStack(
                                            controls=[
                                                nib.Circle(
                                                    fill=nib.Color.ORANGE,
                                                    width=20,
                                                    height=20,
                                                ),
                                                nib.Spacer(),
                                            ],
                                        ),
                                    ],
                                    padding=8,
                                ),
                                # Center content
                                nib.Text("Center", font=nib.Font.CAPTION),
                            ],
                            height=100,
                        ),
                        nib.Divider(),
                        # Section 4: Badge example (practical use case)
                        nib.Text("4. Practical Example: Badge", font=nib.Font.HEADLINE),
                        nib.HStack(
                            controls=[
                                nib.ZStack(
                                    controls=[
                                        nib.SFSymbol(
                                            "bell.fill",
                                            font=nib.Font.system(24),
                                            foreground_color=nib.Color.PRIMARY,
                                        ),
                                        # Badge in top-right
                                        nib.ZStack(
                                            controls=[
                                                nib.Circle(
                                                    fill=nib.Color.RED,
                                                    width=18,
                                                    height=18,
                                                ),
                                                nib.Text(
                                                    "3",
                                                    font=nib.Font.system(
                                                        10, weight=nib.FontWeight.BOLD
                                                    ),
                                                    foreground_color=nib.Color.WHITE,
                                                ),
                                            ],
                                            offset=nib.Offset(12, -12),
                                        ),
                                    ],
                                ),
                                nib.Spacer(),
                            ],
                            padding=20,
                        ),
                    ],
                    spacing=12,
                    padding=16,
                    alignment=nib.HorizontalAlignment.LEADING,
                )
            ]
        )
    )


nib.run(main)
