import sys

sys.path.insert(0, "python")

import nib


def main(app: nib.App):
    app.title = "Video Demo"
    app.width = 500
    app.height = 300
    app.menu = [nib.MenuItem("Quit", action=app.quit)]

    app.build(
        nib.VStack(
            controls=[
                # URL video with autoplay and loop
                nib.Video(
                    src="https://cdn.plyr.io/static/demo/View_From_A_Blue_Moon_Trailer-1080p.mp4",
                    # autoplay=True,
                    loop=True,
                    height=300,
                ),
            ],
        )
    )


nib.run(main)
