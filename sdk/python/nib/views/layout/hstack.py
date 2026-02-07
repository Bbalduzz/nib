"""Horizontal stack layout container.

HStack arranges its child views in a horizontal line from leading to trailing
(left to right in left-to-right locales), with optional spacing between
children and vertical alignment control. This is one of the primary layout
containers in Nib, inspired by SwiftUI's HStack.

Example:
    Basic horizontal stack::

        import nib

        nib.HStack(
            controls=[
                nib.Image(system_name="star"),
                nib.Text("Favorites"),
            ],
            spacing=8,
        )

    With alignment and styling::

        nib.HStack(
            controls=[
                nib.Image(system_name="person.fill"),
                nib.VStack(
                    controls=[
                        nib.Text("Username", font=nib.Font.headline),
                        nib.Text("Status", foreground_color=nib.Color.secondary),
                    ],
                    alignment=nib.HorizontalAlignment.leading,
                ),
            ],
            spacing=12,
            alignment=nib.VerticalAlignment.center,
            padding=16,
        )
"""

import warnings
from typing import Any, List, Optional, Union
from ..base import View
from ...types import VerticalAlignment, resolve_enum


class HStack(View):
    """A horizontal stack layout that arranges children from leading to trailing.

    HStack is a fundamental layout container that positions its child views
    in a horizontal row. Children are rendered in order from leading to trailing
    (left to right in left-to-right locales), with optional spacing between
    them and configurable vertical alignment.

    Attributes:
        _type: The view type identifier ("HStack").
        _children: List of child views to arrange horizontally.
        _spacing: Optional spacing in points between child views.
        _alignment: Vertical alignment of children within the stack.

    Example:
        Simple horizontal arrangement::

            nib.HStack(
                controls=[
                    nib.Text("Label:"),
                    nib.TextField(value="", placeholder="Enter text"),
                ],
                spacing=8,
            )

        Icon with label::

            nib.HStack(
                controls=[
                    nib.Image(system_name="checkmark.circle.fill"),
                    nib.Text("Complete"),
                ],
                spacing=4,
                alignment=nib.VerticalAlignment.center,
                padding=8,
                background=nib.Color.green.opacity(0.2),
            )
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
        """Initialize an HStack layout container.

        Args:
            controls: List of child views to arrange horizontally. This is the
                preferred parameter name.
            children: Alias for controls, provided for backwards compatibility.
                If both are provided, controls takes precedence.
            spacing: The distance in points between adjacent child views.
                If None, uses the system default spacing.
            alignment: Vertical alignment of children within the stack.
                Can be a VerticalAlignment enum value or a string
                ("top", "center", "bottom", "firstTextBaseline",
                "lastTextBaseline"). Defaults to center if None.
            **kwargs: Additional view modifiers passed to the base View class.
                Supports all standard modifiers including padding, background,
                foreground_color, opacity, width, height, etc.

        Example:
            Creating a toolbar-style horizontal layout::

                toolbar = nib.HStack(
                    controls=[
                        nib.Button("Back", action=go_back),
                        nib.Spacer(),
                        nib.Text("Title", font=nib.Font.headline),
                        nib.Spacer(),
                        nib.Button("Done", action=finish),
                    ],
                    spacing=8,
                    padding={"horizontal": 16, "vertical": 8},
                )
        """
        if children is not None and controls is None:
            warnings.warn(
                "'children' is deprecated, use 'controls'",
                DeprecationWarning,
                stacklevel=2,
            )
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])
        self._spacing = spacing
        self._alignment = resolve_enum(alignment)

    @property
    def controls(self) -> List[View]:
        """Get the child views."""
        return self._children

    @controls.setter
    def controls(self, value: List[View]) -> None:
        """Set the child views and trigger UI update."""
        self._children = value
        self._trigger_update()

    def _get_props(self) -> dict:
        """Get the HStack-specific properties for serialization.

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

    def _get_children(self, parent_path: str, depth: int = 0) -> List[dict]:
        """Convert child views to their dictionary representations.

        Args:
            parent_path: The path identifier of this HStack in the view tree,
                used to generate unique paths for child views.
            depth: Current depth in the view tree (for stack overflow protection).

        Returns:
            A list of dictionaries, each representing a serialized child view
            with its assigned path in the view hierarchy.
        """
        visible = [c for c in self._children if c._visible]
        return [child.to_dict(f"{parent_path}.{i}", depth + 1) for i, child in enumerate(visible)]
