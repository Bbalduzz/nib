"""Table view for displaying tabular data.

Provides a macOS-native table view with columns and sortable data.
"""

from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Union
from ..base import View


@dataclass
class TableColumn:
    """Definition of a table column.

    Args:
        id: Unique identifier for the column.
        title: Column header text.
        key: Key to extract value from row data (dot notation supported).
        width: Optional fixed width.
        min_width: Optional minimum width.
        max_width: Optional maximum width.
        alignment: Text alignment ("leading", "center", "trailing").
    """
    id: str
    title: str
    key: str
    width: Optional[float] = None
    min_width: Optional[float] = None
    max_width: Optional[float] = None
    alignment: str = "leading"

    def _to_dict(self) -> dict:
        d = {
            "id": self.id,
            "title": self.title,
            "key": self.key,
            "alignment": self.alignment,
        }
        if self.width is not None:
            d["width"] = self.width
        if self.min_width is not None:
            d["minWidth"] = self.min_width
        if self.max_width is not None:
            d["maxWidth"] = self.max_width
        return d


class Table(View):
    """A view that displays data in a table with columns.

    Table is a macOS-specific control for displaying structured data
    in rows and columns, with optional sorting and selection.

    Args:
        columns: List of TableColumn definitions.
        rows: List of row data dictionaries.
        selection: Currently selected row ID(s).
        on_selection: Callback when selection changes.
        on_sort: Callback when sort order changes, receives (column_id, ascending).
        row_id_key: Key to use for row identification (default "id").
        **kwargs: Additional view modifiers.

    Example:
        Simple table::

            nib.Table(
                columns=[
                    nib.TableColumn("name", "Name", "name"),
                    nib.TableColumn("size", "Size", "size", alignment="trailing"),
                    nib.TableColumn("date", "Modified", "modified"),
                ],
                rows=[
                    {"id": "1", "name": "Document.txt", "size": "4 KB", "modified": "Today"},
                    {"id": "2", "name": "Image.png", "size": "1.2 MB", "modified": "Yesterday"},
                ],
                on_selection=lambda ids: print(f"Selected: {ids}"),
            )
    """

    _type = "Table"

    def __init__(
        self,
        columns: List[TableColumn],
        rows: List[dict],
        selection: Optional[Union[str, List[str]]] = None,
        on_selection: Optional[Callable[[List[str]], None]] = None,
        on_sort: Optional[Callable[[str, bool], None]] = None,
        on_double_click: Optional[Callable[[str], None]] = None,
        row_id_key: str = "id",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._columns = columns
        self._rows = rows
        self._selection = selection
        self._on_selection = on_selection
        self._on_sort = on_sort
        self._on_double_click = on_double_click
        self._row_id_key = row_id_key

    @property
    def columns(self) -> List[TableColumn]:
        """Table columns."""
        return self._columns

    @columns.setter
    def columns(self, val: List[TableColumn]) -> None:
        self._columns = val
        self._mark_dirty()

    @property
    def rows(self) -> List[dict]:
        """Table row data."""
        return self._rows

    @rows.setter
    def rows(self, val: List[dict]) -> None:
        self._rows = val
        self._mark_dirty()

    @property
    def selection(self) -> Optional[Union[str, List[str]]]:
        """Selected row ID(s)."""
        return self._selection

    @selection.setter
    def selection(self, val: Optional[Union[str, List[str]]]) -> None:
        self._selection = val
        self._mark_dirty()

    def _get_props(self) -> dict:
        import json
        props = {
            "tableColumns": [col._to_dict() for col in self._columns],
            "tableRowsJson": json.dumps(self._rows),
            "rowIdKey": self._row_id_key,
        }
        if self._selection is not None:
            props["selection"] = self._selection if isinstance(self._selection, list) else [self._selection]
        return props

    def _handle_event(self, event: str) -> None:
        if event.startswith("selection:") and self._on_selection:
            # Format: "selection:id1,id2,id3"
            ids_str = event[10:]
            ids = ids_str.split(",") if ids_str else []
            self._selection = ids
            self._on_selection(ids)
        elif event.startswith("sort:") and self._on_sort:
            # Format: "sort:column_id:asc" or "sort:column_id:desc"
            parts = event[5:].split(":")
            if len(parts) >= 2:
                column_id = parts[0]
                ascending = parts[1] == "asc"
                self._on_sort(column_id, ascending)
        elif event.startswith("doubleClick:") and self._on_double_click:
            row_id = event[12:]
            self._on_double_click(row_id)
