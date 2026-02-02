"""Form container for grouping data entry controls.

Form provides a container for grouping controls used for data entry,
such as toggles, pickers, text fields, and other input controls.
On macOS, it typically displays as a two-column layout with labels
on the left and controls on the right. This mirrors SwiftUI's Form view.

Example:
    Basic form with controls::

        import nib

        nib.Form(
            controls=[
                nib.Toggle("Enable notifications", is_on=True),
                nib.Picker("Language", options=["English", "Spanish"]),
                nib.TextField(value="", placeholder="Username"),
            ],
        )

    Form with grouped style::

        nib.Form(
            controls=[
                nib.Section(
                    controls=[
                        nib.Toggle("Dark Mode", is_on=False),
                    ],
                    header="Appearance",
                ),
                nib.Section(
                    controls=[
                        nib.Toggle("Notifications", is_on=True),
                    ],
                    header="Notifications",
                ),
            ],
            style=nib.FormStyle.GROUPED,
        )
"""

from typing import Any, List as ListType, Optional, Union
from ..base import View
from ...types import FormStyle, resolve_enum


class Form(View):
    """A container for grouping data entry controls.

    Form is designed for collecting user input through various controls
    like toggles, pickers, text fields, and sliders. On macOS, it typically
    renders as a two-column layout with labels on the left and controls
    on the right, providing a clean and consistent appearance for settings
    and preferences interfaces.

    Form supports different styles:
    - COLUMNS (default on macOS): Two-column layout
    - GROUPED: Grouped sections with visual separation

    Attributes:
        _type: The view type identifier ("Form").
        _children: List of child views contained in the form.
        _style: The form style (columns, grouped, or automatic).

    Example:
        Settings form::

            nib.Form(
                controls=[
                    nib.Toggle("Auto-save", is_on=True),
                    nib.Picker(
                        "Theme",
                        selection="dark",
                        options=["light", "dark", "system"],
                    ),
                    nib.Slider(
                        "Volume",
                        value=0.8,
                        min_value=0,
                        max_value=1,
                    ),
                ],
                style=nib.FormStyle.COLUMNS,
            )

        Form with sections::

            nib.Form(
                controls=[
                    nib.Section(
                        controls=[
                            nib.TextField(value="", placeholder="Name"),
                            nib.TextField(value="", placeholder="Email"),
                        ],
                        header="Account",
                    ),
                    nib.Section(
                        controls=[
                            nib.Toggle("Push notifications", is_on=True),
                            nib.Toggle("Email notifications", is_on=False),
                        ],
                        header="Notifications",
                        footer="Choose how you want to be notified.",
                    ),
                ],
                style=nib.FormStyle.GROUPED,
            )
    """

    _type = "Form"

    def __init__(
        self,
        controls: ListType[View] = None,
        # Alias for backwards compatibility
        children: ListType[View] = None,
        style: Optional[Union[FormStyle, str]] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a Form container.

        Args:
            controls: List of child views to display within the form.
                Typically includes controls like Toggle, Picker, TextField,
                Slider, and Section for grouping. This is the preferred
                parameter name.
            children: Alias for controls, provided for backwards compatibility.
                If both are provided, controls takes precedence.
            style: The visual style for the form. Use FormStyle enum values:
                - FormStyle.AUTOMATIC: Platform default
                - FormStyle.COLUMNS: Two-column layout (default on macOS)
                - FormStyle.GROUPED: Grouped sections with visual separation
            **kwargs: Additional view modifiers passed to the base View class.
                Supports all standard modifiers including padding, background,
                foreground_color, opacity, width, height, etc.

        Example:
            Creating a preferences form::

                prefs_form = nib.Form(
                    controls=[
                        nib.Toggle("Launch at login", is_on=False),
                        nib.Toggle("Check for updates", is_on=True),
                        nib.Picker(
                            "Update frequency",
                            selection="weekly",
                            options=["daily", "weekly", "monthly"],
                        ),
                    ],
                    style=nib.FormStyle.COLUMNS,
                    padding=16,
                )
        """
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])
        self._style = style

    def _get_props(self) -> dict:
        """Get the Form-specific properties for serialization.

        Returns:
            A dictionary containing the form style if set.
            Empty values are omitted.
        """
        props = {}
        if self._style is not None:
            props["formStyle"] = resolve_enum(self._style)
        return props

    def _get_children(self, parent_path: str, depth: int = 0) -> ListType[dict]:
        """Convert child views to their dictionary representations.

        Args:
            parent_path: The path identifier of this Form in the view tree,
                used to generate unique paths for child views.
            depth: Current depth in the view tree (for stack overflow protection).

        Returns:
            A list of dictionaries, each representing a serialized child view
            with its assigned path in the view hierarchy.
        """
        visible = [c for c in self._children if c._visible]
        return [child.to_dict(f"{parent_path}.{i}", depth + 1) for i, child in enumerate(visible)]
