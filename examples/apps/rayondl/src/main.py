import re
import threading
from pathlib import Path

import nib
from services.downloader import (
    NoPresentationError,
    RayonClient,
    RayonError,
)

OUTPUT_DIR = Path.home() / "Downloads" / "RayonExports"
EMAIL = "woppollemauyu-8400@yopmail.com"
PASSWORD = "frontlallero7"


def extract_model_id(url: str) -> str | None:
    """Extract model ID from a Rayon URL."""
    # Patterns:
    # https://www.rayon.design/app/model/{model_id}
    # https://rayon.design/app/model/{model_id}
    # Just the model ID itself (UUID format)

    uuid_pattern = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

    # Try to find UUID in URL
    match = re.search(uuid_pattern, url, re.IGNORECASE)
    if match:
        return match.group(0)

    return None


def main(app: nib.App):
    app.title = "Rayondl"
    app.icon = nib.SFSymbol(
        "arrow.down.document.fill", rendering_mode=nib.SymbolRenderingMode.HIERARCHICAL
    )
    app.width = 320
    app.height = 180
    app.fonts = {
        "terminal-grotesque": "https://fonts.open-foundry.com/terminal-grotesque-open/terminal-grotesque-open.woff2",
        "Geist-SemiBold": "fonts/Geist/Geist-SemiBold.ttf",
        "Geist-Black": "fonts/Geist/Geist-Black.ttf",
        "Geist-ExtraLight": "fonts/Geist/Geist-ExtraLight.ttf",
        "Geist-Thin": "fonts/Geist/Geist-Thin.ttf",
        "GeistMono-Regular": "https://assets.vercel.com/raw/upload/v1700665218/front/geist-font-page/fonts/GeistMono-Regular.otf",
    }
    app.menu = [
        nib.MenuItem("Quit", shortcut="cmd+Q", action=app.quit),
    ]

    progress_bar = nib.ProgressView(
        value=0.0,
        visible=False,
        animation=nib.Animation.easeInOut(0.2),
    )

    def do_download(e):
        model_id = extract_model_id(e)

        def download_thread():
            try:
                app.height += 50
                progress_bar.visible = True
                # progress_bar.value = 0

                client = RayonClient(EMAIL, PASSWORD)
                model = client.get_model(model_id)

                print(model)

                def on_progress(downloaded: int, total: int):
                    if total > 0:
                        print(downloaded / total)
                        progress = downloaded / total
                        progress_bar.value = progress
                        # mb_done = downloaded / (1024 * 1024)
                        # mb_total = total / (1024 * 1024)
                        progress_bar.label = f"{progress:.0%}"

                file_path = client.download(model, OUTPUT_DIR, on_progress=on_progress)
                progress_bar.visible = False
                app.height -= 50
                # Send notification

                app.notify(
                    title="Download Complete",
                    body=f"Saved to {file_path}",
                    sound=True,
                )

            except NoPresentationError:
                print("No PDF available for this model", nib.Color.RED)
            except RayonError as e:
                print(f"Error: {e}", nib.Color.RED)
            except Exception as e:
                print(f"Error: {e}", nib.Color.RED)

        if model_id:
            threading.Thread(target=download_thread, daemon=True).start()

    url_input = nib.TextField(
        placeholder="https://rayon.design/app/model/...",
        style=nib.TextFieldStyle.plain,
        padding=10,
        on_change=do_download,
    )

    home_view = nib.VStack(
        controls=[
            # Header
            nib.HStack(
                [
                    nib.Image(
                        src="icon.png",
                        width=28,
                        height=28,
                        aspect_ratio=nib.ContentMode.FILL,
                    ),
                    nib.VStack(
                        controls=[
                            nib.Text(
                                "RayonDL",
                                style=nib.TextStyle(
                                    font=nib.Font.custom("SF Pro Rounded", 15)
                                ),
                            ),
                            nib.Text(
                                "Download Rayon presentations as PDF",
                                style=nib.TextStyle(
                                    font=nib.Font.custom("SF Pro Rounded", 11),
                                    color=nib.Color.SECONDARY,
                                ),
                            ),
                        ],
                        alignment=nib.HorizontalAlignment.LEADING,
                    ),
                ]
            ),
            nib.ZStack(
                controls=[
                    nib.Rectangle(
                        fill=nib.Color.SECONDARY.with_opacity(0.1),
                        stroke_color=nib.Color.GRAY.with_opacity(0.3),
                        stroke_width=1,
                        corner_radius=8,
                        height=36,
                    ),
                    url_input,
                ]
            ),
            progress_bar,
        ],
        spacing=12,
        padding=20,
        alignment=nib.HorizontalAlignment.LEADING,
    )

    app.build(home_view)


nib.run(main)
