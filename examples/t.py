import nib


def main(app: nib.App):
    app.title = "Todo"
    app.icon = nib.SFSymbol("checklist")
    app.width = 340
    app.height = 450

    """
    nib.ScrollView(
        [
            nib.Text("Todo List"),
            nib.Button("Add Item"),
            nib.Button("Remove Item"),
        ]
    ),
    """

    app.menu = [
        nib.MenuItem(
            content=nib.ScrollView(
                [
                    nib.Text("Todo List"),
                    nib.Button("Add Item"),
                    nib.Button("Remove Item"),
                ]
            ),
            height=200,
        ),
        nib.MenuDivider(),
        nib.MenuItem("New"),
    ]

    app.build(nib.Text("Hello World"))


nib.run(main)
