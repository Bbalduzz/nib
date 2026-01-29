"""Vertical stack layout container.

VStack arranges its child views in a vertical line from top to bottom,
with optional spacing between children and horizontal alignment control.
This is one of the primary layout containers in Nib, inspired by SwiftUI's
VStack.

Example:
    Basic vertical stack::

        import nib

        nib.VStack(
            controls=[
                nib.Text("First"),
                nib.Text("Second"),
            ],
            spacing=8,
        )

    With alignment and styling::

        nib.VStack(
            controls=[
                nib.Text("Title", font=nib.Font.title),
                nib.Text("Subtitle", foreground_color=nib.Color.secondary),
            ],
            spacing=8,
            alignment=nib.HorizontalAlignment.leading,
            padding=16,
            background=nib.Color.gray,
        )
"""

from typing import Any, List, Optional, Union
from ..base import View
from ...types import HorizontalAlignment, resolve_enum


class VStack(View):
    """A vertical stack layout that arranges children from top to bottom.

    VStack is a fundamental layout container that positions its child views
    in a vertical column. Children are rendered in order from top to bottom,
    with optional spacing between them and configurable horizontal alignment.

    Attributes:
        _type: The view type identifier ("VStack").
        _children: List of child views to arrange vertically.
        _spacing: Optional spacing in points between child views.
        _alignment: Horizontal alignment of children within the stack.

    Example:
        Simple vertical arrangement::

            nib.VStack(
                controls=[
                    nib.Text("Line 1"),
                    nib.Text("Line 2"),
                    nib.Text("Line 3"),
                ],
                spacing=4,
            )

        Left-aligned with custom styling::

            nib.VStack(
                controls=[
                    nib.Text("Header", font=nib.Font.title),
                    nib.Text("Description"),
                    nib.Button("Action", action=my_callback),
                ],
                alignment=nib.HorizontalAlignment.leading,
                spacing=12,
                padding=16,
                background=nib.RoundedRectangle(
                    corner_radius=8,
                    fill="#333333",
                ),
            )
    """

    _type = "VStack"

    def __init__(
        self,
        controls: List[View] = None,
        # Alias for backwards compatibility
        children: List[View] = None,
        spacing: Optional[float] = None,
        alignment: Optional[Union[HorizontalAlignment, str]] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a VStack layout container.

        Args:
            controls: List of child views to arrange vertically. This is the
                preferred parameter name.
            children: Alias for controls, provided for backwards compatibility.
                If both are provided, controls takes precedence.
            spacing: The distance in points between adjacent child views.
                If None, uses the system default spacing.
            alignment: Horizontal alignment of children within the stack.
                Can be a HorizontalAlignment enum value or a string
                ("leading", "center", "trailing"). Defaults to center if None.
            **kwargs: Additional view modifiers passed to the base View class.
                Supports all standard modifiers including padding, background,
                foreground_color, opacity, width, height, etc.

        Example:
            Creating a centered vertical stack::

                stack = nib.VStack(
                    controls=[nib.Text("Hello"), nib.Text("World")],
                    spacing=8,
                    alignment=nib.HorizontalAlignment.center,
                    padding=16,
                )
        """
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])
        self._spacing = spacing
        self._alignment = resolve_enum(alignment)

    def _get_props(self) -> dict:
        """Get the VStack-specific properties for serialization.

        Returns:
            A dictionary containing the spacing and alignment properties
            if they are set. Empty values are omitted.
        """
        props = {}
        if self._spacing is not None:
            props["spacing"] = float(self._spacing)
        if self._alignment is not None:
            props["alignment"] = self._alignment
        return props

    def _get_children(self, parent_path: str) -> List[dict]:
        """Convert child views to their dictionary representations.

        Args:
            parent_path: The path identifier of this VStack in the view tree,
                used to generate unique paths for child views.

        Returns:
            A list of dictionaries, each representing a serialized child view
            with its assigned path in the view hierarchy.
        """
        visible = [c for c in self._children if c._visible]
        return [child.to_dict(f"{parent_path}.{i}") for i, child in enumerate(visible)]
