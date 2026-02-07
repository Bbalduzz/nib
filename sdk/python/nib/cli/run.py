"""Hot reload runner for Nib applications.

This module provides the `nib run` command which watches for file changes
and automatically reloads the application while keeping the Swift runtime alive.
"""

import os
import signal
import subprocess
import sys
import threading
import traceback
from pathlib import Path
from typing import Callable, Optional, Set

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

from .. import __version__
from ..core.connection import Connection
from ..core.logging import logger


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

        # File watching
        self._observer: Optional[Observer] = None

        # Reload protection
        self._reload_lock = threading.Lock()
        self._stop_event = threading.Event()

        # Current app state
        self._current_app = None

    def start(self) -> int:
        """Start the hot reload runner."""
        if not self.script_path.exists():
            logger.error(f"Script not found: {self.script_path}")
            return 1

        logger.info(f"Using nib version {__version__}")

        try:
            self._setup_runtime()
            self._setup_watcher()

            # Initial load
            self._reload()

            # Main loop
            self._main_loop()

            return 0
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            return 0
        except Exception as e:
            logger.error(str(e))
            traceback.print_exc()
            return 1
        finally:
            self._teardown()

    def _find_runtime(self) -> Optional[Path]:
        """Find the nib-runtime executable.

        Searches in the following order:
        1. NIB_RUNTIME environment variable
        2. Bundled binary in package (pip install)
        3. System PATH
        4. Common installation locations
        5. Relative to nib package (for development)
        6. Relative to current working directory
        """
        import shutil

        # 1. Check environment variable first
        env_runtime = os.environ.get("NIB_RUNTIME")
        if env_runtime:
            path = Path(env_runtime)
            if path.exists() and path.is_file():
                return path

        # 2. Check bundled binary in package (installed via pip)
        bundled_runtime = Path(__file__).resolve().parent.parent / "bin" / "nib-runtime"
        if bundled_runtime.exists() and bundled_runtime.is_file():
            return bundled_runtime

        # 3. Check PATH (most portable)
        path_runtime = shutil.which("nib-runtime")
        if path_runtime:
            return Path(path_runtime)

        # 4. Check common installation locations
        common_locations = [
            Path.home() / ".local" / "bin" / "nib-runtime",
            Path.home() / ".nib" / "bin" / "nib-runtime",
            Path("/usr/local/bin/nib-runtime"),
            Path("/opt/homebrew/bin/nib-runtime"),
        ]

        for path in common_locations:
            if path.exists() and path.is_file():
                return path

        # 5. Check relative to nib package (editable install during development)
        try:
            current = Path(__file__).resolve().parent
            for _ in range(6):
                package_build = current / "package" / ".build"
                if package_build.exists():
                    for build_type in ["release", "debug"]:
                        runtime = package_build / build_type / "nib-runtime"
                        if runtime.exists() and runtime.is_file():
                            return runtime
                current = current.parent
        except Exception:
            pass

        # 6. Check relative to current working directory
        cwd_locations = [
            Path.cwd() / "package" / ".build" / "release" / "nib-runtime",
            Path.cwd() / "package" / ".build" / "debug" / "nib-runtime",
        ]

        for path in cwd_locations:
            if path.exists() and path.is_file():
                return path

        return None

    def _setup_runtime(self):
        """Launch Swift runtime and establish connection."""
        # Generate socket path
        self._socket_path = f"/tmp/nib-{os.getpid()}.sock"

        # Remove stale socket from a previous crashed run
        if os.path.exists(self._socket_path):
            os.unlink(self._socket_path)

        # Find runtime
        runtime_path = self._find_runtime()
        if not runtime_path:
            raise RuntimeError(
                "Could not find nib-runtime. "
                "Please build the Swift runtime first:\n"
                "  make build-runtime\n"
                "Or manually:\n"
                "  cd package && swift build -c release"
            )

        logger.info(f"Using runtime: {runtime_path}")

        # Launch runtime with socket path
        env = os.environ.copy()
        env["NIB_SOCKET"] = self._socket_path

        self._runtime_process = subprocess.Popen(
            [str(runtime_path)],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Connect to runtime
        self._connection = Connection(self._socket_path)
        if not self._connection.connect():
            raise RuntimeError("Failed to connect to nib-runtime")

        logger.info("Connected to Swift runtime")

        # Monitor runtime process in a daemon thread (like Flet)
        # so the main loop doesn't need to poll
        threading.Thread(
            target=self._monitor_runtime, daemon=True
        ).start()

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
        logger.info(f"Watching {self.script_dir} ({watch_mode})")

    def _on_file_change(self, path: str):
        """Handle file change event."""
        rel_path = Path(path).relative_to(self.script_dir)
        logger.info(f"File changed: {rel_path}")
        self._reload()

    def _reload(self):
        """Reload the user's application."""
        if not self._reload_lock.acquire(blocking=False):
            logger.info("Reload already in progress, skipping")
            return

        logger.info("Reloading...")

        try:
            # Stop old app's render loop before creating a new one
            if self._current_app:
                old_app = self._current_app
                self._current_app = None
                old_app._running = False
                old_app._render_requested.set()

            # Clear cached modules
            self._clear_user_modules()

            # Execute the script
            main_func, app_class, assets_dir = self._exec_script()

            if main_func:
                self._run_function_based(main_func, assets_dir=assets_dir)
            elif app_class:
                self._run_class_based(app_class)
            else:
                logger.warn("No nib.run() call or App subclass found")

        except SyntaxError as e:
            self._handle_syntax_error(e)
        except Exception as e:
            self._handle_runtime_error(e)
        finally:
            self._reload_lock.release()

    def _clear_user_modules(self):
        """Clear user modules from sys.modules for fresh import."""
        to_remove = []
        for name, module in sys.modules.items():
            if name == "__main__":
                continue  # Never remove __main__ — it breaks asset auto-detection
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

        # Intercept nib.run() to capture the main function and kwargs
        captured_main = [None]
        captured_assets_dir = [None]
        original_run = None

        def capture_run(main_func, **kwargs):
            captured_main[0] = main_func
            captured_assets_dir[0] = kwargs.get("assets_dir")

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
            return captured_main[0], None, captured_assets_dir[0]

        # Check for class-based (look for App subclass)
        from nib import App

        for value in namespace.values():
            if (
                isinstance(value, type)
                and issubclass(value, App)
                and value is not App
            ):
                return None, value, None

        return None, None, None

    def _setup_and_run_app(self, app, main_func=None):
        """Wire up an App instance and render the UI."""
        from nib.core.user_defaults import _set_current_app

        app._connection = self._connection
        app._socket_path = self._socket_path
        app._runtime_process = self._runtime_process
        app._running = True

        # When the app calls quit(), signal the main loop directly
        app._quit_callback = lambda: self._stop_event.set()

        app._start_render_loop()
        self._connection.set_event_handler(app._handle_event)
        _set_current_app(app)

        if main_func:
            main_func(app)

        app._render()
        self._current_app = app

    def _run_function_based(self, main_func: Callable, assets_dir=None):
        """Run function-based app."""
        from nib import App

        App._assets_dir_initialized = False
        App._assets_dir = None

        if assets_dir is not None:
            App.set_assets_dir(assets_dir)

        self._setup_and_run_app(App(), main_func=main_func)

    def _run_class_based(self, app_class):
        """Run class-based app."""
        from nib import App

        App._assets_dir_initialized = False
        App._assets_dir = None

        self._setup_and_run_app(app_class())

    def _handle_syntax_error(self, error: SyntaxError):
        """Display syntax error to user."""
        logger.error(f"Syntax error in {error.filename}:{error.lineno}")
        if error.text:
            logger.error(f"  {error.text.rstrip()}")
            if error.offset:
                logger.error(f"  {' ' * (error.offset - 1)}^")
        logger.error(f"  {error.msg}")
        logger.info("Fix the error and save to reload...")

    def _handle_runtime_error(self, error: Exception):
        """Display runtime error to user."""
        logger.error(f"Runtime error: {error}")
        traceback.print_exc()
        logger.info("Fix the error and save to reload...")

    def _monitor_runtime(self):
        """Wait for the runtime process to exit, then signal the main loop."""
        self._runtime_process.wait()
        logger.info("Swift runtime exited")
        self._stop_event.set()

    def _main_loop(self):
        """Main event loop — all exit conditions funnel through _stop_event."""
        self._stop_event.wait()

    def _signal_handler(self, signum, frame):
        """Handle termination signals."""
        self._stop_event.set()

    def _teardown(self):
        """Clean up resources."""

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
