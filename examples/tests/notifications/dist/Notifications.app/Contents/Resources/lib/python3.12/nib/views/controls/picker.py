"""Picker - A control for selecting from a set of options with declarative parameter-based API."""

from typing import Any, Callable, List, Optional, Tuple, Union
from ..base import View
from ...types import PickerStyle, resolve_enum


class Picker(View):
    """
    A control for selecting from a set of mutually exclusive values.

        Picker(
            "Color",
            selection=color,
            options=["Red", "Green", "Blue"],
            on_change=set_color,
        )

        Picker(
            "Size",
            selection=size,
            options=[("s", "Small"), ("m", "Medium"), ("l", "Large")],
            style=PickerStyle.segmented,
        )
    """

    _type = "Picker"

    def __init__(
        self,
        label: str = "",
        selection: str = "",
        options: Optional[Union[List[str], List[Tuple[str, str]]]] = None,
        on_change: Optional[Callable[[str], None]] = None,
        # Picker-specific styling
        style: Optional[Union[PickerStyle, str]] = None,
        disabled: bool = False,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """
        Create a picker.

        Args:
            label: The picker's label
            selection: Currently selected value
            options: List of options. Can be:
                - List of strings: ["Option 1", "Option 2"]
                - List of (value, label) tuples: [("val1", "Label 1"), ("val2", "Label 2")]
            on_change: Callback when selection changes
            style: Picker display style (PickerStyle enum)
        """
        super().__init__(**kwargs)
        self._label = label
        self._selection = selection
        self._options = options or []
        self._on_change = on_change

        # Build picker-specific styles
        self._picker_styles: dict = {}
        if style is not None:
            self._picker_styles["style"] = resolve_enum(style)
        if disabled:
            self._picker_styles["disabled"] = True

    def _get_props(self) -> dict:
        # Normalize options to (value, label) format
        normalized_options = []
        for opt in self._options:
            if isinstance(opt, tuple):
                normalized_options.append({"value": opt[0], "label": opt[1]})
            else:
                normalized_options.append({"value": opt, "label": opt})

        props = {
            "label": self._label,
            "selection": self._selection,
            "options": normalized_options,
        }
        if self._picker_styles:
            props["pickerStyles"] = self._picker_styles
        return props
