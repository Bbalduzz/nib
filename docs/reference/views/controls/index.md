# Controls

Control views are interactive UI elements for displaying content, capturing user input, and triggering actions. All controls inherit from `View` and accept [common modifiers](../../modifiers/index.md) such as `width`, `height`, `padding`, `background`, `foreground_color`, `opacity`, `corner_radius`, `font`, `animation`, and more as constructor parameters.

## Display

| View | Description |
|------|-------------|
| [Text](text.md) | Displays one or more lines of read-only text with optional rich text support. |
| [Label](label.md) | Combines an SF Symbol icon with a text title. |
| [Image](image.md) | Displays an image from a URL, local file, asset reference, or raw bytes. |
| [Video](video.md) | Plays video content from a URL or local file with playback controls. |
| [Markdown](markdown.md) | Renders CommonMark/GitHub Flavored Markdown text natively. |
| [ProgressView](progressview.md) | Shows task progress as a determinate bar or indeterminate spinner. |
| [Gauge](gauge.md) | Displays a value within a bounded range using various gauge styles. |
| [Divider](divider.md) | A thin visual separator line that adapts to its container orientation. |

## Input

| View | Description |
|------|-------------|
| [Button](button.md) | An interactive control that triggers a callback when tapped. |
| [TextField](textfield.md) | A single-line text input field with placeholder and change callbacks. |
| [SecureField](securefield.md) | A single-line text input that masks entered characters for passwords. |
| [TextEditor](texteditor.md) | A multi-line text editing area for longer content. |
| [Toggle](toggle.md) | A binary switch for toggling between on and off states. |
| [Slider](slider.md) | A horizontal track with a draggable thumb for selecting a numeric value. |
| [Picker](picker.md) | A selection control for choosing one option from a set. |

## Rich Content

| View | Description |
|------|-------------|
| [Table](table.md) | Displays structured data in rows and columns with sorting and selection. |
| [Map](map.md) | An interactive MapKit map with markers, annotations, and overlays. |
| [WebView](webview.md) | Embeds web content from a URL or raw HTML using WKWebView. |
| [CameraPreview](camerapreview.md) | Displays a live camera feed from a connected device. |

## Actions

| View | Description |
|------|-------------|
| [Link](link.md) | A clickable element that opens a URL in the default browser. |
| [ShareLink](sharelink.md) | A button that presents the native macOS share sheet. |
