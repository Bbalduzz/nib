import AppKit
import IOKit
import IOKit.graphics
import CoreGraphics

struct ScreenService {

    static func handle(_ payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        switch payload.action {
        case "info":
            handleInfo(requestId: payload.requestId, sendResponse: sendResponse)
        case "list":
            handleListDisplays(requestId: payload.requestId, sendResponse: sendResponse)
        case "setBrightness":
            handleSetBrightness(payload: payload, sendResponse: sendResponse)
        case "setResolution":
            handleSetResolution(payload: payload, sendResponse: sendResponse)
        case "screenshot":
            handleScreenshot(payload: payload, sendResponse: sendResponse)
        case "getDarkMode":
            handleGetDarkMode(requestId: payload.requestId, sendResponse: sendResponse)
        case "setDarkMode":
            handleSetDarkMode(payload: payload, sendResponse: sendResponse)
        case "getColorProfile":
            handleGetColorProfile(requestId: payload.requestId, sendResponse: sendResponse)
        default:
            sendError(requestId: payload.requestId, message: "Unknown action: \(payload.action)", sendResponse: sendResponse)
        }
    }

    // MARK: - Display Info

    private static func handleInfo(requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        guard let screen = NSScreen.main else {
            sendError(requestId: requestId, message: "No main screen found", sendResponse: sendResponse)
            return
        }

        let displayID = CGMainDisplayID()
        let data = buildScreenInfo(screen: screen, displayID: displayID)
        sendResponse(NibServiceResponse(service: "screen", requestId: requestId, data: data))
    }

    private static func handleListDisplays(requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()

        let displays: [[String: Any]] = NSScreen.screens.enumerated().compactMap { index, screen in
            guard let displayID = screen.deviceDescription[NSDeviceDescriptionKey("NSScreenNumber")] as? CGDirectDisplayID else {
                return nil
            }

            return [
                "index": index,
                "displayID": displayID,
                "name": screen.localizedName,
                "width": screen.frame.width,
                "height": screen.frame.height,
                "visibleWidth": screen.visibleFrame.width,
                "visibleHeight": screen.visibleFrame.height,
                "scale": screen.backingScaleFactor,
                "isMain": screen == NSScreen.main,
                "isBuiltin": CGDisplayIsBuiltin(displayID) != 0,
                "refreshRate": getRefreshRate(displayID: displayID),
                "colorSpace": screen.colorSpace?.localizedName ?? "Unknown"
            ]
        }

        // Encode as JSON string for Codable compatibility
        if let jsonData = try? JSONSerialization.data(withJSONObject: displays),
           let jsonString = String(data: jsonData, encoding: .utf8) {
            data.displaysJson = jsonString
        }
        data.count = displays.count
        sendResponse(NibServiceResponse(service: "screen", requestId: requestId, data: data))
    }

    private static func buildScreenInfo(screen: NSScreen, displayID: CGDirectDisplayID) -> NibServiceResponse.ServiceResponseData {
        var data = NibServiceResponse.ServiceResponseData()

        // Basic dimensions
        data.width = screen.frame.width
        data.height = screen.frame.height
        data.visibleWidth = screen.visibleFrame.width
        data.visibleHeight = screen.visibleFrame.height
        data.scale = screen.backingScaleFactor

        // Display properties
        data.isBuiltin = CGDisplayIsBuiltin(displayID) != 0
        data.displayID = Int(displayID)
        data.name = screen.localizedName
        data.refreshRate = getRefreshRate(displayID: displayID)

        // Native resolution
        if let mode = CGDisplayCopyDisplayMode(displayID) {
            data.nativeWidth = mode.pixelWidth
            data.nativeHeight = mode.pixelHeight
        }

        // Brightness (built-in only)
        data.brightness = getBrightness(displayID: displayID)

        // Color info
        data.colorSpace = screen.colorSpace?.localizedName
        // Note: CGDisplayBitsPerPixel was removed; use colorSpace components instead
        data.colorDepth = (screen.colorSpace?.numberOfColorComponents ?? 3) * 8

        // Available resolutions (JSON-encoded for Codable compatibility)
        let resolutions = getAvailableResolutions(displayID: displayID)
        if let jsonData = try? JSONSerialization.data(withJSONObject: resolutions),
           let jsonString = String(data: jsonData, encoding: .utf8) {
            data.availableResolutionsJson = jsonString
        }

        return data
    }

    // MARK: - Brightness

    private static func getBrightness(displayID: CGDirectDisplayID) -> Double? {
        // Method 1: IOKit (works for built-in displays)
        let service = IOServiceGetMatchingService(kIOMainPortDefault, IOServiceMatching("IODisplayConnect"))
        if service != 0 {
            defer { IOObjectRelease(service) }
            var brightness: Float = 0
            if IODisplayGetFloatParameter(service, 0, kIODisplayBrightnessKey as CFString, &brightness) == kIOReturnSuccess {
                return Double(brightness)
            }
        }
        return nil
    }

    private static func handleSetBrightness(payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()
        data.success = false

        guard let brightnessValue = payload.params?["brightness"]?.value as? Double else {
            sendError(requestId: payload.requestId, message: "Missing brightness parameter", sendResponse: sendResponse)
            return
        }

        let brightness = Float(max(0, min(1, brightnessValue)))
        let service = IOServiceGetMatchingService(kIOMainPortDefault, IOServiceMatching("IODisplayConnect"))

        if service != 0 {
            defer { IOObjectRelease(service) }
            let result = IODisplaySetFloatParameter(service, 0, kIODisplayBrightnessKey as CFString, brightness)
            data.success = (result == kIOReturnSuccess)
            data.brightness = Double(brightness)
        }

        sendResponse(NibServiceResponse(service: "screen", requestId: payload.requestId, data: data))
    }

    // MARK: - Resolution

    private static func getAvailableResolutions(displayID: CGDirectDisplayID) -> [[String: Any]] {
        guard let modes = CGDisplayCopyAllDisplayModes(displayID, nil) as? [CGDisplayMode] else {
            return []
        }

        return modes.map { mode in
            [
                "width": mode.width,
                "height": mode.height,
                "pixelWidth": mode.pixelWidth,
                "pixelHeight": mode.pixelHeight,
                "refreshRate": mode.refreshRate,
                "isUsable": mode.isUsableForDesktopGUI()
            ]
        }.filter { $0["isUsable"] as? Bool == true }
    }

    private static func handleSetResolution(payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()
        data.success = false

        guard let width = payload.params?["width"]?.value as? Int,
              let height = payload.params?["height"]?.value as? Int else {
            sendError(requestId: payload.requestId, message: "Missing width/height parameters", sendResponse: sendResponse)
            return
        }

        let displayID = CGMainDisplayID()
        guard let modes = CGDisplayCopyAllDisplayModes(displayID, nil) as? [CGDisplayMode] else {
            sendError(requestId: payload.requestId, message: "Could not get display modes", sendResponse: sendResponse)
            return
        }

        // Find matching mode
        if let targetMode = modes.first(where: {
            $0.width == width &&
            $0.height == height &&
            $0.isUsableForDesktopGUI()
        }) {
            var config: CGDisplayConfigRef?
            if CGBeginDisplayConfiguration(&config) == .success {
                CGConfigureDisplayWithDisplayMode(config, displayID, targetMode, nil)
                let result = CGCompleteDisplayConfiguration(config, .permanently)
                data.success = (result == .success)
            }
        }

        sendResponse(NibServiceResponse(service: "screen", requestId: payload.requestId, data: data))
    }

    // MARK: - Screenshot

    private static func handleScreenshot(payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()
        data.success = false

        let displayID: CGDirectDisplayID
        if let targetDisplay = payload.params?["displayID"]?.value as? UInt32 {
            displayID = targetDisplay
        } else {
            displayID = CGMainDisplayID()
        }

        // Optional region
        var captureRect: CGRect = .null
        if let x = payload.params?["x"]?.value as? Double,
           let y = payload.params?["y"]?.value as? Double,
           let w = payload.params?["width"]?.value as? Double,
           let h = payload.params?["height"]?.value as? Double {
            captureRect = CGRect(x: x, y: y, width: w, height: h)
        }

        guard let image = captureRect.isNull
                ? CGDisplayCreateImage(displayID)
                : CGDisplayCreateImage(displayID, rect: captureRect) else {
            sendError(requestId: payload.requestId, message: "Failed to capture screen", sendResponse: sendResponse)
            return
        }

        // Convert to PNG data
        let bitmapRep = NSBitmapImageRep(cgImage: image)
        if let pngData = bitmapRep.representation(using: .png, properties: [:]) {
            data.success = true
            data.imageData = pngData
            data.imageWidth = image.width
            data.imageHeight = image.height
            data.imageFormat = "png"
        }

        sendResponse(NibServiceResponse(service: "screen", requestId: payload.requestId, data: data))
    }

    // MARK: - Dark Mode

    private static func handleGetDarkMode(requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()

        let appearance = NSApp.effectiveAppearance.name
        data.isDarkMode = appearance == .darkAqua || appearance == .vibrantDark ||
                          appearance == .accessibilityHighContrastDarkAqua ||
                          appearance == .accessibilityHighContrastVibrantDark
        data.appearanceName = appearance.rawValue

        sendResponse(NibServiceResponse(service: "screen", requestId: requestId, data: data))
    }

    private static func handleSetDarkMode(payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()
        data.success = false

        guard let enableDark = payload.params?["enabled"]?.value as? Bool else {
            sendError(requestId: payload.requestId, message: "Missing 'enabled' parameter", sendResponse: sendResponse)
            return
        }

        // Uses AppleScript to toggle system appearance
        let script = """
            tell application "System Events"
                tell appearance preferences
                    set dark mode to \(enableDark)
                end tell
            end tell
        """

        if let appleScript = NSAppleScript(source: script) {
            var error: NSDictionary?
            appleScript.executeAndReturnError(&error)
            data.success = (error == nil)
            if let error = error {
                data.errorMessage = error.description
            }
        }

        sendResponse(NibServiceResponse(service: "screen", requestId: payload.requestId, data: data))
    }

    // MARK: - Color Profile

    private static func handleGetColorProfile(requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()

        if let screen = NSScreen.main, let colorSpace = screen.colorSpace {
            data.colorSpaceName = colorSpace.localizedName
            data.colorComponentCount = colorSpace.numberOfColorComponents

            if let iccData = colorSpace.iccProfileData {
                data.iccProfileSize = iccData.count
            }
        }

        sendResponse(NibServiceResponse(service: "screen", requestId: requestId, data: data))
    }

    // MARK: - Helpers

    private static func getRefreshRate(displayID: CGDirectDisplayID) -> Double {
        if let mode = CGDisplayCopyDisplayMode(displayID) {
            return mode.refreshRate
        }
        return 0
    }

    private static func sendError(requestId: String, message: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()
        data.success = false
        data.errorMessage = message
        sendResponse(NibServiceResponse(service: "screen", requestId: requestId, data: data))
    }
}
