"""Toggle control for switching between on/off states.

The Toggle view provides a binary switch control that allows users to turn
a setting on or off. It supports text labels, custom content views, and
various styling options.

Example:
    Basic toggle::

        nib.Toggle("Enable notifications", is_on=False, on_change=handle_toggle)

    Styled toggle::

        nib.Toggle(
            "Dark Mode",
            is_on=dark_mode_enabled,
            on_change=toggle_dark_mode,
            tint=nib.Color.green,
        )

    Toggle with custom content::

        nib.Toggle(
            content=nib.HStack(controls=[
                nib.Image(system_name="bell.fill"),
                nib.Text("Notifications"),
            ]),
            is_on=notifications_enabled,
            on_change=toggle_notifications,
        )
"""

from typing import Any, Callable, List, Optional, Union
from ..base import View
from ...types import (
    ColorLike,
    ToggleStyle,
    resolve_color,
    resolve_enum,
)


class Toggle(View):
    """A control for switching between on and off states.

    Toggle provides a binary switch that users can tap to toggle between
    two states. It can display a text label or custom content, and triggers
    a callback when the state changes.

    Attributes:
        _label: The text label displayed next to the toggle.
        _is_on: The current on/off state.
        _on_change: Callback function triggered when state changes.
        _content: Custom view content (alternative to label).

    Example:
        Simple toggle with label::

            nib.Toggle(
                "Enable Feature",
                is_on=False,
                on_change=lambda is_on: print(f"Toggled: {is_on}"),
            )

        Toggle with custom tint color::

            nib.Toggle(
                "Airplane Mode",
                is_on=airplane_mode,
                on_change=set_airplane_mode,
                tint=nib.Color.orange,
            )

        Toggle with checkbox style::

            nib.Toggle(
                "I agree to terms",
                is_on=agreed,
                on_change=set_agreed,
                style=nib.ToggleStyle.checkbox,
            )

        Toggle with custom content view::

            nib.Toggle(
                content=nib.Label("Wi-Fi", icon="wifi"),
                is_on=wifi_enabled,
                on_change=toggle_wifi,
            )
    """

    _type = "Toggle"

    def __init__(
        self,
        label: Optional[str] = None,
        is_on: bool = False,
        on_change: Optional[Callable[[bool], None]] = None,
        content: Optional[View] = None,
        # Toggle-specific styling
        style: Optional[Union[ToggleStyle, str]] = None,
        tint: Optional[ColorLike] = None,
        disabled: bool = False,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a Toggle view.

        Args:
            label: Text to display next to the toggle switch. Use this for
                simple text labels.
            is_on: Initial on/off state. True for on, False for off.
            on_change: Callback function called when the toggle state changes.
                Receives a boolean argument indicating the new state.
            content: Custom View to display as the toggle label. This is an
                alternative to the label parameter and provides full control
                over the label appearance.
            style: Visual style of the toggle. Options:
                - ToggleStyle.automatic: System default (usually switch)
                - ToggleStyle.switch: Standard switch style
                - ToggleStyle.checkbox: Checkbox style
                - ToggleStyle.button: Button style
            tint: Tint color for the toggle when in the "on" state.
                Accepts Color enum, hex string, or RGB tuple.
            disabled: Whether the toggle is disabled and non-interactive.
            **kwargs: Standard view modifiers including padding, background,
                foreground_color, opacity, etc.

        Example:
            Create a settings toggle::

                nib.Toggle(
                    "Enable Notifications",
                    is_on=notifications_enabled,
                    on_change=lambda on: update_setting("notifications", on),
                    style=nib.ToggleStyle.switch,
                    tint=nib.Color.blue,
                )
        """
        super().__init__(**kwargs)
        self._label = label or ""
        self._is_on = is_on
        self._on_change = on_change
        self._content = content

        # Build toggle-specific styles
        self._toggle_styles: dict = {}
        if style is not None:
            self._toggle_styles["style"] = resolve_enum(style)
        if tint is not None:
            self._toggle_styles["tint"] = resolve_color(tint)
        if disabled:
            self._toggle_styles["disabled"] = True

    def _get_props(self) -> dict:
        props = {
            "isOn": self._is_on,
        }
        if self._label:
            props["label"] = self._label
        if self._toggle_styles:
            props["toggleStyles"] = self._toggle_styles
        return props

    def _get_children(self, parent_path: str) -> Optional[List[dict]]:
        """Return custom content as children if provided."""
        if self._content:
            return [self._content.to_dict(f"{parent_path}.0")]
        return None
