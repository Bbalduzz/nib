"""
Counter Example

A simple counter demonstrating numericText content transitions
and custom styled buttons with the declarative parameter-based API.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

from nib import (
    Animation,
    App,
    Button,
    ButtonStyle,
    Circle,
    ContentTransition,
    Font,
    FontWeight,
    HorizontalAlignment,
    HStack,
    Image,
    MenuItem,
    State,
    SFSymbol,
    Text,
    VStack,
    ZStack,
)

# Design tokens
BG_DARK = "#1C1C1E"
ACCENT = "#0A84FF"
DESTRUCTIVE = "#FF453A"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#8E8E93"


class Counter(App):
    count = State(0)

    def body(self):
        return VStack(
            children=[
                self._header(),
                self._counter_display(),
                self._controls(),
            ],
            spacing=24,
            padding=24,
            width=280,
            # background=BG_DARK,
            corner_radius=16,
        )

    def _header(self):
        return Text(
            "Counter",
            font=Font.headline,
            foreground_color=TEXT_SECONDARY,
        )

    def _counter_display(self):
        return VStack(
            children=[
                Text(
                    f"{self.count}",
                    font=Font.system(72, FontWeight.bold),
                    foreground_color=TEXT_PRIMARY,
                    content_transition=ContentTransition.numericText,
                ),
                # Label
                Text(
                    "taps" if self.count != 1 else "tap",
                    font=Font.subheadline,
                    foreground_color=TEXT_SECONDARY,
                    content_transition=ContentTransition.interpolate,
                ),
            ],
            spacing=4,
            alignment=HorizontalAlignment.center,
            padding=32,
            animation=Animation.spring(response=0.3, damping=0.7),
            # animation=Animation.easeInOut(0.3),
        )

    def _controls(self):
        return HStack(
            children=[
                self._icon_button(
                    icon="minus",
                    action=self._decrement,
                    color=DESTRUCTIVE,
                ),
                self._icon_button(
                    icon="arrow.counterclockwise",
                    action=self._reset,
                    color=TEXT_SECONDARY,
                    size=40,
                ),
                self._icon_button(
                    icon="plus",
                    action=self._increment,
                    color=ACCENT,
                ),
            ],
            spacing=16,
        )

    def _icon_button(self, icon: str, action, color: str, size: float = 56):
        return Button(
            content=ZStack(
                children=[
                    # Background circle
                    Circle(
                        fill=color,
                        width=size,
                        height=size,
                        opacity=0.15,
                    ),
                    # Icon
                    SFSymbol(
                        icon,
                        font=Font.system(size=size * 0.4, weight=FontWeight.SEMIBOLD),
                        foreground_color=color,
                    ),
                ],
            ),
            style=ButtonStyle.plain,  # remove default button chrome
            action=action,
            animation=Animation.spring(response=0.2, damping=0.6),
        )

    def _increment(self):
        self.count += 1

    def _decrement(self):
        self.count -= 1

    def _reset(self):
        self.count = 0


if __name__ == "__main__":
    application = Counter(icon="number")
    application.menu = [
        MenuItem("Quit", action=application.quit),
    ]

    application.run()
