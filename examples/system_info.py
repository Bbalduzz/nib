"""System Info - Demo of nib system services.

Displays battery, network, and screen information using nib services.
"""

import nib


def main(app: nib.App):
    app.title = "System Info"
    app.icon = nib.SFSymbol("info.circle.fill")
    app.width = 280
    app.height = 380

    # Status labels
    battery_level = nib.Text("--", font=nib.Font.system(24, weight=nib.FontWeight.BOLD))
    battery_state = nib.Text("Loading...", foreground_color=nib.Color.SECONDARY)
    battery_icon = nib.SFSymbol("battery.100", foreground_color=nib.Color.SECONDARY)

    network_status = nib.Text("--", font=nib.Font.system(24, weight=nib.FontWeight.BOLD))
    network_type = nib.Text("Loading...", foreground_color=nib.Color.SECONDARY)
    network_icon = nib.SFSymbol("wifi", foreground_color=nib.Color.SECONDARY)

    brightness_level = nib.Text("--", font=nib.Font.system(24, weight=nib.FontWeight.BOLD))
    screen_size = nib.Text("Loading...", foreground_color=nib.Color.SECONDARY)

    def refresh_all():
        """Refresh all system info."""
        # Battery
        info = app.battery.get_status()
        if info.has_battery and info.level is not None:
            battery_level.content = f"{info.level:.0f}%"
            if info.is_charging:
                battery_icon.name = "bolt.fill"
                battery_icon.foreground_color = nib.Color.GREEN
                battery_state.content = info.state.value.capitalize()
            else:
                battery_icon.name = "battery.100"
                battery_icon.foreground_color = nib.Color.SECONDARY
                battery_state.content = info.state.value.capitalize()
        else:
            battery_level.content = "N/A"
            battery_icon.name = "powerplug.fill"
            battery_icon.foreground_color = nib.Color.SECONDARY
            battery_state.content = "AC Power"

        # Connectivity
        net_info = app.connectivity.get_status()
        if net_info.is_connected:
            network_status.content = "Online"
            network_icon.name = "wifi"
            network_icon.foreground_color = nib.Color.GREEN
            network_type.content = net_info.type.value.capitalize()
        else:
            network_status.content = "Offline"
            network_icon.name = "wifi.slash"
            network_icon.foreground_color = nib.Color.RED
            network_type.content = "No Connection"

        # Screen
        screen_info = app.screen.get_info()
        brightness_level.content = f"{screen_info.brightness * 100:.0f}%"
        screen_size.content = f"{screen_info.width:.0f} x {screen_info.height:.0f} @{screen_info.scale}x"

    def make_section(
        title: str, icon: nib.SFSymbol, value_view: nib.View, detail_icon: nib.View, detail_view: nib.View
    ) -> nib.View:
        """Create a styled info section."""
        return nib.HStack(
            controls=[
                icon,
                nib.VStack(
                    controls=[
                        nib.Text(
                            title,
                            font=nib.Font.caption,
                            foreground_color=nib.Color.SECONDARY,
                        ),
                        value_view,
                        nib.HStack(
                            controls=[detail_icon, detail_view],
                            spacing=4,
                        ),
                    ],
                    alignment=nib.HorizontalAlignment.LEADING,
                    spacing=2,
                ),
                nib.Spacer(),
            ],
            spacing=12,
            padding=12,
            background=nib.RoundedRectangle(
                corner_radius=10,
                fill=nib.Color.SECONDARY.with_opacity(0.1),
            ),
        )

    home_view = nib.VStack(
        controls=[
            # Header
            nib.Text("System Info", font=nib.Font.title2),
            # Battery Section
            make_section(
                "Battery",
                nib.SFSymbol("battery.100.fill", foreground_color=nib.Color.GREEN, scale="large"),
                battery_level,
                battery_icon,
                battery_state,
            ),
            # Network Section
            make_section(
                "Network",
                nib.SFSymbol("antenna.radiowaves.left.and.right", foreground_color=nib.Color.BLUE, scale="large"),
                network_status,
                network_icon,
                network_type,
            ),
            # Screen Section
            make_section(
                "Display",
                nib.SFSymbol("sun.max.fill", foreground_color=nib.Color.ORANGE, scale="large"),
                brightness_level,
                nib.SFSymbol("display", foreground_color=nib.Color.SECONDARY),
                screen_size,
            ),
            # Refresh Button
            nib.Button(
                "Refresh",
                action=refresh_all,
                style=nib.ButtonStyle.BORDERED,
            ),
        ],
        spacing=12,
        padding=16,
    )

    # Refresh when app appears
    app.on_appear = refresh_all

    app.build(home_view)


nib.run(main)
