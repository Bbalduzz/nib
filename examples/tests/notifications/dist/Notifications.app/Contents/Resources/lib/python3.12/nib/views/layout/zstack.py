"""ZStack - Layered stack layout with declarative parameter-based API."""

from typing import Any, List, Optional, Union
from ..base import View
from ...types import Alignment, resolve_enum


class ZStack(View):
    """
    Layered stack layout (views overlap).

        ZStack(
            controls=[
                RoundedRectangle(corner_radius=10, fill=Color.blue),
                Text("Overlay", foreground_color=Color.white),
            ],
            alignment=Alignment.center,
        )
    """

    _type = "ZStack"

    def __init__(
        self,
        controls: List[View] = None,
        # Alias for backwards compatibility
        children: List[View] = None,
        alignment: Optional[Union[Alignment, str]] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])
        self._alignment = resolve_enum(alignment)

    def _get_props(self) -> dict:
        props = {}
        if self._alignment is not None:
            props["alignment"] = self._alignment
        return props

    def _get_children(self, parent_path: str) -> List[dict]:
        return [child.to_dict(f"{parent_path}.{i}") for i, child in enumerate(self._children)]
