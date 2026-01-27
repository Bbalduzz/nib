State
=====

Nib provides reactive state management for updating UI when data changes.

Reactive Properties
-------------------

Views have reactive properties that trigger UI updates when changed:

.. code-block:: python

    import nib

    def main(app: nib.App):
        # Create a Text view
        counter = nib.Text("0")

        def increment():
            # Changing .content triggers a re-render
            counter.content = str(int(counter.content) + 1)

        app.build(
            nib.VStack(
                controls=[
                    counter,
                    nib.Button("Add", action=increment),
                ],
            )
        )

    nib.run(main)

Common Reactive Properties
--------------------------

**Text**

.. code-block:: python

    text = nib.Text("Hello")
    text.content = "World"  # Triggers re-render

**TextField**

.. code-block:: python

    field = nib.TextField(value="")
    field.value = "New value"  # Triggers re-render

**Toggle**

.. code-block:: python

    toggle = nib.Toggle("Option", value=False)
    toggle.value = True  # Triggers re-render

**Slider**

.. code-block:: python

    slider = nib.Slider(value=50, range=(0, 100))
    slider.value = 75  # Triggers re-render

**ProgressView**

.. code-block:: python

    progress = nib.ProgressView(value=0, total=100)
    progress.value = 50  # Triggers re-render

State Descriptor (Class-based)
------------------------------

For class-based apps, use the ``State`` descriptor:

.. autoclass:: nib.State
   :members:
   :undoc-members:

.. code-block:: python

    import nib

    class CounterApp(nib.App):
        count = nib.State(0)

        def body(self):
            return nib.VStack(
                controls=[
                    nib.Text(str(self.count)),
                    nib.Button("Add", action=self.increment),
                ],
            )

        def increment(self):
            self.count += 1  # Triggers re-render

    CounterApp(icon="star").run()

Binding
-------

Two-way binding for connecting state to controls:

.. autoclass:: nib.core.Binding
   :members:
   :undoc-members:

Patterns
--------

**Counter Example**

.. code-block:: python

    def main(app: nib.App):
        count_label = nib.Text("0")

        def increment():
            count_label.content = str(int(count_label.content) + 1)

        def decrement():
            count_label.content = str(int(count_label.content) - 1)

        app.build(
            nib.VStack(
                controls=[
                    count_label,
                    nib.HStack(
                        controls=[
                            nib.Button("-", action=decrement),
                            nib.Button("+", action=increment),
                        ],
                        spacing=8,
                    ),
                ],
                spacing=16,
            )
        )

**Form with Validation**

.. code-block:: python

    def main(app: nib.App):
        name_field = nib.TextField(value="", placeholder="Name")
        error_text = nib.Text("", foreground_color=nib.Color.RED)

        def validate():
            if len(name_field.value) < 3:
                error_text.content = "Name must be at least 3 characters"
            else:
                error_text.content = ""

        name_field.on_change = lambda _: validate()

        app.build(
            nib.VStack(
                controls=[
                    name_field,
                    error_text,
                ],
                spacing=8,
            )
        )

**Loading State**

.. code-block:: python

    def main(app: nib.App):
        status = nib.Text("Ready")
        progress = nib.ProgressView()

        def start_loading():
            status.content = "Loading..."
            # Simulate async work
            # When done:
            # status.content = "Complete!"

        app.build(
            nib.VStack(
                controls=[
                    status,
                    progress,
                    nib.Button("Load", action=start_loading),
                ],
            )
        )
