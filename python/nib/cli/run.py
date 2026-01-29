"""Hot reload runner for Nib applications.

This module provides the `nib run` command which watches for file changes
and automatically reloads the application while keeping the Swift runtime alive.
"""

import os
import signal
import subprocess
import sys
import threading
import time
import traceback
from pathlib import Path
from typing import Callable, Optional, Set

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

from ..core.connection import Connection


# Directories to exclude from watching
EXCLUDED_DIRS = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "dist",
    "build",
    ".eggs",
}


class ReloadHandler(FileSystemEventHandler):
    """Watchdog handler for Python file changes with debouncing."""

    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self._debounce_timer: Optional[threading.Timer] = None
        self._lock = threading.Lock()

    def on_modified(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith(".py"):
            return

        # Skip excluded directories
        path_parts = Path(event.src_path).parts
        if any(part in EXCLUDED_DIRS for part in path_parts):
            return

        # Debounce rapid changes (e.g., editor save)
        with self._lock:
            if self._debounce_timer:
                self._debounce_timer.cancel()

            self._debounce_timer = threading.Timer(
                0.1, self._trigger_callback, [event.src_path]
            )
            self._debounce_timer.start()

    def _trigger_callback(self, path: str):
        with self._lock:
            self._debounce_timer = None
        self.callback(path)


class HotReloadRunner:
    """Manages hot reload of a Nib application.

    Keeps the Swift runtime alive while reloading Python code on file changes.
    """

    def __init__(
        self,
        script_path: Path,
        recursive: bool = False,
    ):
        self.script_path = script_path.resolve()
        self.script_dir = self.script_path.parent
        self.recursive = recursive

        # Runtime management
        self._connection: Optional[Connection] = None
        self._runtime_process: Optional[subprocess.Popen] = None
        self._socket_path: Optional[str] = None
        self._running = False

        # File watching
        self._observer: Optional[Observer] = None

        # Current app state
        self._current_app = None

    def start(self) -> int:
        """Start the hot reload runner."""
        if not self.script_path.exists():
            print(f"[nib] Error: Script not found: {self.script_path}")
            return 1

        try:
            self._setup_runtime()
            self._setup_watcher()
            self._running = True

            # Initial load
            self._reload()

            # Main loop
            self._main_loop()

            return 0
        except KeyboardInterrupt:
            print("\n[nib] Shutting down...")
            return 0
        except Exception as e:
            print(f"[nib] Error: {e}")
            traceback.print_exc()
            return 1
        finally:
            self._teardown()

    def _find_runtime(self) -> Optional[Path]:
        """Find the nib-runtime executable.

        Searches in the following order:
        1. NIB_RUNTIME environment variable
        2. System PATH
        3. Common installation locations
        4. Relative to nib package (for development)
        5. Relative to current working directory
        """
        import shutil

        # 1. Check environment variable first
        env_runtime = os.environ.get("NIB_RUNTIME")
        if env_runtime:
            path = Path(env_runtime)
            if path.exists() and path.is_file():
                return path

        # 2. Check PATH (most portable)
        path_runtime = shutil.which("nib-runtime")
        if path_runtime:
            return Path(path_runtime)

        # 3. Check common installation locations
        common_locations = [
            Path.home() / ".local" / "bin" / "nib-runtime",
            Path.home() / ".nib" / "bin" / "nib-runtime",
            Path("/usr/local/bin/nib-runtime"),
            Path("/opt/homebrew/bin/nib-runtime"),
        ]

        for path in common_locations:
            if path.exists() and path.is_file():
                return path

        # 4. Check relative to nib package (editable install during development)
        try:
            current = Path(__file__).resolve().parent
            for _ in range(6):
                swift_build = current / "swift" / ".build"
                if swift_build.exists():
                    for build_type in ["release", "debug"]:
                        runtime = swift_build / build_type / "nib-runtime"
                        if runtime.exists() and runtime.is_file():
                            return runtime
                current = current.parent
        except Exception:
            pass

        # 5. Check relative to current working directory
        cwd_locations = [
            Path.cwd() / "swift" / ".build" / "release" / "nib-runtime",
            Path.cwd() / "swift" / ".build" / "debug" / "nib-runtime",
        ]

        for path in cwd_locations:
            if path.exists() and path.is_file():
                return path

        return None

    def _setup_runtime(self):
        """Launch Swift runtime and establish connection."""
        # Generate socket path
        self._socket_path = f"/tmp/nib-{os.getpid()}.sock"

        # Find runtime
        runtime_path = self._find_runtime()
        if not runtime_path:
            raise RuntimeError(
                "Could not find nib-runtime. "
                "Please build the Swift runtime first:\n"
                "  cd swift && swift build -c release"
            )

        print(f"[nib] Using runtime: {runtime_path}")

        # Launch runtime with socket path
        env = os.environ.copy()
        env["NIB_SOCKET"] = self._socket_path

        self._runtime_process = subprocess.Popen(
            [str(runtime_path)],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Connect to runtime
        self._connection = Connection(self._socket_path)
        if not self._connection.connect():
            raise RuntimeError("Failed to connect to nib-runtime")

        print("[nib] Connected to Swift runtime")

        # Handle signals
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _setup_watcher(self):
        """Set up file system watcher."""
        handler = ReloadHandler(self._on_file_change)
        self._observer = Observer()

        # Watch the script file's directory
        self._observer.schedule(
            handler,
            str(self.script_dir),
            recursive=self.recursive,
        )
        self._observer.start()

        watch_mode = "recursively" if self.recursive else "non-recursively"
        print(f"[nib] Watching {self.script_dir} ({watch_mode})")

    def _on_file_change(self, path: str):
        """Handle file change event."""
        rel_path = Path(path).relative_to(self.script_dir)
        print(f"\n[nib] File changed: {rel_path}")
        self._reload()

    def _reload(self):
        """Reload the user's application."""
        print("[nib] Reloading...")

        try:
            # Clear cached modules
            self._clear_user_modules()

            # Execute the script
            main_func, app_class = self._exec_script()

            if main_func:
                self._run_function_based(main_func)
            elif app_class:
                self._run_class_based(app_class)
            else:
                print("[nib] Warning: No nib.run() call or App subclass found")

        except SyntaxError as e:
            self._handle_syntax_error(e)
        except Exception as e:
            self._handle_runtime_error(e)

    def _clear_user_modules(self):
        """Clear user modules from sys.modules for fresh import."""
        to_remove = []
        for name, module in sys.modules.items():
            if not hasattr(module, "__file__") or module.__file__ is None:
                continue
            try:
                module_path = Path(module.__file__).resolve()
                if self._is_user_module(module_path):
                    to_remove.append(name)
            except Exception:
                pass

        for name in to_remove:
            del sys.modules[name]

    def _is_user_module(self, module_path: Path) -> bool:
        """Check if a module is from the user's project."""
        try:
            module_path.relative_to(self.script_dir)
            return True
        except ValueError:
            return False

    def _exec_script(self):
        """Execute the script and extract main function or App class."""
        # Read and compile
        code = self.script_path.read_text()
        compiled = compile(code, str(self.script_path), "exec")

        # Create execution namespace
        namespace = {
            "__name__": "__main__",
            "__file__": str(self.script_path),
        }

        # Set __main__.__file__ so nib can detect assets directory
        # Use sys.modules directly to avoid import issues during hot-reload
        main_module = sys.modules.get("__main__")
        if main_module:
            main_module.__file__ = str(self.script_path)

        # Add script directory to path
        if str(self.script_dir) not in sys.path:
            sys.path.insert(0, str(self.script_dir))

        # Intercept nib.run() to capture the main function
        captured_main = [None]
        original_run = None

        def capture_run(main_func, **kwargs):
            captured_main[0] = main_func

        # Temporarily patch nib.run
        import nib

        original_run = nib.run
        nib.run = capture_run

        try:
            exec(compiled, namespace)
        finally:
            nib.run = original_run

        # Check for function-based
        if captured_main[0]:
            return captured_main[0], None

        # Check for class-based (look for App subclass)
        from nib import App

        for value in namespace.values():
            if (
                isinstance(value, type)
                and issubclass(value, App)
                and value is not App
            ):
                return None, value

        return None, None

    def _run_function_based(self, main_func: Callable):
        """Run function-based app."""
        from nib import App
        from nib.core.user_defaults import _set_current_app

        # Reset assets directory detection for fresh detection
        App._assets_dir_initialized = False
        App._assets_dir = None

        # Create new App with existing connection
        app = App()
        app._connection = self._connection
        app._socket_path = self._socket_path
        app._runtime_process = self._runtime_process
        app._running = True

        # Set event handler for this app
        self._connection.set_event_handler(app._handle_event)

        _set_current_app(app)

        # Run user's main function
        main_func(app)

        # Render the UI
        app._render()

        self._current_app = app

    def _run_class_based(self, app_class):
        """Run class-based app."""
        from nib import App
        from nib.core.user_defaults import _set_current_app

        # Reset assets directory detection for fresh detection
        App._assets_dir_initialized = False
        App._assets_dir = None

        # Create instance with existing connection
        app = app_class()
        app._connection = self._connection
        app._socket_path = self._socket_path
        app._runtime_process = self._runtime_process
        app._running = True

        # Set event handler for this app
        self._connection.set_event_handler(app._handle_event)

        _set_current_app(app)

        # Render the UI
        app._render()

        self._current_app = app

    def _handle_syntax_error(self, error: SyntaxError):
        """Display syntax error to user."""
        print(f"\n[nib] Syntax error in {error.filename}:{error.lineno}")
        if error.text:
            print(f"       {error.text.rstrip()}")
            if error.offset:
                print(f"       {' ' * (error.offset - 1)}^")
        print(f"       {error.msg}")
        print("\n[nib] Fix the error and save to reload...")

    def _handle_runtime_error(self, error: Exception):
        """Display runtime error to user."""
        print(f"\n[nib] Runtime error: {error}")
        traceback.print_exc()
        print("\n[nib] Fix the error and save to reload...")

    def _main_loop(self):
        """Main event loop."""
        while self._running:
            try:
                time.sleep(0.1)
                # Check if runtime is still alive
                if self._runtime_process and self._runtime_process.poll() is not None:
                    print("[nib] Swift runtime exited")
                    self._running = False
            except KeyboardInterrupt:
                break

    def _signal_handler(self, signum, frame):
        """Handle termination signals."""
        self._running = False

    def _teardown(self):
        """Clean up resources."""
        self._running = False

        if self._observer:
            self._observer.stop()
            self._observer.join(timeout=1)

        if self._connection:
            self._connection.send_quit()
            self._connection.disconnect()

        if self._runtime_process:
            self._runtime_process.terminate()
            try:
                self._runtime_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self._runtime_process.kill()

        if self._socket_path and os.path.exists(self._socket_path):
            try:
                os.unlink(self._socket_path)
            except Exception:
                pass


def run_with_reload(script: Path, recursive: bool = False) -> int:
    """Run a Nib script with hot reload.

    Args:
        script: Path to the Python script to run.
        recursive: Whether to watch subdirectories.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    runner = HotReloadRunner(script, recursive=recursive)
    return runner.start()
