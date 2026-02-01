import SwiftUI
import WebKit

// MARK: - WebView Builder

extension DynamicView {
    @ViewBuilder
    func buildWebView() -> some View {
        let props = node.props
        let nodeId = node.id

        if let urlString = props.url, let url = URL(string: urlString) {
            NibWebView(
                nodeId: nodeId,
                url: url,
                html: nil,
                baseURL: nil,
                allowsBackForward: props.allowsBackForward ?? true,
                allowsMagnification: props.allowsMagnification ?? true
            )
        } else if let html = props.html {
            let baseURL = props.baseURL.flatMap { URL(string: $0) }
            NibWebView(
                nodeId: nodeId,
                url: nil,
                html: html,
                baseURL: baseURL,
                allowsBackForward: props.allowsBackForward ?? true,
                allowsMagnification: props.allowsMagnification ?? true
            )
        } else {
            webViewPlaceholder("No content")
        }
    }

    @ViewBuilder
    private func webViewPlaceholder(_ message: String) -> some View {
        ZStack {
            Rectangle()
                .fill(Color(NSColor.controlBackgroundColor))
            VStack(spacing: 8) {
                Image(systemName: "globe")
                    .font(.largeTitle)
                    .foregroundColor(.gray)
                Text(message)
                    .font(.caption)
                    .foregroundColor(.gray)
            }
        }
    }
}

// MARK: - WKWebView Wrapper

struct NibWebView: NSViewRepresentable {
    let nodeId: String
    let url: URL?
    let html: String?
    let baseURL: URL?
    let allowsBackForward: Bool
    let allowsMagnification: Bool

    func makeNSView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.preferences.isElementFullscreenEnabled = true

        let webView = WKWebView(frame: .zero, configuration: config)
        webView.allowsBackForwardNavigationGestures = allowsBackForward
        webView.allowsMagnification = allowsMagnification

        // Set navigation delegate for callbacks
        webView.navigationDelegate = context.coordinator

        // Store reference in coordinator for actions
        context.coordinator.webView = webView
        context.coordinator.nodeId = nodeId

        // Register with action registry
        ViewActionRegistry.shared.register(nodeId: nodeId, handler: context.coordinator)

        // Prevent intrinsic size from affecting popover layout
        webView.setContentHuggingPriority(.defaultLow, for: .horizontal)
        webView.setContentHuggingPriority(.defaultLow, for: .vertical)
        webView.setContentCompressionResistancePriority(.defaultLow, for: .horizontal)
        webView.setContentCompressionResistancePriority(.defaultLow, for: .vertical)

        // Load initial content
        loadContent(in: webView)

        return webView
    }

    func updateNSView(_ webView: WKWebView, context: Context) {
        webView.allowsBackForwardNavigationGestures = allowsBackForward
        webView.allowsMagnification = allowsMagnification

        // Update nodeId in case it changed
        if context.coordinator.nodeId != nodeId {
            ViewActionRegistry.shared.unregister(nodeId: context.coordinator.nodeId)
            context.coordinator.nodeId = nodeId
            ViewActionRegistry.shared.register(nodeId: nodeId, handler: context.coordinator)
        }

        // Check if content changed
        let currentURL = webView.url?.absoluteString
        let newURL = url?.absoluteString

        if let newURL = newURL, currentURL != newURL {
            loadContent(in: webView)
        } else if html != nil && currentURL == nil {
            // HTML content and no URL loaded
            loadContent(in: webView)
        }
    }

    private func loadContent(in webView: WKWebView) {
        if let url = url {
            let request = URLRequest(url: url)
            webView.load(request)
        } else if let html = html {
            webView.loadHTMLString(html, baseURL: baseURL)
        }
    }

    static func dismantleNSView(_ webView: WKWebView, coordinator: Coordinator) {
        // Unregister from action registry
        ViewActionRegistry.shared.unregister(nodeId: coordinator.nodeId)

        webView.stopLoading()
        webView.navigationDelegate = nil
        coordinator.webView = nil
    }

    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    class Coordinator: NSObject, WKNavigationDelegate, ActionHandler {
        weak var webView: WKWebView?
        var nodeId: String = ""

        // MARK: - ActionHandler

        func handleAction(_ action: String, params: [String: AnyCodable]?) {
            guard let webView = webView else {
                debugPrint("WebView Coordinator: webView is nil")
                return
            }

            debugPrint("WebView handling action:", action)

            switch action {
            case "reload":
                webView.reload()
            case "goBack":
                webView.goBack()
            case "goForward":
                webView.goForward()
            case "evaluateJS":
                if let script = params?["script"]?.value as? String {
                    webView.evaluateJavaScript(script) { result, error in
                        if let error = error {
                            debugPrint("JS evaluation error:", error.localizedDescription)
                        } else {
                            debugPrint("JS result:", result ?? "nil")
                        }
                    }
                }
            case "loadURL":
                if let urlString = params?["url"]?.value as? String,
                   let url = URL(string: urlString) {
                    webView.load(URLRequest(url: url))
                }
            case "loadHTML":
                if let html = params?["html"]?.value as? String {
                    let baseURL = (params?["baseURL"]?.value as? String).flatMap { URL(string: $0) }
                    webView.loadHTMLString(html, baseURL: baseURL)
                }
            case "stopLoading":
                webView.stopLoading()
            default:
                debugPrint("Unknown WebView action:", action)
            }
        }

        // MARK: - WKNavigationDelegate

        func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
            debugPrint("WebView loaded: \(webView.url?.absoluteString ?? "unknown")")
        }

        func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
            debugPrint("WebView error: \(error.localizedDescription)")
        }

        func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) {
            debugPrint("WebView provisional error: \(error.localizedDescription)")
        }
    }
}
