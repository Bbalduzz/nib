import Foundation
import ServiceManagement

/// Handles Launch at Login operations using SMAppService (macOS 13+)
struct LaunchAtLoginService {
    static func handle(_ payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        switch payload.action {
        case "status":
            var data = NibServiceResponse.ServiceResponseData()
            data.enabled = isEnabled()
            let response = NibServiceResponse(service: "launchAtLogin", requestId: payload.requestId, data: data)
            sendResponse(response)

        case "set":
            // Handle both Bool and Int (MessagePack encodes Python bools as integers)
            let enabledValue = payload.params?["enabled"]?.value
            log.info("Params: \(String(describing: payload.params))")
            log.info("Enabled value: \(String(describing: enabledValue)), type: \(type(of: enabledValue))")
            let enabled: Bool
            if let boolVal = enabledValue as? Bool {
                log.info("Parsed as Bool: \(boolVal)")
                enabled = boolVal
            } else if let intVal = enabledValue as? Int {
                log.info("Parsed as Int: \(intVal)")
                enabled = intVal != 0
            } else {
                log.info("Could not parse, defaulting to false")
                enabled = false
            }
            var data = NibServiceResponse.ServiceResponseData()
            data.success = setEnabled(enabled)
            data.enabled = isEnabled()
            let response = NibServiceResponse(service: "launchAtLogin", requestId: payload.requestId, data: data)
            sendResponse(response)

        default:
            debugPrint("Unknown launchAtLogin action:", payload.action)
        }
    }

    /// Check if launch at login is currently enabled
    private static func isEnabled() -> Bool {
        if #available(macOS 13.0, *) {
            return SMAppService.mainApp.status == .enabled
        } else {
            // Fallback for older macOS versions - not supported
            return false
        }
    }

    /// Set the launch at login state
    private static func setEnabled(_ enabled: Bool) -> Bool {
        if #available(macOS 13.0, *) {
            log.info("Setting launch at login to: \(enabled)")
            log.info("Current status: \(SMAppService.mainApp.status.rawValue)")
            log.info("Bundle identifier: \(Bundle.main.bundleIdentifier ?? "nil")")
            do {
                if enabled {
                    try SMAppService.mainApp.register()
                    log.info("Launch at login enabled")
                } else {
                    try SMAppService.mainApp.unregister()
                    log.info("Launch at login disabled")
                }
                return true
            } catch let error as NSError {
                log.error("Failed to set launch at login: \(error.localizedDescription)")
                log.error("Error domain: \(error.domain), code: \(error.code)")
                return false
            }
        } else {
            log.warn("Launch at login requires macOS 13+")
            return false
        }
    }
}
