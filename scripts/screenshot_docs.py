#!/usr/bin/env python3
"""Automated screenshot generator for nib documentation.

Launches each examples/docs/ script one at a time, clicks the status bar
icon to open the popover, captures a screenshot of the popover window,
and saves it to media/controls/.

Requirements:
    pip install pyobjc-framework-Quartz

macOS permissions (grant to your Terminal app):
    - Accessibility  (System Settings > Privacy & Security > Accessibility)
    - Screen Recording (System Settings > Privacy & Security > Screen Recording)

Usage:
    python scripts/screenshot_docs.py
    python scripts/screenshot_docs.py --delay 3
    python scripts/screenshot_docs.py --only button,text,slider
"""

import argparse
import os
import subprocess
import sys
import time

try:
    from Quartz import (
        CGEventCreateMouseEvent,
        CGEventPost,
        CGWindowListCopyWindowInfo,
        kCGEventLeftMouseDown,
        kCGEventLeftMouseUp,
        kCGEventRightMouseDown,
        kCGEventRightMouseUp,
        kCGHIDEventTap,
        kCGMouseButtonLeft,
        kCGMouseButtonRight,
        kCGNullWindowID,
        kCGWindowBounds,
        kCGWindowListOptionAll,
        kCGWindowNumber,
        kCGWindowOwnerPID,
    )

except ImportError:
    sys.exit(
        "pyobjc-framework-Quartz is required.\n"
        "Install with:  pip install pyobjc-framework-Quartz"
    )

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES_DIR = os.path.join(ROOT, "examples", "docs")
OUTPUT_DIR = os.path.join(ROOT, "docs", "assets", "img", "controls")

CG_WINDOW_LAYER = "kCGWindowLayer"

# ── Window helpers ───────────────────────────────────────────────────────────


def get_all_window_ids():
    """Return a set of every current CGWindow ID."""
    windows = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)
    return {w[kCGWindowNumber] for w in windows}


def get_new_windows(before_ids):
    """Return CGWindow dicts for windows that appeared after *before_ids* snapshot."""
    windows = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)
    return [w for w in windows if w[kCGWindowNumber] not in before_ids]


def get_windows_for_pid(pid):
    """Return all CGWindow dicts owned by *pid*."""
    windows = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)
    return [w for w in windows if w.get(kCGWindowOwnerPID) == pid]


def find_status_item(before_ids):
    """Find the new status-bar-item window (small strip at the top of screen)."""
    for w in get_new_windows(before_ids):
        b = w.get(kCGWindowBounds, {})
        h, width = b.get("Height", 0), b.get("Width", 0)
        if 0 < h <= 50 and width > 0:
            return w
    return None


def find_menu(status_item):
    """Find the menu window spawned by right-clicking a status item."""
    ib = status_item[kCGWindowBounds]
    ix = ib["X"]
    iy = ib["Y"] + ib["Height"]

    best, best_area = None, 0

    windows = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)

    for w in windows:
        layer = w.get(CG_WINDOW_LAYER, 0)
        if layer < 20:
            continue  # menus live on high layers

        b = w.get(kCGWindowBounds, {})
        if not b:
            continue

        # Menu should be roughly under the status item
        if not (ix - 50 <= b["X"] <= ix + 50):
            continue
        if b["Y"] < iy:
            continue

        h, width = b.get("Height", 0), b.get("Width", 0)
        area = h * width

        if area > best_area:
            best, best_area = w, area

    return best


def find_popover(runtime_pid):
    """Find the popover window (the large window owned by the runtime)."""
    best, best_area = None, 0
    for w in get_windows_for_pid(runtime_pid):
        b = w.get(kCGWindowBounds, {})
        h, width = b.get("Height", 0), b.get("Width", 0)
        area = h * width
        if h > 60 and width > 60 and area > best_area:
            best, best_area = w, area
    return best


# ── Input simulation ─────────────────────────────────────────────────────────


def click(x, y, button="left"):
    """Simulate a mouse click at screen coordinates (*x*, *y*).

    button: "left" or "right"
    """
    pos = (x, y)

    if button == "right":
        down_type = kCGEventRightMouseDown
        up_type = kCGEventRightMouseUp
        mouse_button = kCGMouseButtonRight
    else:
        down_type = kCGEventLeftMouseDown
        up_type = kCGEventLeftMouseUp
        mouse_button = kCGMouseButtonLeft

    down = CGEventCreateMouseEvent(None, down_type, pos, mouse_button)
    CGEventPost(kCGHIDEventTap, down)
    time.sleep(0.05)
    up = CGEventCreateMouseEvent(None, up_type, pos, mouse_button)
    CGEventPost(kCGHIDEventTap, up)


# ── Utilities ────────────────────────────────────────────────────────────────


def poll(fn, timeout=15, interval=0.4):
    """Call *fn* repeatedly until it returns a truthy value or *timeout* expires."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        result = fn()
        if result:
            return result
        time.sleep(interval)
    return None


def kill_stale_runtimes():
    """Kill any leftover nib-runtime processes from previous runs."""
    subprocess.run(["pkill", "-f", "nib-runtime"], capture_output=True)
    time.sleep(0.5)


def capture_window(window_id, path):
    """Use macOS screencapture to grab a single window (no shadow)."""
    subprocess.run(["screencapture", "-l", str(window_id), path], check=True)


# ── Per-example flow ─────────────────────────────────────────────────────────


def process_one(script_path, output_path, delay, click_button):
    """Launch one example, open its popover, screenshot it, tear down."""
    name = os.path.splitext(os.path.basename(script_path))[0]
    print(f"\n{'─' * 44}")
    print(f"  {name}")
    print(f"{'─' * 44}")

    kill_stale_runtimes()

    # 1. Snapshot current windows, then launch the app
    before_ids = get_all_window_ids()
    proc = subprocess.Popen(
        ["nib", "run", script_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        # 2. Wait for the status-bar item (a new small window at the top)
        print(f"  waiting for status bar item …")
        item = poll(lambda: find_status_item(before_ids))
        if not item:
            print(f"  SKIP — status bar item not found")
            return False

        runtime_pid = item[kCGWindowOwnerPID]

        # 3. Click the status-bar item to open the popover
        b = item[kCGWindowBounds]
        cx = b["X"] + b["Width"] / 2
        cy = b["Y"] + b["Height"] / 2
        print(f"  clicking status bar ({cx:.0f}, {cy:.0f})")
        click(cx, cy, button=click_button)

        # 4. Wait for the popover window to appear
        print(f"  waiting for {'menu' if click_button == 'right' else 'popover'} …")
        if click_button == "right":
            window = poll(lambda: find_menu(item))
        else:
            window = poll(lambda: find_popover(runtime_pid))

        if not window:
            print(f"  SKIP — window not found")
            return False

        # 5. Let content fully render (images, webviews, etc.)
        time.sleep(delay)

        # 6. Screenshot the popover window
        wid = window[kCGWindowNumber]
        capture_window(wid, output_path)
        print(f"  OK — {os.path.relpath(output_path, ROOT)}")
        return True

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        kill_stale_runtimes()


# ── Entry point ──────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Automated screenshot generator for nib documentation examples."
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Seconds to wait after popover opens for content to render (default: 2)",
    )
    parser.add_argument(
        "--only",
        type=str,
        default="",
        help="Comma-separated list of example names to capture (e.g. button,text)",
    )
    parser.add_argument(
        "--right-click",
        action="store_true",
        help="Use right-click instead of left-click on the status bar item",
    )
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Gather example scripts
    scripts = sorted(f for f in os.listdir(EXAMPLES_DIR) if f.endswith(".py"))

    if args.only:
        keep = {n.strip() for n in args.only.split(",")}
        scripts = [s for s in scripts if os.path.splitext(s)[0] in keep]

    if not scripts:
        sys.exit("No example scripts found in examples/docs/.")

    print(
        f"Found {len(scripts)} example(s).  Output → {os.path.relpath(OUTPUT_DIR, ROOT)}/\n"
    )

    ok, fail = 0, 0
    for s in scripts:
        script_path = os.path.join(EXAMPLES_DIR, s)
        out_name = os.path.splitext(s)[0] + ".png"
        output_path = os.path.join(OUTPUT_DIR, out_name)

        click_button = "right" if args.right_click else "left"

        if process_one(script_path, output_path, args.delay, click_button):
            ok += 1
        else:
            fail += 1

    print(f"\n{'═' * 44}")
    print(f"  Done — {ok} captured, {fail} failed ({ok + fail} total)")
    print(f"{'═' * 44}")


if __name__ == "__main__":
    main()
