Animation
=========

Animations bring your UI to life with smooth transitions.

Animation Class
---------------

.. autoclass:: nib.Animation
   :members:
   :undoc-members:

Creating Animations
-------------------

**Spring Animation (Recommended)**

.. code-block:: python

    nib.Animation.spring()
    nib.Animation.spring(duration=0.5)
    nib.Animation.spring(bounce=0.3)

**Ease Animations**

.. code-block:: python

    nib.Animation.easeIn(duration=0.3)
    nib.Animation.easeOut(duration=0.3)
    nib.Animation.easeInOut(duration=0.3)

**Linear Animation**

.. code-block:: python

    nib.Animation.linear(duration=0.5)

Applying Animations
-------------------

Add the ``animation`` parameter to any view:

.. code-block:: python

    nib.Text(
        "Animated",
        animation=nib.Animation.spring(),
    )

    nib.Rectangle(
        fill=nib.Color.BLUE,
        width=100,
        height=100,
        animation=nib.Animation.easeInOut(0.3),
    )

Content Transitions
-------------------

Animate how content changes:

.. autoclass:: nib.ContentTransition
   :members:
   :undoc-members:

.. code-block:: python

    nib.Text(
        counter_value,
        content_transition=nib.ContentTransition.NUMERICTEXT,
    )

Available transitions:

.. code-block:: python

    nib.ContentTransition.OPACITY       # Fade in/out
    nib.ContentTransition.INTERPOLATE   # Smooth interpolation
    nib.ContentTransition.NUMERICTEXT   # Number counter animation

View Transitions
----------------

Animate view appearance/disappearance:

.. autoclass:: nib.Transition
   :members:
   :undoc-members:

.. code-block:: python

    nib.VStack(
        controls=[...],
        transition=nib.Transition.SLIDE,
    )

Available transitions:

.. code-block:: python

    nib.Transition.OPACITY    # Fade
    nib.Transition.SLIDE      # Slide from edge
    nib.Transition.SCALE      # Scale up/down
    nib.Transition.MOVE       # Move from direction
    nib.Transition.PUSH       # Push old content out

Examples
--------

**Animated Counter**

.. code-block:: python

    counter = nib.Text(
        "0",
        font=nib.Font.LARGE_TITLE,
        content_transition=nib.ContentTransition.NUMERICTEXT,
        animation=nib.Animation.spring(),
    )

    def increment():
        counter.content = str(int(counter.content) + 1)

**Animated Color Change**

.. code-block:: python

    box = nib.Rectangle(
        fill=nib.Color.BLUE,
        width=100,
        height=100,
        animation=nib.Animation.easeInOut(0.5),
    )

    def toggle_color():
        if box._fill == nib.Color.BLUE:
            box.fill = nib.Color.RED
        else:
            box.fill = nib.Color.BLUE

**Loading Spinner with Animation**

.. code-block:: python

    nib.ProgressView(
        animation=nib.Animation.linear(duration=1.0),
    )
