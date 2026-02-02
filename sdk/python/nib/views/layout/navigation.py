"""Navigation views for hierarchical navigation and collapsible content.

This module provides navigation-related views for building hierarchical
navigation interfaces and collapsible content sections. It includes:

- NavigationStack: Container for navigation-based interfaces
- NavigationLink: Clickable link that navigates to a destination view
- DisclosureGroup: Collapsible section that shows/hides content

These views mirror SwiftUI's navigation patterns, enabling drill-down
navigation and expandable/collapsible UI sections.

Example:
    Basic navigation hierarchy::

        import nib

        nib.NavigationStack(
            controls=[
                nib.NavigationLink("Settings", destination=[
                    nib.VStack(
                        controls=[
                            nib.Text("Settings Page"),
                            nib.Toggle("Dark Mode", is_on=False),
                        ],
                    ),
                ]),
                nib.NavigationLink("About", destination=[
                    nib.Text("About this app"),
                ]),
            ],
        )

    Collapsible options::

        nib.DisclosureGroup("Advanced Options", controls=[
            nib.Toggle("Enable logging", is_on=False),
            nib.Toggle("Developer mode", is_on=False),
        ])
"""

from typing import Any, Callable, List as ListType, Optional
from ..base import View


class NavigationStack(View):
    """A container that manages a stack of views for hierarchical navigation.

    NavigationStack provides the foundation for navigation-based interfaces,
    managing a stack of views that users can navigate through. It works in
    conjunction with NavigationLink to create drill-down navigation patterns
    where tapping a link pushes a new view onto the navigation stack.

    The stack maintains navigation history, allowing users to return to
    previous views. The root content is always at the bottom of the stack,
    with destination views pushed on top as the user navigates.

    Attributes:
        _type: The view type identifier ("NavigationStack").
        _children: List of root content views displayed initially.

    Example:
        Settings navigation::

            nib.NavigationStack(
                controls=[
                    nib.List(
                        controls=[
                            nib.NavigationLink("Profile", destination=[
                                nib.ProfileView(),
                            ]),
                            nib.NavigationLink("Notifications", destination=[
                                nib.NotificationSettings(),
                            ]),
                            nib.NavigationLink("Privacy", destination=[
                                nib.PrivacySettings(),
                            ]),
                        ],
                    ),
                ],
            )

        Master-detail interface::

            nib.NavigationStack(
                controls=[
                    nib.List(
                        controls=[
                            nib.NavigationLink(item.name, destination=[
                                nib.ItemDetailView(item=item),
                            ])
                            for item in items
                        ],
                    ),
                ],
            )
    """

    _type = "NavigationStack"

    def __init__(
        self,
        controls: ListType[View] = None,
        # Alias for backwards compatibility
        children: ListType[View] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a NavigationStack container.

        Args:
            controls: List of root content views to display initially.
                These views form the base of the navigation stack and are
                shown when no navigation has occurred or when the user
                navigates back to the root. This is the preferred parameter name.
            children: Alias for controls, provided for backwards compatibility.
                If both are provided, controls takes precedence.
            **kwargs: Additional view modifiers passed to the base View class.
                Supports all standard modifiers including padding, background,
                foreground_color, opacity, width, height, etc.

        Example:
            Creating a navigation-based settings interface::

                settings_nav = nib.NavigationStack(
                    controls=[
                        nib.VStack(
                            controls=[
                                nib.NavigationLink("Account", destination=[...]),
                                nib.NavigationLink("Appearance", destination=[...]),
                                nib.NavigationLink("Help", destination=[...]),
                            ],
                            spacing=8,
                        ),
                    ],
                )
        """
        super().__init__(**kwargs)
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])

    def _get_props(self) -> dict:
        """Get the NavigationStack-specific properties for serialization.

        Returns:
            An empty dictionary as NavigationStack has no additional properties.
        """
        return {}

    def _get_children(self, parent_path: str, depth: int = 0) -> ListType[dict]:
        """Convert child views to their dictionary representations.

        Args:
            parent_path: The path identifier of this NavigationStack in the
                view tree, used to generate unique paths for child views.
            depth: Current depth in the view tree (for stack overflow protection).

        Returns:
            A list of dictionaries, each representing a serialized child view
            with its assigned path in the view hierarchy.
        """
        visible = [c for c in self._children if c._visible]
        return [child.to_dict(f"{parent_path}.{i}", depth + 1) for i, child in enumerate(visible)]


class NavigationLink(View):
    """A clickable view that navigates to a destination when tapped.

    NavigationLink creates a tappable row or element that, when activated,
    pushes a destination view onto the enclosing NavigationStack. This is
    the primary mechanism for creating drill-down navigation interfaces.

    The link displays a label (typically text) and renders with a disclosure
    indicator to show that tapping will navigate to more content. When
    tapped, the destination views are pushed onto the navigation stack.

    Attributes:
        _type: The view type identifier ("NavigationLink").
        _label: The text label displayed for the link.
        _destination: List of views to display when navigated to.

    Example:
        Simple navigation link::

            nib.NavigationLink("Profile", destination=[
                nib.Text("Profile Page"),
                nib.Image(system_name="person.circle"),
            ])

        Dynamic navigation links::

            for item in menu_items:
                nib.NavigationLink(item.title, destination=[
                    nib.ItemDetailView(item),
                ])
    """

    _type = "NavigationLink"

    def __init__(
        self,
        label: str,
        destination: Optional[ListType[View]] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a NavigationLink.

        Args:
            label: The text label to display for the navigation link.
                This text is shown to the user as the tappable element.
            destination: List of views to display when the link is tapped.
                These views are pushed onto the NavigationStack and shown
                as the new screen. If None or empty, the link will have
                no navigation effect.
            **kwargs: Additional view modifiers passed to the base View class.
                Supports all standard modifiers including padding, background,
                foreground_color, opacity, etc.

        Example:
            Creating a settings navigation link::

                settings_link = nib.NavigationLink(
                    "Settings",
                    destination=[
                        nib.VStack(
                            controls=[
                                nib.Text("Settings", font=nib.Font.title),
                                nib.Toggle("Notifications", is_on=True),
                                nib.Toggle("Sound", is_on=False),
                            ],
                            padding=16,
                        ),
                    ],
                )
        """
        super().__init__(**kwargs)
        self._label = label
        self._destination = destination or []

    def _get_props(self) -> dict:
        """Get the NavigationLink-specific properties for serialization.

        Returns:
            A dictionary containing the label property.
        """
        return {"label": self._label}

    def _get_children(self, parent_path: str, depth: int = 0) -> ListType[dict]:
        """Convert destination views to their dictionary representations.

        Args:
            parent_path: The path identifier of this NavigationLink in the
                view tree, used to generate unique paths for destination views.
            depth: Current depth in the view tree (for stack overflow protection).

        Returns:
            A list of dictionaries, each representing a serialized destination
            view with its assigned path in the view hierarchy.
        """
        visible = [c for c in self._destination if c._visible]
        return [child.to_dict(f"{parent_path}.{i}", depth + 1) for i, child in enumerate(visible)]


class DisclosureGroup(View):
    """A collapsible container that shows or hides content on demand.

    DisclosureGroup creates an expandable/collapsible section with a label
    that users can tap to reveal or hide the contained content. This is
    useful for organizing optional or advanced settings, creating
    accordion-style interfaces, or reducing visual clutter by hiding
    less frequently used options.

    The disclosure group displays a disclosure indicator (chevron) next to
    the label that rotates to indicate the expanded/collapsed state. When
    expanded, the child content is revealed with an animation.

    Attributes:
        _type: The view type identifier ("DisclosureGroup").
        _label: The text label for the disclosure group header.
        _children: List of child views shown when expanded.
        _is_expanded: Current expansion state (True = expanded).
        _on_expand: Optional callback invoked when expansion state changes.

    Example:
        Advanced settings section::

            nib.DisclosureGroup("Advanced Options", controls=[
                nib.Toggle("Enable logging", is_on=False),
                nib.Toggle("Developer mode", is_on=False),
                nib.Slider(value=50, min_value=0, max_value=100),
            ])

        Initially expanded group::

            nib.DisclosureGroup(
                "Quick Settings",
                controls=[
                    nib.Toggle("Wi-Fi", is_on=True),
                    nib.Toggle("Bluetooth", is_on=True),
                ],
                is_expanded=True,
            )

        With expansion callback::

            def on_expand(expanded):
                print(f"Group is now {'expanded' if expanded else 'collapsed'}")

            nib.DisclosureGroup(
                "Details",
                controls=[nib.Text("Hidden content")],
                on_expand=on_expand,
            )
    """

    _type = "DisclosureGroup"

    def __init__(
        self,
        label: str,
        controls: ListType[View] = None,
        # Alias for backwards compatibility
        children: ListType[View] = None,
        is_expanded: bool = False,
        on_expand: Optional[Callable[[bool], None]] = None,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a DisclosureGroup.

        Args:
            label: The text label displayed in the disclosure group header.
                This text is always visible regardless of expansion state.
            controls: List of child views to show when the group is expanded.
                These views are hidden when collapsed and revealed when
                expanded. This is the preferred parameter name.
            children: Alias for controls, provided for backwards compatibility.
                If both are provided, controls takes precedence.
            is_expanded: Initial expansion state. If True, the group starts
                expanded with content visible. If False (default), the group
                starts collapsed with content hidden.
            on_expand: Optional callback function that is invoked when the
                expansion state changes. The callback receives a boolean
                parameter indicating the new expansion state (True = expanded,
                False = collapsed).
            **kwargs: Additional view modifiers passed to the base View class.
                Supports all standard modifiers including padding, background,
                foreground_color, opacity, etc.

        Example:
            Creating an expandable FAQ section::

                faq_section = nib.DisclosureGroup(
                    "Frequently Asked Questions",
                    controls=[
                        nib.Text("Q: How do I reset my password?"),
                        nib.Text("A: Go to Settings > Account > Reset Password"),
                        nib.Divider(),
                        nib.Text("Q: Where are my files stored?"),
                        nib.Text("A: Files are stored in ~/Documents/MyApp"),
                    ],
                    is_expanded=False,
                    on_expand=lambda expanded: track_faq_view(expanded),
                )
        """
        super().__init__(**kwargs)
        self._label = label
        # controls is the preferred name, children is alias for backwards compatibility
        self._children = controls if controls is not None else (children or [])
        self._is_expanded = is_expanded
        self._on_expand = on_expand

    def _get_props(self) -> dict:
        """Get the DisclosureGroup-specific properties for serialization.

        Returns:
            A dictionary containing the label and isExpanded properties.
        """
        return {
            "label": self._label,
            "isExpanded": self._is_expanded,
        }

    def _get_children(self, parent_path: str, depth: int = 0) -> ListType[dict]:
        """Convert child views to their dictionary representations.

        Args:
            parent_path: The path identifier of this DisclosureGroup in the
                view tree, used to generate unique paths for child views.
            depth: Current depth in the view tree (for stack overflow protection).

        Returns:
            A list of dictionaries, each representing a serialized child view
            with its assigned path in the view hierarchy.
        """
        visible = [c for c in self._children if c._visible]
        return [child.to_dict(f"{parent_path}.{i}", depth + 1) for i, child in enumerate(visible)]

    def _handle_event(self, event: str) -> None:
        """Handle events from the Swift runtime.

        Processes expansion state change events and invokes the on_expand
        callback if one was provided.

        Args:
            event: The event string from the Swift runtime. Expected format
                is "expand:true" or "expand:false" for expansion state changes.
        """
        if event.startswith("expand:") and self._on_expand:
            value = event.split(":", 1)[1] == "true"
            self._on_expand(value)
