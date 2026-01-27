import Foundation

enum NibMessage {
    case render(RenderPayload)
    case patch(PatchPayload)
    case notify(NotifyPayload)
    case clipboard(ClipboardPayload)
    case fileDialog(FileDialogPayload)
    case userDefaults(UserDefaultsPayload)
    case quit

    struct WindowConfig: Codable {
        let width: CGFloat?
        let height: CGFloat?
    }

    struct RenderPayload: Codable {
        let root: ViewNode?
        let statusBar: StatusBarConfig?
        let window: WindowConfig?
        let menu: [MenuItemConfig]?
        let hotkeys: [String]?
        let fonts: [String: String]?  // Font name -> path or URL

        struct StatusBarConfig: Codable {
            let icon: MenuIconConfig?
            let title: String?
        }
    }

    struct PatchPayload: Codable {
        let patches: [Patch]
        let statusBar: StatusBarConfig?
        let window: WindowConfig?

        struct StatusBarConfig: Codable {
            let icon: MenuIconConfig?
            let title: String?
        }
    }

    struct Patch: Codable {
        let op: String        // "replace", "props", "modifiers", "insert", "remove"
        let id: String
        let node: ViewNode?   // For replace/insert
        let props: [String: AnyCodable]?  // For props update
        let modifiers: [ViewNode.ViewModifier]?  // For modifiers update
    }

    struct NotifyPayload: Codable {
        let title: String
        let body: String?
        let subtitle: String?
        let sound: Bool?
        let identifier: String?
    }

    struct ClipboardPayload: Codable {
        let action: String  // "read" or "write"
        let content: String?
        let requestId: String?
    }

    struct FileDialogPayload: Codable {
        let action: String  // "open" or "save"
        let title: String?
        let types: [String]?
        let multiple: Bool?
        let directory: String?
        let defaultName: String?
        let requestId: String
    }

    struct UserDefaultsPayload: Codable {
        let action: String  // "get", "set", "remove", "clear", "containsKey", "getKeys"
        let key: String?
        let value: AnyCodable?
        let prefix: String?
        let requestId: String?
    }

    struct MenuItemConfig: Codable {
        let id: String
        let title: String?
        let icon: MenuIconConfig?
        let divider: Bool?
        let children: [MenuItemConfig]?
        let shortcut: String?
        let state: String?
        let badge: String?
        let enabled: Bool?
    }

    /// Icon configuration that can be a simple string or a full SFSymbol config
    enum MenuIconConfig: Codable, Equatable {
        case name(String)
        case config(MenuIconFullConfig)

        struct MenuIconFullConfig: Codable, Equatable {
            let name: String
            let weight: String?
            let scale: String?
            let renderingMode: String?
            let color: String?
        }

        init(from decoder: Decoder) throws {
            let container = try decoder.singleValueContainer()
            // Try string first
            if let name = try? container.decode(String.self) {
                self = .name(name)
                return
            }
            // Try full config
            if let config = try? container.decode(MenuIconFullConfig.self) {
                self = .config(config)
                return
            }
            throw DecodingError.typeMismatch(
                MenuIconConfig.self,
                DecodingError.Context(codingPath: decoder.codingPath, debugDescription: "Expected String or MenuIconFullConfig")
            )
        }

        func encode(to encoder: Encoder) throws {
            var container = encoder.singleValueContainer()
            switch self {
            case .name(let name):
                try container.encode(name)
            case .config(let config):
                try container.encode(config)
            }
        }

        var symbolName: String {
            switch self {
            case .name(let name): return name
            case .config(let config): return config.name
            }
        }
    }
}

struct NibEvent: Codable {
    let type: String
    let nodeId: String
    let event: String

    init(nodeId: String, event: String) {
        self.type = "event"
        self.nodeId = nodeId
        self.event = event
    }
}

// Raw message structure for decoding
struct RawMessage: Codable {
    let type: String
    let payload: Payload?

    struct Payload: Codable {
        // For render
        let root: ViewNode?
        let menu: [NibMessage.MenuItemConfig]?
        let hotkeys: [String]?
        let fonts: [String: String]?  // Font name -> path or URL
        // For patch
        let patches: [NibMessage.Patch]?
        // For notify
        let title: String?
        let body: String?
        let subtitle: String?
        let sound: Bool?
        let identifier: String?
        // For clipboard
        let action: String?
        let content: String?
        let requestId: String?
        // For fileDialog
        let types: [String]?
        let multiple: Bool?
        let directory: String?
        let defaultName: String?
        // For userDefaults
        let key: String?
        let value: AnyCodable?
        let prefix: String?
        // Shared
        let statusBar: StatusBarConfig?
        let window: WindowConfig?

        struct StatusBarConfig: Codable {
            let icon: NibMessage.MenuIconConfig?
            let title: String?
        }

        struct WindowConfig: Codable {
            let width: CGFloat?
            let height: CGFloat?
        }
    }
}

// AnyCodable for dynamic values
struct AnyCodable: Codable {
    let value: Any

    init(_ value: Any) {
        self.value = value
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()

        if let intVal = try? container.decode(Int.self) {
            value = intVal
        } else if let doubleVal = try? container.decode(Double.self) {
            value = doubleVal
        } else if let boolVal = try? container.decode(Bool.self) {
            value = boolVal
        } else if let stringVal = try? container.decode(String.self) {
            value = stringVal
        } else if let arrayVal = try? container.decode([AnyCodable].self) {
            value = arrayVal.map { $0.value }
        } else if let dictVal = try? container.decode([String: AnyCodable].self) {
            value = dictVal.mapValues { $0.value }
        } else {
            value = NSNull()
        }
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        switch value {
        case let intVal as Int:
            try container.encode(intVal)
        case let doubleVal as Double:
            try container.encode(doubleVal)
        case let boolVal as Bool:
            try container.encode(boolVal)
        case let stringVal as String:
            try container.encode(stringVal)
        default:
            try container.encodeNil()
        }
    }
}

extension NibMessage {
    static func decode(from data: Data) throws -> NibMessage {
        let decoder = JSONDecoder()
        let raw = try decoder.decode(RawMessage.self, from: data)

        switch raw.type {
        case "render":
            let payload = RenderPayload(
                root: raw.payload?.root,
                statusBar: raw.payload?.statusBar.map {
                    RenderPayload.StatusBarConfig(icon: $0.icon, title: $0.title)
                },
                window: raw.payload?.window.map {
                    WindowConfig(width: $0.width, height: $0.height)
                },
                menu: raw.payload?.menu,
                hotkeys: raw.payload?.hotkeys,
                fonts: raw.payload?.fonts
            )
            return .render(payload)
        case "patch":
            let payload = PatchPayload(
                patches: raw.payload?.patches ?? [],
                statusBar: raw.payload?.statusBar.map {
                    PatchPayload.StatusBarConfig(icon: $0.icon, title: $0.title)
                },
                window: raw.payload?.window.map {
                    WindowConfig(width: $0.width, height: $0.height)
                }
            )
            return .patch(payload)
        case "notify":
            guard let title = raw.payload?.title else {
                throw NibMessageError.decodingFailed("notify requires title")
            }
            let payload = NotifyPayload(
                title: title,
                body: raw.payload?.body,
                subtitle: raw.payload?.subtitle,
                sound: raw.payload?.sound,
                identifier: raw.payload?.identifier
            )
            return .notify(payload)
        case "clipboard":
            guard let action = raw.payload?.action else {
                throw NibMessageError.decodingFailed("clipboard requires action")
            }
            let payload = ClipboardPayload(
                action: action,
                content: raw.payload?.content,
                requestId: raw.payload?.requestId
            )
            return .clipboard(payload)
        case "fileDialog":
            guard let action = raw.payload?.action,
                  let requestId = raw.payload?.requestId else {
                throw NibMessageError.decodingFailed("fileDialog requires action and requestId")
            }
            let payload = FileDialogPayload(
                action: action,
                title: raw.payload?.title,
                types: raw.payload?.types,
                multiple: raw.payload?.multiple,
                directory: raw.payload?.directory,
                defaultName: raw.payload?.defaultName,
                requestId: requestId
            )
            return .fileDialog(payload)
        case "userDefaults":
            guard let action = raw.payload?.action else {
                throw NibMessageError.decodingFailed("userDefaults requires action")
            }
            let payload = UserDefaultsPayload(
                action: action,
                key: raw.payload?.key,
                value: raw.payload?.value,
                prefix: raw.payload?.prefix,
                requestId: raw.payload?.requestId
            )
            return .userDefaults(payload)
        case "quit":
            return .quit
        default:
            throw NibMessageError.unknownType(raw.type)
        }
    }
}

enum NibMessageError: Error {
    case unknownType(String)
    case decodingFailed(String)
}
