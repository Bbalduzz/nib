"""Section container for grouping content with headers and footers.

Section provides a container for grouping related content together within a
List view. It supports optional header and footer text to provide context
and additional information for the grouped content. This mirrors SwiftUI's
Section view used within List.

Example:
    Basic section with header::

        import nib

        nib.Section(
            controls=[
                nib.Text("Item 1"),
                nib.Text("Item 2"),
            ],
            header="My Section",
        )

    Section with header and footer::

        nib.Section(
            controls=[
                nib.Toggle("Enable feature", is_on=True),
            ],
            header="Settings",
            footer="Enabling this feature will improve performance.",
        )
"""

from typing import Any, List as ListType, Optional
from ..base import View


class Section(View):
    """A container for grouping content with optional header and footer.

    Section is designed to be used within a List view to organize content
    into logical groups. Each section can have an optional header displayed
    above the content and an optional footer displayed below. This is
    commonly used for settings screens, forms, and categorized lists.

    The header typically describes the section's purpose, while the footer
    often provides additional context, explanations, or disclaimers about
    the section's content.

    Attributes:
        _type: The view type identifier ("Section").
        _children: List of child views contained in the section.
        _header: Optional header text displayed above the content.
        _footer: Optional footer text displayed below the content.

    Example:
        Settings section::

            nib.Section(
                controls=[
                    nib.Toggle("Dark Mode", is_on=False),
                    nib.Toggle("Auto-brightness", is_on=True),
                ],
                header="Display",
                footer="Adjust display settings for comfortable viewing.",
            )

        Form section::

            nib.Section(
                controls=[
                    nib.TextField(value="", placeholder="Username"),
                    nib.SecureField(value="", placeholder="Password"),
                ],
                header="Account",
            )
    """

    _type = "Section"

    def __init__(
        self,
        controls: ListType[View] = None,
        # Alias for backwards compatibility
        children: ListType[View] = None,
        header: Optional[str] = None,
        footer: Optional[str] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a Section container.

        Args:
            controls: List of child views to display within the section.
                These views are rendered between the header and footer.
                This is the preferred parameter name.
            children: Alias for controls, provided for backwards compatibility.
                If both are provided, controls takes precedence.
            header: Optional text to display above the section content.
                Typically used to label or categorize the section's content.
                Rendered in a secondary text style.
            footer: Optional text to display below the section content.
                Often used for explanatory text, disclaimers, or additional
                context about the section. Rendered in a smaller, secondary
                text style.
            **kwargs: Additional view modifiers passed to the base View class.
                Supports all standard modifiers including padding, background,
                foreground_color, opacity, width, height, etc.

        Example:
            Creating a privacy settings section::

                privacy_section = nib.Section(
                    controls=[
                        nib.Toggle("Location Services", is_on=True),
                        nib.Toggle("Analytics", is_on=False),
                        nib.Toggle("Personalized Ads", is_on=False),
                    ],
                    header="Privacy",
                    footer="These settings control how your data is used. "
                           "You can change them at any time.",
                )
        """
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])
        self._header = header
        self._footer = footer

    def _get_props(self) -> dict:
        """Get the Section-specific properties for serialization.

        Returns:
            A dictionary containing the header and footer properties
            if they are set. Empty values are omitted.
        """
        props = {}
        if self._header:
            props["header"] = self._header
        if self._footer:
            props["footer"] = self._footer
        return props

    def _get_children(self, parent_path: str) -> ListType[dict]:
        """Convert child views to their dictionary representations.

        Args:
            parent_path: The path identifier of this Section in the view tree,
                used to generate unique paths for child views.

        Returns:
            A list of dictionaries, each representing a serialized child view
            with its assigned path in the view hierarchy.
        """
        visible = [c for c in self._children if c._visible]
        return [child.to_dict(f"{parent_path}.{i}") for i, child in enumerate(visible)]
