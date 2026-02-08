# Concepts

This section covers the core ideas behind Nib: how it works, how your code turns into a native macOS interface, and how you interact with it.

Nib runs two processes connected by a Unix socket. Python owns the logic. Swift owns the screen. Understanding this boundary -- and how data flows across it -- is the key to building effective Nib apps.

- [Architecture](architecture.md) -- The two-process model, message types, and data flow.
- [Reactivity](reactivity.md) -- How property mutations trigger UI updates.
- [View Tree](view-tree.md) -- How views are structured, serialized, and identified.
- [Modifiers](modifiers.md) -- Styling views through constructor parameters.
- [Event Handling](event-handling.md) -- How user interactions flow from Swift to Python.
