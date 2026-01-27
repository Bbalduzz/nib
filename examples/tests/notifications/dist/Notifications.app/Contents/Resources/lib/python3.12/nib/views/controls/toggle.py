"""Toggle - A control for switching between on/off states with declarative parameter-based API."""

from typing import Any, Callable, List, Optional, Union
from ..base import View
from ...types import (
    ColorLike,
    ToggleStyle,
    resolve_color,
    resolve_enum,
)


class Toggle(View):
    """
    A control for switching between on and off states.

        Toggle("Enable notifications", is_on=enabled, on_change=toggle)

        Toggle(
            "Dark Mode",
            is_on=self.dark_mode,
            on_change=self.toggle_dark_mode,
            style=ToggleStyle.switch,
            tint=Color.green,
        )

        # Custom content
        Toggle(
            content=HStack([
                Image(system_name="bell.fill"),
                Text("Notifications"),
            ]),
            is_on=self.enabled,
            on_change=self.toggle,
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
