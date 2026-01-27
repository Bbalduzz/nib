"""
Did You Know? - Music Info Popover

A recreation of the SwiftUI PopoverView showing currently playing music info.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

import nib

# Design tokens
CARD_BG = "#262626"
CARD_BORDER = "#696969"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#999999"
ACCENT = "#FF9500"


# State
class State:
    show_full_description = False
    is_loading = False


def main(app: nib.App):
    app.title = "Did You Know?"
    app.icon = nib.SFSymbol("music.note.list")
    app.width = 350
    # app.height = 800
    app.menu = [
        nib.MenuItem("Quit", action=app.quit),
    ]

    state = State()

    # Mock data (in real app, this would come from a service)
    track = {
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "source": "Spotify",
        "source_color": CARD_BORDER,
        "year": "1975",
        "country_flag": "🇬🇧",
        "country_name": "United Kingdom",
        "duration": "5:55",
        "writers": ["Freddie Mercury"],
        "producers": ["Roy Thomas Baker", "Queen"],
        "album": "A Night at the Opera",
        "description": (
            "Bohemian Rhapsody is a song by the British rock band Queen. It was written by "
            "Freddie Mercury for the band's 1975 album A Night at the Opera. The song is a "
            "six-minute suite, consisting of several sections without a chorus: an intro, "
            "a ballad segment, an operatic passage, a hard rock part and a reflective coda. "
            "The song is a masterpiece of studio production and arrangement."
        ),
    }

    # ─────────────────────────────────────────────────────────────────────────
    # Build UI
    # ─────────────────────────────────────────────────────────────────────────

    def build_ui():
        if state.show_full_description:
            app.build(expanded_description_view())
        else:
            app.build(main_view())

    # ─────────────────────────────────────────────────────────────────────────
    # Main View
    # ─────────────────────────────────────────────────────────────────────────

    def main_view():
        return nib.VStack(
            controls=[
                header_view(),
                content_view(),
            ],
            spacing=12,
            # padding=16,
            padding={"top": 12, "bottom": 12, "leading": 10, "trailing": 10},
            # padding={"horizontal": 16, "vertical": 0},
            # width=300,
        )

    # ─────────────────────────────────────────────────────────────────────────
    # Expanded Description View
    # ─────────────────────────────────────────────────────────────────────────

    def expanded_description_view():
        def go_back():
            state.show_full_description = False
            build_ui()

        return nib.VStack(
            controls=[
                # Header with back button
                nib.HStack(
                    controls=[
                        nib.Button(
                            content=nib.HStack(
                                controls=[
                                    nib.SFSymbol(
                                        "chevron.left",
                                        font=nib.Font.system(
                                            12, nib.FontWeight.semibold
                                        ),
                                        foreground_color=ACCENT,
                                    ),
                                    nib.Text(
                                        "Back",
                                        font=nib.Font.system(12, nib.FontWeight.medium),
                                        foreground_color=ACCENT,
                                    ),
                                ],
                                spacing=4,
                            ),
                            padding={"horizontal": 5},
                            action=go_back,
                            style=nib.ButtonStyle.plain,
                        ),
                        nib.Spacer(),
                        nib.Text(
                            "About this song",
                            font=nib.Font.system(13, nib.FontWeight.semibold),
                            foreground_color=TEXT_PRIMARY,
                        ),
                        nib.Spacer(),
                        # Placeholder for balance
                        nib.Text("Back", font=nib.Font.system(12), opacity=0),
                    ],
                    padding={"bottom": 4},
                ),
                # Full description in scroll view
                nib.ScrollView(
                    controls=[
                        nib.Text(
                            track["description"],
                            font=nib.Font.system(12),
                            foreground_color="#FFFFFFE6",
                        ),
                    ],
                ),
            ],
            spacing=12,
            padding=16,
            width=340,
        )

    # ─────────────────────────────────────────────────────────────────────────
    # Header View
    # ─────────────────────────────────────────────────────────────────────────

    def header_view():
        return nib.HStack(
            controls=[
                # Track info
                nib.HStack(
                    controls=[
                        nib.ZStack(
                            controls=[
                                nib.RoundedRectangle(
                                    corner_radius=8,
                                    fill=track["source_color"],
                                    width=44,
                                    height=44,
                                ),
                                nib.SFSymbol(
                                    "music.note",
                                    font=nib.Font.system(16),
                                    foreground_color="#FFFFFFCC",
                                ),
                            ],
                        ),
                        nib.VStack(
                            controls=[
                                nib.Text(
                                    track["title"],
                                    font=nib.Font.system(13, nib.FontWeight.semibold),
                                    foreground_color=TEXT_PRIMARY,
                                ),
                                nib.Text(
                                    track["artist"],
                                    font=nib.Font.system(11),
                                    foreground_color=TEXT_SECONDARY,
                                ),
                            ],
                            spacing=2,
                            alignment=nib.HorizontalAlignment.leading,
                        ),
                    ],
                    spacing=12,
                ),
                nib.Spacer(),
                nib.HStack(
                    controls=[
                        nib.Circle(
                            fill="#1DB954",  # Spotify green
                            width=6,
                            height=6,
                        ),
                        nib.Text(
                            track["source"],
                            font=nib.Font.system(9, nib.FontWeight.medium),
                            foreground_color="#b2b2b2",
                        ),
                    ],
                    spacing=6,
                    padding={"horizontal": 7, "vertical": 5},
                    background="#3A3A3A",
                    clip_shape=nib.Capsule(width=20, height=10),
                ),
            ],
            max_width=float("inf"),
            padding=12,
            background=nib.RoundedRectangle(
                corner_radius=10,
                fill=CARD_BG,
                stroke_color="#383837",
                stroke_width=1,
                height=70,
            ),
            # border_color=CARD_BORDER,
        )

    # ─────────────────────────────────────────────────────────────────────────
    # Content View
    # ─────────────────────────────────────────────────────────────────────────

    def content_view():
        if state.is_loading:
            return nib.HStack(
                controls=[
                    nib.ProgressView(scale=0.7),
                    nib.Text(
                        "Detecting music...",
                        font=nib.Font.system(12),
                        foreground_color=TEXT_SECONDARY,
                    ),
                ],
                spacing=12,
                max_width=float("inf"),
                padding=20,
                background=CARD_BG,
                corner_radius=10,
                border_width=1,
            )
        else:
            return facts_grid()

    # ─────────────────────────────────────────────────────────────────────────
    # Facts Grid
    # ─────────────────────────────────────────────────────────────────────────

    def facts_grid():
        def show_description():
            state.show_full_description = True
            build_ui()

        controls = [
            # Main facts row
            nib.HStack(
                controls=[
                    fact_card(track["year"], None, "Released"),
                    fact_card(track["country_flag"], None, track["country_name"]),
                    fact_card(track["duration"], None, "Duration"),
                ],
                spacing=10,
            ),
        ]

        # Writers
        if track["writers"]:
            controls.append(
                info_row("pencil", "Written by", ", ".join(track["writers"][:3]))
            )

        # Producers
        if track["producers"]:
            controls.append(
                info_row(
                    "slider.horizontal.3",
                    "Produced by",
                    ", ".join(track["producers"][:2]),
                )
            )

        # Album
        if track["album"]:
            controls.append(info_row("opticaldisc", "Album", track["album"]))

        # Description card
        if track["description"]:
            desc = track["description"]
            snippet = desc[:120] + ("..." if len(desc) > 120 else "")
            controls.append(
                nib.Button(
                    content=nib.VStack(
                        controls=[
                            nib.HStack(
                                controls=[
                                    nib.SFSymbol(
                                        "quote.opening",
                                        font=nib.Font.system(10),
                                        foreground_color=ACCENT,
                                    ),
                                    nib.Text(
                                        "About this song",
                                        font=nib.Font.system(10, nib.FontWeight.medium),
                                        foreground_color=TEXT_SECONDARY,
                                    ),
                                    nib.SFSymbol(
                                        "chevron.right",
                                        font=nib.Font.system(
                                            9, nib.FontWeight.semibold
                                        ),
                                        foreground_color="#99999980",
                                    ),
                                ],
                                spacing=4,
                            ),
                            nib.Text(
                                snippet,
                                font=nib.Font.system(11),
                                foreground_color="#696969",
                            ),
                        ],
                        alignment=nib.HorizontalAlignment.leading,
                        spacing=6,
                        max_width=float("inf"),
                        padding=12,
                        background=nib.RoundedRectangle(
                            corner_radius=10,
                            fill=CARD_BG,
                            stroke_color="#383837",
                            stroke_width=1,
                            height=60,
                        ),
                    ),
                    action=show_description,
                    style=nib.ButtonStyle.plain,
                )
            )

        return nib.VStack(controls=controls, spacing=10)

    def fact_card(value: str, unit: str | None, label: str):
        value_controls = [
            nib.Text(
                value,
                font=nib.Font.system(20, nib.FontWeight.semibold),
                foreground_color=TEXT_PRIMARY,
            ),
        ]
        if unit:
            value_controls.append(
                nib.Text(
                    unit,
                    font=nib.Font.system(11, nib.FontWeight.medium),
                    foreground_color=TEXT_SECONDARY,
                )
            )

        return nib.VStack(
            controls=[
                nib.HStack(controls=value_controls, spacing=2),
                nib.Text(
                    label,
                    font=nib.Font.system(10, nib.FontWeight.medium),
                    foreground_color=TEXT_SECONDARY,
                ),
            ],
            spacing=4,
            max_width=float("inf"),
            padding=14,
            background=nib.RoundedRectangle(
                corner_radius=10,
                fill=CARD_BG,
                stroke_color="#383837",
                stroke_width=1,
                width=100,
                height=70,
            ),
        )

    def info_row(icon: str, label: str, value: str):
        return nib.HStack(
            controls=[
                nib.SFSymbol(
                    icon,
                    font=nib.Font.system(10),
                    foreground_color=TEXT_SECONDARY,
                    width=14,
                ),
                nib.Text(
                    label,
                    font=nib.Font.system(10, nib.FontWeight.medium),
                    foreground_color=TEXT_SECONDARY,
                ),
                nib.Text(
                    value,
                    font=nib.Font.system(11),
                    foreground_color="#FFFFFFE6",
                ),
                nib.Spacer(),
            ],
            max_width=float("inf"),
            spacing=8,
            padding=10,
            background=nib.RoundedRectangle(
                corner_radius=10,
                fill=CARD_BG,
                stroke_color="#383837",
                stroke_width=1,
                height=35,
            ),
        )

    # Initial build
    build_ui()


if __name__ == "__main__":
    nib.run(main)
