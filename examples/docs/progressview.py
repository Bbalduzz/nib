import nib


def main(app: nib.App):
    app.title = "ProgressView"
    app.icon = nib.SFSymbol("hourglass")
    app.width = 300
    app.height = 300

    progress = nib.ProgressView(value=0.0, total=1.0, label="Downloading...")
    progress_text = nib.Text("0%", font=nib.Font.CAPTION)

    def advance():
        new_val = min(progress.value + 0.1, 1.0)
        progress.value = new_val
        progress_text.content = f"{int(new_val * 100)}%"

    def reset():
        progress.value = 0.0
        progress_text.content = "0%"

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Indeterminate", font=nib.Font.HEADLINE),
                nib.ProgressView(),
                nib.Divider(),
                nib.Text("Linear", font=nib.Font.HEADLINE),
                progress,
                progress_text,
                nib.HStack(
                    controls=[
                        nib.Button("+10%", action=advance, style=nib.ButtonStyle.BORDERED),
                        nib.Button("Reset", action=reset, style=nib.ButtonStyle.BORDERED),
                    ],
                    spacing=8,
                ),
                nib.Divider(),
                nib.Text("Circular", font=nib.Font.HEADLINE),
                nib.ProgressView(
                    value=0.65,
                    total=1.0,
                    style=nib.ProgressStyle.CIRCULAR,
                    tint=nib.Color.ORANGE,
                ),
            ],
            spacing=10,
            padding=20,
        )
    )


nib.run(main)
