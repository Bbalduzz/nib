import nib


def main(app: nib.App):
    app.title = "TextEditor"
    app.icon = nib.SFSymbol("doc.text")
    app.width = 300
    app.height = 350

    char_count = nib.Text("0 characters", font=nib.Font.CAPTION, foreground_color=nib.Color.SECONDARY)

    def on_change(value):
        char_count.content = f"{len(value)} characters"

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Notes", font=nib.Font.HEADLINE),
                nib.TextEditor(
                    text="",
                    placeholder="Write your notes here...",
                    on_change=on_change,
                    height=200,
                ),
                char_count,
            ],
            spacing=8,
            alignment=nib.Alignment.LEADING,
            padding=20,
        )
    )


nib.run(main)
