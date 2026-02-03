"""Demo of the FilePicker API.

Shows how to use:
- pick_files(): Select one or multiple files with filtering
- pick_directory(): Select folders
- save_file(): Save dialog with suggested filename
"""

import os

import nib


def main(app: nib.App):
    app.title = "FilePicker"
    app.icon = nib.SFSymbol("folder.fill")
    app.width = 380
    app.height = 450

    def my_quit():
        print("my_quit called!")  # Debug
        app.quit()

    app.menu = [nib.MenuItem("Quit", action=my_quit)]
    app.on_quit = lambda: print("Bye!")
    app.on_appear = lambda: print("App appeared!")
    app.on_disappear = lambda: print("App disappeared!")
    picker = nib.FilePicker()

    # Status display
    status_text = nib.Text(
        "No file selected",
        font=nib.Font.CAPTION,
        foreground_color=nib.Color.SECONDARY,
    )

    # File info display
    file_info = nib.Text("", font=nib.Font.system(11, weight=nib.FontWeight.REGULAR))

    def update_status(msg: str):
        status_text.content = msg
        file_info.content = ""

    def show_file_info(files: list[nib.PickedFile]):
        if not files:
            return
        info_lines = []
        for f in files[:3]:  # Show max 3 files
            size_kb = f.size / 1024
            tags_str = f", tags: {f.tags}" if f.tags else ""
            info_lines.append(f"{f.name} ({size_kb:.1f} KB){tags_str}")
        if len(files) > 3:
            info_lines.append(f"... and {len(files) - 3} more")
        file_info.content = "\n".join(info_lines)

    # Pick single file
    def pick_single():
        files = picker.pick_files(
            title="Select a File",
            button_label="Choose",
        )
        if files:
            update_status(f"Selected: {files[0].name}")
            show_file_info(files)
        else:
            update_status("Cancelled")

    # Pick multiple images
    def pick_images():
        files = picker.pick_files(
            multiple=True,
            extensions=["png", "jpg", "jpeg", "gif", "webp"],
            title="Select Images",
            message="Choose one or more image files",
            button_label="Select Images",
        )
        if files:
            update_status(f"Selected {len(files)} image(s)")
            show_file_info(files)
        else:
            update_status("Cancelled")

    # Pick with UTType
    def pick_documents():
        files = picker.pick_files(
            multiple=True,
            uttypes=["public.text", "com.adobe.pdf"],
            title="Select Documents",
            shows_hidden_files=False,
        )
        if files:
            update_status(f"Selected {len(files)} document(s)")
            show_file_info(files)
        else:
            update_status("Cancelled")

    # Pick directory
    def pick_folder():
        dirs = picker.pick_directory(
            title="Select Output Folder",
            message="Choose where to save files",
            can_create_directories=True,
        )
        if dirs:
            folder_name = os.path.basename(dirs[0])
            update_status(f"Folder: {folder_name}")
            file_info.content = dirs[0]
        else:
            update_status("Cancelled")

    # Save file
    def save_document():
        result = picker.save_file(
            filename="untitled.txt",
            extensions=["txt", "md"],
            title="Save Document",
            name_field_label="Export as:",
            shows_tag_field=True,
        )
        if result:
            update_status(f"Save to: {os.path.basename(result.path)}")
            tags_str = f"Tags: {result.tags}" if result.tags else "No tags"
            file_info.content = f"{result.path}\n{tags_str}"
        else:
            update_status("Cancelled")

    # Pick with validation
    def pick_small_files():
        def validate(paths: list[str]) -> str | None:
            for p in paths:
                size = os.path.getsize(p)
                if size > 1_000_000:  # 1 MB limit
                    return f"File too large: {os.path.basename(p)} ({size // 1024} KB > 1 MB)"
            return None

        files = picker.pick_files(
            multiple=True,
            title="Select Small Files",
            message="Files must be under 1 MB",
            validator=validate,
        )
        if files:
            total_size = sum(f.size for f in files)
            update_status(
                f"Selected {len(files)} file(s), {total_size // 1024} KB total"
            )
            show_file_info(files)
        else:
            update_status("Cancelled or validation failed")

    app.build(
        nib.VStack(
            controls=[
                nib.Text("FilePicker Demo", font=nib.Font.TITLE2),
                nib.Divider(),
                # Status section
                nib.VStack(
                    controls=[status_text, file_info],
                    spacing=4,
                    padding={"horizontal": 12, "vertical": 8},
                    background=nib.Rectangle(
                        corner_radius=8,
                        fill=nib.Color.rgba(0, 0, 0, 0.05),
                    ),
                ),
                nib.Spacer(),
                # Buttons
                nib.VStack(
                    controls=[
                        nib.Text("Pick Files", font=nib.Font.HEADLINE),
                        nib.HStack(
                            controls=[
                                nib.Button("Single File", action=pick_single),
                                nib.Button("Images", action=pick_images),
                            ],
                            spacing=8,
                        ),
                        nib.HStack(
                            controls=[
                                nib.ZStack(
                                    [
                                        nib.Rectangle(
                                            corner_radius=5,
                                            fill=nib.LinearGradient(
                                                colors=[
                                                    nib.Color.WHITE.with_opacity(0.8),
                                                    nib.Color.GRAY.with_opacity(0.8),
                                                ],
                                                start=(0, 0),
                                                end=(0, 1),
                                            ),
                                            height=22,
                                            width=90,
                                        ),
                                        nib.Button(
                                            "Documents",
                                            action=pick_documents,
                                            style=nib.ButtonStyle.PLAIN,
                                        ),
                                    ]
                                ),
                                nib.Button("Small (<1MB)", action=pick_small_files),
                            ],
                            spacing=8,
                        ),
                        nib.Divider(),
                        nib.Text("Directories & Save", font=nib.Font.HEADLINE),
                        nib.HStack(
                            controls=[
                                nib.Button("Pick Folder", action=pick_folder),
                                nib.Button("Save File...", action=save_document),
                            ],
                            spacing=8,
                        ),
                    ],
                    spacing=12,
                ),
            ],
            spacing=16,
            padding=20,
        )
    )


nib.run(main)
