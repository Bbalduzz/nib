# Style Enums

Nib provides style enums that control the visual appearance of interactive controls. Each enum maps directly to a SwiftUI style protocol.

All enums use UPPERCASE names (preferred). Lowercase aliases exist for backwards compatibility but are deprecated.

---

## ButtonStyle

Controls the visual appearance of `Button` views.

```python
nib.Button("Click", style=nib.ButtonStyle.BORDERED_PROMINENT)
```

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `ButtonStyle.AUTOMATIC` | `.automatic` | System default style. |
| `ButtonStyle.BORDERED` | `.bordered` | Button with a visible border. |
| `ButtonStyle.BORDERED_PROMINENT` | `.borderedProminent` | Bordered button with accent color fill. |
| `ButtonStyle.BORDERLESS` | `.borderless` | No visible border (text only). |
| `ButtonStyle.PLAIN` | `.plain` | Minimal styling with no visual effects. |
| `ButtonStyle.LINK` | `.link` | Appears as a clickable link. |

```python
nib.VStack(controls=[
    nib.Button("Primary", action=do_save, style=nib.ButtonStyle.BORDERED_PROMINENT),
    nib.Button("Secondary", action=do_cancel, style=nib.ButtonStyle.BORDERED),
    nib.Button("Learn More", action=do_help, style=nib.ButtonStyle.LINK),
])
```

---

## ButtonRole

Assigns a semantic role to a `Button`, which affects its appearance.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `ButtonRole.DESTRUCTIVE` | `.destructive` | Indicates a destructive action (typically red). |
| `ButtonRole.CANCEL` | `.cancel` | Indicates a cancel action. |

```python
nib.Button("Delete", action=delete_item, role=nib.ButtonRole.DESTRUCTIVE)
```

---

## BorderShape

Controls the border shape of buttons and other controls.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `BorderShape.AUTOMATIC` | `.automatic` | System default shape. |
| `BorderShape.CAPSULE` | `.capsule` | Pill-shaped border. |
| `BorderShape.ROUNDED_RECTANGLE` | `.roundedRectangle` | Rounded rectangle border. |
| `BorderShape.CIRCLE` | `.circle` | Circular border. |

---

## ControlSize

Controls the size of interactive controls.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `ControlSize.MINI` | `.mini` | Smallest size. |
| `ControlSize.SMALL` | `.small` | Small size. |
| `ControlSize.REGULAR` | `.regular` | Default size. |
| `ControlSize.LARGE` | `.large` | Large size. |
| `ControlSize.EXTRA_LARGE` | `.extraLarge` | Largest size. |

```python
nib.Button("Compact", action=do_action, control_size=nib.ControlSize.SMALL)
```

---

## LabelStyle

Controls how `Label` views display their title and icon.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `LabelStyle.AUTOMATIC` | `.automatic` | System default (shows both title and icon). |
| `LabelStyle.TITLE_ONLY` | `.titleOnly` | Show only the text title. |
| `LabelStyle.ICON_ONLY` | `.iconOnly` | Show only the icon. |
| `LabelStyle.TITLE_AND_ICON` | `.titleAndIcon` | Show both title and icon. |

```python
nib.Label("Settings", icon="gear", style=nib.LabelStyle.TITLE_AND_ICON)
```

---

## ToggleStyle

Controls the visual appearance of `Toggle` views.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `ToggleStyle.AUTOMATIC` | `.automatic` | System default style. |
| `ToggleStyle.SWITCH` | `.switch` | macOS-style toggle switch. |
| `ToggleStyle.BUTTON` | `.button` | Toggle that looks like a button. |
| `ToggleStyle.CHECKBOX` | `.checkbox` | Checkbox style (macOS native). |

```python
nib.Toggle("Dark Mode", is_on=True, style=nib.ToggleStyle.SWITCH)
nib.Toggle("Enable Notifications", is_on=False, style=nib.ToggleStyle.CHECKBOX)
```

---

## TextFieldStyle

Controls the visual appearance of `TextField` views.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `TextFieldStyle.AUTOMATIC` | `.automatic` | System default style. |
| `TextFieldStyle.PLAIN` | `.plain` | No border or background. |
| `TextFieldStyle.ROUNDED_BORDER` | `.roundedBorder` | Rounded border with background. |
| `TextFieldStyle.SQUARE_BORDER` | `.squareBorder` | Square border with background. |

```python
nib.TextField("Search...", text="", style=nib.TextFieldStyle.ROUNDED_BORDER)
```

---

## EditorStyle

Controls the visual appearance of `TextEditor` views (macOS 14+).

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `EditorStyle.AUTOMATIC` | `.automatic` | System default style. |
| `EditorStyle.PLAIN` | `.plain` | No border or background styling. |

```python
nib.TextEditor(text="", editor_style=nib.EditorStyle.PLAIN)
```

---

## PickerStyle

Controls the visual appearance of `Picker` views.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `PickerStyle.AUTOMATIC` | `.automatic` | System default style. |
| `PickerStyle.MENU` | `.menu` | Dropdown menu (compact). |
| `PickerStyle.SEGMENTED` | `.segmented` | Segmented control (horizontal tabs). |
| `PickerStyle.WHEEL` | `.wheel` | Scrolling wheel picker. |
| `PickerStyle.INLINE` | `.inline` | Inline list of options. |

```python
nib.Picker(
    "Color",
    options=["Red", "Green", "Blue"],
    selection="Red",
    style=nib.PickerStyle.SEGMENTED,
)
```

---

## ProgressStyle

Controls the visual appearance of `ProgressView` views.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `ProgressStyle.AUTOMATIC` | `.automatic` | System default style. |
| `ProgressStyle.LINEAR` | `.linear` | Horizontal progress bar. |
| `ProgressStyle.CIRCULAR` | `.circular` | Spinning circle indicator. |

```python
nib.ProgressView(value=0.65, style=nib.ProgressStyle.LINEAR)
nib.ProgressView(style=nib.ProgressStyle.CIRCULAR)  # Indeterminate spinner
```

---

## FormStyle

Controls the visual layout of `Form` containers.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `FormStyle.AUTOMATIC` | `.automatic` | Platform default style. |
| `FormStyle.COLUMNS` | `.columns` | Two-column layout with labels left and controls right (macOS default). |
| `FormStyle.GROUPED` | `.grouped` | Grouped sections with visual separation. |

```python
nib.Form(
    controls=[
        nib.TextField("Name", text=""),
        nib.Toggle("Notifications", is_on=True),
    ],
    style=nib.FormStyle.GROUPED,
)
```
