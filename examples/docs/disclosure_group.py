import nib


def main(app: nib.App):
    app.title = "DisclosureGroup"
    app.icon = nib.SFSymbol("chevron.down")
    app.width = 300
    app.height = 350

    app.build(
        nib.VStack(
            controls=[
                nib.DisclosureGroup(
                    "General",
                    controls=[
                        nib.Toggle("Notifications", is_on=True),
                        nib.Toggle("Sound", is_on=False),
                    ],
                    is_expanded=True,
                ),
                nib.DisclosureGroup(
                    "Advanced",
                    controls=[
                        nib.Toggle("Debug Mode", is_on=False),
                        nib.Toggle("Verbose Logging", is_on=False),
                        nib.Slider(
                            label="Timeout",
                            value=30,
                            min_value=5,
                            max_value=120,
                            step=5,
                        ),
                    ],
                    is_expanded=False,
                ),
                nib.DisclosureGroup(
                    "About",
                    controls=[
                        nib.Text("Version 1.0.0", font=nib.Font.CAPTION),
                        nib.Link("Website", url="https://example.com"),
                    ],
                    is_expanded=False,
                ),
            ],
            spacing=4,
            padding=20,
        )
    )


nib.run(main)
