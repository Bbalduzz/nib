import AVFoundation
import UserNotifications

/// Handles permission check and request operations for Camera, Microphone, and Notifications.
struct PermissionService {
    static func handle(_ payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        guard let permission = payload.params?["permission"]?.value as? String else {
            var data = NibServiceResponse.ServiceResponseData()
            data.success = false
            data.errorMessage = "Missing 'permission' parameter"
            sendResponse(NibServiceResponse(service: "permissions", requestId: payload.requestId, data: data))
            return
        }

        switch payload.action {
        case "check":
            handleCheck(permission: permission, requestId: payload.requestId, sendResponse: sendResponse)
        case "request":
            handleRequest(permission: permission, requestId: payload.requestId, sendResponse: sendResponse)
        default:
            debugPrint("Unknown permissions action:", payload.action)
        }
    }

    // MARK: - Check

    private static func handleCheck(permission: String, requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        switch permission {
        case "camera":
            let status = AVCaptureDevice.authorizationStatus(for: .video)
            sendStatusResponse(status: mapAVStatus(status), requestId: requestId, sendResponse: sendResponse)

        case "microphone":
            let status = AVCaptureDevice.authorizationStatus(for: .audio)
            sendStatusResponse(status: mapAVStatus(status), requestId: requestId, sendResponse: sendResponse)

        case "notifications":
            let semaphore = DispatchSemaphore(value: 0)
            var statusString = "notDetermined"
            UNUserNotificationCenter.current().getNotificationSettings { settings in
                statusString = mapNotificationStatus(settings.authorizationStatus)
                semaphore.signal()
            }
            semaphore.wait()
            sendStatusResponse(status: statusString, requestId: requestId, sendResponse: sendResponse)

        default:
            var data = NibServiceResponse.ServiceResponseData()
            data.success = false
            data.errorMessage = "Unknown permission: \(permission)"
            sendResponse(NibServiceResponse(service: "permissions", requestId: requestId, data: data))
        }
    }

    // MARK: - Request

    private static func handleRequest(permission: String, requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        switch permission {
        case "camera":
            AVCaptureDevice.requestAccess(for: .video) { granted in
                sendSuccessResponse(success: granted, requestId: requestId, sendResponse: sendResponse)
            }

        case "microphone":
            AVCaptureDevice.requestAccess(for: .audio) { granted in
                sendSuccessResponse(success: granted, requestId: requestId, sendResponse: sendResponse)
            }

        case "notifications":
            UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
                if let error = error {
                    log.error("Notification permission error: \(error.localizedDescription)")
                }
                sendSuccessResponse(success: granted, requestId: requestId, sendResponse: sendResponse)
            }

        default:
            var data = NibServiceResponse.ServiceResponseData()
            data.success = false
            data.errorMessage = "Unknown permission: \(permission)"
            sendResponse(NibServiceResponse(service: "permissions", requestId: requestId, data: data))
        }
    }

    // MARK: - Helpers

    private static func mapAVStatus(_ status: AVAuthorizationStatus) -> String {
        switch status {
        case .authorized: return "authorized"
        case .denied: return "denied"
        case .notDetermined: return "notDetermined"
        case .restricted: return "restricted"
        @unknown default: return "notDetermined"
        }
    }

    private static func mapNotificationStatus(_ status: UNAuthorizationStatus) -> String {
        switch status {
        case .authorized, .provisional, .ephemeral: return "authorized"
        case .denied: return "denied"
        case .notDetermined: return "notDetermined"
        @unknown default: return "notDetermined"
        }
    }

    private static func sendStatusResponse(status: String, requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()
        data.permissionStatus = status
        sendResponse(NibServiceResponse(service: "permissions", requestId: requestId, data: data))
    }

    private static func sendSuccessResponse(success: Bool, requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()
        data.success = success
        sendResponse(NibServiceResponse(service: "permissions", requestId: requestId, data: data))
    }
}
