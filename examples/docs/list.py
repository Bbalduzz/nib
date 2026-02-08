import nib


def main(app: nib.App):
    app.title = "List"
    app.icon = nib.SFSymbol("list.bullet")
    app.width = 300
    app.height = 400

    app.build(
        nib.List(
            controls=[
                nib.Section(
                    controls=[
                        nib.Label("Inbox", icon="tray"),
                        nib.Label("Sent", icon="paperplane"),
                        nib.Label("Drafts", icon="doc"),
                        nib.Label("Trash", icon="trash"),
                    ],
                    header="Mailboxes",
                ),
                nib.Section(
                    controls=[
                        nib.Label("Work", icon="briefcase"),
                        nib.Label("Personal", icon="person"),
                        nib.Label("Travel", icon="airplane"),
                    ],
                    header="Folders",
                ),
            ],
        )
    )


nib.run(main)
