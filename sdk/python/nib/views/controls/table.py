"""Table view for displaying tabular data.

Renders a collection of Python objects using declarative column definitions,
backed by a native macOS NSTableView with column headers, sorting, and selection.
"""

from typing import Any, Callable, List, Optional, Sequence, Union

from ..base import View


class ColumnWidth:
    """Column width specification.

    Use the static constructors to create width specs:
        ColumnWidth.fixed(100)
        ColumnWidth.range(min=80, ideal=150, max=300)
    """

    def __init__(self, type: str, value: float = 0,
                 min: float = 0, ideal: float = 0, max: float = 0):
        self._type = type
        self._value = value
        self._min = min
        self._ideal = ideal
        self._max = max

    @staticmethod
    def fixed(px: float) -> "ColumnWidth":
        """Fixed column width in points."""
        return ColumnWidth("fixed", value=px)

    @staticmethod
    def range(min: float = 0, ideal: float = 0, max: float = 0) -> "ColumnWidth":
        """Flexible column width with min/ideal/max constraints."""
        return ColumnWidth("range", min=min, ideal=ideal, max=max)

    def _to_dict(self) -> dict:
        if self._type == "fixed":
            return {"type": "fixed", "value": float(self._value)}
        return {
            "type": "range",
            "min": float(self._min),
            "ideal": float(self._ideal),
            "max": float(self._max),
        }


class TableColumn:
    """Defines how a table column behaves and renders.

    Args:
        title: Column header text.
        key: Extracts a value from a row object. Used for default text
            rendering and sorting.
        cell: Custom cell renderer. Receives a row object, returns a View.
            If omitted, ``Text(str(key(row)))`` is used.
        width: Column width spec (ColumnWidth.fixed or ColumnWidth.range).
        alignment: Text alignment ("leading", "center", "trailing").
        sortable: Whether the column can be sorted by clicking its header.

    Example::

        TableColumn("Name", key=lambda f: f.name)
        TableColumn("Preview", cell=lambda f: nib.Image(f.thumb), sortable=False)
        TableColumn("Size", key=lambda f: f.size, width=ColumnWidth.fixed(80))
    """

    def __init__(
        self,
        title: str,
        *,
        key: Optional[Callable[[Any], Any]] = None,
        cell: Optional[Callable[[Any], View]] = None,
        width: Optional[ColumnWidth] = None,
        alignment: str = "leading",
        sortable: bool = True,
    ):
        self.title = title
        self.key = key
        self.cell = cell
        self.width = width
        self.alignment = alignment
        self.sortable = sortable

    def _to_dict(self, index: int) -> dict:
        d = {
            "id": str(index),
            "title": self.title,
            "alignment": self.alignment,
            "sortable": self.sortable,
        }
        if self.width is not None:
            d["width"] = self.width._to_dict()
        return d


class Table(View):
    """A native macOS table view.

    Renders a collection of Python objects using declarative column definitions,
    with built-in support for column headers, sorting, and selection.

    Rows are plain Python objects. Columns define how data is displayed via
    ``key`` (value extraction) or ``cell`` (custom View rendering).

    Args:
        rows: The data backing the table. Any sequence of Python objects.
        columns: List of TableColumn definitions.
        selection: Currently selected row object(s), or None.
        on_select: Callback when selection changes. Receives a list of
            selected row objects.
        **kwargs: Standard view modifiers (width, height, padding, etc.).

    Example::

        nib.Table(
            rows=files,
            columns=[
                nib.TableColumn("Name", key=lambda f: f["name"]),
                nib.TableColumn("Size", key=lambda f: f["size"], alignment="trailing"),
            ],
            on_select=lambda rows: print(f"Selected: {rows}"),
            width=400,
            height=300,
        )
    """

    _type = "Table"

    def __init__(
        self,
        rows: Sequence = (),
        columns: Optional[List[TableColumn]] = None,
        selection: Optional[Union[Any, List[Any]]] = None,
        on_select: Optional[Callable[[List[Any]], None]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._rows = list(rows)
        self._columns = columns or []
        self._selection = selection
        self._on_select = on_select
        self._sort_column_idx: Optional[int] = None
        self._sort_ascending: bool = True
        # Build cell views
        self._children: List[View] = []
        self._row_id_map: dict = {}  # id(obj) str -> obj
        self._rebuild_cells()

    @property
    def rows(self) -> list:
        """Table row data."""
        return self._rows

    @rows.setter
    def rows(self, val: Sequence) -> None:
        self._rows = list(val)
        self._rebuild_cells()
        self._trigger_update()

    @property
    def columns(self) -> List[TableColumn]:
        """Table column definitions."""
        return self._columns

    @columns.setter
    def columns(self, val: List[TableColumn]) -> None:
        self._columns = val
        self._rebuild_cells()
        self._trigger_update()

    @property
    def selection(self):
        """Currently selected row object(s)."""
        return self._selection

    @selection.setter
    def selection(self, val) -> None:
        self._selection = val
        self._trigger_update()

    @property
    def _display_rows(self) -> list:
        """Rows in display order (sorted if applicable)."""
        if self._sort_column_idx is None:
            return self._rows
        col = self._columns[self._sort_column_idx]
        if col.key is None:
            return self._rows
        try:
            return sorted(self._rows, key=col.key, reverse=not self._sort_ascending)
        except Exception:
            return self._rows

    def _rebuild_cells(self) -> None:
        """Compute cell Views from rows x columns."""
        from .text import Text

        cells: List[View] = []
        self._row_id_map = {}
        display_rows = self._display_rows

        for row in display_rows:
            row_id = str(id(row))
            self._row_id_map[row_id] = row
            for col in self._columns:
                if col.cell is not None:
                    try:
                        cell_view = col.cell(row)
                    except Exception:
                        cell_view = Text("")
                elif col.key is not None:
                    try:
                        val = col.key(row)
                        cell_view = Text(str(val) if val is not None else "")
                    except Exception:
                        cell_view = Text("")
                else:
                    cell_view = Text(str(row) if row is not None else "")
                cells.append(cell_view)

        self._children = cells
        # Propagate app reference to new cell views
        app = getattr(self, "_app", None)
        if app is not None:
            for child in self._children:
                child._set_app(app)

    def _get_props(self) -> dict:
        display_rows = self._display_rows
        row_ids = [str(id(row)) for row in display_rows]

        props = {
            "tableColumns": [col._to_dict(i) for i, col in enumerate(self._columns)],
            "numColumns": len(self._columns),
            "rowIds": row_ids,
        }

        if self._sort_column_idx is not None:
            props["tableSortColumn"] = str(self._sort_column_idx)
            props["tableSortAscending"] = self._sort_ascending

        if self._selection is not None:
            sel = self._selection if isinstance(self._selection, (list, set, tuple)) else [self._selection]
            props["tableSelection"] = [str(id(r)) for r in sel]

        return props

    def _handle_event(self, event: str) -> None:
        if event.startswith("selection:"):
            ids_str = event[10:]
            ids = set(ids_str.split(",")) if ids_str else set()
            selected = [self._row_id_map[rid] for rid in ids if rid in self._row_id_map]
            self._selection = selected
            if self._on_select:
                self._on_select(selected)
        elif event.startswith("sort:"):
            col_idx_str = event[5:]
            try:
                col_idx = int(col_idx_str)
            except ValueError:
                return
            if col_idx < 0 or col_idx >= len(self._columns):
                return
            if not self._columns[col_idx].sortable:
                return
            if self._sort_column_idx == col_idx:
                self._sort_ascending = not self._sort_ascending
            else:
                self._sort_column_idx = col_idx
                self._sort_ascending = True
            self._rebuild_cells()
            self._trigger_update()
