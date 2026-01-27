TextField
=========

A control for entering and editing text.

.. code-block:: python

    nib.TextField(
        value="",
        placeholder="Enter your name",
        on_change=lambda text: print(text),
    )

.. autoclass:: nib.TextField
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``value`` - Current text value
- ``placeholder`` - Placeholder text when empty
- ``on_change`` - Callback when text changes
- ``on_submit`` - Callback when return/enter is pressed
- ``style`` - Text field style (:class:`~nib.TextFieldStyle`)

SecureField
-----------

A text field that hides the entered text (for passwords).

.. code-block:: python

    nib.SecureField(
        value="",
        placeholder="Password",
        on_change=lambda text: print("Password changed"),
    )

.. autoclass:: nib.SecureField
   :members:
   :undoc-members:
   :show-inheritance:

Examples
--------

**Basic Text Field**

.. code-block:: python

    name_field = nib.TextField(
        value="",
        placeholder="Enter your name",
    )

    # Access the value later
    print(name_field.value)

**With Change Handler**

.. code-block:: python

    def on_text_change(text: str):
        print(f"Text changed to: {text}")

    nib.TextField(
        value="",
        placeholder="Type something",
        on_change=on_text_change,
    )

**With Submit Handler**

.. code-block:: python

    def on_submit(text: str):
        print(f"Submitted: {text}")

    nib.TextField(
        value="",
        placeholder="Press Enter to submit",
        on_submit=on_submit,
    )

**Login Form**

.. code-block:: python

    username = nib.TextField(
        value="",
        placeholder="Username",
    )

    password = nib.SecureField(
        value="",
        placeholder="Password",
    )

    nib.VStack(
        controls=[
            username,
            password,
            nib.Button("Login", action=login),
        ],
        spacing=12,
    )

**Styled Text Field**

.. code-block:: python

    nib.TextField(
        value="",
        placeholder="Rounded style",
        style=nib.TextFieldStyle.ROUNDEDBORDER,
    )
