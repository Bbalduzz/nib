State & Reactivity
==================

Nib uses a reactive model where mutating view properties automatically
triggers re-renders.

Reactive Properties
-------------------

All view properties are reactive. Changing them updates the UI:

.. code-block:: python

    # Create view
    text = nib.Text("Hello")
    counter = 0

    def increment():
        global counter
        counter += 1
        text.content = f"Count: {counter}"  # Triggers re-render

    app.build(
        nib.VStack(controls=[
            text,
            nib.Button("Increment", action=increment),
        ])
    )

Common Reactive Properties
--------------------------

Text
~~~~

.. code-block:: python

    text = nib.Text("Initial")
    text.content = "Updated"  # Re-renders

TextField
~~~~~~~~~

.. code-block:: python

    field = nib.TextField(value="")

    # Read current value
    print(field.value)

    # Set value (triggers re-render)
    field.value = "New value"

    # React to user changes
    field = nib.TextField(
        value="",
        on_change=lambda v: print(f"User typed: {v}"),
    )

Toggle
~~~~~~

.. code-block:: python

    toggle = nib.Toggle("Dark Mode", value=False)

    # Read state
    if toggle.value:
        print("Enabled")

    # Set state
    toggle.value = True

    # React to changes
    toggle = nib.Toggle(
        "Dark Mode",
        value=False,
        on_change=lambda enabled: print(f"Toggled: {enabled}"),
    )

Slider
~~~~~~

.. code-block:: python

    slider = nib.Slider(value=50, range=(0, 100))

    # Update value
    slider.value = 75

Styling Properties
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    rect = nib.Rectangle(fill="#FF0000")
    rect.fill = "#00FF00"          # Change color

    text = nib.Text("Hello")
    text.foreground_color = "#FF0000"
    text.opacity = 0.5

Canvas
~~~~~~

.. code-block:: python

    canvas = nib.Canvas(width=400, height=300)

    # Replace all commands
    canvas.draw([nib.draw.Circle(cx=100, cy=100, radius=50, fill="#FF0000")])

    # Add single command
    canvas.append(nib.draw.Rect(x=10, y=10, width=50, height=50, fill="#00FF00"))

    # Clear canvas
    canvas.clear()

State Patterns
--------------

Using Closures
~~~~~~~~~~~~~~

Capture state in closures:

.. code-block:: python

    def main(app: nib.App):
        count = 0
        label = nib.Text("Count: 0")

        def increment():
            nonlocal count
            count += 1
            label.content = f"Count: {count}"

        app.build(
            nib.VStack(controls=[
                label,
                nib.Button("Add", action=increment),
            ])
        )

Using Dictionaries
~~~~~~~~~~~~~~~~~~

For complex state:

.. code-block:: python

    state = {
        "count": 0,
        "name": "User",
        "items": [],
    }

    count_label = nib.Text(f"Count: {state['count']}")

    def update_count():
        state["count"] += 1
        count_label.content = f"Count: {state['count']}"

View References
~~~~~~~~~~~~~~~

Keep references to views you need to update:

.. code-block:: python

    # Store views you'll update
    status_text = nib.Text("Ready")
    progress = nib.ProgressView(value=0)

    def start_task():
        status_text.content = "Working..."
        progress.value = 0.5

    def finish_task():
        status_text.content = "Done!"
        progress.value = 1.0

Conditional UI
--------------

Rebuild the UI based on state:

.. code-block:: python

    def main(app: nib.App):
        logged_in = False
        username = ""

        def render():
            if logged_in:
                app.build(
                    nib.VStack(controls=[
                        nib.Text(f"Welcome, {username}!"),
                        nib.Button("Logout", action=logout),
                    ])
                )
            else:
                app.build(
                    nib.VStack(controls=[
                        nib.TextField(
                            value=username,
                            placeholder="Username",
                            on_change=lambda v: set_username(v),
                        ),
                        nib.Button("Login", action=login),
                    ])
                )

        def set_username(value):
            nonlocal username
            username = value

        def login():
            nonlocal logged_in
            if username:
                logged_in = True
                render()

        def logout():
            nonlocal logged_in
            logged_in = False
            render()

        render()

UserDefaults
------------

Persist state across sessions:

.. code-block:: python

    from nib import UserDefaults

    defaults = UserDefaults()

    # Save values
    defaults["theme"] = "dark"
    defaults["volume"] = 0.8

    # Read values (with defaults)
    theme = defaults.get("theme", "light")
    volume = defaults.get("volume", 1.0)

    # Delete value
    del defaults["theme"]

See :doc:`/services/index` for more on UserDefaults.
