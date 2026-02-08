import nib


def main(app: nib.App):
    app.title = "Styled Card"
    app.icon = nib.SFSymbol("rectangle.fill")
    app.width = 320
    app.height = 300

    app.build(
        nib.VStack(
            controls=[
                nib.VStack(
                    controls=[
                        nib.HStack(
                            controls=[
                                nib.SFSymbol(
                                    "bolt.fill",
                                    foreground_color=nib.Color.YELLOW,
                                    font=nib.Font.TITLE,
                                ),
                                nib.VStack(
                                    controls=[
                                        nib.Text("Performance", font=nib.Font.HEADLINE),
                                        nib.Text(
                                            "System stats",
                                            font=nib.Font.CAPTION,
                                            foreground_color=nib.Color.SECONDARY,
                                        ),
                                    ],
                                    alignment=nib.HorizontalAlignment.LEADING,
                                    spacing=2,
                                ),
                                nib.Spacer(),
                                nib.Text(
                                    "98%",
                                    font=nib.Font.TITLE,
                                    foreground_color=nib.Color.GREEN,
                                ),
                            ],
                            spacing=12,
                            alignment=nib.VerticalAlignment.CENTER,
                        ),
                        nib.Divider(),
                        nib.HStack(
                            controls=[
                                _metric("CPU", "12%"),
                                _metric("RAM", "4.2 GB"),
                                _metric("Disk", "128 GB"),
                            ],
                            spacing=16,
                        ),
                    ],
                    spacing=12,
                    padding=16,
                    background=nib.Rectangle(
                        corner_radius=12,
                        fill="#1c1c1e",
                        stroke="#2c2c2e",
                        stroke_width=1,
                    ),
                    shadow_color="#000000",
                    shadow_radius=8,
                    shadow_y=4,
                ),
            ],
            padding=16,
        )
    )


def _metric(label, value):
    return nib.VStack(
        controls=[
            nib.Text(value, font=nib.Font.system(14, nib.FontWeight.SEMIBOLD)),
            nib.Text(
                label, font=nib.Font.CAPTION, foreground_color=nib.Color.SECONDARY
            ),
        ],
        spacing=2,
    )


nib.run(main)
