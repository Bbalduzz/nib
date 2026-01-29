Gauge
=====

A view that displays a value within a range, similar to a speedometer or fuel gauge.

.. code-block:: python

    import nib

    # Simple gauge
    gauge = nib.Gauge(
        value=0.75,
        label="Battery",
        current_value_label="75%",
    )

    # Circular gauge with tint
    cpu_gauge = nib.Gauge(
        value=0.65,
        label="CPU",
        current_value_label="65%",
        style=nib.GaugeStyle.ACCESSORY_CIRCULAR,
        tint=nib.Color.BLUE,
    )

    # Linear gauge with min/max labels
    progress = nib.Gauge(
        value=0.35,
        min_value=0,
        max_value=100,
        label="Download",
        current_value_label="35%",
        min_value_label="0%",
        max_value_label="100%",
        style=nib.GaugeStyle.LINEAR_CAPACITY,
        tint=nib.Color.PURPLE,
    )

Parameters
----------

value : float
    Current value to display.

min_value : float, optional
    Minimum value of the range (default: 0.0).

max_value : float, optional
    Maximum value of the range (default: 1.0).

label : str or View, optional
    Label describing the gauge. Can be a string or a custom View.

current_value_label : str or View, optional
    Label showing the current value.

min_value_label : str or View, optional
    Label for the minimum value.

max_value_label : str or View, optional
    Label for the maximum value.

style : GaugeStyle, optional
    Visual style of the gauge (default: AUTOMATIC).

tint : Color or str, optional
    Color tint for the gauge.

Gauge Styles
------------

.. code-block:: python

    nib.GaugeStyle.AUTOMATIC              # System default
    nib.GaugeStyle.LINEAR_CAPACITY        # Horizontal bar
    nib.GaugeStyle.CIRCULAR_CAPACITY      # Circular ring
    nib.GaugeStyle.ACCESSORY_LINEAR       # Compact linear
    nib.GaugeStyle.ACCESSORY_CIRCULAR     # Compact circular
    nib.GaugeStyle.ACCESSORY_LINEAR_CAPACITY
    nib.GaugeStyle.ACCESSORY_CIRCULAR_CAPACITY

Custom View Labels
------------------

All label parameters accept either strings or Views for full customization:

.. code-block:: python

    # Gauge with custom view labels
    gauge = nib.Gauge(
        value=0.5,
        label=nib.Label("Speed", system_image="speedometer"),
        current_value_label=nib.Text("50%", font=nib.Font.headline),
        min_value_label=nib.SFSymbol("tortoise", foreground_color=nib.Color.GREEN),
        max_value_label=nib.SFSymbol("hare", foreground_color=nib.Color.RED),
        style=nib.GaugeStyle.LINEAR_CAPACITY,
    )

.. note::

    The ``accessoryCircular`` style does not display the label visually - it only
    shows the current value. Use ``LINEAR_CAPACITY`` to see all labels.

Example: System Monitor
-----------------------

.. code-block:: python

    import nib

    def main(app: nib.App):
        app.title = "System Monitor"

        cpu = nib.Gauge(
            value=0.65,
            label="CPU",
            current_value_label="65%",
            style=nib.GaugeStyle.ACCESSORY_CIRCULAR,
            tint=nib.Color.BLUE,
        )

        memory = nib.Gauge(
            value=0.42,
            label="Memory",
            current_value_label="42%",
            style=nib.GaugeStyle.ACCESSORY_CIRCULAR,
            tint=nib.Color.GREEN,
        )

        disk = nib.Gauge(
            value=0.78,
            label="Disk",
            current_value_label="78%",
            style=nib.GaugeStyle.ACCESSORY_CIRCULAR,
            tint=nib.Color.ORANGE,
        )

        app.build(
            nib.HStack(
                controls=[cpu, memory, disk],
                spacing=16,
                padding=16,
            )
        )

    nib.run(main)
