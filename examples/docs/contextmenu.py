import nib


def main(app: nib.App):
    app.title = "Context Menu"
    app.icon = nib.SFSymbol("cursorarrow.click.2")
    app.width = 300
    app.height = 200

    label = nib.Text("Right-click anywhere", font=nib.Font.HEADLINE)
    dark_mode = False

    def copy_text():
        app.clipboard = label.content
        label.content = "Copied!"

    def toggle_dark(value):
        nonlocal dark_mode
        dark_mode = value
        label.content = f"Dark mode: {'on' if value else 'off'}"

    def on_pick(value):
        label.content = f"Selected: {value}"

    app.build(
        nib.VStack(
            controls=[label],
            context_menu=[
                nib.Button("Copy Text", action=copy_text),
                nib.Button(
                    content=nib.HStack(
                        controls=[nib.SFSymbol("info"), nib.Text("Info")]
                    ),
                    action=lambda: None,
                ),
                nib.Button(
                    "Delete", action=lambda: print("Deleted"), role="destructive"
                ),
                nib.Divider(),
                nib.Toggle("Dark Mode", is_on=dark_mode, on_change=toggle_dark),
                nib.Picker(
                    "Size",
                    selection="Medium",
                    options=["Small", "Medium", "Large"],
                    on_change=on_pick,
                ),
                nib.Divider(),
                nib.Text("v1.0.0", foreground_color="#888"),
                nib.ShareLink(items=["Hello from nib!"], label="Share"),
            ],
            padding=40,
        )
    )


nib.run(main)
