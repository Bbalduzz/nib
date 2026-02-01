"""Divider view for visually separating content.

The Divider view creates a thin horizontal line used to visually separate
content within a layout. It automatically adapts to its container orientation.

Example:
    Basic divider::

        nib.Divider()

    Styled divider::

        nib.Divider(foreground_color=nib.Color.gray, padding=8)

    Divider in a VStack::

        nib.VStack(controls=[
            nib.Text("Section 1"),
            nib.Divider(),
            nib.Text("Section 2"),
        ])
"""

from typing import Any
from ..base import View


class Divider(View):
    """A visual element used to separate content sections.

    Divider creates a thin line that helps visually organize content by
    separating different sections. In a VStack, it appears as a horizontal
    line. In an HStack, it appears as a vertical line.

    The divider automatically sizes itself to fit its container while
    maintaining a minimal thickness.

    Example:
        Basic separator::

            nib.Divider()

        Colored divider::

            nib.Divider(foreground_color=nib.Color.gray)

        Divider with padding::

            nib.Divider(padding={"vertical": 10})

        Divider in a list layout::

            nib.VStack(controls=[
                nib.Text("Item 1"),
                nib.Divider(foreground_color="#E0E0E0"),
                nib.Text("Item 2"),
                nib.Divider(foreground_color="#E0E0E0"),
                nib.Text("Item 3"),
            ], spacing=8)
    """

    _type = "Divider"

    def __init__(
        self,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a Divider view.

        Args:
            **kwargs: Standard view modifiers. Common options include:
                - foreground_color: Color of the divider line
                - padding: Space around the divider
                - opacity: Transparency of the divider (0.0 to 1.0)

        Example:
            Create a subtle section divider::

                nib.Divider(
                    foreground_color=nib.Color.gray,
                    opacity=0.5,
                    padding={"vertical": 8},
                )
        """
        super().__init__(**kwargs)
