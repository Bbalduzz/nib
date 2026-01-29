import Foundation
import IOKit
import IOKit.ps

/// Handles battery status queries using IOKit
struct BatteryService {
    static func handleStatus(requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()

        // Get power source info using IOKit
        if let powerInfo = IOPSCopyPowerSourcesInfo()?.takeRetainedValue(),
           let powerSources = IOPSCopyPowerSourcesList(powerInfo)?.takeRetainedValue() as? [CFTypeRef],
           let source = powerSources.first,
           let description = IOPSGetPowerSourceDescription(powerInfo, source)?.takeUnretainedValue() as? [String: Any] {

            // Battery level
            if let currentCapacity = description[kIOPSCurrentCapacityKey as String] as? Int,
               let maxCapacity = description[kIOPSMaxCapacityKey as String] as? Int,
               maxCapacity > 0 {
                data.level = Double(currentCapacity) / Double(maxCapacity) * 100.0
            }

            // Power state
            if let isCharging = description[kIOPSIsChargingKey as String] as? Bool {
                data.isCharging = isCharging
                data.state = isCharging ? "charging" : "discharging"
            }

            // Check if on AC power
            if let powerSource = description[kIOPSPowerSourceStateKey as String] as? String {
                if powerSource == kIOPSACPowerValue as String {
                    if data.isCharging != true {
                        data.state = "full"
                    }
                }
            }

            // Time remaining
            if let timeRemaining = description[kIOPSTimeToEmptyKey as String] as? Int, timeRemaining > 0 {
                data.timeRemaining = timeRemaining
            }

            data.hasBattery = true
        } else {
            // No battery (desktop Mac)
            data.hasBattery = false
            data.level = nil
            data.isCharging = false
            data.state = "acPower"
        }

        data.isLowPowerMode = ProcessInfo.processInfo.isLowPowerModeEnabled

        let response = NibServiceResponse(service: "battery", requestId: requestId, data: data)
        sendResponse(response)
    }
}
