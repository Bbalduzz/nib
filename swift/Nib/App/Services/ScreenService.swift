import AppKit
import IOKit

/// Handles screen/display info and brightness control
struct ScreenService {
    static func handle(_ payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        switch payload.action {
        case "info":
            handleInfo(requestId: payload.requestId, sendResponse: sendResponse)
        case "setBrightness":
            handleSetBrightness(payload: payload, sendResponse: sendResponse)
        default:
            debugPrint("Unknown screen action:", payload.action)
        }
    }

    private static func handleInfo(requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()

        if let screen = NSScreen.main {
            data.width = screen.frame.width
            data.height = screen.frame.height
            data.scale = screen.backingScaleFactor
            data.isBuiltin = CGDisplayIsBuiltin(CGMainDisplayID()) != 0

            // Get brightness (only works for built-in displays)
            var brightness: Float = 0.5
            let service = IOServiceGetMatchingService(kIOMainPortDefault, IOServiceMatching("IODisplayConnect"))
            if service != 0 {
                var brightnessValue: Float = 0
                let result = IODisplayGetFloatParameter(service, 0, kIODisplayBrightnessKey as CFString, &brightnessValue)
                if result == kIOReturnSuccess {
                    brightness = brightnessValue
                }
                IOObjectRelease(service)
            }
            data.brightness = Double(brightness)
        }

        let response = NibServiceResponse(service: "screen", requestId: requestId, data: data)
        sendResponse(response)
    }

    private static func handleSetBrightness(payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()
        data.success = false

        if let brightnessValue = payload.params?["brightness"]?.value as? Double {
            let brightness = Float(max(0, min(1, brightnessValue)))
            let service = IOServiceGetMatchingService(kIOMainPortDefault, IOServiceMatching("IODisplayConnect"))
            if service != 0 {
                let result = IODisplaySetFloatParameter(service, 0, kIODisplayBrightnessKey as CFString, brightness)
                data.success = (result == kIOReturnSuccess)
                IOObjectRelease(service)
            }
        }

        let response = NibServiceResponse(service: "screen", requestId: payload.requestId, data: data)
        sendResponse(response)
    }
}
