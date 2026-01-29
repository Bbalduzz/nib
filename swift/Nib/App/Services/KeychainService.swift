import Foundation
import Security

/// Handles Keychain password storage operations
struct KeychainService {
    static func handle(_ payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        let service = payload.params?["service"]?.value as? String ?? ""
        let account = payload.params?["account"]?.value as? String ?? ""

        switch payload.action {
        case "get":
            var data = NibServiceResponse.ServiceResponseData()
            if let password = getPassword(service: service, account: account) {
                data.password = password
            }
            let response = NibServiceResponse(service: "keychain", requestId: payload.requestId, data: data)
            sendResponse(response)

        case "set":
            let password = payload.params?["password"]?.value as? String ?? ""
            var data = NibServiceResponse.ServiceResponseData()
            data.success = setPassword(service: service, account: account, password: password)
            let response = NibServiceResponse(service: "keychain", requestId: payload.requestId, data: data)
            sendResponse(response)

        case "delete":
            var data = NibServiceResponse.ServiceResponseData()
            data.success = deletePassword(service: service, account: account)
            let response = NibServiceResponse(service: "keychain", requestId: payload.requestId, data: data)
            sendResponse(response)

        case "exists":
            var data = NibServiceResponse.ServiceResponseData()
            data.exists = getPassword(service: service, account: account) != nil
            let response = NibServiceResponse(service: "keychain", requestId: payload.requestId, data: data)
            sendResponse(response)

        default:
            debugPrint("Unknown keychain action:", payload.action)
        }
    }

    private static func getPassword(service: String, account: String) -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess,
              let data = result as? Data,
              let password = String(data: data, encoding: .utf8) else {
            return nil
        }
        return password
    }

    private static func setPassword(service: String, account: String, password: String) -> Bool {
        // First try to delete existing item
        _ = deletePassword(service: service, account: account)

        guard let passwordData = password.data(using: .utf8) else { return false }

        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account,
            kSecValueData as String: passwordData
        ]

        let status = SecItemAdd(query as CFDictionary, nil)
        return status == errSecSuccess
    }

    private static func deletePassword(service: String, account: String) -> Bool {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account
        ]

        let status = SecItemDelete(query as CFDictionary)
        return status == errSecSuccess || status == errSecItemNotFound
    }
}
