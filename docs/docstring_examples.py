"""
Sample Docstrings Example for Nib Project
==========================================

This file demonstrates the Google-style docstring format that Sphinx with
Napoleon will parse for the Nib project. Use these examples as a reference
when documenting your code.

Note:
    This file is for documentation purposes only and is not part of the
    actual Nib package.
"""

from __future__ import annotations

from typing import Callable


class ExampleView:
    """A sample view class demonstrating proper Google-style documentation.

    This class shows how to document a typical Nib view with all its
    components: class docstring, constructor, methods, and properties.

    Attributes:
        content: The text content displayed by this view.
        font: The font style applied to the content.
        foreground_color: The color of the text.

    Example:
        Creating a basic view::

            view = ExampleView(
                content="Hello, World!",
                font=Font.title,
                foreground_color=Color.blue,
            )

        Updating the content triggers a re-render::

            view.content = "New content"
    """

    def __init__(
        self,
        content: str,
        font: str | None = None,
        foreground_color: str | None = None,
        padding: float | dict[str, float] | None = None,
        on_tap: Callable[[], None] | None = None,
    ) -> None:
        """Initialize a new ExampleView.

        Args:
            content: The text content to display. This is the primary
                content of the view.
            font: Optional font style. Can be one of the predefined
                Font constants like ``Font.title`` or ``Font.body``.
            foreground_color: Optional text color. Accepts color names,
                hex values, or Color constants.
            padding: Optional padding around the content. Can be a single
                float for uniform padding, or a dict with keys like
                ``top``, ``bottom``, ``leading``, ``trailing``,
                ``horizontal``, or ``vertical``.
            on_tap: Optional callback function invoked when the view
                is tapped. Takes no arguments and returns nothing.

        Raises:
            ValueError: If content is empty or None.

        Example:
            Basic initialization::

                view = ExampleView("Hello")

            With all options::

                view = ExampleView(
                    content="Styled text",
                    font=Font.headline,
                    foreground_color="#FF0000",
                    padding={"horizontal": 16, "vertical": 8},
                    on_tap=lambda: print("Tapped!"),
                )
        """
        if not content:
            raise ValueError("Content cannot be empty")

        self._content = content
        self._font = font
        self._foreground_color = foreground_color
        self._padding = padding
        self._on_tap = on_tap

    @property
    def content(self) -> str:
        """The text content of this view.

        Setting this property triggers an automatic re-render of the view.

        Returns:
            The current text content.

        Example:
            >>> view = ExampleView("Hello")
            >>> view.content
            'Hello'
            >>> view.content = "World"
            >>> view.content
            'World'
        """
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        self._content = value
        self._trigger_render()

    def apply_modifier(
        self,
        modifier_type: str,
        value: str | float | bool,
    ) -> "ExampleView":
        """Apply a modifier to this view.

        Modifiers change the appearance or behavior of a view without
        creating a new view instance.

        Args:
            modifier_type: The type of modifier to apply. Valid types
                include ``"opacity"``, ``"scale"``, ``"rotation"``.
            value: The value for the modifier. Type depends on the
                modifier type.

        Returns:
            Self, allowing for method chaining.

        Raises:
            ValueError: If modifier_type is not recognized.
            TypeError: If value is not the correct type for the modifier.

        Example:
            Applying multiple modifiers::

                view = ExampleView("Text")
                view.apply_modifier("opacity", 0.5)
                view.apply_modifier("scale", 1.2)

        Note:
            Some modifiers may not be compatible with each other.
            See the modifier documentation for details.
        """
        # Implementation here
        return self

    def _trigger_render(self) -> None:
        """Trigger a re-render of this view.

        This is an internal method called when view properties change.
        It sends an update message to the Swift runtime.

        Warning:
            This method is for internal use only. Do not call directly.
        """
        pass


def create_stack(
    controls: list[ExampleView],
    spacing: float = 8.0,
    alignment: str = "center",
) -> dict:
    """Create a vertical stack layout containing multiple views.

    Stacks arrange their children vertically with optional spacing
    between elements.

    Args:
        controls: List of views to include in the stack. Views are
            rendered in order from top to bottom.
        spacing: Space between each view in points. Defaults to 8.0.
        alignment: Horizontal alignment of views within the stack.
            One of ``"leading"``, ``"center"``, or ``"trailing"``.
            Defaults to ``"center"``.

    Returns:
        A dictionary representing the stack configuration, ready to
        be serialized and sent to the Swift runtime.

    Raises:
        ValueError: If controls is empty.
        ValueError: If alignment is not one of the valid options.

    Example:
        Creating a simple stack::

            stack = create_stack(
                controls=[
                    ExampleView("Title", font=Font.title),
                    ExampleView("Subtitle", font=Font.caption),
                ],
                spacing=4.0,
            )

        With custom alignment::

            stack = create_stack(
                controls=[...],
                alignment="leading",
            )

    See Also:
        :func:`create_horizontal_stack`: For horizontal layouts.
        :class:`ExampleView`: The base view class.
    """
    if not controls:
        raise ValueError("Controls list cannot be empty")

    valid_alignments = {"leading", "center", "trailing"}
    if alignment not in valid_alignments:
        raise ValueError(f"Alignment must be one of {valid_alignments}")

    return {
        "type": "vstack",
        "controls": controls,
        "spacing": spacing,
        "alignment": alignment,
    }


# Type alias example with documentation
ViewCallback = Callable[[ExampleView], None]
"""Type alias for view callback functions.

A callback that receives a view instance when triggered.

Example:
    Using the callback type::

        def my_callback(view: ExampleView) -> None:
            print(f"View content: {view.content}")

        callback: ViewCallback = my_callback
"""
