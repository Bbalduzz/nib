import nib


def main(app: nib.App):
    app.title = "Table"
    app.icon = nib.SFSymbol("tablecells")
    app.width = 400
    app.height = 350

    selected_label = nib.Text("No selection", font=nib.Font.CAPTION, foreground_color=nib.Color.SECONDARY)

    def on_selection(ids):
        if ids:
            selected_label.content = f"Selected: {', '.join(ids)}"
        else:
            selected_label.content = "No selection"

    app.build(
        nib.VStack(
            controls=[
                nib.Table(
                    columns=[
                        nib.TableColumn("name", "Name", "name"),
                        nib.TableColumn("type", "Type", "type", width=80),
                        nib.TableColumn("size", "Size", "size", width=80, alignment="trailing"),
                    ],
                    rows=[
                        {"id": "1", "name": "README.md", "type": "Markdown", "size": "2 KB"},
                        {"id": "2", "name": "main.py", "type": "Python", "size": "4 KB"},
                        {"id": "3", "name": "icon.png", "type": "Image", "size": "32 KB"},
                        {"id": "4", "name": "config.json", "type": "JSON", "size": "1 KB"},
                        {"id": "5", "name": "style.css", "type": "CSS", "size": "8 KB"},
                    ],
                    on_selection=on_selection,
                    height=250,
                ),
                selected_label,
            ],
            spacing=8,
            padding=20,
        )
    )


nib.run(main)
