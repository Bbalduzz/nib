import nib


def main(app: nib.App):
    app.title = "Grid"
    app.icon = nib.SFSymbol("square.grid.2x2")
    app.width, app.height = 320, 350

    colors = [
        ("Red", nib.Color.RED),
        ("Orange", nib.Color.ORANGE),
        ("Yellow", nib.Color.YELLOW),
        ("Green", nib.Color.GREEN),
        ("Blue", nib.Color.BLUE),
        ("Purple", nib.Color.PURPLE),
    ]

    # 1. Create the Header
    header_row = nib.GridRow(
        controls=[
            nib.Text("Name", font=nib.Font.HEADLINE),
            nib.Text("Preview", font=nib.Font.HEADLINE),
        ]
    )

    # 2. Create the Data Rows
    data_rows = [
        nib.GridRow(
            controls=[
                nib.Text(name),
                nib.Rectangle(fill=color, width=40, height=24, corner_radius=4),
            ]
        )
        for name, color in colors
    ]

    # 3. Build the UI
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Grid", font=nib.Font.HEADLINE),
                nib.Grid(
                    # Combine header and data using unpacking (*)
                    controls=[header_row, *data_rows],
                    horizontal_spacing=16,
                    vertical_spacing=8,
                ),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
