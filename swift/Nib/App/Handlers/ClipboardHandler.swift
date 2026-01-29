import AppKit

/// Handles clipboard read/write operations
struct ClipboardHandler {
    static func handle(_ payload: NibMessage.ClipboardPayload, sendEvent: @escaping (String, String) -> Void) {
        switch payload.action {
        case "write":
            if let content = payload.content {
                NSPasteboard.general.clearContents()
                NSPasteboard.general.setString(content, forType: .string)
                debugPrint("Clipboard write successful")
            }
        case "read":
            let content = NSPasteboard.general.string(forType: .string) ?? ""
            let requestId = payload.requestId ?? ""
            sendEvent(requestId, "clipboard:\(content)")
            debugPrint("Clipboard read:", content.prefix(50))
        default:
            debugPrint("Unknown clipboard action:", payload.action)
        }
    }
}
