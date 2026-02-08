"""
Noteit - A nib application
"""

import dbm
import json
import lzma
import uuid
from datetime import datetime
from pathlib import Path

import nib

DB_PATH = Path(__file__).resolve().parent / "notes.db"

FONT_OPTIONS = [
    "Iosevka",
    "System",
    "Menlo",
    "Monaco",
    "SF Mono",
    "Courier New",
    "Helvetica Neue",
]

WEIGHT_OPTIONS = ["thin", "light", "regular", "medium", "semibold", "bold", "heavy"]

WEIGHT_MAP = {
    "thin": nib.FontWeight.THIN,
    "light": nib.FontWeight.LIGHT,
    "regular": nib.FontWeight.REGULAR,
    "medium": nib.FontWeight.MEDIUM,
    "semibold": nib.FontWeight.SEMIBOLD,
    "bold": nib.FontWeight.BOLD,
    "heavy": nib.FontWeight.HEAVY,
}


def compress(note_dict):
    return lzma.compress(json.dumps(note_dict).encode())


def decompress(data):
    return json.loads(lzma.decompress(data))


def main(app: nib.App):
    app.icon = nib.SFSymbol(
        "text.redaction", rendering_mode=nib.SymbolRenderingMode.HIERARCHICAL
    )
    app.height = 200
    app.fonts = {
        "Iosevka": "fonts/Iosevka/Iosevka-Regular.ttf",
        "Iosevka-BoldItalic": "fonts/Iosevka/Iosevka-BoldItalic.ttf",
    }

    current_note_id = None

    settings = nib.Settings(
        {
            "width": 280,
            "height": 200,
            "database_path": str(DB_PATH.resolve()),
            "accent_color": "#ED9516",
            "font": "Iosevka",
            "font_size": 14,
            "font_weight": "bold",
            "text_color": "#FFFFFF",
            "text_opacity": 0.7,
            "line_spacing": 4,
            "editor_bg_opacity": 0.0,
        }
    )
    app.register_settings(settings)

    word_count = nib.Text(
        "0",
        font=nib.Font.custom("Iosevka", size=11),
        foreground_color=nib.Color("#4D535E"),
    )

    text_editor = nib.TextEditor(
        style=nib.TextEditorStyle(
            font=nib.Font.custom("Iosevka", size=13, weight=nib.FontWeight.BOLD),
            foreground_color=nib.Color.WHITE.with_opacity(0.7),
            background_color=nib.Color.BLACK.with_opacity(0),
            line_spacing=4,
        ),
        on_change=lambda text: setattr(word_count, "content", str(len(text.split()))),
    )

    def apply_editor_style():
        font_name = settings.font
        font_size = settings.font_size
        weight = WEIGHT_MAP.get(settings.font_weight, nib.FontWeight.BOLD)
        text_color = settings.text_color
        text_opacity = settings.text_opacity
        line_spacing = settings.line_spacing
        editor_bg_opacity = settings.editor_bg_opacity

        text_editor.style = nib.TextEditorStyle(
            font=nib.Font.custom(font_name, size=font_size, weight=weight),
            foreground_color=nib.Color(text_color).with_opacity(text_opacity),
            background_color=nib.Color.BLACK.with_opacity(editor_bg_opacity),
            line_spacing=line_spacing,
        )
        text_editor.update()

    def update_setting(name, value):
        setattr(settings, name, value)
        app.width = settings.width
        app.height = settings.height
        apply_editor_style()

    # --- Note storage ---

    def save_note():
        nonlocal current_note_id
        print("Saving note...")
        text = text_editor.text
        if not text.strip():
            return
        note_id = current_note_id or str(uuid.uuid4())
        note = {
            "title": text.strip().split("\n")[0][:50],
            "content": text,
            "timestamp": datetime.now().isoformat(),
            "word_count": len(text.split()),
        }
        with dbm.open(str(DB_PATH), "c") as db:
            db[note_id] = compress(note)
        current_note_id = note_id
        word_count.content = str(note["word_count"])
        rebuild_menu()

    def load_note(key):
        nonlocal current_note_id
        with dbm.open(str(DB_PATH), "r") as db:
            note = decompress(db[key])
        text_editor.text = note["content"]
        word_count.content = str(note["word_count"])
        current_note_id = key
        app.update()

    def new_note():
        nonlocal current_note_id
        text_editor.text = ""
        word_count.content = "0"
        current_note_id = None
        app.update()

    def delete_note(key):
        nonlocal current_note_id
        with dbm.open(str(DB_PATH), "c") as db:
            del db[key]
        if current_note_id == key:
            new_note()
        rebuild_menu()

    def rebuild_menu():
        notes = []
        try:
            with dbm.open(str(DB_PATH), "r") as db:
                for key in db.keys():
                    note = decompress(db[key])
                    note["id"] = key.decode() if isinstance(key, bytes) else key
                    notes.append(note)
        except dbm.error:
            pass

        notes.sort(key=lambda n: n["timestamp"], reverse=True)

        menu_items = []

        if notes:
            for note in notes:
                did = note["id"]

                def make_load_action(k):
                    return lambda: load_note(k)

                def make_delete_action(k):
                    return lambda: delete_note(k)

                dt = datetime.fromisoformat(note["timestamp"])
                date_str = dt.strftime("%b %d, %H:%M")
                wc = f"{note['word_count']}w"

                menu_items.append(
                    nib.MenuItem(
                        content=nib.VStack(
                            [
                                nib.Text(
                                    note["title"][:20] + "...",
                                    font=nib.Font.custom("Iosevka", size=12),
                                ),
                                nib.Text(
                                    f"{date_str}  {wc}",
                                    font=nib.Font.CAPTION,
                                    foreground_color=nib.Color.WHITE.with_opacity(0.5),
                                ),
                            ],
                            alignment=nib.Alignment.LEADING,
                            margin={"leading": -35},
                        ),
                        action=make_load_action(did),
                        height=38,
                        menu=[
                            nib.MenuItem(
                                "Delete",
                                icon="trash",
                                action=make_delete_action(did),
                            ),
                        ],
                    )
                )
        else:
            menu_items.append(
                nib.MenuItem(
                    content=nib.VStack(
                        [
                            nib.Text("No notes saved"),
                            nib.Text(
                                "Here you'll see the history",
                                font=nib.Font.CAPTION,
                                foreground_color=nib.Color.WHITE.with_opacity(0.5),
                            ),
                        ],
                        alignment=nib.Alignment.LEADING,
                        margin={"leading": -40},
                    ),
                    height=35,
                )
            )

        menu_items.extend(
            [
                nib.MenuDivider(),
                nib.MenuItem(
                    "Settings",
                    shortcut="cmd+,",
                    action=lambda: app.settings.open(),
                ),
                nib.MenuItem("Quit", shortcut="cmd+q", action=app.quit),
            ]
        )

        app.menu = menu_items
        app.update()

    # --- Hotkeys ---

    @app.hotkey("ctrl+s")
    def _save():
        save_note()

    @app.hotkey("ctrl+n")
    def _new():
        new_note()

    # --- Settings page ---

    app.settings = nib.SettingsPage(
        title="Preferences",
        width=450,
        height=350,
        tabs=[
            nib.SettingsTab(
                "General",
                icon="gear",
                content=nib.Form(
                    controls=[
                        nib.Section(
                            header="Info",
                            controls=[
                                nib.HStack(
                                    [
                                        nib.Text("Database"),
                                        nib.Spacer(),
                                        nib.Text(
                                            str(DB_PATH.resolve()),
                                            style=nib.TextStyle(
                                                color=nib.Color.WHITE.with_opacity(0.5)
                                            ),
                                        ),
                                    ],
                                    on_click=lambda _: print(
                                        "open filepicker and select new database path"
                                    ),
                                ),
                            ],
                        ),
                        nib.Section(
                            controls=[
                                nib.HStack(
                                    [
                                        nib.Text("Popup width"),
                                        nib.Slider(
                                            label="width",
                                            value=280,
                                            min_value=0,
                                            max_value=600,
                                            on_change=lambda v: update_setting(
                                                "width", v
                                            ),
                                        ),
                                    ]
                                ),
                                nib.HStack(
                                    [
                                        nib.Text("Popup height"),
                                        nib.Slider(
                                            label="height",
                                            value=300,
                                            min_value=0,
                                            max_value=600,
                                            on_change=lambda v: update_setting(
                                                "height", v
                                            ),
                                        ),
                                    ]
                                ),
                                nib.TextField(
                                    "Accent Color",
                                    value=settings.accent_color,
                                    on_submit=lambda v: update_setting(
                                        "accent_color", v
                                    ),
                                ),
                            ],
                            header="Appearance",
                        ),
                    ],
                    style=nib.FormStyle.GROUPED,
                ),
            ),
            nib.SettingsTab(
                "Editor",
                icon="textformat.size",
                content=nib.Form(
                    style=nib.FormStyle.GROUPED,
                    controls=[
                        nib.Section(
                            header="Typography",
                            controls=[
                                nib.Picker(
                                    label="Font",
                                    selection=settings.font,
                                    options=FONT_OPTIONS,
                                    on_change=lambda v: update_setting("font", v),
                                ),
                                nib.Picker(
                                    label="Weight",
                                    selection=settings.font_weight,
                                    options=WEIGHT_OPTIONS,
                                    on_change=lambda v: update_setting(
                                        "font_weight", v
                                    ),
                                ),
                                nib.HStack(
                                    [
                                        nib.Text("Font size"),
                                        nib.Slider(
                                            label="size",
                                            value=settings.font_size,
                                            min_value=8,
                                            max_value=24,
                                            step=1,
                                            on_change=lambda v: update_setting(
                                                "font_size", v
                                            ),
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        nib.Section(
                            header="Appearance",
                            controls=[
                                nib.TextField(
                                    "Text color",
                                    value=settings.text_color,
                                    on_submit=lambda v: update_setting("text_color", v),
                                ),
                                nib.HStack(
                                    [
                                        nib.Text("Text opacity"),
                                        nib.Slider(
                                            label="opacity",
                                            value=settings.text_opacity,
                                            min_value=0.0,
                                            max_value=1.0,
                                            on_change=lambda v: update_setting(
                                                "text_opacity", v
                                            ),
                                        ),
                                    ]
                                ),
                                nib.HStack(
                                    [
                                        nib.Text("Editor bg opacity"),
                                        nib.Slider(
                                            label="bg opacity",
                                            value=settings.editor_bg_opacity,
                                            min_value=0.0,
                                            max_value=1.0,
                                            on_change=lambda v: update_setting(
                                                "editor_bg_opacity", v
                                            ),
                                        ),
                                    ]
                                ),
                                nib.HStack(
                                    [
                                        nib.Text("Line spacing"),
                                        nib.Slider(
                                            label="spacing",
                                            value=settings.line_spacing,
                                            min_value=0,
                                            max_value=12,
                                            step=1,
                                            on_change=lambda v: update_setting(
                                                "line_spacing", v
                                            ),
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )

    # --- Commands row ---
    accent = settings.accent_color

    commands_row = nib.HStack(
        controls=[
            nib.HStack(
                controls=[
                    nib.Text(
                        "^s",
                        font=nib.Font.custom(
                            "Iosevka-BoldItalic", weight=nib.FontWeight.BOLD, size=13
                        ),
                        foreground_color=nib.Color(accent),
                    ),
                    nib.Text(
                        "ave",
                        font=nib.Font.custom("Iosevka", size=13),
                    ),
                ],
                spacing=0.5,
                on_click=save_note,
            ),
            nib.HStack(
                controls=[
                    nib.Text(
                        "^n",
                        font=nib.Font.custom(
                            "Iosevka-BoldItalic", weight=nib.FontWeight.BOLD, size=13
                        ),
                        foreground_color=nib.Color(accent),
                    ),
                    nib.Text(
                        "ew",
                        font=nib.Font.custom("Iosevka", size=13),
                    ),
                ],
                spacing=0.5,
                on_click=new_note,
            ),
        ],
        spacing=12,
    )

    # --- Build UI ---

    app.build(
        nib.VStack(
            controls=[
                text_editor,
                nib.HStack([word_count, nib.Spacer(), commands_row]),
            ],
            padding={"leading": 14, "trailing": 14, "top": 14, "bottom": 10},
        )
    )

    rebuild_menu()


nib.run(main, assets_dir="assets")
