import AppKit
import UniformTypeIdentifiers

/// Handles open/save file dialog operations
struct FileDialogHandler {
    static func handle(_ payload: NibMessage.FileDialogPayload, sendEvent: @escaping (String, String) -> Void) {
        switch payload.action {
        case "open":
            handleOpenDialog(payload, sendEvent: sendEvent)
        case "save":
            handleSaveDialog(payload, sendEvent: sendEvent)
        default:
            debugPrint("Unknown fileDialog action:", payload.action)
        }
    }

    private static func handleOpenDialog(_ payload: NibMessage.FileDialogPayload, sendEvent: @escaping (String, String) -> Void) {
        let panel = NSOpenPanel()
        panel.title = payload.title ?? "Open File"
        panel.allowsMultipleSelection = payload.multiple ?? false
        panel.canChooseDirectories = false
        panel.canChooseFiles = true

        if let directory = payload.directory {
            panel.directoryURL = URL(fileURLWithPath: directory)
        }

        if let types = payload.types, !types.isEmpty {
            panel.allowedContentTypes = types.compactMap { ext in
                UTType(filenameExtension: ext)
            }
        }

        let response = panel.runModal()
        if response == .OK {
            let paths = panel.urls.map { $0.path }.joined(separator: "\n")
            sendEvent(payload.requestId, "fileDialog:\(paths)")
        } else {
            sendEvent(payload.requestId, "fileDialog:")
        }
    }

    private static func handleSaveDialog(_ payload: NibMessage.FileDialogPayload, sendEvent: @escaping (String, String) -> Void) {
        let panel = NSSavePanel()
        panel.title = payload.title ?? "Save File"

        if let directory = payload.directory {
            panel.directoryURL = URL(fileURLWithPath: directory)
        }
        if let defaultName = payload.defaultName {
            panel.nameFieldStringValue = defaultName
        }

        if let types = payload.types, !types.isEmpty {
            panel.allowedContentTypes = types.compactMap { ext in
                UTType(filenameExtension: ext)
            }
        }

        let response = panel.runModal()
        if response == .OK, let url = panel.url {
            sendEvent(payload.requestId, "fileDialog:\(url.path)")
        } else {
            sendEvent(payload.requestId, "fileDialog:")
        }
    }
}
