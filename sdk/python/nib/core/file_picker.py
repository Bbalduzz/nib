"""File picker dialogs for selecting and saving files.

This module provides the :class:`FilePicker` class for showing native macOS
file dialogs (NSOpenPanel and NSSavePanel) with full access to their options.

Example:
    Picking files::

        import nib

        picker = nib.FilePicker()

        # Pick image files
        files = picker.pick_files(
            multiple=True,
            extensions=["png", "jpg", "gif"],
            title="Select Images",
        )
        if files:
            for f in files:
                print(f.name, f.size, f.tags)

    Picking a directory::

        dirs = picker.pick_directory(title="Select Output Folder")
        if dirs:
            output_dir = dirs[0]

    Saving a file::

        result = picker.save_file(
            filename="output.png",
            extensions=["png"],
            title="Save Image",
        )
        if result:
            print(f"Save to: {result.path}")
"""

from dataclasses import dataclass
import uuid
from typing import TYPE_CHECKING, Callable, Optional

from .pending import PendingRequests

if TYPE_CHECKING:
    from .app import App


# Thread-safe storage for blocking responses
_pending = PendingRequests()


@dataclass
class PickedFile:
    """A file selected by the user.

    Attributes:
        name: The filename (e.g., "image.png").
        path: The full file path.
        size: File size in bytes.
        uti: Uniform Type Identifier (e.g., "public.png").
        tags: List of macOS Finder tags.
    """
    name: str
    path: str
    size: int
    uti: Optional[str]
    tags: list[str]


@dataclass
class SaveResult:
    """Result from a save file dialog.

    Attributes:
        path: The chosen save path.
        tags: User-selected Finder tags.
    """
    path: str
    tags: list[str]


def _handle_file_dialog_response(response: dict) -> None:
    """Handle a file dialog response from Swift.

    Called by Connection when a fileDialogResponse message is received.
    """
    request_id = response.get("requestId", "")
    _pending.resolve(request_id, response)


class FilePicker:
    """Native macOS file picker dialogs.

    Provides methods to show open file, open directory, and save file dialogs
    with full access to NSOpenPanel and NSSavePanel options.

    All methods are synchronous and will block until the user makes a selection
    or cancels the dialog.

    Args:
        app: The App instance to use. If not provided, uses the current
            running app from :func:`nib.run`.

    Example::

        picker = nib.FilePicker()
        files = picker.pick_files(extensions=["txt", "md"])
        if files:
            for f in files:
                print(f.path)
    """

    def __init__(self, app: Optional["App"] = None):
        self._app = app

    def _get_app(self) -> Optional["App"]:
        """Get the App instance to use."""
        if self._app:
            return self._app
        # Try to get the current running app
        from .user_defaults import _get_current_app
        return _get_current_app()

    def _wait_for_response(self, request_id: str, timeout: float = 300.0) -> Optional[dict]:
        """Wait for a response from Swift."""
        return _pending.wait(request_id, timeout)

    def pick_files(
        self,
        *,
        multiple: bool = False,
        extensions: Optional[list[str]] = None,
        uttypes: Optional[list[str]] = None,
        directory: Optional[str] = None,
        title: str = "Select Files",
        message: Optional[str] = None,
        button_label: str = "Open",
        shows_hidden_files: bool = False,
        resolves_aliases: bool = True,
        allows_other_file_types: bool = False,
        treats_packages_as_directories: bool = False,
        validator: Optional[Callable[[list[str]], Optional[str]]] = None,
    ) -> Optional[list[PickedFile]]:
        """Open a file picker dialog.

        Args:
            multiple: Allow selecting multiple files.
            extensions: Allowed file extensions (e.g., ["png", "jpg"]).
            uttypes: Allowed Uniform Type Identifiers (e.g., ["public.image"]).
            directory: Initial directory path.
            title: Dialog window title.
            message: Prompt text displayed below the title.
            button_label: Text for the OK button.
            shows_hidden_files: Show hidden files in the dialog.
            resolves_aliases: Follow alias files to their targets.
            allows_other_file_types: Allow files outside the allowed types.
            treats_packages_as_directories: Treat .app bundles as folders.
            validator: Function to validate selection. Return None if valid,
                or an error message string if invalid. Dialog stays open on error.

        Returns:
            List of :class:`PickedFile` objects, or None if cancelled.
        """
        app = self._get_app()
        if not app or not app._connection:
            return None

        request_id = str(uuid.uuid4())
        _pending.create(request_id)

        app._connection.send_file_dialog(
            action="pickFiles",
            request_id=request_id,
            title=title,
            message=message,
            button_label=button_label,
            directory=directory,
            shows_hidden_files=shows_hidden_files,
            resolves_aliases=resolves_aliases,
            multiple=multiple,
            extensions=extensions,
            uttypes=uttypes,
            allows_other_file_types=allows_other_file_types,
            treats_packages_as_directories=treats_packages_as_directories,
        )

        response = self._wait_for_response(request_id)
        if not response or response.get("cancelled", True):
            return None

        files_data = response.get("files", [])
        if not files_data:
            return None

        files = [
            PickedFile(
                name=f["name"],
                path=f["path"],
                size=f["size"],
                uti=f.get("uti"),
                tags=f.get("tags", []),
            )
            for f in files_data
        ]

        # Run validator if provided
        if validator:
            paths = [f.path for f in files]
            error = validator(paths)
            if error:
                # TODO: Re-show dialog with error message
                # For now, just return None on validation failure
                return None

        return files

    def pick_directory(
        self,
        *,
        multiple: bool = False,
        directory: Optional[str] = None,
        title: str = "Select Folder",
        message: Optional[str] = None,
        button_label: str = "Select",
        shows_hidden_files: bool = False,
        resolves_aliases: bool = True,
        can_create_directories: bool = True,
        validator: Optional[Callable[[list[str]], Optional[str]]] = None,
    ) -> Optional[list[str]]:
        """Open a directory picker dialog.

        Args:
            multiple: Allow selecting multiple directories.
            directory: Initial directory path.
            title: Dialog window title.
            message: Prompt text displayed below the title.
            button_label: Text for the OK button.
            shows_hidden_files: Show hidden files in the dialog.
            resolves_aliases: Follow alias files to their targets.
            can_create_directories: Allow creating new folders in the dialog.
            validator: Function to validate selection. Return None if valid,
                or an error message string if invalid. Dialog stays open on error.

        Returns:
            List of directory paths, or None if cancelled.
        """
        app = self._get_app()
        if not app or not app._connection:
            return None

        request_id = str(uuid.uuid4())
        _pending.create(request_id)

        app._connection.send_file_dialog(
            action="pickDirectory",
            request_id=request_id,
            title=title,
            message=message,
            button_label=button_label,
            directory=directory,
            shows_hidden_files=shows_hidden_files,
            resolves_aliases=resolves_aliases,
            multiple=multiple,
            can_create_directories=can_create_directories,
        )

        response = self._wait_for_response(request_id)
        if not response or response.get("cancelled", True):
            return None

        directories = response.get("directories", [])
        if not directories:
            return None

        # Run validator if provided
        if validator:
            error = validator(directories)
            if error:
                return None

        return directories

    def save_file(
        self,
        *,
        filename: Optional[str] = None,
        extensions: Optional[list[str]] = None,
        uttypes: Optional[list[str]] = None,
        directory: Optional[str] = None,
        title: str = "Save File",
        message: Optional[str] = None,
        button_label: str = "Save",
        name_field_label: str = "Save As:",
        shows_hidden_files: bool = False,
        can_create_directories: bool = True,
        allows_other_file_types: bool = False,
        shows_tag_field: bool = True,
        validator: Optional[Callable[[str], Optional[str]]] = None,
    ) -> Optional[SaveResult]:
        """Open a save file dialog.

        Args:
            filename: Suggested filename.
            extensions: Allowed file extensions.
            uttypes: Allowed Uniform Type Identifiers.
            directory: Initial directory path.
            title: Dialog window title.
            message: Prompt text displayed below the title.
            button_label: Text for the Save button.
            name_field_label: Label for the filename text field.
            shows_hidden_files: Show hidden files in the dialog.
            can_create_directories: Allow creating new folders in the dialog.
            allows_other_file_types: Allow extensions outside the allowed list.
            shows_tag_field: Show the macOS Finder tags selector.
            validator: Function to validate the path. Return None if valid,
                or an error message string if invalid. Dialog stays open on error.

        Returns:
            :class:`SaveResult` with path and tags, or None if cancelled.
        """
        app = self._get_app()
        if not app or not app._connection:
            return None

        request_id = str(uuid.uuid4())
        _pending.create(request_id)

        app._connection.send_file_dialog(
            action="saveFile",
            request_id=request_id,
            title=title,
            message=message,
            button_label=button_label,
            directory=directory,
            shows_hidden_files=shows_hidden_files,
            filename=filename,
            name_field_label=name_field_label,
            can_create_directories=can_create_directories,
            extensions=extensions,
            uttypes=uttypes,
            allows_other_file_types=allows_other_file_types,
            shows_tag_field=shows_tag_field,
        )

        response = self._wait_for_response(request_id)
        if not response or response.get("cancelled", True):
            return None

        save_result = response.get("saveResult")
        if not save_result:
            return None

        result = SaveResult(
            path=save_result["path"],
            tags=save_result.get("tags", []),
        )

        # Run validator if provided
        if validator:
            error = validator(result.path)
            if error:
                return None

        return result
