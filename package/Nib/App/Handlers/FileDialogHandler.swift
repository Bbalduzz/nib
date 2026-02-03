import AppKit
import UniformTypeIdentifiers

/// Handles file picker and save dialog operations
struct FileDialogHandler {
    typealias SendResponse = (NibMessage.FileDialogResponse) -> Void

    static func handle(_ payload: NibMessage.FileDialogPayload, sendResponse: @escaping SendResponse) {
        switch payload.action {
        case "pickFiles":
            handlePickFiles(payload, sendResponse: sendResponse)
        case "pickDirectory":
            handlePickDirectory(payload, sendResponse: sendResponse)
        case "saveFile":
            handleSaveFile(payload, sendResponse: sendResponse)
        default:
            debugPrint("Unknown fileDialog action:", payload.action)
            sendResponse(NibMessage.FileDialogResponse(
                type: "fileDialogResponse",
                requestId: payload.requestId,
                cancelled: true,
                files: nil,
                directories: nil,
                saveResult: nil
            ))
        }
    }

    // MARK: - Pick Files

    private static func handlePickFiles(_ payload: NibMessage.FileDialogPayload, sendResponse: @escaping SendResponse) {
        let panel = NSOpenPanel()

        // Common configuration
        configureCommon(panel: panel, payload: payload)

        // File picker specific
        panel.canChooseFiles = true
        panel.canChooseDirectories = false
        panel.allowsMultipleSelection = payload.multiple ?? false

        // File type filtering
        if let extensions = payload.extensions, !extensions.isEmpty {
            panel.allowedContentTypes = extensions.compactMap { UTType(filenameExtension: $0) }
        } else if let uttypes = payload.uttypes, !uttypes.isEmpty {
            panel.allowedContentTypes = uttypes.compactMap { UTType($0) }
        }

        if let allowsOther = payload.allowsOtherFileTypes {
            panel.allowsOtherFileTypes = allowsOther
        }

        if let treatsPackages = payload.treatsPackagesAsDirectories {
            panel.treatsFilePackagesAsDirectories = treatsPackages
        }

        let response = panel.runModal()
        if response == .OK {
            let files = panel.urls.map { getFileInfo(url: $0) }
            sendResponse(NibMessage.FileDialogResponse(
                type: "fileDialogResponse",
                requestId: payload.requestId,
                cancelled: false,
                files: files,
                directories: nil,
                saveResult: nil
            ))
        } else {
            sendResponse(NibMessage.FileDialogResponse(
                type: "fileDialogResponse",
                requestId: payload.requestId,
                cancelled: true,
                files: nil,
                directories: nil,
                saveResult: nil
            ))
        }
    }

    // MARK: - Pick Directory

    private static func handlePickDirectory(_ payload: NibMessage.FileDialogPayload, sendResponse: @escaping SendResponse) {
        let panel = NSOpenPanel()

        // Common configuration
        configureCommon(panel: panel, payload: payload)

        // Directory picker specific
        panel.canChooseFiles = false
        panel.canChooseDirectories = true
        panel.allowsMultipleSelection = payload.multiple ?? false

        if let canCreate = payload.canCreateDirectories {
            panel.canCreateDirectories = canCreate
        }

        let response = panel.runModal()
        if response == .OK {
            let directories = panel.urls.map { $0.path }
            sendResponse(NibMessage.FileDialogResponse(
                type: "fileDialogResponse",
                requestId: payload.requestId,
                cancelled: false,
                files: nil,
                directories: directories,
                saveResult: nil
            ))
        } else {
            sendResponse(NibMessage.FileDialogResponse(
                type: "fileDialogResponse",
                requestId: payload.requestId,
                cancelled: true,
                files: nil,
                directories: nil,
                saveResult: nil
            ))
        }
    }

    // MARK: - Save File

    private static func handleSaveFile(_ payload: NibMessage.FileDialogPayload, sendResponse: @escaping SendResponse) {
        let panel = NSSavePanel()

        // Common configuration
        configureCommon(panel: panel, payload: payload)

        // Save dialog specific
        if let filename = payload.filename {
            panel.nameFieldStringValue = filename
        }

        if let nameFieldLabel = payload.nameFieldLabel {
            panel.nameFieldLabel = nameFieldLabel
        }

        if let showsTagField = payload.showsTagField {
            panel.showsTagField = showsTagField
        }

        if let canCreate = payload.canCreateDirectories {
            panel.canCreateDirectories = canCreate
        }

        // File type filtering
        if let extensions = payload.extensions, !extensions.isEmpty {
            panel.allowedContentTypes = extensions.compactMap { UTType(filenameExtension: $0) }
        } else if let uttypes = payload.uttypes, !uttypes.isEmpty {
            panel.allowedContentTypes = uttypes.compactMap { UTType($0) }
        }

        if let allowsOther = payload.allowsOtherFileTypes {
            panel.allowsOtherFileTypes = allowsOther
        }

        let response = panel.runModal()
        if response == .OK, let url = panel.url {
            // Get tags from panel
            let tags = panel.tagNames ?? []
            sendResponse(NibMessage.FileDialogResponse(
                type: "fileDialogResponse",
                requestId: payload.requestId,
                cancelled: false,
                files: nil,
                directories: nil,
                saveResult: NibMessage.SaveResultInfo(path: url.path, tags: tags)
            ))
        } else {
            sendResponse(NibMessage.FileDialogResponse(
                type: "fileDialogResponse",
                requestId: payload.requestId,
                cancelled: true,
                files: nil,
                directories: nil,
                saveResult: nil
            ))
        }
    }

    // MARK: - Common Configuration

    private static func configureCommon(panel: NSSavePanel, payload: NibMessage.FileDialogPayload) {
        if let title = payload.title {
            panel.title = title
        }

        if let message = payload.message {
            panel.message = message
        }

        if let buttonLabel = payload.buttonLabel {
            panel.prompt = buttonLabel
        }

        if let directory = payload.directory {
            panel.directoryURL = URL(fileURLWithPath: directory)
        }

        if let showsHidden = payload.showsHiddenFiles {
            panel.showsHiddenFiles = showsHidden
        }

        // resolvesAliases is only available on NSOpenPanel
        if let panel = panel as? NSOpenPanel, let resolvesAliases = payload.resolvesAliases {
            panel.resolvesAliases = resolvesAliases
        }
    }

    // MARK: - File Info Helpers

    private static func getFileInfo(url: URL) -> NibMessage.PickedFileInfo {
        let name = url.lastPathComponent
        let path = url.path

        // Get file size
        var size: Int64 = 0
        if let attrs = try? FileManager.default.attributesOfItem(atPath: path),
           let fileSize = attrs[.size] as? Int64 {
            size = fileSize
        }

        // Get UTI
        var uti: String? = nil
        if let typeIdentifier = try? url.resourceValues(forKeys: [.typeIdentifierKey]).typeIdentifier {
            uti = typeIdentifier
        }

        // Get Finder tags
        var tags: [String] = []
        if let tagNames = try? url.resourceValues(forKeys: [.tagNamesKey]).tagNames {
            tags = tagNames
        }

        return NibMessage.PickedFileInfo(
            name: name,
            path: path,
            size: size,
            uti: uti,
            tags: tags
        )
    }
}
