"""Scrollable container view.

ScrollView provides a scrollable region that can contain content larger than
its visible bounds. It supports vertical, horizontal, or bidirectional scrolling
with optional scroll indicators. This is essential for displaying lists, forms,
or any content that may exceed the available screen space.

Example:
    Basic vertical scroll view::

        import nib

        nib.ScrollView(
            controls=[
                nib.Text("Item 1"),
                nib.Text("Item 2"),
                nib.Text("Item 3"),
                # ... many more items
            ],
        )

    Horizontal scrolling gallery::

        nib.ScrollView(
            controls=[
                nib.HStack(
                    controls=[
                        nib.Image(url=url) for url in image_urls
                    ],
                    spacing=8,
                ),
            ],
            axes="horizontal",
            shows_indicators=False,
        )
"""

from typing import Any, List as ListType, Literal
from ..base import View


class ScrollView(View):
    """A scrollable container that allows content to exceed visible bounds.

    ScrollView wraps its child content in a scrollable region, enabling users
    to pan through content that is larger than the visible area. It supports
    vertical scrolling (default), horizontal scrolling, or scrolling in both
    directions simultaneously.

    The scroll view automatically determines the content size based on its
    children and enables scrolling when the content exceeds the available
    space.

    Attributes:
        _type: The view type identifier ("ScrollView").
        _children: List of child views contained in the scroll view.
        _axes: The scroll direction ("vertical", "horizontal", or "both").
        _shows_indicators: Whether to display scroll indicators.

    Example:
        Scrollable list of items::

            nib.ScrollView(
                controls=[
                    nib.VStack(
                        controls=[nib.Text(f"Item {i}") for i in range(100)],
                        spacing=4,
                    ),
                ],
                height=300,
            )

        Bidirectional scrolling for large content::

            nib.ScrollView(
                controls=[
                    nib.Image(url="large_image.png"),
                ],
                axes="both",
                shows_indicators=True,
            )
    """

    _type = "ScrollView"

    def __init__(
        self,
        controls: ListType[View] = None,
        # Alias for backwards compatibility
        children: ListType[View] = None,
        axes: Literal["vertical", "horizontal", "both"] = "vertical",
        shows_indicators: bool = True,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a ScrollView container.

        Args:
            controls: List of child views to display in the scroll view.
                The content size is determined by the combined size of all
                children. This is the preferred parameter name.
            children: Alias for controls, provided for backwards compatibility.
                If both are provided, controls takes precedence.
            axes: The scroll direction. Can be "vertical" (default) for
                up/down scrolling, "horizontal" for left/right scrolling,
                or "both" for bidirectional scrolling.
            shows_indicators: Whether to show scroll indicators (scrollbars).
                Defaults to True. Set to False for a cleaner appearance
                when scroll indicators are not needed.
            **kwargs: Additional view modifiers passed to the base View class.
                Supports all standard modifiers including padding, background,
                foreground_color, opacity, width, height, etc.

        Example:
            Creating a scrollable form::

                form = nib.ScrollView(
                    controls=[
                        nib.VStack(
                            controls=[
                                nib.TextField(value="", placeholder="Name"),
                                nib.TextField(value="", placeholder="Email"),
                                nib.TextField(value="", placeholder="Message"),
                                nib.Button("Submit", action=submit_form),
                            ],
                            spacing=12,
                            padding=16,
                        ),
                    ],
                    axes="vertical",
                    shows_indicators=True,
                    height=400,
                )
        """
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])
        self._axes = axes
        self._shows_indicators = shows_indicators

    @property
    def controls(self) -> ListType[View]:
        """Get the child views."""
        return self._children

    @controls.setter
    def controls(self, value: ListType[View]) -> None:
        """Set the child views and trigger UI update."""
        self._children = value
        self._trigger_update()

    def _get_props(self) -> dict:
        """Get the ScrollView-specific properties for serialization.

        Returns:
            A dictionary containing the axes and showsIndicators properties.
        """
        return {
            "axes": self._axes,
            "showsIndicators": self._shows_indicators,
        }

    def _get_children(self, parent_path: str, depth: int = 0) -> ListType[dict]:
        """Convert child views to their dictionary representations.

        Args:
            parent_path: The path identifier of this ScrollView in the view tree,
                used to generate unique paths for child views.
            depth: Current depth in the view tree (for stack overflow protection).

        Returns:
            A list of dictionaries, each representing a serialized child view
            with its assigned path in the view hierarchy.
        """
        visible = [c for c in self._children if c._visible]
        return [child.to_dict(f"{parent_path}.{i}", depth + 1) for i, child in enumerate(visible)]
