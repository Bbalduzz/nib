import nib


def main(app: nib.App):
    app.title = "Form"
    app.icon = nib.SFSymbol("doc.plaintext")
    app.width = 350
    app.height = 350

    app.build(
        nib.Form(
            controls=[
                nib.Section(
                    controls=[
                        nib.TextField(
                            "Name",
                            value="",
                            style=nib.TextFieldStyle.ROUNDED_BORDER,
                        ),
                        nib.TextField(
                            "Email",
                            value="",
                            style=nib.TextFieldStyle.ROUNDED_BORDER,
                        ),
                    ],
                    header="Account",
                ),
                nib.Section(
                    controls=[
                        nib.Toggle("Dark Mode", is_on=False),
                        nib.Picker(
                            "Language",
                            selection="English",
                            options=["English", "Spanish", "French"],
                            style=nib.PickerStyle.MENU,
                        ),
                        nib.Slider(
                            label="Font Size",
                            value=14,
                            min_value=10,
                            max_value=24,
                            step=1,
                        ),
                    ],
                    header="Preferences",
                ),
            ],
            style=nib.FormStyle.GROUPED,
        )
    )


nib.run(main)
