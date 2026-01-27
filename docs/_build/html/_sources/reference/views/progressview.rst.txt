ProgressView
============

A view that shows progress toward completion of a task.

.. code-block:: python

    # Indeterminate (spinning)
    nib.ProgressView()

    # Determinate (progress bar)
    nib.ProgressView(value=0.75, total=1.0)

.. autoclass:: nib.ProgressView
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``value`` - Current progress value (optional, omit for indeterminate)
- ``total`` - Total value representing completion (default: 1.0)
- ``label`` - Optional label text
- ``style`` - Progress style (:class:`~nib.ProgressStyle`)

Examples
--------

**Indeterminate Progress (Spinner)**

.. code-block:: python

    nib.ProgressView()

**Determinate Progress**

.. code-block:: python

    nib.ProgressView(value=0.5, total=1.0)

**With Label**

.. code-block:: python

    nib.ProgressView(
        value=75,
        total=100,
        label="Downloading...",
    )

**Download Progress**

.. code-block:: python

    progress = nib.ProgressView(value=0, total=100)
    status = nib.Text("0%")

    def update_progress(downloaded: int, total: int):
        progress.value = downloaded
        progress.total = total
        status.content = f"{int(downloaded/total*100)}%"

    nib.VStack(
        controls=[
            nib.Text("Downloading file..."),
            progress,
            status,
        ],
        spacing=8,
    )

**Linear Style**

.. code-block:: python

    nib.ProgressView(
        value=0.6,
        style=nib.ProgressStyle.LINEAR,
    )

**Circular Style**

.. code-block:: python

    nib.ProgressView(
        value=0.6,
        style=nib.ProgressStyle.CIRCULAR,
    )

**Loading State**

.. code-block:: python

    nib.HStack(
        controls=[
            nib.ProgressView(),
            nib.Text("Loading...", foreground_color=nib.Color.SECONDARY),
        ],
        spacing=8,
    )
