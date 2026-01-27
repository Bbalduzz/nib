"""Transparent container for grouping views.

Group provides a transparent container that groups multiple views together
without adding any visual structure or layout behavior. It is useful for
applying modifiers to multiple views simultaneously or for returning
multiple views from conditional logic while maintaining a single parent.

Example:
    Grouping views for shared modifiers::

        import nib

        nib.Group(
            controls=[
                nib.Text("Line 1"),
                nib.Text("Line 2"),
            ],
            opacity=0.5,
        )

    Conditional view groups::

        def get_content(show_details):
            if show_details:
                return nib.Group(
                    controls=[
                        nib.Text("Title"),
                        nib.Text("Subtitle"),
                        nib.Text("Description"),
                    ],
                )
            else:
                return nib.Text("Title only")
"""

from typing import Any, List as ListType
from ..base import View


class Group(View):
    """A transparent container that groups views without visual structure.

    Group is a utility container that combines multiple views into a single
    unit without affecting their visual appearance or layout. Unlike VStack,
    HStack, or other layout containers, Group does not impose any positioning
    or spacing on its children.

    Common use cases include:
    - Applying modifiers to multiple views at once
    - Returning multiple views from conditional expressions
    - Working around single-child limitations in certain contexts
    - Organizing code without affecting visual output

    Attributes:
        _type: The view type identifier ("Group").
        _children: List of child views contained in the group.

    Example:
        Applying shared opacity::

            nib.Group(
                controls=[
                    nib.Image(system_name="star"),
                    nib.Text("Favorite"),
                ],
                opacity=0.7,
            )

        Conditional content::

            if is_premium:
                content = nib.Group(
                    controls=[
                        nib.Text("Premium Features"),
                        nib.Button("Feature 1", action=feature1),
                        nib.Button("Feature 2", action=feature2),
                    ],
                )
            else:
                content = nib.Text("Upgrade to Premium")
    """

    _type = "Group"

    def __init__(
        self,
        controls: ListType[View] = None,
        # Alias for backwards compatibility
        children: ListType[View] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a Group container.

        Args:
            controls: List of child views to group together. The views are
                rendered without any additional layout structure imposed by
                the group itself. This is the preferred parameter name.
            children: Alias for controls, provided for backwards compatibility.
                If both are provided, controls takes precedence.
            **kwargs: Additional view modifiers passed to the base View class.
                These modifiers are applied to the group as a whole, affecting
                all children. Supports all standard modifiers including padding,
                background, foreground_color, opacity, etc.

        Example:
            Creating a group with shared styling::

                styled_group = nib.Group(
                    controls=[
                        nib.Text("Important"),
                        nib.Text("Information"),
                    ],
                    foreground_color=nib.Color.red,
                    font=nib.Font.bold,
                )
        """
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])

    def _get_props(self) -> dict:
        """Get the Group-specific properties for serialization.

        Returns:
            An empty dictionary as Group has no additional properties.
        """
        return {}

    def _get_children(self, parent_path: str) -> ListType[dict]:
        """Convert child views to their dictionary representations.

        Args:
            parent_path: The path identifier of this Group in the view tree,
                used to generate unique paths for child views.

        Returns:
            A list of dictionaries, each representing a serialized child view
            with its assigned path in the view hierarchy.
        """
        return [child.to_dict(f"{parent_path}.{i}") for i, child in enumerate(self._children)]
