import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

import nib


def main(app):
    logo = nib.Image(
        src="/Users/edoardobalducci/Documents/work/nib/media/nib-logo-white.svg",
        width=14,
        height=14,
    )
    app.icon = logo
    app.build(nib.ZStack([logo], margin=10))


nib.run(main)
