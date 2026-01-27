"""Button - Interactive button control with declarative parameter-based API."""

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
    """
    A control that initiates an action.

    All styling is done via constructor parameters:

        Button(
            "Submit",
            action=submit,
            style=ButtonStyle.borderedProminent,
            tint=Color.blue,
        )

        Button(
            "Delete",
            icon="trash",
            action=delete,
            role=ButtonRole.destructive,
        )

        # Custom content
        Button(
            content=HStack([
                Image(system_name="star"),
                Text("Favorite"),
            ]),
            action=favorite,
            background=Color.yellow,
            corner_radius=10,
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
