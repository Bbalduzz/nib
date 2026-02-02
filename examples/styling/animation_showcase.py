"""Animation Showcase - Demonstrates all nib animation features.

This example showcases:
1. Sticky animations (property changes animate automatically)
2. Asymmetric transitions (different in/out animations)
3. Combined transitions (multiple effects together)
4. Pre-built custom transitions (pop_fade, bounce_in)
5. Custom keyframe transitions
"""

import nib


def main(app: nib.App):
    app.title = "Animation Demo"
    app.icon = nib.SFSymbol("wand.and.stars")
    app.width = 500
    app.height = 520

    # Colors
    bg_color = "#1C1C1E"
    text_secondary = "#8E8E93"
    accent = "#0A84FF"

    # =========================================================================
    # SECTION 1: Sticky Animations
    # =========================================================================
    # When you set animation on a view, ALL property changes animate

    progress_value = 0.0
    progress_bar = nib.Rectangle(
        corner_radius=4,
        fill=accent,
        width=progress_value,
        height=8,
        animation=nib.Animation.spring(response=0.4, damping=0.7),
    )

    progress_text = nib.Text(
        "0%",
        font=nib.Font.system(14, weight=nib.FontWeight.SEMIBOLD),
        animation=nib.Animation.easeInOut(0.3),
        content_transition=nib.ContentTransition.NUMERIC_TEXT,
    )

    def animate_progress():
        nonlocal progress_value
        progress_value = (progress_value + 0.25) % 1.25
        if progress_value > 1.0:
            progress_value = 0.0
        # These property changes will animate because animation is set
        progress_bar.width = progress_value * 200
        progress_text.content = f"{int(progress_value * 100)}%"

    sticky_section = nib.VStack(
        controls=[
            nib.Text(
                "Sticky Animations",
                font=nib.Font.caption,
                foreground_color=text_secondary,
            ),
            nib.Text(
                "Property changes animate automatically",
                font=nib.Font.system(11),
                foreground_color=text_secondary,
            ),
            nib.HStack(
                controls=[
                    nib.ZStack(
                        controls=[
                            nib.Rectangle(
                                corner_radius=4, fill="#333", width=200, height=8
                            ),
                            progress_bar,
                        ],
                        alignment=nib.Alignment.LEADING,
                    ),
                    progress_text,
                ],
                spacing=12,
            ),
            nib.Button(
                "Animate Progress",
                action=animate_progress,
                style=nib.ButtonStyle.BORDERED,
            ),
        ],
        alignment=nib.HorizontalAlignment.LEADING,
        spacing=8,
        padding=12,
        margin=16,
        background=nib.Rectangle(corner_radius=10, fill=bg_color),
    )

    # =========================================================================
    # SECTION 2: Asymmetric Transitions
    # =========================================================================
    # Different animations for appearing vs disappearing

    asymmetric_visible = True
    asymmetric_box = nib.Rectangle(
        corner_radius=8,
        fill="#30D158",
        width=60,
        height=60,
        transition=nib.Transition.asymmetric(
            insertion=nib.Transition.SCALE,
            removal=nib.Transition.OPACITY,
        ),
    )

    def toggle_asymmetric():
        nonlocal asymmetric_visible
        asymmetric_visible = not asymmetric_visible
        asymmetric_box.visible = asymmetric_visible

    asymmetric_section = nib.VStack(
        controls=[
            nib.Text(
                "Asymmetric Transitions",
                font=nib.Font.caption,
                foreground_color=text_secondary,
            ),
            nib.Text(
                "Scale in, fade out",
                font=nib.Font.system(11),
                foreground_color=text_secondary,
            ),
            nib.HStack(
                controls=[
                    asymmetric_box,
                    nib.Button(
                        "Toggle",
                        action=toggle_asymmetric,
                        style=nib.ButtonStyle.BORDERED,
                    ),
                ],
                spacing=16,
            ),
        ],
        alignment=nib.HorizontalAlignment.LEADING,
        spacing=8,
        padding=12,
        background=nib.Rectangle(corner_radius=10, fill=bg_color),
    )

    # =========================================================================
    # SECTION 3: Combined Transitions
    # =========================================================================
    # Multiple transition effects at once

    combined_visible = True
    combined_box = nib.Rectangle(
        corner_radius=8,
        fill="#FF9F0A",
        width=60,
        height=60,
        transition=nib.Transition.combined(
            nib.Transition.OPACITY,
            nib.Transition.SCALE,
        ),
    )

    def toggle_combined():
        nonlocal combined_visible
        combined_visible = not combined_visible
        combined_box.visible = combined_visible

    combined_section = nib.VStack(
        controls=[
            nib.Text(
                "Combined Transitions",
                font=nib.Font.caption,
                foreground_color=text_secondary,
            ),
            nib.Text(
                "Opacity + Scale together",
                font=nib.Font.system(11),
                foreground_color=text_secondary,
            ),
            nib.HStack(
                controls=[
                    combined_box,
                    nib.Button(
                        "Toggle", action=toggle_combined, style=nib.ButtonStyle.BORDERED
                    ),
                ],
                spacing=16,
            ),
        ],
        alignment=nib.HorizontalAlignment.LEADING,
        spacing=8,
        padding=12,
        background=nib.Rectangle(corner_radius=10, fill=bg_color),
    )

    # =========================================================================
    # SECTION 4: Pre-built Custom Transitions
    # =========================================================================

    popfade_visible = True
    popfade_box = nib.Rectangle(
        corner_radius=8,
        fill="#BF5AF2",
        width=60,
        height=60,
        transition=nib.Transition.pop_fade(),
    )

    def toggle_popfade():
        nonlocal popfade_visible
        popfade_visible = not popfade_visible
        popfade_box.visible = popfade_visible

    bounce_visible = True
    bounce_box = nib.Rectangle(
        corner_radius=8,
        fill="#FF453A",
        width=60,
        height=60,
        transition=nib.Transition.bounce_in(),
    )

    def toggle_bounce():
        nonlocal bounce_visible
        bounce_visible = not bounce_visible
        bounce_box.visible = bounce_visible

    prebuilt_section = nib.VStack(
        controls=[
            nib.Text(
                "Pre-built Custom Transitions",
                font=nib.Font.caption,
                foreground_color=text_secondary,
            ),
            nib.HStack(
                controls=[
                    nib.VStack(
                        controls=[
                            popfade_box,
                            nib.Text(
                                "pop_fade",
                                font=nib.Font.system(10),
                                foreground_color=text_secondary,
                            ),
                            nib.Button(
                                "Toggle",
                                action=toggle_popfade,
                                style=nib.ButtonStyle.BORDERED,
                            ),
                        ],
                        spacing=4,
                    ),
                    nib.VStack(
                        controls=[
                            bounce_box,
                            nib.Text(
                                "bounce_in",
                                font=nib.Font.system(10),
                                foreground_color=text_secondary,
                            ),
                            nib.Button(
                                "Toggle",
                                action=toggle_bounce,
                                style=nib.ButtonStyle.BORDERED,
                            ),
                        ],
                        spacing=4,
                    ),
                ],
                spacing=24,
            ),
        ],
        alignment=nib.HorizontalAlignment.LEADING,
        spacing=8,
        padding=12,
        background=nib.Rectangle(corner_radius=10, fill=bg_color),
    )

    # =========================================================================
    # SECTION 5: Custom Keyframe Transitions
    # =========================================================================

    # Custom swoosh transition
    swoosh_transition = (
        nib.Transition.custom("swoosh")
        .at(0.0, opacity=0, scale=0.5, offset_x=-30)
        .at(0.5, opacity=1, scale=1.1, offset_x=5)
        .at(1.0, opacity=1, scale=1.0, offset_x=0)
        .build()
    )

    swoosh_visible = True
    swoosh_box = nib.Rectangle(
        corner_radius=8,
        fill="#64D2FF",
        width=60,
        height=60,
        transition=swoosh_transition,
    )

    def toggle_swoosh():
        nonlocal swoosh_visible
        swoosh_visible = not swoosh_visible
        swoosh_box.visible = swoosh_visible

    custom_section = nib.VStack(
        controls=[
            nib.Text(
                "Custom Keyframe Transition",
                font=nib.Font.caption,
                foreground_color=text_secondary,
            ),
            nib.Text(
                "Swoosh: scale + offset + opacity",
                font=nib.Font.system(11),
                foreground_color=text_secondary,
            ),
            nib.HStack(
                controls=[
                    swoosh_box,
                    nib.Button(
                        "Toggle", action=toggle_swoosh, style=nib.ButtonStyle.BORDERED
                    ),
                ],
                spacing=16,
            ),
        ],
        alignment=nib.HorizontalAlignment.LEADING,
        spacing=8,
        padding=12,
        background=nib.Rectangle(corner_radius=10, fill=bg_color),
    )

    # =========================================================================
    # MAIN VIEW
    # =========================================================================

    app.build(
        nib.ScrollView(
            controls=[
                nib.VStack(
                    controls=[
                        nib.Text(
                            "Animation Showcase",
                            font=nib.Font.system(18, weight=nib.FontWeight.BOLD),
                        ),
                        sticky_section,
                        asymmetric_section,
                        combined_section,
                        prebuilt_section,
                        custom_section,
                    ],
                    spacing=12,
                    padding=16,
                )
            ],
        )
    )


nib.run(main)
