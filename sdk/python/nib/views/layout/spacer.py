"""Flexible spacer view.

Spacer provides flexible space that expands to fill available room within
a stack layout (HStack or VStack). It is commonly used to push other views
to the edges of their container or to create even spacing between elements.

Example:
    Push content to opposite edges::

        import nib

        nib.HStack(
            controls=[
                nib.Text("Left"),
                nib.Spacer(),
                nib.Text("Right"),
            ],
        )

    Create a toolbar with centered title::

        nib.HStack(
            controls=[
                nib.Button("Back", action=go_back),
                nib.Spacer(),
                nib.Text("Title", font=nib.Font.headline),
                nib.Spacer(),
                nib.Button("Done", action=finish),
            ],
        )
"""

from typing import Any, Optional

from ..base import View


class Spacer(View):
    """A flexible space that expands to fill available room in stack layouts.

    Spacer is a layout primitive that takes up as much space as available
    within its parent stack (HStack or VStack). When multiple spacers are
    present, they divide the available space equally. This makes Spacer
    essential for creating flexible layouts where elements need to be
    pushed apart or distributed evenly.

    In an HStack, Spacer expands horizontally. In a VStack, it expands
    vertically. The expansion is constrained by sibling views and the
    parent container's bounds.

    Attributes:
        _type: The view type identifier ("Spacer").
        _min_length: Optional minimum length in points that the spacer must
            occupy, even when space is limited.

    Example:
        Right-aligned content::

            nib.HStack(
                controls=[
                    nib.Spacer(),
                    nib.Button("Action", action=do_action),
                ],
            )

        Even distribution with minimum spacing::

            nib.HStack(
                controls=[
                    nib.Text("A"),
                    nib.Spacer(min_length=20),
                    nib.Text("B"),
                    nib.Spacer(min_length=20),
                    nib.Text("C"),
                ],
            )

        Bottom-aligned footer::

            nib.VStack(
                controls=[
                    nib.Text("Header"),
                    nib.Text("Content"),
                    nib.Spacer(),
                    nib.Text("Footer"),
                ],
                height=400,
            )
    """

    _type = "Spacer"

    def __init__(
        self,
        min_length: Optional[float] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a Spacer view.

        Args:
            min_length: Optional minimum length in points that the spacer
                must occupy. If provided, the spacer will not shrink below
                this size even when space is limited. Useful for ensuring
                minimum gaps between elements.
            **kwargs: Additional view modifiers passed to the base View class.
                While spacers typically don't need visual styling, modifiers
                like frame constraints can still be applied.

        Example:
            Creating a spacer with minimum size::

                spacer = nib.Spacer(min_length=16)

            Using spacer to push a button to the right::

                nib.HStack(
                    controls=[
                        nib.Text("Label"),
                        nib.Spacer(),
                        nib.Button("Action", action=callback),
                    ],
                )
        """
        super().__init__(**kwargs)
        self._min_length = min_length

    def _get_props(self) -> dict:
        """Get the Spacer-specific properties for serialization.

        Returns:
            A dictionary containing the minLength property if set.
            Empty values are omitted.
        """
        props = {}
        if self._min_length is not None:
            props["minLength"] = float(self._min_length)
        return props
