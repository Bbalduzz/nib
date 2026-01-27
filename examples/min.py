import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

import nib

"""
def main(app: nib.App):
    app.title = "Test"
    app.icon = nib.SFSymbol("star")
    app.build(nib.Text("Hello"))
nib.run(main)
"""


def on_open():
    print("Popover opened!")
    # Refresh data, update UI, etc.


def main(app):
    app.title = "Test"
    app.icon = nib.SFSymbol(
        "arrowshape.forward.circle.fill",
        rendering_mode=nib.SymbolRenderingMode.HIERARCHICAL,
    )
    app.on_appear = on_open
    app.menu = [
        nib.MenuItem(
            "Settings",
            icon=nib.SFSymbol(
                "gear.circle.fill",
                rendering_mode=nib.SymbolRenderingMode.HIERARCHICAL,
            ),
            shortcut="cmd+,",
        ),
        nib.MenuItem(
            "More Options",
            menu=[
                nib.MenuItem("Option A", badge="3"),
                nib.MenuItem("Option B", enabled=False),
                nib.MenuItem(
                    "Even More",
                    menu=[
                        nib.MenuItem("Nested Item", badge="99+"),
                    ],
                ),
            ],
        ),
        nib.MenuDivider(),
        nib.MenuItem("Quit", action=app.quit),
    ]

    app.build(
        nib.VStack(
            controls=[
                nib.ZStack(
                    controls=[
                        nib.Text(
                            "Demo", font=nib.Font.custom("SF Compact Rounded", size=16)
                        ),
                        nib.RoundedRectangle(
                            corner_radius=8,
                            stroke_color="red",
                            stroke_width=2,
                            width=100,
                            height=40,
                        ),
                    ],
                ),
            ],
        )
    )


nib.run(main)
