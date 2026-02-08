import nib


def main(app: nib.App):
    app.title = "Picker"
    app.icon = nib.SFSymbol("list.bullet")
    app.width = 300
    app.height = 350

    selected = nib.Text("Selected: Medium", font=nib.Font.CAPTION, foreground_color=nib.Color.SECONDARY)

    def on_change(value):
        selected.content = f"Selected: {value}"

    app.build(
        nib.VStack(
            controls=[
                nib.Form(
                    controls=[
                        nib.Section(
                            controls=[
                                nib.Picker(
                                    "Size",
                                    selection="Medium",
                                    options=["Small", "Medium", "Large"],
                                    style=nib.PickerStyle.MENU,
                                    on_change=on_change,
                                ),
                            ],
                            header="Menu Style",
                        ),
                        nib.Section(
                            controls=[
                                nib.Picker(
                                    "Color",
                                    selection="Blue",
                                    options=["Red", "Blue", "Green"],
                                    style=nib.PickerStyle.SEGMENTED,
                                ),
                            ],
                            header="Segmented Style",
                        ),
                        nib.Section(
                            controls=[
                                nib.Picker(
                                    "Priority",
                                    selection="normal",
                                    options=[
                                        ("low", "Low"),
                                        ("normal", "Normal"),
                                        ("high", "High"),
                                    ],
                                    style=nib.PickerStyle.INLINE,
                                ),
                            ],
                            header="Inline with (value, label) tuples",
                        ),
                    ],
                    style=nib.FormStyle.GROUPED,
                ),
                selected,
            ],
            spacing=8,
            padding=20,
        )
    )


nib.run(main)
