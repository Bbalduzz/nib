import nib
from nib.notifications import Notification, NotificationSound


def main(app: nib.App):
    app.title = "Notifications"
    app.icon = nib.SFSymbol("bell")
    app.width = 300
    app.height = 250

    status = nib.Text("No notification sent yet.", font=nib.Font.CAPTION, foreground_color=nib.Color.SECONDARY)

    def send_basic():
        app.notify("Hello!", "This is a basic notification.")
        status.content = "Basic notification sent."

    def send_rich():
        app.notifications.push(
            Notification(
                title="Download Complete",
                body="Your file has been downloaded successfully.",
                subtitle="2.4 MB",
                sound=NotificationSound(),
            )
        )
        status.content = "Rich notification sent."

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Notifications", font=nib.Font.TITLE),
                nib.Divider(),
                nib.Button(
                    "Send Basic",
                    icon="bell",
                    action=send_basic,
                    style=nib.ButtonStyle.BORDERED,
                ),
                nib.Button(
                    "Send Rich",
                    icon="bell.badge",
                    action=send_rich,
                    style=nib.ButtonStyle.BORDERED_PROMINENT,
                ),
                nib.Spacer(),
                status,
            ],
            spacing=10,
            padding=20,
        )
    )


nib.run(main)
