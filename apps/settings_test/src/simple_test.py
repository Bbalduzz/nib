"""Simple test app without Settings."""
import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Simple Test"
    app.width = 300
    app.height = 200

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Simple Test App", font=nib.Font.title),
                nib.Button("Click Me", action=lambda: print("Clicked!")),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
