"""Picker control for selecting from a set of mutually exclusive options.

The Picker view provides a selection control that allows users to choose one
option from a predefined set. It supports various display styles including
dropdown menus, segmented controls, and wheels.

Example:
    Simple picker with string options::

        nib.Picker(
            "Color",
            selection="red",
            options=["Red", "Green", "Blue"],
            on_change=set_color,
        )

    Picker with value-label tuples::

        nib.Picker(
            "Size",
            selection="m",
            options=[("s", "Small"), ("m", "Medium"), ("l", "Large")],
            style=nib.PickerStyle.segmented,
        )

    Segmented control style::

        nib.Picker(
            "View Mode",
            selection=view_mode,
            options=["List", "Grid", "Gallery"],
            style=nib.PickerStyle.segmented,
        )
"""

from typing import Any, Callable, List, Optional, Tuple, Union
from ..base import View
from ...types import PickerStyle, resolve_enum


class Picker(View):
    """A control for selecting from a set of mutually exclusive values.

    Picker displays a list of options and allows the user to select one.
    Options can be simple strings (where the value equals the label) or
    tuples of (value, label) for separate internal values and display text.

    Attributes:
        _label: The picker's descriptive label.
        _selection: The currently selected value.
        _options: List of available options.
        _on_change: Callback function triggered when selection changes.

    Example:
        Color picker dropdown::

            nib.Picker(
                "Favorite Color",
                selection=current_color,
                options=["Red", "Green", "Blue", "Yellow"],
                on_change=set_favorite_color,
            )

        Size picker with separate values and labels::

            nib.Picker(
                "T-Shirt Size",
                selection="m",
                options=[
                    ("xs", "Extra Small"),
                    ("s", "Small"),
                    ("m", "Medium"),
                    ("l", "Large"),
                    ("xl", "Extra Large"),
                ],
                on_change=set_size,
            )

        Segmented control for view switching::

            nib.Picker(
                "",
                selection=view_mode,
                options=["Day", "Week", "Month"],
                style=nib.PickerStyle.segmented,
                on_change=switch_view,
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
        """Initialize a Picker view.

        Args:
            label: Descriptive label for the picker. Displayed above or beside
                the options depending on the style.
            selection: Currently selected option value. Must match one of the
                values in the options list.
            options: List of available options. Can be provided in two formats:
                - List of strings: ["Option 1", "Option 2", "Option 3"]
                  In this case, the string serves as both value and label.
                - List of (value, label) tuples: [("val1", "Label 1"), ("val2", "Label 2")]
                  Use this when you need separate internal values and display text.
            on_change: Callback function called when the selection changes.
                Receives the newly selected value as a string argument.
            style: Visual style of the picker. Options:
                - PickerStyle.automatic: System default (usually menu)
                - PickerStyle.menu: Dropdown menu style
                - PickerStyle.segmented: Horizontal segmented control
                - PickerStyle.wheel: Spinning wheel picker
                - PickerStyle.inline: Inline list of options
            disabled: Whether the picker is disabled and non-interactive.
            **kwargs: Standard view modifiers including padding, background,
                foreground_color, opacity, etc.

        Example:
            Create a priority picker::

                nib.Picker(
                    "Priority",
                    selection="medium",
                    options=[
                        ("low", "Low"),
                        ("medium", "Medium"),
                        ("high", "High"),
                        ("urgent", "Urgent"),
                    ],
                    on_change=set_priority,
                    style=nib.PickerStyle.menu,
                )
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
