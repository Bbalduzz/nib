"""Grid layouts for arranging views in rows and columns.

Provides Grid, LazyVGrid, and LazyHGrid for flexible grid-based layouts.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union
from ..base import View


class GridItemSize(Enum):
    """Grid item sizing strategy."""
    FIXED = "fixed"
    FLEXIBLE = "flexible"
    ADAPTIVE = "adaptive"


@dataclass
class GridItem:
    """Specification for a column or row in a grid.

    Args:
        size: Sizing strategy (fixed, flexible, or adaptive).
        value: Size value - meaning depends on size type:
            - fixed: exact size in points
            - flexible: minimum size (expands to fill)
            - adaptive: minimum item size (fits as many as possible)
        maximum: Maximum size for flexible items.
        spacing: Spacing after this item.
        alignment: Alignment within the item.

    Example:
        Fixed 100pt columns::

            GridItem(GridItemSize.FIXED, 100)

        Flexible columns with min 50pt::

            GridItem(GridItemSize.FLEXIBLE, 50)

        Adaptive columns, at least 80pt each::

            GridItem(GridItemSize.ADAPTIVE, 80)
    """
    size: GridItemSize = GridItemSize.FLEXIBLE
    value: Optional[float] = None
    maximum: Optional[float] = None
    spacing: Optional[float] = None
    alignment: Optional[str] = None

    def _to_dict(self) -> dict:
        d = {"size": self.size.value}
        if self.value is not None:
            d["value"] = float(self.value)
        if self.maximum is not None:
            d["maximum"] = float(self.maximum)
        if self.spacing is not None:
            d["spacing"] = float(self.spacing)
        if self.alignment is not None:
            d["alignment"] = self.alignment
        return d


# Convenience constructors
def fixed(size: float, spacing: Optional[float] = None) -> GridItem:
    """Create a fixed-size grid item."""
    return GridItem(GridItemSize.FIXED, size, spacing=spacing)


def flexible(minimum: float = 10, maximum: Optional[float] = None, spacing: Optional[float] = None) -> GridItem:
    """Create a flexible grid item that expands to fill available space."""
    return GridItem(GridItemSize.FLEXIBLE, minimum, maximum, spacing)


def adaptive(minimum: float, maximum: Optional[float] = None, spacing: Optional[float] = None) -> GridItem:
    """Create an adaptive grid item that fits as many items as possible."""
    return GridItem(GridItemSize.ADAPTIVE, minimum, maximum, spacing)


class LazyVGrid(View):
    """A container that arranges views in a vertically scrolling grid.

    LazyVGrid creates a grid that grows vertically, with columns defined
    by GridItem specifications. Views are loaded lazily as they become visible.

    Args:
        columns: List of GridItem specifications for columns.
        controls: Child views to arrange in the grid.
        spacing: Vertical spacing between rows.
        alignment: Horizontal alignment of grid content.
        pinned_views: Views to pin to top/bottom ("header", "footer").
        **kwargs: Additional view modifiers.

    Example:
        Three-column grid::

            nib.LazyVGrid(
                columns=[
                    nib.GridItem(nib.GridItemSize.FLEXIBLE),
                    nib.GridItem(nib.GridItemSize.FLEXIBLE),
                    nib.GridItem(nib.GridItemSize.FLEXIBLE),
                ],
                controls=[
                    nib.Text("1"), nib.Text("2"), nib.Text("3"),
                    nib.Text("4"), nib.Text("5"), nib.Text("6"),
                ],
                spacing=10,
            )

        Adaptive grid (as many 100pt columns as fit)::

            nib.LazyVGrid(
                columns=[nib.adaptive(100)],
                controls=items,
            )
    """

    _type = "LazyVGrid"

    def __init__(
        self,
        columns: List[GridItem],
        controls: Optional[List[View]] = None,
        spacing: Optional[float] = None,
        alignment: Optional[str] = None,
        pinned_views: Optional[List[str]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._columns = columns
        self._controls = controls or []
        self._spacing = spacing
        self._alignment = alignment
        self._pinned_views = pinned_views

        for child in self._controls:
            child._parent = self

    @property
    def columns(self) -> List[GridItem]:
        """Column specifications."""
        return self._columns

    @columns.setter
    def columns(self, val: List[GridItem]) -> None:
        self._columns = val
        self._mark_dirty()

    @property
    def controls(self) -> List[View]:
        """Child views."""
        return self._controls

    @controls.setter
    def controls(self, val: List[View]) -> None:
        for child in self._controls:
            child._parent = None
        self._controls = val
        for child in self._controls:
            child._parent = self
        self._mark_dirty()

    def _get_props(self) -> dict:
        props = {
            "columns": [col._to_dict() for col in self._columns],
        }
        if self._spacing is not None:
            props["spacing"] = float(self._spacing)
        if self._alignment is not None:
            props["alignment"] = self._alignment
        if self._pinned_views is not None:
            props["pinnedViews"] = self._pinned_views
        return props

    def _get_children(self, parent_path: str = "", depth: int = 0) -> list:
        visible = [c for c in self._controls if c._visible]
        return [child.to_dict(f"{parent_path}.{i}", depth + 1) for i, child in enumerate(visible)]


class LazyHGrid(View):
    """A container that arranges views in a horizontally scrolling grid.

    LazyHGrid creates a grid that grows horizontally, with rows defined
    by GridItem specifications. Views are loaded lazily as they become visible.

    Args:
        rows: List of GridItem specifications for rows.
        controls: Child views to arrange in the grid.
        spacing: Horizontal spacing between columns.
        alignment: Vertical alignment of grid content.
        pinned_views: Views to pin to leading/trailing.
        **kwargs: Additional view modifiers.

    Example:
        Two-row horizontal grid::

            nib.LazyHGrid(
                rows=[
                    nib.GridItem(nib.GridItemSize.FIXED, 50),
                    nib.GridItem(nib.GridItemSize.FIXED, 50),
                ],
                controls=items,
                spacing=10,
            )
    """

    _type = "LazyHGrid"

    def __init__(
        self,
        rows: List[GridItem],
        controls: Optional[List[View]] = None,
        spacing: Optional[float] = None,
        alignment: Optional[str] = None,
        pinned_views: Optional[List[str]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._rows = rows
        self._controls = controls or []
        self._spacing = spacing
        self._alignment = alignment
        self._pinned_views = pinned_views

        for child in self._controls:
            child._parent = self

    @property
    def rows(self) -> List[GridItem]:
        """Row specifications."""
        return self._rows

    @rows.setter
    def rows(self, val: List[GridItem]) -> None:
        self._rows = val
        self._mark_dirty()

    @property
    def controls(self) -> List[View]:
        """Child views."""
        return self._controls

    @controls.setter
    def controls(self, val: List[View]) -> None:
        for child in self._controls:
            child._parent = None
        self._controls = val
        for child in self._controls:
            child._parent = self
        self._mark_dirty()

    def _get_props(self) -> dict:
        props = {
            "rows": [row._to_dict() for row in self._rows],
        }
        if self._spacing is not None:
            props["spacing"] = float(self._spacing)
        if self._alignment is not None:
            props["alignment"] = self._alignment
        if self._pinned_views is not None:
            props["pinnedViews"] = self._pinned_views
        return props

    def _get_children(self, parent_path: str = "", depth: int = 0) -> list:
        visible = [c for c in self._controls if c._visible]
        return [child.to_dict(f"{parent_path}.{i}", depth + 1) for i, child in enumerate(visible)]


class Grid(View):
    """A container that arranges views in a fixed grid.

    Grid arranges views in a two-dimensional layout with explicit
    row and column structure. Unlike LazyVGrid/LazyHGrid, Grid is
    not lazy and sizes all views immediately.

    Args:
        controls: Child views (use GridRow to define rows).
        alignment: Default alignment for cells.
        horizontal_spacing: Spacing between columns.
        vertical_spacing: Spacing between rows.
        **kwargs: Additional view modifiers.

    Example:
        Simple 2x2 grid::

            nib.Grid(
                controls=[
                    nib.GridRow([nib.Text("A"), nib.Text("B")]),
                    nib.GridRow([nib.Text("C"), nib.Text("D")]),
                ],
                horizontal_spacing=10,
                vertical_spacing=10,
            )
    """

    _type = "Grid"

    def __init__(
        self,
        controls: Optional[List[View]] = None,
        alignment: Optional[str] = None,
        horizontal_spacing: Optional[float] = None,
        vertical_spacing: Optional[float] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._controls = controls or []
        self._alignment = alignment
        self._horizontal_spacing = horizontal_spacing
        self._vertical_spacing = vertical_spacing

        for child in self._controls:
            child._parent = self

    @property
    def controls(self) -> List[View]:
        """Child views (GridRow elements)."""
        return self._controls

    @controls.setter
    def controls(self, val: List[View]) -> None:
        for child in self._controls:
            child._parent = None
        self._controls = val
        for child in self._controls:
            child._parent = self
        self._mark_dirty()

    def _get_props(self) -> dict:
        props = {}
        if self._alignment is not None:
            props["alignment"] = self._alignment
        if self._horizontal_spacing is not None:
            props["horizontalSpacing"] = float(self._horizontal_spacing)
        if self._vertical_spacing is not None:
            props["verticalSpacing"] = float(self._vertical_spacing)
        return props

    def _get_children(self, parent_path: str = "", depth: int = 0) -> list:
        visible = [c for c in self._controls if c._visible]
        return [child.to_dict(f"{parent_path}.{i}", depth + 1) for i, child in enumerate(visible)]


class GridRow(View):
    """A row within a Grid.

    Args:
        controls: Views in this row.
        alignment: Vertical alignment for this row.

    Example:
        Grid row with alignment::

            nib.GridRow(
                [nib.Text("Label"), nib.TextField(value="")],
                alignment="center",
            )
    """

    _type = "GridRow"

    def __init__(
        self,
        controls: Optional[List[View]] = None,
        alignment: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._controls = controls or []
        self._alignment = alignment

        for child in self._controls:
            child._parent = self

    @property
    def controls(self) -> List[View]:
        """Views in this row."""
        return self._controls

    @controls.setter
    def controls(self, val: List[View]) -> None:
        for child in self._controls:
            child._parent = None
        self._controls = val
        for child in self._controls:
            child._parent = self
        self._mark_dirty()

    def _get_props(self) -> dict:
        props = {}
        if self._alignment is not None:
            props["alignment"] = self._alignment
        return props

    def _get_children(self, parent_path: str = "", depth: int = 0) -> list:
        visible = [c for c in self._controls if c._visible]
        return [child.to_dict(f"{parent_path}.{i}", depth + 1) for i, child in enumerate(visible)]
