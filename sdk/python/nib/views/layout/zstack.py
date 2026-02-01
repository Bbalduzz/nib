"""Layered stack layout container.

ZStack overlays its child views on top of each other along the z-axis,
with the first child at the back and subsequent children layered on top.
This enables creating complex layered compositions such as backgrounds,
overlays, badges, and other stacked visual elements.

Example:
    Basic layered stack::

        import nib

        nib.ZStack(
            controls=[
                nib.RoundedRectangle(corner_radius=10, fill=nib.Color.blue),
                nib.Text("Overlay", foreground_color=nib.Color.white),
            ],
            alignment=nib.Alignment.center,
        )

    Creating a badge overlay::

        nib.ZStack(
            controls=[
                nib.Image(system_name="bell.fill"),
                nib.Circle(fill=nib.Color.red, width=12, height=12),
            ],
            alignment=nib.Alignment.topTrailing,
        )
"""

from typing import Any, List, Optional, Union
from ..base import View
from ...types import Alignment, resolve_enum


class ZStack(View):
    """A layered stack layout that overlays children along the z-axis.

    ZStack positions its child views on top of each other, creating a
    layered composition. The first child in the controls list is rendered
    at the back (bottom layer), and each subsequent child is rendered
    on top of the previous ones. This is useful for creating backgrounds,
    overlays, badges, and complex layered UI elements.

    Unlike VStack and HStack which arrange children sequentially, ZStack
    allows children to occupy the same space, with alignment controlling
    how they are positioned relative to each other.

    Attributes:
        _type: The view type identifier ("ZStack").
        _children: List of child views to layer on top of each other.
        _alignment: Two-dimensional alignment of children within the stack.

    Example:
        Card with background::

            nib.ZStack(
                controls=[
                    nib.RoundedRectangle(corner_radius=12, fill="#1a1a1a"),
                    nib.VStack(
                        controls=[
                            nib.Text("Card Title", font=nib.Font.headline),
                            nib.Text("Card content goes here"),
                        ],
                        padding=16,
                    ),
                ],
            )

        Image with gradient overlay::

            nib.ZStack(
                controls=[
                    nib.Image(url="https://example.com/image.jpg"),
                    nib.Rectangle(fill=nib.Color.black.opacity(0.3)),
                    nib.Text("Caption", foreground_color=nib.Color.white),
                ],
                alignment=nib.Alignment.bottom,
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
        """Initialize a ZStack layout container.

        Args:
            controls: List of child views to layer on top of each other.
                Views are rendered in order, with the first view at the back
                and subsequent views layered on top. This is the preferred
                parameter name.
            children: Alias for controls, provided for backwards compatibility.
                If both are provided, controls takes precedence.
            alignment: Two-dimensional alignment of children within the stack.
                Can be an Alignment enum value or a string ("center", "top",
                "bottom", "leading", "trailing", "topLeading", "topTrailing",
                "bottomLeading", "bottomTrailing"). Defaults to center if None.
            **kwargs: Additional view modifiers passed to the base View class.
                Supports all standard modifiers including padding, background,
                foreground_color, opacity, width, height, etc.

        Example:
            Creating a notification badge::

                badge = nib.ZStack(
                    controls=[
                        nib.Image(system_name="envelope.fill"),
                        nib.Text("3", font=nib.Font.caption)
                            .background(nib.Circle(fill=nib.Color.red)),
                    ],
                    alignment=nib.Alignment.topTrailing,
                )
        """
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])
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
        """Get the ZStack-specific properties for serialization.

        Returns:
            A dictionary containing the alignment property if set.
            Empty values are omitted.
        """
        props = {}
        if self._alignment is not None:
            props["alignment"] = self._alignment
        return props

    def _get_children(self, parent_path: str) -> List[dict]:
        """Convert child views to their dictionary representations.

        Args:
            parent_path: The path identifier of this ZStack in the view tree,
                used to generate unique paths for child views.

        Returns:
            A list of dictionaries, each representing a serialized child view
            with its assigned path in the view hierarchy.
        """
        visible = [c for c in self._children if c._visible]
        return [child.to_dict(f"{parent_path}.{i}") for i, child in enumerate(visible)]
