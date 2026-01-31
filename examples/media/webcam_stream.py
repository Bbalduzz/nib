"""Webcam streaming to Canvas example with effects.

Streams live webcam video to a nib Canvas using cv2.
Requires: pip install opencv-python numpy
"""

import threading
import time

import nib

try:
    import cv2
    import numpy as np
except ImportError:
    print("This example requires opencv-python and numpy:")
    print("  pip install opencv-python numpy")
    exit(1)


EFFECTS = [
    "None",
    "Grayscale",
    "Edges",
    "Cartoon",
    "Sepia",
    "Invert",
    "Blur",
    "Pixelate",
]


def apply_effect(frame, effect):
    """Apply a cv2 effect to the frame."""
    if effect == "None":
        return frame

    elif effect == "Grayscale":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    elif effect == "Edges":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    elif effect == "Cartoon":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
        )
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        return cv2.bitwise_and(color, color, mask=edges)

    elif effect == "Sepia":
        kernel = np.array(
            [[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]
        )
        sepia = cv2.transform(frame, kernel)
        return np.clip(sepia, 0, 255).astype(np.uint8)

    elif effect == "Invert":
        return cv2.bitwise_not(frame)

    elif effect == "Blur":
        return cv2.GaussianBlur(frame, (21, 21), 0)

    elif effect == "Pixelate":
        h, w = frame.shape[:2]
        small = cv2.resize(frame, (w // 10, h // 10), interpolation=cv2.INTER_LINEAR)
        return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

    return frame


def main(app: nib.App):
    app.title = "Webcam FX"
    app.width = 340
    app.height = 340

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open camera")
        return

    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    canvas = nib.Canvas(width=320, height=240, background_color="#000000")
    status_text = nib.Text("Starting...", font=nib.Font.caption)

    current_effect = ["None"]
    running = True
    frame_count = 0
    start_time = time.time()

    def capture_loop():
        nonlocal frame_count, start_time

        # Wait for canvas to be connected to app
        while getattr(canvas, "_app", None) is None:
            time.sleep(0.1)

        while running:
            ret, frame = cap.read()
            if not ret or frame is None:
                time.sleep(0.1)
                continue

            frame = cv2.resize(frame, (320, 240))
            frame = apply_effect(frame, current_effect[0])

            _, encoded = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

            canvas.draw(
                [
                    nib.draw.Image(
                        data=encoded.tobytes(), x=0, y=0, width=320, height=240
                    )
                ]
            )

            frame_count += 1
            elapsed = time.time() - start_time
            if elapsed >= 0.25:
                fps = frame_count / elapsed
                status_text.content = f"{current_effect[0]} | {fps:.0f} FPS"
                frame_count = 0
                start_time = time.time()

            # time.sleep(1 / 120)

    def on_effect_change(value):
        current_effect[0] = value

    app.build(
        nib.VStack(
            controls=[
                canvas,
                nib.Picker(
                    options=EFFECTS,
                    selection="None",
                    on_change=on_effect_change,
                ),
                status_text,
            ],
            spacing=8,
            padding=10,
        )
    )

    # Start capture thread AFTER build()
    thread = threading.Thread(target=capture_loop, daemon=True)
    thread.start()

    import atexit

    def cleanup():
        nonlocal running
        running = False
        cap.release()

    atexit.register(cleanup)


nib.run(main)
