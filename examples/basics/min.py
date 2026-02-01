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


def main(app):
    app.title = "Minimal"
    app.icon = nib.SFSymbol(
        "arrowshape.forward.circle.fill",
        rendering_mode=nib.SymbolRenderingMode.HIERARCHICAL,
    )
    app.height = 200
    app.on_appear = lambda: print("Popover opened!")
    app.on_disappear = lambda: print("Popover closed!")
    app.on_quit = lambda: print("App quitting!")
    app.menu = [
        nib.MenuItem(
            content=nib.HStack(
                controls=[
                    nib.SFSymbol("star.fill", foreground_color=nib.Color.YELLOW),
                    nib.VStack(
                        controls=[
                            nib.Text("Premium", font=nib.Font.HEADLINE),
                            nib.Text(
                                "Upgrade now",
                                style=nib.TextStyle(
                                    color=nib.Color.SECONDARY,
                                    font=nib.Font.system(
                                        10, weight=nib.FontWeight.LIGHT
                                    ),
                                ),
                            ),
                        ],
                        spacing=2,
                    ),
                    nib.Spacer(),
                ],
                alignment=nib.HorizontalAlignment.CENTER,
                padding={"leading": 12},
                spacing=8,
            ),
            shortcut="cmd+,",
        ),
        nib.MenuItem(
            "More Options",
            menu=[
                nib.MenuItem("Option A", badge="3"),
                nib.MenuItem("Option B", shortcut="cmd+R", enabled=False),
                nib.MenuItem(
                    "Even More",
                    menu=[
                        nib.MenuItem("Nested Item", badge="99+"),
                    ],
                ),
            ],
        ),
        nib.MenuDivider(),
        nib.MenuItem("Quit", shortcut="cmd+Q", action=app.quit),
    ]

    app.build(
        nib.VStack(
            controls=[
                nib.ZStack(
                    controls=[
                        nib.Text(
                            "Right click on the statusbar title",
                            style=nib.TextStyle(
                                font=nib.Font.custom("SF Compact Rounded", size=16),
                            ),
                            tooltip=nib.Text("Check this tooltip"),
                        ),
                        nib.RoundedRectangle(
                            corner_radius=8,
                            stroke_color=nib.Color.SECONDARY,
                            stroke_width=2,
                            height=40,
                        ),
                    ],
                    margin=20,
                    on_hover=lambda hovering: print(f"Hovering: {hovering}"),
                ),
                nib.Spacer(),
                nib.HStack(
                    [
                        nib.Text(
                            "Quit",
                            style=nib.TextStyle(
                                color=nib.Color.SECONDARY,
                                font=nib.Font.custom("SF Pro Rounded", size=14),
                            ),
                        ),
                        nib.Spacer(),
                        nib.ZStack(
                            [
                                nib.Text(
                                    "Q",
                                    style=nib.TextStyle(
                                        color=nib.Color.WHITE.with_opacity(0.6),
                                        font=nib.Font.custom("SF Pro Rounded", size=11),
                                    ),
                                ),
                                nib.RoundedRectangle(
                                    fill=nib.Color.SECONDARY.with_opacity(0.2),
                                    stroke_color=nib.Color.GRAY,
                                    stroke_width=1,
                                    corner_radius=6,
                                    width=20,
                                    height=20,
                                ),
                            ]
                        ),
                    ],
                    margin=12,
                ),
            ],
        )
    )


nib.run(main)
