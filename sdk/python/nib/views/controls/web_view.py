"""WebView for displaying web content.

The WebView displays web content from URLs or raw HTML with navigation
and JavaScript support.

Example:
    Load a URL::

        nib.WebView(
            url="https://example.com",
            width=400,
            height=300,
        )

    Load raw HTML::

        nib.WebView(
            html="<h1>Hello World</h1>",
            width=400,
            height=300,
        )
"""

from typing import Any, Callable, Optional

from ..base import View


class WebView(View):
    """A view that displays web content using WKWebView.

    WebView can load content from URLs or raw HTML strings. It supports
    navigation callbacks and JavaScript evaluation.

    Attributes:
        url: The URL to load.
        html: Raw HTML content to display.

    Example:
        Basic web view::

            nib.WebView(
                url="https://example.com",
                width=400,
                height=300,
            )

        Web view with HTML content::

            nib.WebView(
                html=\"\"\"
                <html>
                    <body style="background: #1a1a1a; color: white;">
                        <h1>Hello from Nib!</h1>
                    </body>
                </html>
                \"\"\",
                width=400,
                height=300,
            )

        Web view with navigation callback::

            def on_nav(url: str):
                print(f"Navigating to: {url}")

            nib.WebView(
                url="https://example.com",
                on_navigate=on_nav,
                width=400,
                height=300,
            )
    """

    _type = "WebView"

    def __init__(
        self,
        url: Optional[str] = None,
        html: Optional[str] = None,
        base_url: Optional[str] = None,
        on_load: Optional[Callable[[], None]] = None,
        on_navigate: Optional[Callable[[str], None]] = None,
        on_error: Optional[Callable[[str], None]] = None,
        allows_back_forward: bool = True,
        allows_magnification: bool = True,
        # View modifiers passed through
        **kwargs: Any,
    ):
        """Initialize a WebView.

        Args:
            url: URL to load. Mutually exclusive with html.
            html: Raw HTML content to display. Mutually exclusive with url.
            base_url: Base URL for resolving relative links in HTML content.
            on_load: Callback when page finishes loading.
            on_navigate: Callback when navigation occurs, receives the new URL.
            on_error: Callback when loading fails, receives error message.
            allows_back_forward: Whether back/forward navigation is enabled.
            allows_magnification: Whether pinch-to-zoom is enabled.
            **kwargs: Standard view modifiers including:
                - width, height: WebView dimensions
                - corner_radius: Rounded corners
                - opacity: Transparency (0.0 to 1.0)

        Example:
            Create a web view loading a URL::

                nib.WebView(
                    url="https://example.com",
                    width=400,
                    height=300,
                )
        """
        super().__init__(**kwargs)
        self._url = url
        self._html = html
        self._base_url = base_url
        self._on_load = on_load
        self._on_navigate = on_navigate
        self._on_error = on_error
        self._allows_back_forward = allows_back_forward
        self._allows_magnification = allows_magnification

    @property
    def url(self) -> Optional[str]:
        """Get the current URL."""
        return self._url

    @url.setter
    def url(self, value: Optional[str]) -> None:
        """Set URL and trigger navigation."""
        self._url = value
        self._html = None  # Clear HTML when setting URL
        self._trigger_update()

    @property
    def html(self) -> Optional[str]:
        """Get the current HTML content."""
        return self._html

    @html.setter
    def html(self, value: Optional[str]) -> None:
        """Set HTML content and trigger re-render."""
        self._html = value
        self._url = None  # Clear URL when setting HTML
        self._trigger_update()

    def load_url(self, url: str) -> None:
        """Load a new URL.

        Args:
            url: The URL to load.
        """
        self.url = url

    def load_html(self, html: str, base_url: Optional[str] = None) -> None:
        """Load HTML content.

        Args:
            html: The HTML content to display.
            base_url: Base URL for resolving relative links.
        """
        self._base_url = base_url
        self.html = html

    def reload(self) -> None:
        """Reload the current page."""
        if self._app:
            self._app._send_action(self._id, "reload")

    def go_back(self) -> None:
        """Navigate back in history."""
        if self._app:
            self._app._send_action(self._id, "goBack")

    def go_forward(self) -> None:
        """Navigate forward in history."""
        if self._app:
            self._app._send_action(self._id, "goForward")

    def evaluate_js(
        self,
        script: str,
        callback: Optional[Callable[[Optional[str]], None]] = None,
    ) -> None:
        """Evaluate JavaScript in the web view.

        Args:
            script: JavaScript code to execute.
            callback: Optional callback to receive the result.
        """
        if self._app:
            self._app._send_action(self._id, "evaluateJS", {"script": script})
            # TODO: Handle callback when result comes back

    def _get_props(self) -> dict:
        props = {}

        if self._url:
            props["url"] = self._url
        elif self._html:
            props["html"] = self._html
            if self._base_url:
                props["baseURL"] = self._base_url

        props["allowsBackForward"] = self._allows_back_forward
        props["allowsMagnification"] = self._allows_magnification

        return props
