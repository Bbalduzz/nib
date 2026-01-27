"""TextField - Single-line text input with declarative parameter-based API."""

from typing import Any, Callable, Optional, Union
from ..base import View
from ...types import TextFieldStyle, resolve_enum


class TextField(View):
    """
    A control for entering single-line text.

    The value property can be read and written directly:

        input = nib.TextField(value="0")

        def increment(e):
            input.value = str(int(input.value) + 1)

    Or use on_change callback:

        TextField(
            placeholder="Email",
            value=email,
            on_change=update_email,
            style=TextFieldStyle.roundedBorder,
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
        on_submit: Optional[Callable[[], None]] = None,
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
        """Get the current text value."""
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        """Set the text value and trigger UI update."""
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
    """
    A control for entering secure text (passwords).

        SecureField(placeholder="Password", value=password, on_change=update_password)

        SecureField(
            placeholder="Password",
            value=password,
            on_change=update_password,
            style=TextFieldStyle.roundedBorder,
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
        on_submit: Optional[Callable[[], None]] = None,
        # SecureField-specific styling
        style: Optional[Union[TextFieldStyle, str]] = None,
        disabled: bool = False,
        # View modifiers passed through
        **kwargs: Any,
    ):
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
        """Get the current text value."""
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        """Set the text value and trigger UI update."""
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
