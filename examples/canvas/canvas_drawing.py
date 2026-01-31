"""Canvas Drawing Example - Draw with mouse/pen like Flet.

This example demonstrates the Canvas gesture callbacks for creating
a simple drawing application.
"""

import nib


def main(app: nib.App):
    app.title = "Draw"
    app.icon = nib.SFSymbol("pencil.tip")
    app.width = 440
    app.height = 380

    # Canvas for drawing
    canvas = nib.Canvas(
        width=420,
        height=300,
        background_color="#FFFFFF",
        enable_gestures=True,
    )

    # Drawing state
    last_x = 0.0
    last_y = 0.0
    stroke_color = "#000000"
    stroke_width = 3

    def on_pan_start(e: nib.PanEvent):
        nonlocal last_x, last_y
        last_x = e.x
        last_y = e.y

    def on_pan_update(e: nib.PanEvent):
        nonlocal last_x, last_y
        # Draw line from last position to current
        canvas.append(
            nib.draw.Line(
                x1=last_x,
                y1=last_y,
                x2=e.x,
                y2=e.y,
                stroke=stroke_color,
                stroke_width=stroke_width,
                line_cap="round",
            )
        )
        last_x = e.x
        last_y = e.y

    canvas.on_pan_start = on_pan_start
    canvas.on_pan_update = on_pan_update

    # Clear button
    def clear_canvas():
        canvas.clear()

    # Color buttons
    def set_black():
        nonlocal stroke_color
        stroke_color = "#000000"

    def set_red():
        nonlocal stroke_color
        stroke_color = "#e74c3c"

    def set_blue():
        nonlocal stroke_color
        stroke_color = "#3498db"

    def set_green():
        nonlocal stroke_color
        stroke_color = "#2ecc71"

    # Width buttons
    def set_thin():
        nonlocal stroke_width
        stroke_width = 2

    def set_medium():
        nonlocal stroke_width
        stroke_width = 5

    def set_thick():
        nonlocal stroke_width
        stroke_width = 10

    app.build(
        nib.VStack(
            controls=[
                # Toolbar
                nib.HStack(
                    controls=[
                        nib.Button("Clear", action=clear_canvas),
                        nib.Spacer(),
                        # Color picker
                        nib.Text("Color:", font=nib.Font.caption),
                        nib.Button("Black", action=set_black),
                        nib.Button("Red", action=set_red),
                        nib.Button("Blue", action=set_blue),
                        nib.Button("Green", action=set_green),
                        nib.Spacer(),
                        # Width picker
                        nib.Text("Width:", font=nib.Font.caption),
                        nib.Button("Thin", action=set_thin),
                        nib.Button("Med", action=set_medium),
                        nib.Button("Thick", action=set_thick),
                    ],
                    spacing=4,
                ),
                # Canvas with border
                nib.VStack(
                    controls=[canvas],
                    background=nib.RoundedRectangle(
                        corner_radius=5,
                        stroke="#cccccc",
                        stroke_width=1,
                    ),
                ),
            ],
            spacing=10,
            padding=10,
        )
    )


nib.run(main)
