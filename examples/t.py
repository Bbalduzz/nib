import nib


def main(app: nib.App):
    app.title = "test"
    status = nib.Text("Off")

    def on_toggle(is_on: bool):
        status.content = "On" if is_on else "Off"

    app.build(
        nib.VStack(
            controls=[
                nib.Toggle(
                    "Enable notifications",
                    is_on=False,
                    on_change=on_toggle,
                ),
                status,
            ],
            spacing=12,
            padding=16,
        )
    )


nib.run(main)
