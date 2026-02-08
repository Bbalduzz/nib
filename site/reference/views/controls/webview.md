# WebView

![WebView control](../../../assets/img/controls/webview.png)

A view that embeds web content using WKWebView. WebView can load content from URLs or raw HTML strings. It supports navigation callbacks, JavaScript evaluation, and back/forward history.

## Constructor

```python
nib.WebView(
    url=None,
    html=None,
    base_url=None,
    on_load=None,
    on_navigate=None,
    on_error=None,
    allows_back_forward=True,
    allows_magnification=True,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | `str` | `None` | URL to load. Mutually exclusive with `html`. |
| `html` | `str` | `None` | Raw HTML content to display. Mutually exclusive with `url`. |
| `base_url` | `str` | `None` | Base URL for resolving relative links in HTML content. |
| `on_load` | `Callable[[], None]` | `None` | Callback when the page finishes loading. |
| `on_navigate` | `Callable[[str], None]` | `None` | Callback when navigation occurs. Receives the new URL. |
| `on_error` | `Callable[[str], None]` | `None` | Callback when loading fails. Receives the error message. |
| `allows_back_forward` | `bool` | `True` | Whether back/forward navigation is enabled. |
| `allows_magnification` | `bool` | `True` | Whether pinch-to-zoom is enabled. |
| `**modifiers` | | | Common view modifiers: `width`, `height`, `corner_radius`, `opacity`, `padding`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `url` | `str` | Get or set the URL. Setting clears `html` and triggers navigation. |
| `html` | `str` | Get or set the HTML content. Setting clears `url` and triggers a re-render. |

## Methods

| Method | Description |
|--------|-------------|
| `load_url(url)` | Load a new URL. |
| `load_html(html, base_url=None)` | Load HTML content with an optional base URL. |
| `reload()` | Reload the current page. |
| `go_back()` | Navigate back in history. |
| `go_forward()` | Navigate forward in history. |
| `evaluate_js(script, callback=None)` | Execute JavaScript code in the web view. |

## Examples

### Load a URL

```python
import nib

def main(app: nib.App):
    app.build(
        nib.WebView(
            url="https://example.com",
            width=400,
            height=300,
            corner_radius=8,
            padding=16,
        )
    )

nib.run(main)
```

### Display custom HTML

```python
import nib

def main(app: nib.App):
    app.build(
        nib.WebView(
            html="""
            <html>
            <body style="font-family: -apple-system; padding: 20px;
                         background: #1a1a1a; color: white;">
                <h1>Hello from Nib!</h1>
                <p>This is rendered HTML content.</p>
            </body>
            </html>
            """,
            width=400,
            height=250,
            corner_radius=8,
            padding=16,
        )
    )

nib.run(main)
```

### Web view with navigation and JavaScript

```python
import nib

def main(app: nib.App):
    web = nib.WebView(
        url="https://example.com",
        on_navigate=lambda url: print(f"Navigating to: {url}"),
        on_load=lambda: print("Page loaded"),
        width=400,
        height=300,
    )

    app.build(
        nib.VStack(controls=[
            nib.HStack(controls=[
                nib.Button("Back", action=web.go_back),
                nib.Button("Forward", action=web.go_forward),
                nib.Button("Reload", action=web.reload),
                nib.Button("Run JS", action=lambda: web.evaluate_js(
                    "document.title"
                )),
            ], spacing=4),
            web,
        ], spacing=8, padding=16)
    )

nib.run(main)
```
