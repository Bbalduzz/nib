"""
System Features Test - Test nib notifications, clipboard, and file dialogs

Tests macOS system features from a bundled nib app.
"""

import nib


def main(app: nib.App):
    app.title = "System Test"
    app.icon = nib.SFSymbol("gearshape.fill")
    app.width = 320
    app.height = 480
    app.menu = [
        nib.MenuItem("Quit", action=app.quit),
    ]

    status = nib.Text("Ready")

    # --- Notifications ---
    notify_count = 0

    def send_basic():
        nonlocal notify_count
        notify_count += 1
        app.notify("Hello!", f"This is notification #{notify_count}")
        status.content = f"Sent notification #{notify_count}"

    def send_with_subtitle():
        nonlocal notify_count
        notify_count += 1
        app.notify(
            title="Download Complete",
            body="Your file has been saved successfully.",
            subtitle="System Test",
        )
        status.content = f"Sent notification #{notify_count}"

    # --- Clipboard ---
    clipboard_input = nib.TextField(value="", placeholder="Text to copy...")

    def copy_to_clipboard():
        text = clipboard_input.value
        if text:
            app.clipboard = text
            status.content = f"Copied: {text[:20]}{'...' if len(text) > 20 else ''}"
        else:
            status.content = "Nothing to copy"

    def read_clipboard():
        def on_read(text: str):
            if text:
                status.content = (
                    f"Clipboard: {text[:30]}{'...' if len(text) > 30 else ''}"
                )
            else:
                status.content = "Clipboard is empty"

        app.get_clipboard(on_read)

    # --- File Dialogs ---
    def open_file():
        def on_files(paths: list[str]):
            if paths:
                status.content = f"Selected: {paths[0].split('/')[-1]}"
            else:
                status.content = "No file selected"

        app.open_file_dialog(
            callback=on_files,
            title="Select a file",
            types=["txt", "md", "py"],
        )

    def open_multiple():
        def on_files(paths: list[str]):
            if paths:
                status.content = f"Selected {len(paths)} file(s)"
            else:
                status.content = "No files selected"

        app.open_file_dialog(
            callback=on_files,
            title="Select files",
            multiple=True,
        )

    def save_file():
        def on_path(path: str | None):
            if path:
                status.content = f"Save to: {path.split('/')[-1]}"
            else:
                status.content = "Save cancelled"

        app.save_file_dialog(
            callback=on_path,
            title="Save as",
            default_name="untitled.txt",
        )

    # --- Build UI ---
    app.build(
        nib.ScrollView(
            [
                nib.VStack(
                    controls=[
                        # Header
                        nib.Text("System Features Test", font=nib.Font.title),
                        nib.Spacer(min_length=8),
                        # Notifications Section
                        nib.Text("Notifications", font=nib.Font.headline),
                        nib.HStack(
                            controls=[
                                nib.Button("Send Basic", action=send_basic),
                                nib.Button("With Subtitle", action=send_with_subtitle),
                            ],
                            spacing=8,
                        ),
                        nib.Spacer(min_length=12),
                        nib.Divider(),
                        nib.Spacer(min_length=12),
                        # Clipboard Section
                        nib.Text("Clipboard", font=nib.Font.headline),
                        clipboard_input,
                        nib.HStack(
                            controls=[
                                nib.Button("Copy", action=copy_to_clipboard),
                                nib.Button("Read", action=read_clipboard),
                            ],
                            spacing=8,
                        ),
                        nib.Spacer(min_length=12),
                        nib.Divider(),
                        nib.Spacer(min_length=12),
                        # File Dialogs Section
                        nib.Text("File Dialogs", font=nib.Font.headline),
                        nib.HStack(
                            controls=[
                                nib.Button("Open File", action=open_file),
                                nib.Button("Open Multiple", action=open_multiple),
                            ],
                            spacing=8,
                        ),
                        nib.Button("Save File", action=save_file),
                        nib.Spacer(min_length=16),
                        nib.Divider(),
                        # Status
                        nib.Spacer(min_length=8),
                        nib.Text(
                            "Status:",
                            font=nib.Font.caption,
                            foreground_color=nib.Color.secondary,
                        ),
                        status,
                    ],
                    spacing=6,
                    padding=20,
                )
            ]
        )
    )


nib.run(main)
