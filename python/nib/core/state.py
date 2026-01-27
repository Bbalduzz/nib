"""Reactive state management for Nib applications.

This module provides descriptor-based reactive state primitives that
automatically trigger UI re-renders when values change.

The :class:`State` descriptor is designed for use with class-based App
definitions, while the function-based approach uses direct property
mutation on views (e.g., ``text.content = "new value"``).

Example:
    Class-based state management::

        class CounterApp(nib.App):
            count = nib.State(0)

            def body(self):
                return nib.VStack(controls=[
                    nib.Text(f"Count: {self.count}"),
                    nib.Button("Increment", action=self.increment),
                ])

            def increment(self):
                self.count += 1  # Automatically triggers re-render
"""

from typing import Any, Callable, Generic, TypeVar, Optional

T = TypeVar("T")


class State(Generic[T]):
    """Reactive state descriptor that triggers re-renders when modified.

    A Python descriptor that stores state per-instance and automatically
    calls the owner's ``_trigger_rerender()`` method when the value changes.

    This is primarily used for class-based App definitions. For function-based
    apps, use direct property mutation on views instead.

    Attributes:
        _initial: The initial/default value for this state.
        _name: The mangled attribute name used for storage.

    Example:
        Using State in a class-based App::

            class MyApp(nib.App):
                name = nib.State("")
                count = nib.State(0)
                enabled = nib.State(True)

                def body(self):
                    return nib.VStack(controls=[
                        nib.Text(f"Hello, {self.name}!"),
                        nib.Text(f"Count: {self.count}"),
                        nib.Toggle(is_on=self.enabled),
                    ])

                def increment(self):
                    self.count += 1  # Triggers re-render

    Note:
        The state value is stored in a mangled attribute on the instance
        (e.g., ``_state_count``) to avoid conflicts with other attributes.
    """

    def __init__(self, initial: T) -> None:
        """Initialize a State descriptor with a default value.

        Args:
            initial: The initial value for this state variable.
        """
        self._initial = initial
        self._name: Optional[str] = None

    def __set_name__(self, owner: type, name: str) -> None:
        """Called when the descriptor is assigned to a class attribute.

        Args:
            owner: The class that owns this descriptor.
            name: The attribute name this descriptor is assigned to.
        """
        self._name = f"_state_{name}"

    def __get__(self, obj: Any, objtype: Optional[type] = None) -> T:
        """Get the current state value.

        Args:
            obj: The instance to get the value from.
            objtype: The owner class type.

        Returns:
            The current state value, or the descriptor itself if accessed
            from the class (not an instance).
        """
        if obj is None:
            return self  # type: ignore
        return getattr(obj, self._name, self._initial)

    def __set__(self, obj: Any, value: T) -> None:
        """Set the state value and trigger a re-render if changed.

        Args:
            obj: The instance to set the value on.
            value: The new value to set.
        """
        old_value = getattr(obj, self._name, self._initial)
        setattr(obj, self._name, value)
        if old_value != value and hasattr(obj, "_trigger_rerender"):
            obj._trigger_rerender()


class Binding(Generic[T]):
    """Two-way binding to a state value.

    A Binding wraps getter and setter functions to provide bidirectional
    data flow between a state variable and a UI control.

    This is useful for controls like TextField where the control needs
    to both read the current value and write changes back to state.

    Attributes:
        _getter: Function that returns the current value.
        _setter: Function that updates the value.

    Example:
        Creating a binding to an app state::

            class MyApp(nib.App):
                name = nib.State("")

                def body(self):
                    return nib.TextField(
                        text=Binding(
                            getter=lambda: self.name,
                            setter=lambda v: setattr(self, "name", v),
                        )
                    )

    Note:
        For most use cases, the function-based approach with ``on_change``
        callbacks is simpler and more explicit.
    """

    def __init__(self, getter: Callable[[], T], setter: Callable[[T], None]) -> None:
        """Initialize a two-way binding.

        Args:
            getter: Function that returns the current value.
            setter: Function that updates the value.
        """
        self._getter = getter
        self._setter = setter

    @property
    def value(self) -> T:
        """Get the current bound value.

        Returns:
            The current value from the getter function.
        """
        return self._getter()

    @value.setter
    def value(self, new_value: T) -> None:
        """Set the bound value.

        Args:
            new_value: The new value to set via the setter function.
        """
        self._setter(new_value)
