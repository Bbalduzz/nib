import nib


def main(app: nib.App):
    app.title = "Table Example"
    app.icon = nib.SFSymbol("tablecells.fill")
    app.width = 400
    app.height = 300

    files = [
        {"name": "Document.txt", "size": "4 KB", "modified": "Today"},
        {"name": "Image.png", "size": "1.2 MB", "modified": "Yesterday"},
        {"name": "Archive.zip", "size": "45 MB", "modified": "Last week"},
    ]

    app.build(
        nib.Table(
            rows=files,
            columns=[
                nib.TableColumn(
                    "Name",
                    key=lambda f: f["name"],
                    width=nib.ColumnWidth.range(min=50, ideal=150, max=300),
                ),
                nib.TableColumn(
                    "Size",
                    key=lambda f: f["size"],
                    alignment="trailing",
                    width=nib.ColumnWidth.fixed(80),
                ),
                nib.TableColumn(
                    "Modified",
                    key=lambda f: f["modified"],
                    width=nib.ColumnWidth.fixed(100),
                ),
            ],
            on_select=lambda rows: print(f"Selected: {[r['name'] for r in rows]}"),
        )
    )


nib.run(main)
