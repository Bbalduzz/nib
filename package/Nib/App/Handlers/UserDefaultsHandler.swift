import Foundation

/// Handles UserDefaults get/set/remove operations
struct UserDefaultsHandler {
    /// Background queue for UserDefaults operations to avoid blocking the main thread
    private static let queue = DispatchQueue(label: "nib.userdefaults", qos: .userInitiated)

    static func handle(_ payload: NibMessage.UserDefaultsPayload, sendEvent: @escaping (String, String) -> Void) {
        // Handle on background queue to avoid blocking UI
        queue.async {
            handleSync(payload, sendEvent: sendEvent)
        }
    }

    private static func handleSync(_ payload: NibMessage.UserDefaultsPayload, sendEvent: @escaping (String, String) -> Void) {
        let defaults = UserDefaults.standard
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
            if let value = payload.value?.value {
                defaults.set(value, forKey: key)
                debugPrint("UserDefaults set:", key, "=", value)
            } else {
                defaults.removeObject(forKey: key)
                debugPrint("UserDefaults set nil for:", key)
            }

        case "remove":
            guard let key = payload.key else {
                debugPrint("UserDefaults remove: key required")
                return
            }
            defaults.removeObject(forKey: key)
            debugPrint("UserDefaults removed:", key)

        case "clear":
            // Clear all keys with the app's bundle identifier prefix
            let domain = Bundle.main.bundleIdentifier ?? "nib"
            defaults.removePersistentDomain(forName: domain)
            debugPrint("UserDefaults cleared for domain:", domain)

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
