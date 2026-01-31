"""New Features Demo - Showcases new nib components.

Demonstrates Gauge, TextEditor, Grid, VisualEffectBlur, and more.
"""

import nib


def main(app: nib.App):
    app.title = "New Features"
    app.icon = nib.SFSymbol("sparkles")
    app.width = 380
    app.height = 550

    # ----- Gauges Section -----
    # Circular gauges (accessoryCircular doesn't show labels visually)
    cpu_gauge = nib.Gauge(
        value=0.65,
        label="CPU",
        current_value_label="65%",
        style=nib.GaugeStyle.CIRCULAR_CAPACITY,
        tint=nib.Color.BLUE,
    )

    memory_gauge = nib.Gauge(
        value=0.42,
        label="Mem",
        current_value_label="42%",
        style=nib.GaugeStyle.ACCESSORY_LINEAR_CAPACITY,
        tint=nib.Color.GREEN,
    )

    disk_gauge = nib.Gauge(
        value=0.78,
        label="Disk",
        current_value_label="78%",
        style=nib.GaugeStyle.ACCESSORY_CIRCULAR,
        tint=nib.Color.ORANGE,
    )

    # Linear gauge with VIEW labels - this style shows all labels!
    linear_gauge = nib.Gauge(
        value=0.35,
        label=nib.HStack(
            controls=[
                nib.SFSymbol("arrow.down.circle.fill"),
                nib.Text("Download", font=nib.Font.caption),
            ],
            spacing=4,
        ),
        current_value_label=nib.Text("35%", font=nib.Font.SUBHEADLINE),
        min_value_label=nib.SFSymbol("tortoise", foreground_color=nib.Color.GREEN),
        max_value_label=nib.SFSymbol("hare", foreground_color=nib.Color.RED),
        style=nib.GaugeStyle.LINEAR_CAPACITY,
        tint=nib.Color.WHITE,
    )

    gauges_section = nib.VStack(
        controls=[
            nib.Text("Gauges", font=nib.Font.headline),
            nib.HStack(
                controls=[cpu_gauge, disk_gauge, memory_gauge],
                spacing=16,
            ),
            linear_gauge,
        ],
        spacing=12,
        padding=12,
        background=nib.RoundedRectangle(
            corner_radius=10,
            fill=nib.Color.SECONDARY.with_opacity(0.1),
        ),
    )

    # ----- Grid Section -----
    grid_items = []
    colors = [
        nib.Color.RED,
        nib.Color.ORANGE,
        nib.Color.YELLOW,
        nib.Color.GREEN,
        nib.Color.BLUE,
        nib.Color.PURPLE,
    ]
    for color in colors:
        grid_items.append(
            nib.RoundedRectangle(
                corner_radius=6,
                fill=color,
                width=50,
                height=50,
            )
        )

    grid_section = nib.VStack(
        controls=[
            nib.Text("LazyVGrid", font=nib.Font.headline),
            nib.LazyVGrid(
                columns=[
                    nib.GridItem(nib.GridItemSize.FLEXIBLE),
                    nib.GridItem(nib.GridItemSize.FLEXIBLE),
                    nib.GridItem(nib.GridItemSize.FLEXIBLE),
                ],
                controls=grid_items,
                spacing=8,
            ),
        ],
        spacing=12,
        padding=12,
        background=nib.RoundedRectangle(
            corner_radius=10,
            fill=nib.Color.SECONDARY.with_opacity(0.1),
        ),
    )

    # ----- TextEditor Section -----
    notes = nib.TextEditor(
        # text="Write your notes here...",
        placeholder="Enter text",
        content_background=False,
        background=nib.RoundedRectangle(
            corner_radius=8,
            # fill=nib.Color.BLACK.with_opacity(0.1),
        ),
    )

    editor_section = nib.VStack(
        controls=[
            nib.Text("TextEditor", font=nib.Font.headline),
            notes,
        ],
        spacing=12,
        padding=12,
        height=120,
        background=nib.RoundedRectangle(
            corner_radius=10,
            fill=nib.Color.SECONDARY.with_opacity(0.1),
        ),
    )

    # ----- Share Section with Blur -----
    # ShareLink with custom view content
    share_button = nib.ShareLink(
        items=["Check out nib - Python framework for macOS menu bar apps!"],
        content=nib.HStack(
            controls=[
                nib.SFSymbol("square.and.arrow.up"),
                nib.Text("Share"),
            ],
            spacing=4,
        ),
    )

    share_section = nib.HStack(
        controls=[
            nib.SFSymbol("sparkles", foreground_color=nib.Color.BLUE),
            nib.Text("Share this app"),
            nib.Spacer(),
            share_button,
        ],
        spacing=12,
        padding=12,
        background=nib.VisualEffectBlur(
            material=nib.BlurStyle.THIN,
            corner_radius=10,
        ),
    )

    # ----- Main View -----
    main_view = nib.VStack(
        controls=[
            gauges_section,
            grid_section,
            editor_section,
            share_section,
        ],
        spacing=12,
        padding=16,
    )

    app.build(nib.ScrollView(controls=[main_view]))


nib.run(main)
