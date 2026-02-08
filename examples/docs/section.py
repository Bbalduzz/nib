import nib


def main(app: nib.App):
    app.title = "Section"
    app.icon = nib.SFSymbol("rectangle.3.group")
    app.width = 300
    app.height = 350

    app.build(
        nib.Form(
            controls=[
                nib.Section(
                    controls=[
                        nib.Toggle("Wi-Fi", is_on=True),
                        nib.Toggle("Bluetooth", is_on=True),
                    ],
                    header="Connectivity",
                    footer="Turn off to save battery.",
                ),
                nib.Section(
                    controls=[
                        nib.Toggle("Notifications", is_on=True),
                        nib.Toggle("Sound", is_on=False),
                    ],
                    header="Alerts",
                ),
                nib.Section(
                    controls=[
                        nib.Label("Version", icon="info.circle"),
                        nib.Label("License", icon="doc.text"),
                    ],
                    header="About",
                ),
            ],
            style=nib.FormStyle.GROUPED,
        )
    )


nib.run(main)
