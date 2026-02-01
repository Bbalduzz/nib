"""TextField controls for single-line and secure text input.

This module provides TextField for general text input and SecureField for
password and sensitive data entry. Both support placeholder text, change
callbacks, and various styling options.

Example:
    Basic text field::

        nib.TextField(placeholder="Enter your name", value="")

    Text field with callback::

        nib.TextField(
            placeholder="Email",
            value=email,
            on_change=update_email,
            style=nib.TextFieldStyle.roundedBorder,
        )

    Secure password field::

        nib.SecureField(
            placeholder="Password",
            value=password,
            on_change=update_password,
        )
"""

from typing import Any, Callable, Optional, Union
from ..base import View
from ...types import TextFieldStyle, resolve_enum


class TextField(View):
    """A control for entering single-line text input.

    TextField provides a single-line text input field with optional placeholder
    text. The value property is reactive - reading and writing it directly
    allows for easy state management.

    Attributes:
        value: The current text value in the field.

    Example:
        Basic text input::

            name_field = nib.TextField(
                placeholder="Enter your name",
                value="",
            )

        Text field with change callback::

            nib.TextField(
                placeholder="Search...",
                value=search_query,
                on_change=handle_search,
                style=nib.TextFieldStyle.roundedBorder,
            )

        Reactive value updates::

            input_field = nib.TextField(value="0")

            def increment():
                current = int(input_field.value)
                input_field.value = str(current + 1)

        Text field with submit action::

            def on_search(query: str):
                print(f"Searching for: {query}")

            nib.TextField(
                placeholder="Press Enter to search",
                value="",
                on_submit=on_search,
                submit_label="Search",
            )
    """

    _type = "TextField"

    def __init__(
        self,
        placeholder: str = "",
        value: str = "",
        # Alias for backwards compatibility
        text: str = None,
        on_change: Optional[Callable[[str], None]] = None,
        on_submit: Optional[Callable[[str], None]] = None,
        # TextField-specific styling
        style: Optional[Union[TextFieldStyle, str]] = None,
        autocapitalization: Optional[str] = None,
        autocorrection: Optional[bool] = None,
        keyboard_type: Optional[str] = None,
        submit_label: Optional[str] = None,
        disabled: bool = False,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a TextField view.

        Args:
            placeholder: Hint text displayed when the field is empty.
            value: Initial text value. Use the value property for reactive updates.
            text: Deprecated alias for value parameter. Use value instead.
            on_change: Callback function called when text changes.
                Receives the new text value as a string argument.
            on_submit: Callback function called when the user presses Return/Enter.
                Receives the current text value as a string argument.
            style: Visual style of the text field. Options:
                - TextFieldStyle.automatic: System default
                - TextFieldStyle.plain: Plain style without decorations
                - TextFieldStyle.roundedBorder: Rounded border style
            autocapitalization: Autocapitalization behavior. Options include
                "none", "words", "sentences", "allCharacters".
            autocorrection: Whether to enable autocorrection. True to enable,
                False to disable, None for system default.
            keyboard_type: Type of keyboard to display. Options include
                "default", "asciiCapable", "numbersAndPunctuation",
                "URL", "numberPad", "emailAddress", "decimalPad".
            submit_label: Label for the Return/Enter key (e.g., "Search", "Go").
            disabled: Whether the text field is disabled and non-interactive.
            **kwargs: Standard view modifiers including padding, background,
                foreground_color, font, opacity, etc.

        Example:
            Create an email input field::

                nib.TextField(
                    placeholder="your@email.com",
                    value="",
                    on_change=validate_email,
                    keyboard_type="emailAddress",
                    autocapitalization="none",
                    autocorrection=False,
                )
        """
        super().__init__(**kwargs)
        self._placeholder = placeholder
        # value is the preferred name, text is alias for backwards compatibility
        self._value = value if text is None else text
        self._on_change = on_change
        self._on_submit = on_submit

        # Build text field-specific styles
        self._text_field_styles: dict = {}
        if style is not None:
            self._text_field_styles["style"] = resolve_enum(style)
        if autocapitalization is not None:
            self._text_field_styles["autocapitalization"] = autocapitalization
        if autocorrection is not None:
            self._text_field_styles["autocorrection"] = autocorrection
        if keyboard_type is not None:
            self._text_field_styles["keyboardType"] = keyboard_type
        if submit_label is not None:
            self._text_field_styles["submitLabel"] = submit_label
        if disabled:
            self._text_field_styles["disabled"] = True

    @property
    def value(self) -> str:
        """Get the current text value.

        Returns:
            The current text string in the field.
        """
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        """Set the text value and trigger UI update.

        Args:
            new_value: The new text string to set.

        Note:
            Only triggers a UI update if the value actually changed.
        """
        if self._value != new_value:
            self._value = new_value
            self._trigger_update()

    def _get_props(self) -> dict:
        props = {
            "placeholder": self._placeholder,
            "text": self._value,  # Swift expects "text" prop
        }
        if self._text_field_styles:
            props["textFieldStyles"] = self._text_field_styles
        return props


class SecureField(View):
    """A control for entering secure text such as passwords.

    SecureField provides a text input field that obscures the entered text,
    suitable for passwords and other sensitive information. It behaves like
    TextField but masks the input characters.

    Attributes:
        value: The current text value in the field (masked in UI).

    Example:
        Basic password field::

            nib.SecureField(
                placeholder="Password",
                value="",
                on_change=handle_password_change,
            )

        Styled secure field::

            nib.SecureField(
                placeholder="Enter PIN",
                value=pin,
                on_change=update_pin,
                style=nib.TextFieldStyle.roundedBorder,
            )

        Secure field with submit action::

            def authenticate(password: str):
                # Verify password
                pass

            nib.SecureField(
                placeholder="Password",
                value="",
                on_submit=authenticate,
            )
    """

    _type = "SecureField"

    def __init__(
        self,
        placeholder: str = "",
        value: str = "",
        # Alias for backwards compatibility
        text: str = None,
        on_change: Optional[Callable[[str], None]] = None,
        on_submit: Optional[Callable[[str], None]] = None,
        # SecureField-specific styling
        style: Optional[Union[TextFieldStyle, str]] = None,
        disabled: bool = False,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a SecureField view.

        Args:
            placeholder: Hint text displayed when the field is empty.
            value: Initial text value (will be masked in the UI).
            text: Deprecated alias for value parameter. Use value instead.
            on_change: Callback function called when text changes.
                Receives the new text value as a string argument.
            on_submit: Callback function called when the user presses Return/Enter.
                Receives the current text value as a string argument.
            style: Visual style of the secure field. Options:
                - TextFieldStyle.automatic: System default
                - TextFieldStyle.plain: Plain style without decorations
                - TextFieldStyle.roundedBorder: Rounded border style
            disabled: Whether the secure field is disabled and non-interactive.
            **kwargs: Standard view modifiers including padding, background,
                foreground_color, font, opacity, etc.

        Example:
            Create a password field with validation::

                nib.SecureField(
                    placeholder="Password (min 8 chars)",
                    value="",
                    on_change=validate_password,
                    on_submit=login,
                    style=nib.TextFieldStyle.roundedBorder,
                )
        """
        super().__init__(**kwargs)
        self._placeholder = placeholder
        # value is the preferred name, text is alias for backwards compatibility
        self._value = value if text is None else text
        self._on_change = on_change
        self._on_submit = on_submit

        # Build secure field-specific styles
        self._secure_field_styles: dict = {}
        if style is not None:
            self._secure_field_styles["style"] = resolve_enum(style)
        if disabled:
            self._secure_field_styles["disabled"] = True

    @property
    def value(self) -> str:
        """Get the current text value.

        Returns:
            The current text string in the field.
        """
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        """Set the text value and trigger UI update.

        Args:
            new_value: The new text string to set.

        Note:
            Only triggers a UI update if the value actually changed.
        """
        if self._value != new_value:
            self._value = new_value
            self._trigger_update()

    def _get_props(self) -> dict:
        props = {
            "placeholder": self._placeholder,
            "text": self._value,  # Swift expects "text" prop
        }
        if self._secure_field_styles:
            props["textFieldStyles"] = self._secure_field_styles
        return props
