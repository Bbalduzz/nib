import nib


def main(app):
    app.title = "Minimal"
    app.icon = nib.SFSymbol(
        "arrowshape.forward.circle.fill",
        rendering_mode=nib.SymbolRenderingMode.HIERARCHICAL,
    )
    app.height = 400
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
            height=40,
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
                        nib.MenuItem(
                            "Nested Item",
                            badge="99+",
                            action=lambda: print("Nested Item clicked"),
                        ),
                    ],
                ),
            ],
        ),
        nib.MenuDivider(),
        nib.MenuItem(
            "Settings",
            shortcut="cmd+,",
            action=lambda: app.settings.open(),
        ),
        nib.MenuItem("Quit", shortcut="cmd+Q", action=app.quit),
    ]

    settings = nib.Settings(
        {
            "dark_mode": False,
            "accent_color": "BLUE",
            "notifications": True,
            "volume": 0.0,
            "username": "guest",
        }
    )
    app.register_settings(settings)

    dark_mode_value = nib.Text(settings.dark_mode)
    accent_color_value = nib.Text(settings.accent_color)
    notifications_value = nib.Text(settings.notifications)
    volume_value = nib.Text(settings.volume)
    username_value = nib.Text(settings.username)

    status_stack = nib.Form(
        controls=[
            nib.HStack([nib.Text("Hello!"), nib.Spacer(), username_value]),
            nib.HStack([nib.Text("Dark Mode:"), nib.Spacer(), dark_mode_value]),
            nib.HStack([nib.Text("Accent Color:"), nib.Spacer(), accent_color_value]),
            nib.HStack([nib.Text("Notifications:"), nib.Spacer(), notifications_value]),
            nib.HStack([nib.Text("Volume:"), nib.Spacer(), volume_value]),
        ],
        style=nib.FormStyle.GROUPED,
        # alignment=nib.Alignment.LEADING,
    )

    def update_status():
        dark_mode_value.content = settings.dark_mode
        accent_color_value.content = settings.accent_color
        notifications_value.content = settings.notifications
        volume_value.content = settings.volume
        username_value.content = settings.username

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
                            controls=[
                                nib.Toggle(
                                    "Dark Mode",
                                    is_on=False,
                                    on_change=lambda v: (
                                        setattr(settings, "dark_mode", v),
                                        update_status(),
                                    ),
                                ),
                                nib.Picker(
                                    "Accent color",
                                    options=["RED", "BLUE", "WHITE"],
                                    style=nib.PickerStyle.MENU,
                                    on_change=lambda v: (
                                        setattr(settings, "accent_color", v),
                                        update_status(),
                                    ),
                                ),
                                nib.Toggle(
                                    content=nib.VStack(
                                        [
                                            nib.Text("Title", font=nib.Font.TITLE2),
                                            nib.Text(
                                                "This is a subheading",
                                                font=nib.Font.SUBHEADLINE,
                                            ),
                                        ],
                                        alignment=nib.Alignment.LEADING,
                                    )
                                ),
                            ],
                            header="Appearance",
                        ),
                        nib.Section(
                            controls=[
                                nib.Toggle(
                                    "Notifications",
                                    is_on=True,
                                    on_change=lambda v: (
                                        setattr(settings, "notifications", v),
                                        update_status(),
                                    ),
                                ),
                                nib.HStack(
                                    [
                                        nib.Text("Volume"),
                                        nib.Slider(
                                            label="Volume",
                                            value=50,
                                            min_value=0,
                                            max_value=100,
                                            on_change=lambda v: (
                                                setattr(settings, "volume", v),
                                                update_status(),
                                            ),
                                        ),
                                    ]
                                ),
                            ],
                            header="Notifications",
                        ),
                    ],
                    style=nib.FormStyle.GROUPED,
                ),
            ),
            nib.SettingsTab(
                "Account",
                icon="person",
                content=nib.Form(
                    controls=[
                        nib.Section(
                            header="Profile",
                            controls=[
                                nib.TextField(
                                    "Username",
                                    value=settings.username,
                                    on_submit=lambda v: (
                                        setattr(settings, "username", v),
                                        update_status(),
                                    ),
                                ),
                            ],
                        )
                    ],
                    style=nib.FormStyle.GROUPED,
                ),
            ),
        ],
    )

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
                        nib.Rectangle(
                            corner_radius=nib.CornerRadius.all(5),
                            stroke_color=nib.Color.SECONDARY,
                            stroke_width=2,
                            height=40,
                        ),
                    ],
                    margin=20,
                    on_hover=lambda hovering: print(f"Hovering: {hovering}"),
                ),
                status_stack,
                nib.Spacer(),
                settings_button := nib.HStack(
                    [
                        nib.Text(
                            "Settings",
                            style=nib.TextStyle(
                                color=nib.Color.SECONDARY,
                                font=nib.Font.custom("SF Pro Rounded", size=14),
                            ),
                        ),
                        nib.Spacer(),
                        nib.ZStack(
                            [
                                nib.Text(
                                    "S",
                                    style=nib.TextStyle(
                                        color=nib.Color.WHITE.with_opacity(0.6),
                                        font=nib.Font.custom("SF Pro Rounded", size=11),
                                    ),
                                ),
                                nib.Rectangle(
                                    fill=nib.Color.SECONDARY.with_opacity(0.2),
                                    stroke_color=nib.Color.GRAY,
                                    stroke_width=1,
                                    corner_radius=nib.CornerRadius.all(5),
                                    width=20,
                                    height=20,
                                ),
                            ]
                        ),
                    ],
                    margin={"leading": 12, "trailing": 12},
                    on_hover=lambda is_hovered: setattr(
                        settings_button,
                        "background",
                        nib.Rectangle(
                            fill=nib.Color.BLACK.with_opacity(0.2),
                            height=30,
                            margin={"leading": 6, "trailing": 6},
                            corner_radius=nib.CornerRadius.all(5),
                        ),
                    )
                    if is_hovered
                    else setattr(settings_button, "background", None),
                    on_click=lambda: app.settings.open(),
                    animation=nib.Animation.easeIn(0.1),
                ),
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
                                nib.Rectangle(
                                    fill=nib.Color.SECONDARY.with_opacity(0.2),
                                    stroke_color=nib.Color.GRAY,
                                    stroke_width=1,
                                    corner_radius=nib.CornerRadius.all(5),
                                    width=20,
                                    height=20,
                                ),
                            ]
                        ),
                    ],
                    margin={"leading": 12, "trailing": 12, "bottom": 12},
                ),
            ],
        )
    )


nib.run(main)
