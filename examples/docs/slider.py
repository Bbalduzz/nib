import nib


def main(app: nib.App):
    app.title = "Slider"
    app.icon = nib.SFSymbol("slider.horizontal.3")
    app.width = 300
    app.height = 250

    value_label = nib.Text("50", font=nib.Font.TITLE)

    def on_change(value):
        value_label.content = str(int(value))

    app.build(
        nib.VStack(
            controls=[
                value_label,
                nib.Divider(),
                nib.Text("Continuous", font=nib.Font.CAPTION),
                nib.Slider(
                    value=50,
                    min_value=0,
                    max_value=100,
                    on_change=on_change,
                ),
                nib.Text("Stepped (0, 25, 50, 75, 100)", font=nib.Font.CAPTION),
                nib.Slider(
                    value=50,
                    min_value=0,
                    max_value=100,
                    step=25,
                    on_change=on_change,
                ),
                nib.Text("Tinted", font=nib.Font.CAPTION),
                nib.Slider(
                    value=75,
                    min_value=0,
                    max_value=100,
                    tint=nib.Color.GREEN,
                ),
            ],
            spacing=8,
            alignment=nib.Alignment.LEADING,
            padding=20,
        )
    )


nib.run(main)
