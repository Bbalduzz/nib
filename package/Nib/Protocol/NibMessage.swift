import Foundation

enum NibMessage {
    case render(RenderPayload)
    case patch(PatchPayload)
    case notify(NotifyPayload)
    case clipboard(ClipboardPayload)
    case fileDialog(FileDialogPayload)
    case userDefaults(UserDefaultsPayload)
    case service(ServicePayload)
    case action(ActionPayload)
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

    struct ServicePayload: Codable {
        let service: String  // "battery", "connectivity", "screen"
        let action: String   // "status", "info", "setBrightness", etc.
        let requestId: String
        let params: [String: AnyCodable]?
    }

    struct ActionPayload: Codable {
        let nodeId: String   // Target view node ID
        let action: String   // Action to perform (e.g., "reload", "goBack", "goForward")
        let params: [String: AnyCodable]?
    }

    struct MenuItemConfig: Codable {
        let id: String
        let title: String?
        let icon: MenuIconConfig?
        let content: ViewNode?  // Custom view content for rich menu items
        let height: CGFloat?    // Custom height for content-based items
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
        case view(ViewNode)  // Any SwiftUI view

        struct MenuIconFullConfig: Codable, Equatable {
            let name: String
            let weight: String?
            let scale: String?
            let renderingMode: String?
            let color: String?
        }

        private struct ViewWrapper: Codable {
            let view: ViewNode
        }

        init(from decoder: Decoder) throws {
            let container = try decoder.singleValueContainer()
            // Try string first
            if let name = try? container.decode(String.self) {
                self = .name(name)
                return
            }
            // Try view wrapper (dict with "view" key)
            if let wrapper = try? container.decode(ViewWrapper.self) {
                self = .view(wrapper.view)
                return
            }
            // Try full config
            if let config = try? container.decode(MenuIconFullConfig.self) {
                self = .config(config)
                return
            }
            throw DecodingError.typeMismatch(
                MenuIconConfig.self,
                DecodingError.Context(codingPath: decoder.codingPath, debugDescription: "Expected String, MenuIconFullConfig, or ViewWrapper")
            )
        }

        func encode(to encoder: Encoder) throws {
            var container = encoder.singleValueContainer()
            switch self {
            case .name(let name):
                try container.encode(name)
            case .config(let config):
                try container.encode(config)
            case .view(let viewNode):
                try container.encode(ViewWrapper(view: viewNode))
            }
        }

        var symbolName: String? {
            switch self {
            case .name(let name): return name
            case .config(let config): return config.name
            case .view: return nil
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

struct NibServiceResponse: Codable {
    let type: String
    let service: String
    let requestId: String
    let data: ServiceResponseData

    init(service: String, requestId: String, data: ServiceResponseData) {
        self.type = "serviceResponse"
        self.service = service
        self.requestId = requestId
        self.data = data
    }

    struct ServiceResponseData: Codable {
        // Battery - basic
        var level: Double?
        var isCharging: Bool?
        var state: String?
        var hasBattery: Bool?
        var isLowPowerMode: Bool?
        var timeRemaining: Int?

        // Battery - extended status
        var currentCapacity: Int?
        var maxCapacity: Int?
        var isPluggedIn: Bool?
        var timeToEmpty: Int?
        var timeToEmptyFormatted: String?
        var timeToFullCharge: Int?
        var timeToFullChargeFormatted: String?
        var powerSource: String?
        var batteryType: String?
        var serialNumber: String?
        var isCharged: Bool?
        var isFinishingCharge: Bool?
        var thermalState: String?
        var amperage: Int?
        var voltage: Double?
        var wattage: Double?

        // Battery - health
        var cycleCount: Int?
        var designCapacity: Int?
        var healthPercent: Double?
        var temperatureCelsius: Double?
        var temperatureFahrenheit: Double?
        var manufactureDate: String?
        var manufacturer: String?
        var deviceName: String?
        var condition: String?
        var optimizedChargingEngaged: Bool?

        // Battery - thermal
        var thermalStateRaw: Int?
        var recommendation: String?

        // Battery - sleep
        var assertionID: Int?

        // Battery - history
        var note: String?
        var systemUptime: Double?
        var systemUptimeFormatted: String?

        // Connectivity
        var isConnected: Bool?
        var connectionType: String?
        var isExpensive: Bool?
        var isConstrained: Bool?
        var ssid: String?
        var interfaceName: String?

        // Screen - basic
        var brightness: Double?
        var isBuiltin: Bool?
        var width: Double?
        var height: Double?
        var scale: Double?

        // Screen - extended
        var visibleWidth: Double?
        var visibleHeight: Double?
        var displayID: Int?
        var name: String?
        var refreshRate: Double?
        var nativeWidth: Int?
        var nativeHeight: Int?
        var colorSpace: String?
        var colorDepth: Int?
        var availableResolutionsJson: String?  // JSON-encoded array
        var displaysJson: String?              // JSON-encoded array
        var count: Int?

        // Screen - dark mode
        var isDarkMode: Bool?
        var appearanceName: String?

        // Screen - color profile
        var colorSpaceName: String?
        var colorComponentCount: Int?
        var iccProfileSize: Int?

        // Generic
        var success: Bool?
        var errorMessage: String?

        // Keychain
        var password: String?
        var exists: Bool?

        // LaunchAtLogin
        var enabled: Bool?

        // Camera
        var devices: [CameraDevice]?
        var imageData: Data?
        var imageWidth: Int?
        var imageHeight: Int?
        var imageFormat: String?
        var isStreaming: Bool?
        var isStreamFrame: Bool?

        private enum CodingKeys: String, CodingKey {
            // Battery
            case level, isCharging, state, hasBattery, isLowPowerMode, timeRemaining
            case currentCapacity, maxCapacity, isPluggedIn
            case timeToEmpty, timeToEmptyFormatted, timeToFullCharge, timeToFullChargeFormatted
            case powerSource, batteryType, serialNumber, isCharged, isFinishingCharge
            case thermalState, amperage, voltage, wattage
            case cycleCount, designCapacity, healthPercent
            case temperatureCelsius, temperatureFahrenheit, manufactureDate
            case manufacturer, deviceName, condition, optimizedChargingEngaged
            case thermalStateRaw, recommendation, assertionID
            case note, systemUptime, systemUptimeFormatted
            // Connectivity
            case isConnected, connectionType = "type", isExpensive, isConstrained, ssid, interfaceName
            case brightness, isBuiltin, width, height, scale
            case visibleWidth, visibleHeight, displayID, name, refreshRate
            case nativeWidth, nativeHeight, colorSpace, colorDepth
            case availableResolutionsJson, displaysJson, count
            case isDarkMode, appearanceName
            case colorSpaceName, colorComponentCount, iccProfileSize
            case success, errorMessage
            case password, exists
            case enabled
            case devices, imageData, imageWidth, imageHeight, imageFormat, isStreaming, isStreamFrame
        }
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
        // For service
        let service: String?
        let params: [String: AnyCodable]?
        // For action
        let nodeId: String?
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
