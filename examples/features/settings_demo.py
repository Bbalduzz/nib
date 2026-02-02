"""Demo of Settings and UserDefaults.

Shows the difference between:
- Settings class: Instant reads from cache, async writes (recommended)
- UserDefaults: Direct access with network round-trip (slower)
"""

import time

import nib


def main(app: nib.App):
    app.title = "Settings Demo"
    app.icon = nib.SFSymbol("gearshape.fill")
    app.width = 350
    app.height = 400

    # Create Settings with defaults (sync cache + async persist)
    settings = nib.Settings(
        {
            "dark_mode": False,
            "font_size": 14,
            "username": "guest",
            "counter": 0,
        }
    )
    app.register_settings(settings)

    # UI elements
    status_text = nib.Text(
        "", font=nib.Font.CAPTION, foreground_color=nib.Color.SECONDARY
    )
    counter_text = nib.Text(f"Counter: {settings.counter}", font=nib.Font.HEADLINE)

    def update_status(msg: str):
        status_text.content = msg

    # Settings class demo (instant)
    def increment_counter():
        start = time.perf_counter()
        settings.counter = settings.counter + 1  # Read + write
        elapsed = (time.perf_counter() - start) * 1000
        counter_text.content = f"Counter: {settings.counter}"
        update_status(f"Settings: {elapsed:.2f}ms (cached)")

    def reset_counter():
        settings.counter = 0
        counter_text.content = f"Counter: {settings.counter}"
        update_status("Counter reset")

    # UserDefaults demo (direct, slower)
    def test_user_defaults():
        defaults = nib.UserDefaults()

        # Time a direct read
        start = time.perf_counter()
        value = defaults.get("test_key", default="none")
        read_time = (time.perf_counter() - start) * 1000

        # Time a direct write
        start = time.perf_counter()
        defaults.set("test_key", f"value_{time.time()}")
        write_time = (time.perf_counter() - start) * 1000

        update_status(f"UserDefaults: read={read_time:.1f}ms, write={write_time:.1f}ms")

    # Compare performance
    def run_benchmark():
        update_status("Running benchmark...")

        # Benchmark Settings (cached)
        start = time.perf_counter()
        for _ in range(100):
            _ = settings.counter
            settings.counter = settings.counter + 1
        settings_time = (time.perf_counter() - start) * 1000
        counter_text.content = f"Counter: {settings.counter}"

        # Benchmark UserDefaults (direct) - just 5 reads
        defaults = nib.UserDefaults()
        start = time.perf_counter()
        for i in range(5):
            defaults.get(f"bench_{i}", default=0)
        ud_time = (time.perf_counter() - start) * 1000

        update_status(
            f"100 Settings ops: {settings_time:.1f}ms | 5 UserDefaults reads: {ud_time:.1f}ms"
        )

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Settings vs UserDefaults", font=nib.Font.TITLE),
                nib.Divider(),
                # Settings class section
                nib.VStack(
                    controls=[
                        nib.Text(
                            "Settings Class (Recommended)", font=nib.Font.HEADLINE
                        ),
                        nib.Text(
                            "Instant reads from cache, async persistence",
                            font=nib.Font.CAPTION,
                            foreground_color=nib.Color.SECONDARY,
                        ),
                        counter_text,
                        nib.HStack(
                            controls=[
                                nib.Button("+1", action=increment_counter),
                                nib.Button("Reset", action=reset_counter),
                            ],
                            spacing=8,
                        ),
                    ],
                    spacing=8,
                    padding=12,
                    background=nib.Rectangle(
                        corner_radius=8,
                        fill=nib.Color.hex("#1a1a1a"),
                    ),
                ),
                nib.Spacer(min_length=8),
                # UserDefaults section
                nib.VStack(
                    controls=[
                        nib.Text("UserDefaults (Direct)", font=nib.Font.HEADLINE),
                        nib.Text(
                            "Network round-trip per operation",
                            font=nib.Font.CAPTION,
                            foreground_color=nib.Color.SECONDARY,
                        ),
                        nib.Button("Test Read/Write", action=test_user_defaults),
                    ],
                    spacing=8,
                    padding=12,
                    background=nib.Rectangle(
                        corner_radius=8,
                        fill=nib.Color.hex("#1a1a1a"),
                    ),
                ),
                nib.Spacer(min_length=8),
                # Benchmark
                nib.Button(
                    "Run Benchmark",
                    action=run_benchmark,
                    style=nib.ButtonStyle.BORDERED_PROMINENT,
                ),
                nib.Spacer(),
                status_text,
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
