# pyproject.toml Configuration

Nib reads project settings from the `[tool.nib]` section of `pyproject.toml`. This lets you define build defaults so that `nib run` and `nib build` work without any flags.

## Sections overview

| Section | Purpose |
|---------|---------|
| `[tool.nib]` | Entry point and top-level settings |
| `[tool.nib.build]` | Build configuration (name, icon, version, etc.) |
| `[tool.nib.build.plist]` | Info.plist options (category, dock icon, URL schemes, etc.) |
| `[tool.nib.build.plist.usage]` | Privacy permission descriptions |
| `[tool.nib.build.plist.custom]` | Arbitrary Info.plist keys |
| `[[tool.nib.build.plist.document_types]]` | File type associations |

---

## `[tool.nib]`

Top-level project settings.

| Key | Type | Description |
|-----|------|-------------|
| `entry` | `string` | Path to the entry point script. Used by `nib run` and `nib build` when no script argument is given. Default: `src/main.py` |

```toml
[tool.nib]
entry = "src/main.py"
```

---

## `[tool.nib.build]`

Build configuration. All keys are optional -- sensible defaults are used when omitted.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `name` | `string` | Project name | App display name shown in the menu bar and Finder |
| `identifier` | `string` | `com.nib.<name>` | macOS bundle identifier |
| `version` | `string` | `1.0.0` | App version string (`CFBundleShortVersionString`) |
| `icon` | `string` | `src/assets/icon.png` | Path to icon file (`.icns` or `.png` -- PNG is auto-converted) |
| `min_macos` | `string` | Current system version | Minimum macOS version required to run the app |
| `exclude` | `list[string]` | `[]` | Packages to exclude from the bundle |
| `extra_deps` | `list[string]` | `[]` | Additional pip packages to include if auto-detection misses them |
| `launch_at_login` | `bool` | `false` | Register the app to start automatically at login (requires signed app) |
| `arch` | `string` | Current machine | Target architecture: `arm64` or `x86_64` |
| `native` | `bool` | `false` | Compile Python to native `.so` via Cython |
| `obfuscate` | `bool` | `false` | Strip debug info from `.pyc` bytecode |
| `optimize` | `bool` | `false` | Optimize bundle size (strip binaries, prune stdlib) |

```toml
[tool.nib.build]
name = "Weather Widget"
identifier = "com.example.weatherwidget"
version = "2.1.0"
icon = "src/assets/icon.png"
min_macos = "14.0"
extra_deps = ["requests", "pillow"]
launch_at_login = true
```

!!! info "Dependency detection"
    If your `pyproject.toml` has a `[project].dependencies` list, Nib uses those packages directly instead of auto-detecting imports via AST analysis. The `nib` package itself is automatically excluded.

---

## `[tool.nib.build.plist]`

Controls values written to the app's `Info.plist`. These affect how macOS treats your application.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `copyright` | `string` | -- | Human-readable copyright string |
| `category` | `string` | -- | App Store category (e.g., `public.app-category.utilities`) |
| `notification_style` | `string` | -- | Notification display style: `banner`, `alert`, or `none` |
| `dock_icon` | `bool` | `false` | Show the app in the Dock (default: menu bar only) |
| `background_only` | `bool` | `false` | Run as a background daemon with no UI |
| `build_number` | `string` | Same as `version` | Internal build number (`CFBundleVersion`), separate from the display version |
| `allow_http` | `bool` or `list[string]` | `false` | Allow insecure HTTP connections. `true` allows all domains; a list allows specific domains only |
| `url_schemes` | `list[string]` | -- | Register custom URL schemes (e.g., `["myapp"]` for `myapp://`) |

```toml
[tool.nib.build.plist]
copyright = "Copyright 2025 Your Name"
category = "public.app-category.utilities"
notification_style = "banner"
dock_icon = false
build_number = "42"
url_schemes = ["myapp"]
```

### `allow_http`

By default, macOS enforces App Transport Security (HTTPS only). You can relax this globally or per-domain:

```toml
# Allow HTTP to all domains
allow_http = true

# Allow HTTP to specific domains only
allow_http = ["api.example.com", "cdn.example.com"]
```

---

## Document type associations

Register your app as a handler for specific file types using TOML array-of-tables syntax.

| Key | Type | Description |
|-----|------|-------------|
| `name` | `string` | Display name for the document type |
| `extensions` | `list[string]` | File extensions to associate (without the dot) |
| `role` | `string` | `Viewer` or `Editor` |

```toml
[[tool.nib.build.plist.document_types]]
name = "Text Document"
extensions = ["txt", "md"]
role = "Viewer"

[[tool.nib.build.plist.document_types]]
name = "JSON File"
extensions = ["json"]
role = "Editor"
```

---

## `[tool.nib.build.plist.usage]`

Privacy permission descriptions. macOS requires a usage string for each protected resource your app accesses. If the user's code references `Permission.CAMERA` or `Permission.MICROPHONE`, Nib auto-detects them with generic descriptions -- but you should provide your own.

| Key | Plist key | Description |
|-----|-----------|-------------|
| `camera` | `NSCameraUsageDescription` | Camera access |
| `microphone` | `NSMicrophoneUsageDescription` | Microphone access |
| `location` | `NSLocationUsageDescription` | Location services |
| `apple_events` | `NSAppleEventsUsageDescription` | Controlling other apps via Apple Events |
| `contacts` | `NSContactsUsageDescription` | Contacts database |
| `photos` | `NSPhotoLibraryUsageDescription` | Photo library |
| `calendars` | `NSCalendarsUsageDescription` | Calendar data |
| `reminders` | `NSRemindersUsageDescription` | Reminders |
| `bluetooth` | `NSBluetoothAlwaysUsageDescription` | Bluetooth |
| `speech_recognition` | `NSSpeechRecognitionUsageDescription` | Speech recognition |
| `desktop_folder` | `NSDesktopFolderUsageDescription` | Desktop folder |
| `downloads_folder` | `NSDownloadsFolderUsageDescription` | Downloads folder |
| `network_volumes` | `NSNetworkVolumesUsageDescription` | Network volumes |
| `removable_volumes` | `NSRemovableVolumesUsageDescription` | Removable volumes |
| `accessibility` | `NSAccessibilityUsageDescription` | Accessibility features |

```toml
[tool.nib.build.plist.usage]
camera = "This app uses the camera for video preview."
microphone = "This app uses the microphone for voice commands."
location = "This app uses your location to show local weather."
```

---

## `[tool.nib.build.plist.custom]`

An escape hatch for arbitrary `Info.plist` keys. Values in this section are merged last and can override anything set by other options.

```toml
[tool.nib.build.plist.custom]
NSSupportsAutomaticTermination = true
NSSupportsSuddenTermination = true
MyCustomKey = "custom value"
```

---

## Complete example

A fully annotated `pyproject.toml` with all available options:

```toml
[project]
name = "weather-widget"
version = "2.1.0"
description = "A macOS menu bar weather app"
requires-python = ">=3.10"
dependencies = [
    "requests",
    "pillow",
]

[tool.nib]
# Entry point script -- used by `nib run` and `nib build`
entry = "src/main.py"

[tool.nib.build]
# App display name
name = "Weather Widget"

# Bundle identifier
identifier = "com.example.weatherwidget"

# App version (overrides [project].version for the bundle)
version = "2.1.0"

# Icon file (.icns or .png -- PNG is auto-converted)
icon = "src/assets/icon.png"

# Minimum macOS version
min_macos = "14.0"

# Packages to exclude from bundling
exclude = []

# Additional dependencies if auto-detection misses them
extra_deps = []

# Start at login (requires signed app)
launch_at_login = false

[tool.nib.build.plist]
copyright = "Copyright 2025 Jane Developer"
category = "public.app-category.weather"
notification_style = "banner"
dock_icon = false
background_only = false
build_number = "42"
allow_http = ["api.weather.com"]
url_schemes = ["weather-widget"]

# File type associations
[[tool.nib.build.plist.document_types]]
name = "Weather Data"
extensions = ["weather", "json"]
role = "Viewer"

# Privacy descriptions
[tool.nib.build.plist.usage]
location = "Weather Widget uses your location to show local forecasts."
camera = "Weather Widget uses the camera for sky condition detection."

# Custom plist keys (escape hatch)
[tool.nib.build.plist.custom]
NSSupportsAutomaticTermination = true
```
