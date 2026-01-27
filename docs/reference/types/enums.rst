Enums
=====

Nib provides various enums for configuring view appearance and behavior.

Alignment
---------

HorizontalAlignment
^^^^^^^^^^^^^^^^^^^

.. autoclass:: nib.HorizontalAlignment
   :members:
   :undoc-members:

.. code-block:: python

    nib.HorizontalAlignment.LEADING   # Left-aligned
    nib.HorizontalAlignment.CENTER    # Center-aligned
    nib.HorizontalAlignment.TRAILING  # Right-aligned

VerticalAlignment
^^^^^^^^^^^^^^^^^

.. autoclass:: nib.VerticalAlignment
   :members:
   :undoc-members:

.. code-block:: python

    nib.VerticalAlignment.TOP
    nib.VerticalAlignment.CENTER
    nib.VerticalAlignment.BOTTOM

Alignment
^^^^^^^^^

.. autoclass:: nib.Alignment
   :members:
   :undoc-members:

.. code-block:: python

    nib.Alignment.CENTER
    nib.Alignment.TOP
    nib.Alignment.BOTTOM
    nib.Alignment.LEADING
    nib.Alignment.TRAILING
    nib.Alignment.TOPLEADING
    nib.Alignment.TOPTRAILING
    nib.Alignment.BOTTOMLEADING
    nib.Alignment.BOTTOMTRAILING

Button Styles
-------------

ButtonStyle
^^^^^^^^^^^

.. autoclass:: nib.ButtonStyle
   :members:
   :undoc-members:

.. code-block:: python

    nib.ButtonStyle.AUTOMATIC        # System default
    nib.ButtonStyle.BORDERED         # Bordered button
    nib.ButtonStyle.BORDEREDPROMINENT  # Prominent bordered (filled)
    nib.ButtonStyle.BORDERLESS       # No border
    nib.ButtonStyle.PLAIN            # Plain text

ButtonRole
^^^^^^^^^^

.. autoclass:: nib.ButtonRole
   :members:
   :undoc-members:

.. code-block:: python

    nib.ButtonRole.NONE          # Default role
    nib.ButtonRole.CANCEL        # Cancel action
    nib.ButtonRole.DESTRUCTIVE   # Destructive action (red)

ControlSize
^^^^^^^^^^^

.. autoclass:: nib.ControlSize
   :members:
   :undoc-members:

.. code-block:: python

    nib.ControlSize.MINI
    nib.ControlSize.SMALL
    nib.ControlSize.REGULAR
    nib.ControlSize.LARGE
    nib.ControlSize.EXTRALARGE

Control Styles
--------------

ToggleStyle
^^^^^^^^^^^

.. autoclass:: nib.ToggleStyle
   :members:
   :undoc-members:

.. code-block:: python

    nib.ToggleStyle.AUTOMATIC
    nib.ToggleStyle.SWITCH      # iOS-style switch
    nib.ToggleStyle.CHECKBOX    # Checkbox style
    nib.ToggleStyle.BUTTON      # Button that toggles

TextFieldStyle
^^^^^^^^^^^^^^

.. autoclass:: nib.TextFieldStyle
   :members:
   :undoc-members:

.. code-block:: python

    nib.TextFieldStyle.AUTOMATIC
    nib.TextFieldStyle.PLAIN
    nib.TextFieldStyle.ROUNDEDBORDER  # Rounded border style

PickerStyle
^^^^^^^^^^^

.. autoclass:: nib.PickerStyle
   :members:
   :undoc-members:

.. code-block:: python

    nib.PickerStyle.AUTOMATIC
    nib.PickerStyle.MENU        # Dropdown menu
    nib.PickerStyle.SEGMENTED   # Segmented control
    nib.PickerStyle.WHEEL       # Wheel picker

ProgressStyle
^^^^^^^^^^^^^

.. autoclass:: nib.ProgressStyle
   :members:
   :undoc-members:

.. code-block:: python

    nib.ProgressStyle.AUTOMATIC
    nib.ProgressStyle.LINEAR    # Progress bar
    nib.ProgressStyle.CIRCULAR  # Circular progress

Text Styles
-----------

TruncationMode
^^^^^^^^^^^^^^

.. autoclass:: nib.TruncationMode
   :members:
   :undoc-members:

.. code-block:: python

    nib.TruncationMode.HEAD    # ...rest of text
    nib.TruncationMode.MIDDLE  # start...end
    nib.TruncationMode.TAIL    # text...

TextCase
^^^^^^^^

.. autoclass:: nib.TextCase
   :members:
   :undoc-members:

.. code-block:: python

    nib.TextCase.UPPERCASE
    nib.TextCase.LOWERCASE

Image Styles
------------

ContentMode
^^^^^^^^^^^

.. autoclass:: nib.ContentMode
   :members:
   :undoc-members:

.. code-block:: python

    nib.ContentMode.FIT    # Fit within bounds
    nib.ContentMode.FILL   # Fill bounds (may crop)

ImageRenderingMode
^^^^^^^^^^^^^^^^^^

.. autoclass:: nib.ImageRenderingMode
   :members:
   :undoc-members:

.. code-block:: python

    nib.ImageRenderingMode.ORIGINAL  # Original colors
    nib.ImageRenderingMode.TEMPLATE  # Tintable

SymbolScale
^^^^^^^^^^^

.. autoclass:: nib.SymbolScale
   :members:
   :undoc-members:

.. code-block:: python

    nib.SymbolScale.SMALL
    nib.SymbolScale.MEDIUM
    nib.SymbolScale.LARGE

SymbolRenderingMode
^^^^^^^^^^^^^^^^^^^

.. autoclass:: nib.SymbolRenderingMode
   :members:
   :undoc-members:

.. code-block:: python

    nib.SymbolRenderingMode.MONOCHROME
    nib.SymbolRenderingMode.MULTICOLOR
    nib.SymbolRenderingMode.HIERARCHICAL
    nib.SymbolRenderingMode.PALETTE

Scroll
------

ScrollAxis
^^^^^^^^^^

.. autoclass:: nib.ScrollAxis
   :members:
   :undoc-members:

.. code-block:: python

    nib.ScrollAxis.VERTICAL
    nib.ScrollAxis.HORIZONTAL
    nib.ScrollAxis.BOTH

Effects
-------

BlendMode
^^^^^^^^^

.. autoclass:: nib.BlendMode
   :members:
   :undoc-members:

.. code-block:: python

    nib.BlendMode.NORMAL
    nib.BlendMode.MULTIPLY
    nib.BlendMode.SCREEN
    nib.BlendMode.OVERLAY
    # ... and more
