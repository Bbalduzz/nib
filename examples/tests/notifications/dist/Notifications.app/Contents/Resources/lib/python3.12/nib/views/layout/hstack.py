"""HStack - Horizontal stack layout with declarative parameter-based API."""

from typing import Any, List, Optional, Union
from ..base import View
from ...types import VerticalAlignment, resolve_enum


class HStack(View):
    """
    Horizontal stack layout.

        HStack(
            controls=[Image(system_name="star"), Text("Favorites")],
            spacing=8,
            alignment=VerticalAlignment.center,
            padding=12,
        )

    Supports all View modifiers (padding, background, overlay, etc.) via **kwargs.
    """

    _type = "HStack"

    def __init__(
        self,
        controls: List[View] = None,
        # Alias for backwards compatibility
        children: List[View] = None,
        spacing: Optional[float] = None,
        alignment: Optional[Union[VerticalAlignment, str]] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])
        self._spacing = spacing
        self._alignment = resolve_enum(alignment)

    def _get_props(self) -> dict:
        props = {}
        if self._spacing is not None:
            props["spacing"] = float(self._spacing)
        if self._alignment is not None:
            props["alignment"] = self._alignment
        return props

    def _get_children(self, parent_path: str) -> List[dict]:
        return [child.to_dict(f"{parent_path}.{i}") for i, child in enumerate(self._children)]
