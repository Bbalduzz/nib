"""Animated "talking" waveform visualization."""

import math
import random
import threading
import time

import nib


def main(app: nib.App):
    app.title = "Voice"
    app.icon = nib.SFSymbol("waveform")
    app.width = 420
    app.height = 140

    num_bars = 100
    bar_width = 2
    bar_gap = 2
    max_height = 70
    canvas_width = num_bars * (bar_width + bar_gap) + 20
    canvas_height = 90
    center_y = canvas_height / 2

    canvas = nib.Canvas(width=canvas_width, height=canvas_height)

    is_talking = [False]
    levels = [0.05] * num_bars
    envelope = [0.0] * num_bars  # Speech envelope pattern

    def draw():
        commands = []
        for i, level in enumerate(levels):
            x = 10 + i * (bar_width + bar_gap)
            height = max(2, level * max_height)
            y = center_y - height / 2

            # Brightness: dim when low, bright when high
            brightness = int(100 + level * 155)
            color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"

            commands.append(
                nib.draw.Rect(
                    x=x,
                    y=y,
                    width=bar_width,
                    height=height,
                    corner_radius=1,
                    fill=color,
                )
            )
        canvas.draw(commands)

    def generate_speech_envelope():
        """Generate natural speech-like envelope with words and pauses."""
        # Create 3-5 "word" clusters
        num_words = random.randint(3, 5)
        env = [0.1] * num_bars

        for _ in range(num_words):
            # Random position and width for each "word"
            center = random.randint(10, num_bars - 10)
            width = random.randint(8, 20)
            intensity = random.uniform(0.5, 1.0)

            for i in range(num_bars):
                dist = abs(i - center)
                if dist < width:
                    # Smooth falloff
                    falloff = 1 - (dist / width) ** 2
                    env[i] = max(env[i], intensity * falloff)

        return env

    def animate():
        def run():
            nonlocal envelope
            frame = 0
            envelope = generate_speech_envelope()

            while is_talking[0]:
                # Regenerate envelope periodically (new "sentence")
                if frame % 40 == 0:
                    envelope = generate_speech_envelope()

                # Animate bars based on envelope + randomness
                for i in range(num_bars):
                    base = envelope[i]
                    # Add variation
                    variation = random.uniform(0.7, 1.3)
                    target = base * variation * random.uniform(0.5, 1.0)
                    # Smooth transition
                    levels[i] = levels[i] * 0.4 + target * 0.6

                draw()
                frame += 1
                time.sleep(0.04)

            # Fade out
            for _ in range(15):
                for i in range(num_bars):
                    levels[i] *= 0.75
                draw()
                time.sleep(0.025)

        threading.Thread(target=run, daemon=True).start()

    def toggle():
        is_talking[0] = not is_talking[0]
        if is_talking[0]:
            animate()

    draw()

    app.build(
        nib.VStack(
            controls=[
                canvas,
                nib.Button("Talk", action=toggle),
            ],
            spacing=12,
            padding=10,
        )
    )


nib.run(main)
