"""List view container for displaying rows of data.

List provides a container that displays rows of data arranged in a single
scrollable column. It is optimized for displaying collections of similar items
and supports grouping content into sections with headers and footers. This
mirrors SwiftUI's List view behavior.

Example:
    Basic list of items::

        import nib

        nib.List(
            controls=[
                nib.Text("Item 1"),
                nib.Text("Item 2"),
                nib.Text("Item 3"),
            ],
        )

    List with sections::

        nib.List(
            controls=[
                nib.Section(
                    controls=[nib.Text("Apple"), nib.Text("Banana")],
                    header="Fruits",
                ),
                nib.Section(
                    controls=[nib.Text("Carrot"), nib.Text("Broccoli")],
                    header="Vegetables",
                ),
            ],
        )
"""

from typing import Any, List as ListType
from ..base import View


class List(View):
    """A container that displays rows of data in a single scrollable column.

    List is a specialized container optimized for displaying collections of
    items in a vertically scrolling column. It provides native list styling
    and behavior, including proper row separators and section support.

    Unlike a simple VStack, List is optimized for displaying many items
    efficiently and provides a more native appearance for list-based
    interfaces like settings screens, menus, and data tables.

    Attributes:
        _type: The view type identifier ("List").
        _children: List of child views (rows or sections) to display.

    Example:
        Simple item list::

            nib.List(
                controls=[
                    nib.Text("First item"),
                    nib.Text("Second item"),
                    nib.Text("Third item"),
                ],
            )

        Settings-style list with sections::

            nib.List(
                controls=[
                    nib.Section(
                        controls=[
                            nib.Toggle("Notifications", is_on=True),
                            nib.Toggle("Sound", is_on=False),
                        ],
                        header="Preferences",
                        footer="Manage your notification settings",
                    ),
                    nib.Section(
                        controls=[
                            nib.NavigationLink("About", destination=[...]),
                            nib.NavigationLink("Help", destination=[...]),
                        ],
                        header="Information",
                    ),
                ],
            )
    """

    _type = "List"

    def __init__(
        self,
        controls: ListType[View] = None,
        # Alias for backwards compatibility
        children: ListType[View] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a List container.

        Args:
            controls: List of child views to display as rows. Can contain
                individual views (displayed as rows) or Section views for
                grouped content with headers and footers. This is the
                preferred parameter name.
            children: Alias for controls, provided for backwards compatibility.
                If both are provided, controls takes precedence.
            **kwargs: Additional view modifiers passed to the base View class.
                Supports all standard modifiers including padding, background,
                foreground_color, opacity, width, height, etc.

        Example:
            Creating a contact list::

                contact_list = nib.List(
                    controls=[
                        nib.HStack(
                            controls=[
                                nib.Image(system_name="person.circle"),
                                nib.Text(contact.name),
                            ],
                            spacing=8,
                        )
                        for contact in contacts
                    ],
                    height=400,
                )
        """
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])

    def _get_props(self) -> dict:
        """Get the List-specific properties for serialization.

        Returns:
            An empty dictionary as List has no additional properties.
        """
        return {}

    def _get_children(self, parent_path: str) -> ListType[dict]:
        """Convert child views to their dictionary representations.

        Args:
            parent_path: The path identifier of this List in the view tree,
                used to generate unique paths for child views.

        Returns:
            A list of dictionaries, each representing a serialized child view
            (row or section) with its assigned path in the view hierarchy.
        """
        return [child.to_dict(f"{parent_path}.{i}") for i, child in enumerate(self._children)]
