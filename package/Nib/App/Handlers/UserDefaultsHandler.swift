import Foundation

/// Handles UserDefaults get/set/remove operations
struct UserDefaultsHandler {
    /// Background queue for UserDefaults operations to avoid blocking the main thread
    private static let queue = DispatchQueue(label: "nib.userdefaults", qos: .userInitiated)

    /// Get the UserDefaults instance for the current app.
    /// Uses NIB_BUNDLE_ID env var (dev mode) or Bundle.main.bundleIdentifier (bundled mode).
    private static func getDefaults() -> UserDefaults {
        // In dev mode, NIB_BUNDLE_ID is passed from Python
        // In bundled mode, use the app's actual bundle identifier
        let bundleId = ProcessInfo.processInfo.environment["NIB_BUNDLE_ID"]
            ?? Bundle.main.bundleIdentifier
            ?? "com.nib.app"

        // Use suite name to ensure each app has its own storage
        return UserDefaults(suiteName: bundleId) ?? UserDefaults.standard
    }

    static func handle(_ payload: NibMessage.UserDefaultsPayload, sendEvent: @escaping (String, String) -> Void) {
        // Handle on background queue to avoid blocking UI
        queue.async {
            handleSync(payload, sendEvent: sendEvent)
        }
    }

    private static func handleSync(_ payload: NibMessage.UserDefaultsPayload, sendEvent: @escaping (String, String) -> Void) {
        let defaults = getDefaults()
        let requestId = payload.requestId ?? ""

        switch payload.action {
        case "get":
            guard let key = payload.key else {
                sendEvent(requestId, "userDefaults:error:key required")
                return
            }
            let value = defaults.object(forKey: key)
            let response = encodeValue(value)
            sendEvent(requestId, "userDefaults:get:\(response)")
            debugPrint("UserDefaults get:", key, "=", response)

        case "set":
            guard let key = payload.key else {
                debugPrint("UserDefaults set: key required")
                return
            }
            // Prefer valueJson (JSON-encoded string) over value (AnyCodable, unreliable with MessagePack)
            if let jsonString = payload.valueJson {
                if let jsonData = jsonString.data(using: .utf8),
                   let jsonValue = try? JSONSerialization.jsonObject(with: jsonData, options: .fragmentsAllowed) {
                    defaults.set(jsonValue, forKey: key)
                    debugPrint("UserDefaults set:", key, "=", jsonValue)
                } else {
                    // If JSON parsing fails, store as string
                    defaults.set(jsonString, forKey: key)
                    debugPrint("UserDefaults set (string):", key, "=", jsonString)
                }
            } else if let anyCodable = payload.value {
                // Fallback to legacy AnyCodable
                defaults.set(anyCodable.value, forKey: key)
                debugPrint("UserDefaults set (legacy):", key, "=", anyCodable.value)
            } else {
                defaults.removeObject(forKey: key)
                debugPrint("UserDefaults removed:", key)
            }

        case "remove":
            guard let key = payload.key else {
                debugPrint("UserDefaults remove: key required")
                return
            }
            defaults.removeObject(forKey: key)
            debugPrint("UserDefaults removed:", key)

        case "clear":
            // Clear all keys for this app's UserDefaults suite
            let bundleId = ProcessInfo.processInfo.environment["NIB_BUNDLE_ID"]
                ?? Bundle.main.bundleIdentifier
                ?? "com.nib.app"
            defaults.removePersistentDomain(forName: bundleId)
            debugPrint("UserDefaults cleared for domain:", bundleId)

        case "containsKey":
            guard let key = payload.key else {
                sendEvent(requestId, "userDefaults:containsKey:false")
                return
            }
            let exists = defaults.object(forKey: key) != nil
            sendEvent(requestId, "userDefaults:containsKey:\(exists)")
            debugPrint("UserDefaults containsKey:", key, "=", exists)

        case "getKeys":
            let prefix = payload.prefix ?? ""
            let allKeys = defaults.dictionaryRepresentation().keys
            let matchingKeys = allKeys.filter { $0.hasPrefix(prefix) }
            let keysString = matchingKeys.joined(separator: "\n")
            sendEvent(requestId, "userDefaults:getKeys:\(keysString)")
            debugPrint("UserDefaults getKeys with prefix:", prefix, "found:", matchingKeys.count)

        default:
            debugPrint("Unknown userDefaults action:", payload.action)
        }
    }

    private static func encodeValue(_ value: Any?) -> String {
        guard let value = value else { return "null" }

        switch value {
        case let string as String:
            // Escape special characters for safe transmission
            let escaped = string
                .replacingOccurrences(of: "\\", with: "\\\\")
                .replacingOccurrences(of: "\n", with: "\\n")
                .replacingOccurrences(of: ":", with: "\\:")
            return "string:\(escaped)"
        case let number as NSNumber:
            // Check if it's a boolean
            if CFGetTypeID(number) == CFBooleanGetTypeID() {
                return "bool:\(number.boolValue)"
            }
            // Check if it's an integer or floating point
            if floor(number.doubleValue) == number.doubleValue {
                return "int:\(number.intValue)"
            }
            return "float:\(number.doubleValue)"
        case let data as Data:
            return "data:\(data.base64EncodedString())"
        case let array as [Any]:
            // Encode array as JSON
            if let jsonData = try? JSONSerialization.data(withJSONObject: array),
               let jsonString = String(data: jsonData, encoding: .utf8) {
                return "array:\(jsonString)"
            }
            return "null"
        case let dict as [String: Any]:
            // Encode dictionary as JSON
            if let jsonData = try? JSONSerialization.data(withJSONObject: dict),
               let jsonString = String(data: jsonData, encoding: .utf8) {
                return "dict:\(jsonString)"
            }
            return "null"
        default:
            return "null"
        }
    }
}
