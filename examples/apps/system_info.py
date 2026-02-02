"""System Info - Comprehensive system information dashboard.

Showcases all nib services: battery, screen, and connectivity.
"""

import nib
from nib.services.battery import ThermalState


def main(app: nib.App):
    app.title = "System Info"
    app.icon = nib.SFSymbol("info.circle.fill")
    app.width = 360
    app.height = 520

    # Colors
    card_bg = "#1C1C1E"
    text_secondary = "#8E8E93"
    accent_green = "#30D158"
    accent_blue = "#0A84FF"
    accent_orange = "#FF9F0A"
    accent_red = "#FF453A"
    accent_purple = "#BF5AF2"

    # Helper functions
    def make_card(title: str, *controls):
        return nib.VStack(
            controls=[
                nib.Text(title, font=nib.Font.caption, foreground_color=text_secondary),
                *controls,
            ],
            alignment=nib.HorizontalAlignment.LEADING,
            spacing=8,
            padding=12,
            background=nib.Rectangle(corner_radius=10, fill=card_bg, opacity=0.6),
        )

    def make_stat_row(icon: str, label: str, value_view, icon_color=None):
        return nib.HStack(
            controls=[
                nib.SFSymbol(
                    icon,
                    font=nib.Font.system(14),
                    foreground_color=icon_color or text_secondary,
                ),
                nib.Text(label, foreground_color=text_secondary),
                nib.Spacer(),
                value_view,
            ],
            spacing=8,
        )

    # =========================================================================
    # BATTERY STATUS
    # =========================================================================
    battery_level = nib.Text("--", font=nib.Font.system(24, weight=nib.FontWeight.BOLD))
    battery_state = nib.Text(
        "--", font=nib.Font.caption, foreground_color=text_secondary
    )
    battery_time = nib.Text("", font=nib.Font.caption, foreground_color=text_secondary)
    battery_power = nib.Text("", font=nib.Font.caption, foreground_color=text_secondary)

    def refresh_battery():
        try:
            info = app.battery.get_status()
            if info.has_battery and info.level is not None:
                battery_level.content = f"{info.level:.0f}%"
                if info.level >= 50:
                    battery_level.foreground_color = accent_green
                elif info.level >= 20:
                    battery_level.foreground_color = accent_orange
                else:
                    battery_level.foreground_color = accent_red

                battery_state.content = info.state.value.replace("_", " ").title()

                if info.is_charging and info.time_to_full_formatted:
                    battery_time.content = f"Full in {info.time_to_full_formatted}"
                elif info.time_remaining_formatted:
                    battery_time.content = f"{info.time_remaining_formatted} remaining"
                else:
                    battery_time.content = ""

                if info.wattage:
                    battery_power.content = f"{info.wattage:.1f}W"
                else:
                    battery_power.content = ""
            else:
                battery_level.content = "AC"
                battery_level.foreground_color = accent_blue
                battery_state.content = "No Battery"
                battery_time.content = ""
                battery_power.content = ""
        except Exception as e:
            battery_level.content = "Error"
            battery_state.content = str(e)[:30]

    battery_card = make_card(
        "BATTERY",
        nib.HStack(
            controls=[
                nib.VStack(
                    controls=[battery_level, battery_state],
                    alignment=nib.HorizontalAlignment.LEADING,
                    spacing=2,
                ),
                nib.Spacer(),
                nib.VStack(
                    controls=[battery_time, battery_power],
                    alignment=nib.HorizontalAlignment.TRAILING,
                    spacing=2,
                ),
            ],
        ),
    )

    # =========================================================================
    # BATTERY HEALTH
    # =========================================================================
    health_percent = nib.Text(
        "--", font=nib.Font.system(18, weight=nib.FontWeight.SEMIBOLD)
    )
    health_cycles = nib.Text("--", foreground_color=text_secondary)
    health_temp = nib.Text("--", foreground_color=text_secondary)
    health_condition = nib.Text("--", foreground_color=text_secondary)

    def refresh_health():
        try:
            health = app.battery.get_health()
            if health.health_percent is not None:
                health_percent.content = f"{health.health_percent:.0f}%"
                if health.health_percent >= 80:
                    health_percent.foreground_color = accent_green
                elif health.health_percent >= 60:
                    health_percent.foreground_color = accent_orange
                else:
                    health_percent.foreground_color = accent_red
            else:
                health_percent.content = "N/A"

            health_cycles.content = (
                f"{health.cycle_count} cycles" if health.cycle_count else "N/A"
            )
            health_temp.content = (
                f"{health.temperature_celsius:.1f}°C"
                if health.temperature_celsius
                else "N/A"
            )
            health_condition.content = health.condition or "N/A"
        except Exception:
            health_percent.content = "N/A"

    health_card = make_card(
        "BATTERY HEALTH",
        make_stat_row("heart.fill", "Health", health_percent, accent_green),
        make_stat_row("arrow.triangle.2.circlepath", "Cycles", health_cycles),
        make_stat_row("thermometer", "Temp", health_temp),
        make_stat_row("checkmark.shield", "Condition", health_condition),
    )

    # =========================================================================
    # THERMAL STATE
    # =========================================================================
    thermal_state = nib.Text(
        "--", font=nib.Font.system(16, weight=nib.FontWeight.SEMIBOLD)
    )
    thermal_icon = nib.SFSymbol(
        "thermometer.low", font=nib.Font.system(20), foreground_color=accent_green
    )

    def refresh_thermal():
        try:
            thermal = app.battery.get_thermal_state()
            thermal_state.content = thermal.state.value.title()
            if thermal.state == ThermalState.NOMINAL:
                thermal_state.foreground_color = accent_green
                thermal_icon.name = "thermometer.low"
                thermal_icon.foreground_color = accent_green
            elif thermal.state == ThermalState.FAIR:
                thermal_state.foreground_color = accent_orange
                thermal_icon.name = "thermometer.medium"
                thermal_icon.foreground_color = accent_orange
            elif thermal.state == ThermalState.SERIOUS:
                thermal_state.foreground_color = accent_orange
                thermal_icon.name = "thermometer.high"
                thermal_icon.foreground_color = accent_orange
            else:
                thermal_state.foreground_color = accent_red
                thermal_icon.name = "thermometer.sun.fill"
                thermal_icon.foreground_color = accent_red
        except Exception:
            thermal_state.content = "N/A"

    thermal_card = make_card(
        "THERMAL",
        nib.HStack(
            controls=[thermal_icon, thermal_state, nib.Spacer()],
            spacing=8,
        ),
    )

    # =========================================================================
    # DISPLAY
    # =========================================================================
    display_name = nib.Text(
        "--", font=nib.Font.system(14, weight=nib.FontWeight.SEMIBOLD)
    )
    display_res = nib.Text("--", foreground_color=text_secondary)
    display_brightness = nib.Text("--", foreground_color=text_secondary)
    display_refresh = nib.Text("--", foreground_color=text_secondary)

    def refresh_display():
        try:
            info = app.screen.get_info()
            display_name.content = info.name or "Display"
            display_res.content = (
                f"{info.width:.0f}×{info.height:.0f} @{info.scale:.0f}x"
            )
            if info.brightness is not None:
                display_brightness.content = f"{info.brightness * 100:.0f}%"
            else:
                display_brightness.content = "N/A"
            if info.refresh_rate:
                display_refresh.content = f"{info.refresh_rate:.0f}Hz"
            else:
                display_refresh.content = "N/A"
        except Exception:
            display_name.content = "Error"

    display_card = make_card(
        "DISPLAY",
        display_name,
        make_stat_row("rectangle.on.rectangle", "Resolution", display_res),
        make_stat_row("sun.max", "Brightness", display_brightness, accent_orange),
        make_stat_row("speedometer", "Refresh", display_refresh),
    )

    # =========================================================================
    # APPEARANCE
    # =========================================================================
    appearance_text = nib.Text(
        "--", font=nib.Font.system(16, weight=nib.FontWeight.SEMIBOLD)
    )
    appearance_icon = nib.SFSymbol(
        "moon.fill", font=nib.Font.system(18), foreground_color=accent_purple
    )

    def refresh_appearance():
        try:
            info = app.screen.get_dark_mode()
            if info.is_dark_mode:
                appearance_text.content = "Dark"
                appearance_icon.name = "moon.fill"
                appearance_icon.foreground_color = accent_purple
            else:
                appearance_text.content = "Light"
                appearance_icon.name = "sun.max.fill"
                appearance_icon.foreground_color = accent_orange
        except Exception:
            appearance_text.content = "N/A"

    def toggle_appearance():
        try:
            info = app.screen.get_dark_mode()
            app.screen.set_dark_mode(not info.is_dark_mode)
            refresh_appearance()
        except Exception:
            pass

    appearance_card = make_card(
        "APPEARANCE",
        nib.HStack(
            controls=[
                appearance_icon,
                appearance_text,
                nib.Spacer(),
                nib.Button(
                    "Toggle", action=toggle_appearance, style=nib.ButtonStyle.BORDERED
                ),
            ],
            spacing=8,
        ),
    )

    # =========================================================================
    # NETWORK
    # =========================================================================
    network_status = nib.Text(
        "--", font=nib.Font.system(16, weight=nib.FontWeight.SEMIBOLD)
    )
    network_type = nib.Text("--", foreground_color=text_secondary)
    network_ssid = nib.Text("", foreground_color=text_secondary)
    network_icon = nib.SFSymbol(
        "wifi", font=nib.Font.system(18), foreground_color=accent_blue
    )

    def refresh_network():
        try:
            info = app.connectivity.get_status()
            if info.is_connected:
                network_status.content = "Connected"
                network_status.foreground_color = accent_green
                network_icon.foreground_color = accent_green
                network_type.content = info.type.value.title()
                if info.type.value == "wifi":
                    network_icon.name = "wifi"
                    network_ssid.content = info.ssid or ""
                elif info.type.value == "ethernet":
                    network_icon.name = "cable.connector"
                    network_ssid.content = ""
                else:
                    network_icon.name = "network"
                    network_ssid.content = ""
            else:
                network_status.content = "Offline"
                network_status.foreground_color = accent_red
                network_icon.name = "wifi.slash"
                network_icon.foreground_color = accent_red
                network_type.content = "No Connection"
                network_ssid.content = ""
        except Exception:
            network_status.content = "Error"

    network_card = make_card(
        "NETWORK",
        nib.HStack(
            controls=[network_icon, network_status, nib.Spacer(), network_type],
            spacing=8,
        ),
        network_ssid,
    )

    # =========================================================================
    # REFRESH ALL
    # =========================================================================
    def refresh_all():
        refresh_battery()
        refresh_health()
        refresh_thermal()
        refresh_display()
        refresh_appearance()
        refresh_network()

    # =========================================================================
    # MAIN VIEW
    # =========================================================================
    app.build(
        nib.ScrollView(
            controls=[
                nib.VStack(
                    controls=[
                        battery_card,
                        health_card,
                        thermal_card,
                        display_card,
                        appearance_card,
                        network_card,
                        nib.Button(
                            "Refresh All",
                            action=refresh_all,
                            style=nib.ButtonStyle.BORDERED,
                        ),
                    ],
                    spacing=10,
                    padding=12,
                )
            ],
        )
    )

    app.on_appear = refresh_all


nib.run(main)
