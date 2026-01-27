"""State management for Nib."""

from typing import Any, Generic, TypeVar, Optional

T = TypeVar("T")


class State(Generic[T]):
    """
    Reactive state that triggers re-renders when modified.

    Usage:
        class MyApp(App):
            count = State(0)

            def body(self):
                return Text(f"Count: {self.count}")

            def increment(self):
                self.count += 1
    """

    def __init__(self, initial: T):
        self._initial = initial
        self._name: Optional[str] = None

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = f"_state_{name}"

    def __get__(self, obj: Any, objtype: Optional[type] = None) -> T:
        if obj is None:
            return self  # type: ignore
        return getattr(obj, self._name, self._initial)

    def __set__(self, obj: Any, value: T) -> None:
        old_value = getattr(obj, self._name, self._initial)
        setattr(obj, self._name, value)
        if old_value != value and hasattr(obj, "_trigger_rerender"):
            obj._trigger_rerender()


class Binding(Generic[T]):
    """
    Two-way binding to a state value.

    Usage:
        TextField(text=self.bind("name"))
    """

    def __init__(self, getter: callable, setter: callable):
        self._getter = getter
        self._setter = setter

    @property
    def value(self) -> T:
        return self._getter()

    @value.setter
    def value(self, new_value: T) -> None:
        self._setter(new_value)
