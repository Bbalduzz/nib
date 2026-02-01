"""Demo of Launch at Login service.

Shows how to enable/disable launch at login in response to user action.
Per Mac App Store guidelines, this must be triggered by user interaction.
"""

import nib


def main(app: nib.App):
    app.title = "Launch at Login"
    app.icon = nib.SFSymbol("power")
    app.width = 300
    app.height = 200
    app.menu = [nib.MenuItem("Quit", action=app.quit)]

    # Status text
    status_text = nib.Text("Checking...", font=nib.Font.HEADLINE)

    def update_status():
        if app.launch_at_login.is_enabled:
            status_text.content = "Enabled"
            status_text.foreground_color = nib.Color.GREEN
        else:
            status_text.content = "Disabled"
            status_text.foreground_color = nib.Color.SECONDARY

    def toggle_launch_at_login():
        current = app.launch_at_login.is_enabled
        success = app.launch_at_login.set(not current)
        if success:
            update_status()
        else:
            status_text.content = "Failed"
            status_text.foreground_color = nib.Color.RED

    # Use on_appear to check status after connection is ready
    app.on_appear = update_status

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Launch at Login", font=nib.Font.TITLE),
                nib.Divider(),
                nib.HStack(
                    controls=[
                        nib.Text("Status:", foreground_color=nib.Color.SECONDARY),
                        status_text,
                    ],
                    spacing=8,
                ),
                nib.Spacer(),
                nib.Button(
                    "Toggle Launch at Login",
                    action=toggle_launch_at_login,
                    style=nib.ButtonStyle.BORDERED_PROMINENT,
                ),
                nib.Spacer(),
                nib.Text(
                    "Note: Requires macOS 13+ and a bundled app.",
                    font=nib.Font.CAPTION,
                    foreground_color=nib.Color.SECONDARY,
                ),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
