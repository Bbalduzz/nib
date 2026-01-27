"""Divider - Visual separator line with declarative parameter-based API."""

from typing import Any
from ..base import View


class Divider(View):
    """
    A visual element used to separate content.

        Divider()

        Divider(foreground_color=Color.gray, padding=8)
    """

    _type = "Divider"

    def __init__(
        self,
        # View modifiers passed through
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
