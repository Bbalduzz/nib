"""
YouTube Video Downloader

A minimal, macOS-native status bar app for downloading YouTube videos.
Showcases nib's function-based API with reactive state updates.
"""

import subprocess
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

import nib

try:
    from pytubefix import YouTube

    HAS_PYTUBEFIX = True
except ImportError:
    HAS_PYTUBEFIX = False

# ─────────────────────────────────────────────────────────────────────────────
# Design Tokens
# ─────────────────────────────────────────────────────────────────────────────

SURFACE = "#2C2C2E"
SURFACE_ELEVATED = "#3A3A3C"
ACCENT = "#0A84FF"
SUCCESS = "#30D158"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#8E8E93"
TEXT_TERTIARY = "#636366"

SP = {"xs": 4, "sm": 8, "md": 12, "lg": 16, "xl": 24}
RADIUS = {"sm": 6, "md": 10, "lg": 14}


# ─────────────────────────────────────────────────────────────────────────────
# State
# ─────────────────────────────────────────────────────────────────────────────


class AppState:
    READY = "ready"
    LOADING = "loading"
    PREVIEW = "preview"
    DOWNLOADING = "downloading"
    DONE = "done"

    def __init__(self):
        self.current = self.READY
        self.url = ""
        self.video_title = ""
        self.video_author = ""
        self.video_duration = 0
        self.video_thumbnail = ""
        self.download_progress = 0.0
        self.download_type = "video"
        self.yt = None
        self.downloaded_file = None
        self.download_path = str(Path.home() / "Downloads")


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def truncate(text: str, max_len: int) -> str:
    return text if len(text) <= max_len else text[: max_len - 1] + "…"


def card(content, padding=None):
    return nib.VStack(
        controls=[content],
        padding=padding or SP["lg"],
        background=SURFACE,
        corner_radius=RADIUS["lg"],
    )


# ─────────────────────────────────────────────────────────────────────────────
# Main App
# ─────────────────────────────────────────────────────────────────────────────


def main(app: nib.App):
    app.title = "TubeGrab"
    app.icon = nib.SFSymbol("arrow.down.circle.fill")

    state = AppState()

    # ─────────────────────────────────────────────────────────────────────────
    # Build UI based on state
    # ─────────────────────────────────────────────────────────────────────────

    def build_ui():
        app.build(
            nib.VStack(
                controls=[header(), content()],
                spacing=SP["lg"],
                padding=SP["xl"],
                width=320.0,
                animation=nib.Animation.easeInOut(0.3),
            )
        )

    def set_state(new_state):
        state.current = new_state
        build_ui()

    # ─────────────────────────────────────────────────────────────────────────
    # Header
    # ─────────────────────────────────────────────────────────────────────────

    def header():
        return nib.HStack(
            controls=[
                nib.SFSymbol(
                    "arrow.down.circle.fill",
                    font=nib.Font.title2,
                    foreground_color=ACCENT,
                ),
                nib.Text("TubeGrab", font=nib.Font.headline),
            ],
            spacing=SP["sm"],
        )

    # ─────────────────────────────────────────────────────────────────────────
    # Content Router
    # ─────────────────────────────────────────────────────────────────────────

    def content():
        match state.current:
            case AppState.READY:
                return ready_view()
            case AppState.LOADING:
                return loading_view()
            case AppState.PREVIEW:
                return preview_view()
            case AppState.DOWNLOADING:
                return downloading_view()
            case AppState.DONE:
                return done_view()
        return ready_view()

    # ─────────────────────────────────────────────────────────────────────────
    # Ready View
    # ─────────────────────────────────────────────────────────────────────────

    def ready_view():
        return nib.HStack(
            controls=[
                nib.SFSymbol("link", foreground_color=TEXT_TERTIARY),
                nib.TextField(
                    placeholder="Paste YouTube link...",
                    value=state.url,
                    on_submit=on_url_change,
                    style=nib.TextFieldStyle.PLAIN,
                ),
            ],
            spacing=SP["sm"],
            padding=SP["md"],
            background=SURFACE_ELEVATED,
            corner_radius=RADIUS["md"],
            width=260,
        )

    # ─────────────────────────────────────────────────────────────────────────
    # Loading View
    # ─────────────────────────────────────────────────────────────────────────

    def loading_view():
        return card(
            nib.VStack(
                controls=[
                    nib.ProgressView(),
                    nib.Text(
                        "Fetching video info...",
                        font=nib.Font.subheadline,
                        foreground_color=TEXT_SECONDARY,
                    ),
                ],
                spacing=SP["md"],
                alignment=nib.HorizontalAlignment.center,
            ),
            padding=SP["xl"],
        )

    # ─────────────────────────────────────────────────────────────────────────
    # Preview View
    # ─────────────────────────────────────────────────────────────────────────

    def preview_view():
        mins, secs = divmod(state.video_duration, 60)
        duration_str = f"{mins}:{secs:02d}"

        def thumbnail():
            if state.video_thumbnail:
                return nib.Image(
                    url=state.video_thumbnail,
                    resizable=True,
                    scaled_to_fill=True,
                    width=80.0,
                    height=45.0,
                    clip_shape=nib.Rectangle(corner_radius=RADIUS["sm"]),
                )
            return nib.ZStack(
                controls=[
                    nib.Rectangle(
                        corner_radius=RADIUS["sm"],
                        fill=SURFACE_ELEVATED,
                        width=80.0,
                        height=45.0,
                    ),
                    nib.SFSymbol(
                        "play.fill",
                        font=nib.Font.body,
                        foreground_color=nib.Color.secondary,
                    ),
                ]
            )

        def download_button(label, icon, action, primary=True):
            return nib.Button(
                content=nib.HStack(
                    controls=[nib.SFSymbol(icon), nib.Text(label)],
                    spacing=SP["xs"],
                ),
                action=action,
                style=nib.ButtonStyle.borderedProminent
                if primary
                else nib.ButtonStyle.bordered,
                tint=ACCENT if primary else TEXT_SECONDARY,
            )

        return card(
            nib.VStack(
                controls=[
                    nib.HStack(
                        controls=[
                            thumbnail(),
                            nib.VStack(
                                controls=[
                                    nib.Text(
                                        truncate(state.video_title, 20),
                                        font=nib.Font.subheadline,
                                    ),
                                    nib.Text(
                                        f"{state.video_author} · {duration_str}",
                                        font=nib.Font.caption,
                                        foreground_color=TEXT_SECONDARY,
                                    ),
                                ],
                                spacing=SP["xs"],
                                alignment=nib.HorizontalAlignment.leading,
                            ),
                        ],
                        spacing=SP["md"],
                    ),
                    nib.HStack(
                        controls=[
                            download_button(
                                "Video", "film", download_video, primary=True
                            ),
                            download_button(
                                "Audio", "music.note", download_audio, primary=False
                            ),
                        ],
                        spacing=SP["sm"],
                    ),
                ],
                spacing=SP["lg"],
            )
        )

    # ─────────────────────────────────────────────────────────────────────────
    # Downloading View
    # ─────────────────────────────────────────────────────────────────────────

    def downloading_view():
        progress = state.download_progress
        pct = int(progress * 100)
        type_label = "video" if state.download_type == "video" else "audio"
        bar_width = 256.0

        return card(
            nib.VStack(
                controls=[
                    nib.VStack(
                        controls=[
                            nib.Text(
                                truncate(state.video_title, 28),
                                font=nib.Font.subheadline,
                            ),
                            nib.Text(
                                f"Downloading {type_label}...",
                                font=nib.Font.caption,
                                foreground_color=TEXT_SECONDARY,
                            ),
                        ],
                        spacing=SP["xs"],
                        alignment=nib.HorizontalAlignment.leading,
                    ),
                    nib.ZStack(
                        controls=[
                            nib.Rectangle(
                                corner_radius=2,
                                fill=SURFACE_ELEVATED,
                                width=bar_width,
                                height=4.0,
                            ),
                            nib.HStack(
                                controls=[
                                    nib.Rectangle(
                                        corner_radius=2,
                                        fill=ACCENT,
                                        width=bar_width * progress,
                                        height=4.0,
                                        animation=nib.Animation.easeOut(0.2),
                                    ),
                                    nib.Spacer(),
                                ],
                                spacing=0,
                            ),
                        ]
                    ),
                    nib.Text(
                        f"{pct}%",
                        font=nib.Font.caption,
                        foreground_color=TEXT_SECONDARY,
                    ),
                ],
                spacing=SP["md"],
            )
        )

    # ─────────────────────────────────────────────────────────────────────────
    # Done View
    # ─────────────────────────────────────────────────────────────────────────

    def done_view():
        return card(
            nib.VStack(
                controls=[
                    nib.ZStack(
                        controls=[
                            nib.Circle(fill=SUCCESS, width=48.0, height=48.0),
                            nib.SFSymbol(
                                "checkmark",
                                font=nib.Font.title2,
                                foreground_color=TEXT_PRIMARY,
                            ),
                        ]
                    ),
                    nib.VStack(
                        controls=[
                            nib.Text("Download Complete", font=nib.Font.headline),
                            nib.Text(
                                "Saved to Downloads",
                                font=nib.Font.caption,
                                foreground_color=TEXT_SECONDARY,
                            ),
                        ],
                        spacing=SP["xs"],
                        alignment=nib.HorizontalAlignment.center,
                    ),
                    nib.HStack(
                        controls=[
                            nib.Button(
                                content=nib.HStack(
                                    controls=[
                                        nib.SFSymbol("folder"),
                                        nib.Text("Show in Finder"),
                                    ],
                                    spacing=SP["xs"],
                                ),
                                action=open_finder,
                                style=nib.ButtonStyle.bordered,
                                tint=TEXT_SECONDARY,
                            ),
                            nib.Button(
                                content=nib.HStack(
                                    controls=[
                                        nib.SFSymbol("plus"),
                                        nib.Text("New Download"),
                                    ],
                                    spacing=SP["xs"],
                                ),
                                action=reset,
                                style=nib.ButtonStyle.borderedProminent,
                                tint=ACCENT,
                            ),
                        ],
                        spacing=SP["sm"],
                    ),
                ],
                spacing=SP["lg"],
                alignment=nib.HorizontalAlignment.center,
            )
        )

    # ─────────────────────────────────────────────────────────────────────────
    # Actions
    # ─────────────────────────────────────────────────────────────────────────

    def is_youtube_url(url: str) -> bool:
        """Check if the URL looks like a YouTube link."""
        return any(
            domain in url
            for domain in ["youtube.com/watch", "youtu.be/", "youtube.com/shorts"]
        )

    def on_url_change(value: str):
        state.url = value.strip()
        print(state.url)
        if is_youtube_url(state.url) and state.current == AppState.READY:
            fetch()

    def fetch():
        if not state.url:
            return
        set_state(State.LOADING)
        try:
            state.yt = YouTube(state.url)
            state.video_title = state.yt.title or "Unknown"
            state.video_author = state.yt.author or "Unknown"
            state.video_duration = state.yt.length or 0
            state.video_thumbnail = state.yt.thumbnail_url or ""
            set_state(State.PREVIEW)
        except Exception as e:
            print(f"Error: {e}")
            set_state(State.READY)

    def download_video():
        state.download_type = "video"
        start_download(video=True)

    def download_audio():
        state.download_type = "audio"
        start_download(video=False)

    def start_download(video: bool):
        set_state(State.DOWNLOADING)
        state.download_progress = 0.0

        def on_progress(stream, chunk, remaining):
            total = stream.filesize
            downloaded = total - remaining
            state.download_progress = downloaded / total if total > 0 else 0
            build_ui()  # Update progress bar

        def do_download():
            try:
                yt = YouTube(state.url, on_progress_callback=on_progress)
                stream = (
                    yt.streams.get_highest_resolution()
                    if video
                    else yt.streams.get_audio_only()
                )
                state.downloaded_file = stream.download(output_path=state.download_path)
                state.download_progress = 1.0
                set_state(State.DONE)
            except Exception as e:
                print(f"Error: {e}")
                set_state(State.PREVIEW)

        threading.Thread(target=do_download, daemon=True).start()

    def open_finder():
        if state.downloaded_file:
            subprocess.run(["open", "-R", state.downloaded_file])
        else:
            subprocess.run(["open", state.download_path])

    def reset():
        state.url = ""
        state.video_title = ""
        state.video_author = ""
        state.video_duration = 0
        state.video_thumbnail = ""
        state.download_progress = 0.0
        state.yt = None
        state.downloaded_file = None
        set_state(State.READY)

    # Initial build
    build_ui()


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not HAS_PYTUBEFIX:
        print("Please install pytubefix: pip install pytubefix")
        sys.exit(1)
    nib.run(main)
