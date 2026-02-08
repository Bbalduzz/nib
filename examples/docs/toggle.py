import nib


def main(app: nib.App):
    app.title = "Toggle"
    app.icon = nib.SFSymbol("switch.2")
    app.width = 300
    app.height = 300

    status = nib.Text("Wi-Fi: Off", font=nib.Font.CAPTION, foreground_color=nib.Color.SECONDARY)

    def on_wifi(value):
        status.content = f"Wi-Fi: {'On' if value else 'Off'}"

    app.build(
        nib.VStack(
            controls=[
                nib.Form(
                    controls=[
                        nib.Section(
                            controls=[
                                nib.Toggle("Wi-Fi", is_on=False, on_change=on_wifi),
                                nib.Toggle("Bluetooth", is_on=True),
                                nib.Toggle("Airplane Mode", is_on=False),
                            ],
                            header="Connectivity",
                        ),
                        nib.Section(
                            controls=[
                                nib.Toggle(
                                    "Checkbox style",
                                    is_on=True,
                                    style=nib.ToggleStyle.CHECKBOX,
                                ),
                            ],
                            header="Styles",
                        ),
                    ],
                    style=nib.FormStyle.GROUPED,
                ),
                status,
            ],
            spacing=8,
            padding=20,
        )
    )


nib.run(main)
