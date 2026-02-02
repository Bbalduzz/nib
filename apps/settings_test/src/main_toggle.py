"""Test Toggle in MAIN window (not settings)."""
import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Main Toggle Test"
    app.width = 300
    app.height = 200

    def on_toggle_change(value):
        print(f"[DEBUG] Main toggle changed to: {value}")

    # NO settings page - just main app with Toggle
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Main Window Toggle Test"),
                nib.Toggle("Test Toggle", is_on=False, on_change=on_toggle_change),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
