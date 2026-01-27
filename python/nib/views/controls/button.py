"""Button control for triggering actions with optional icons and custom content.

The Button view creates an interactive control that triggers a callback function
when tapped. Buttons can display text labels, SF Symbols icons, or completely
custom content views.

Example:
    Simple text button::

        nib.Button("Click Me", action=handle_click)

    Button with icon::

        nib.Button(
            "Settings",
            icon="gear",
            action=open_settings,
        )

    Styled button::

        nib.Button(
            "Submit",
            action=submit_form,
            style=nib.ButtonStyle.borderedProminent,
            tint=nib.Color.blue,
        )
"""

from typing import Any, Callable, List, Optional, Union
from ..base import View
from ...types import (
    ButtonRole,
    ButtonStyle,
    BorderShape,
    ControlSize,
    LabelStyle,
    ColorLike,
    resolve_color,
    resolve_enum,
)


class Button(View):
    """A control that initiates an action when tapped.

    Button is the primary interactive control for triggering actions. It supports
    text labels, SF Symbol icons, or fully custom content views. Various styles
    and roles can be applied to match the button's purpose (e.g., destructive
    actions use a red tint).

    Attributes:
        _label: The text label displayed on the button.
        _icon: The SF Symbol name for the button icon.
        _action: The callback function triggered on tap.
        _content: Custom view content (alternative to label/icon).

    Example:
        Text button with action::

            nib.Button("Save", action=save_document)

        Button with icon and label::

            nib.Button(
                "Delete",
                icon="trash",
                action=delete_item,
                role=nib.ButtonRole.destructive,
            )

        Styled prominent button::

            nib.Button(
                "Continue",
                action=proceed,
                style=nib.ButtonStyle.borderedProminent,
                control_size=nib.ControlSize.large,
            )

        Button with custom content::

            nib.Button(
                content=nib.HStack(controls=[
                    nib.Image(system_name="star.fill"),
                    nib.Text("Favorite"),
                ]),
                action=toggle_favorite,
            )
    """

    _type = "Button"

    def __init__(
        self,
        label: Optional[str] = None,
        icon: Optional[str] = None,
        action: Optional[Callable] = None,
        content: Optional["View"] = None,
        # Button-specific styling
        style: Optional[Union[ButtonStyle, str]] = None,
        role: Optional[Union[ButtonRole, str]] = None,
        border_shape: Optional[Union[BorderShape, str]] = None,
        control_size: Optional[Union[ControlSize, str]] = None,
        label_style: Optional[Union[LabelStyle, str]] = None,
        tint: Optional[ColorLike] = None,
        disabled: bool = False,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a Button view.

        Args:
            label: Text to display on the button. Use this for simple text buttons.
            icon: SF Symbol name to display (e.g., "gear", "trash", "star.fill").
                Can be combined with label or used alone.
            action: Callback function to execute when the button is tapped.
                Should be a callable with no required arguments.
            content: Custom View to use as button content. This is an alternative
                to using label/icon and provides full control over button appearance.
            style: Visual style of the button. Options include:
                - ButtonStyle.automatic: System default
                - ButtonStyle.bordered: Bordered style
                - ButtonStyle.borderedProminent: Prominent bordered style
                - ButtonStyle.borderless: No border
                - ButtonStyle.plain: Plain text style
            role: Semantic role affecting button appearance. Options:
                - ButtonRole.destructive: Red tint for destructive actions
                - ButtonRole.cancel: Cancel button styling
            border_shape: Shape of the button border. Options:
                - BorderShape.automatic: System default
                - BorderShape.capsule: Pill-shaped
                - BorderShape.roundedRectangle: Rounded corners
            control_size: Size of the control. Options:
                - ControlSize.mini, ControlSize.small
                - ControlSize.regular, ControlSize.large
            label_style: Style for the label content. Options include:
                - LabelStyle.automatic, LabelStyle.titleOnly
                - LabelStyle.iconOnly, LabelStyle.titleAndIcon
            tint: Tint color for the button (Color enum, hex string, or tuple).
            disabled: Whether the button is disabled and non-interactive.
            **kwargs: Standard view modifiers including padding, background,
                foreground_color, opacity, corner_radius, etc.

        Example:
            Create a destructive delete button::

                nib.Button(
                    "Delete",
                    icon="trash",
                    action=delete_item,
                    role=nib.ButtonRole.destructive,
                    style=nib.ButtonStyle.bordered,
                )
        """
        # Initialize base View with modifiers
        super().__init__(**kwargs)

        self._label = label
        self._icon = icon
        self._action = action
        self._content = content

        # Build button-specific styles
        self._button_styles: dict = {}

        if style is not None:
            self._button_styles["style"] = resolve_enum(style)
        if role is not None:
            self._button_styles["role"] = resolve_enum(role)
        if border_shape is not None:
            self._button_styles["borderShape"] = resolve_enum(border_shape)
        if control_size is not None:
            self._button_styles["controlSize"] = resolve_enum(control_size)
        if label_style is not None:
            self._button_styles["labelStyle"] = resolve_enum(label_style)
        if tint is not None:
            self._button_styles["tint"] = resolve_color(tint)
        if disabled:
            self._button_styles["disabled"] = True

    def _get_props(self) -> dict:
        props = {}
        if self._label:
            props["label"] = self._label
        if self._icon:
            props["icon"] = self._icon
        if self._button_styles:
            props["buttonStyles"] = self._button_styles
        return props

    def _get_children(self, parent_path: str) -> Optional[List[dict]]:
        """Return custom content as children if provided."""
        if self._content:
            return [self._content.to_dict(f"{parent_path}.0")]
        return None
