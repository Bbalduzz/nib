"""Spacer - Flexible space."""

from typing import Any, Optional

from ..base import View


class Spacer(View):
    """Flexible spacer."""

    _type = "Spacer"

    def __init__(
        self,
        min_length: Optional[float] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._min_length = min_length

    def _get_props(self) -> dict:
        props = {}
        if self._min_length is not None:
            props["minLength"] = float(self._min_length)
        return props
