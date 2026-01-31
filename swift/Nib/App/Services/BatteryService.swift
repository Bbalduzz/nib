import Foundation
import IOKit
import IOKit.ps
import IOKit.pwr_mgt

/// Handles battery and power management queries
struct BatteryService {

    static func handle(_ payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        switch payload.action {
        case "status":
            handleStatus(requestId: payload.requestId, sendResponse: sendResponse)
        case "health":
            handleHealth(requestId: payload.requestId, sendResponse: sendResponse)
        case "history":
            handleHistory(requestId: payload.requestId, sendResponse: sendResponse)
        case "thermalState":
            handleThermalState(requestId: payload.requestId, sendResponse: sendResponse)
        case "preventSleep":
            handlePreventSleep(payload: payload, sendResponse: sendResponse)
        case "allowSleep":
            handleAllowSleep(payload: payload, sendResponse: sendResponse)
        default:
            sendError(requestId: payload.requestId, message: "Unknown action: \(payload.action)", sendResponse: sendResponse)
        }
    }

    // MARK: - Status

    static func handleStatus(requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()

        guard let powerInfo = IOPSCopyPowerSourcesInfo()?.takeRetainedValue(),
              let powerSources = IOPSCopyPowerSourcesList(powerInfo)?.takeRetainedValue() as? [CFTypeRef],
              let source = powerSources.first,
              let description = IOPSGetPowerSourceDescription(powerInfo, source)?.takeUnretainedValue() as? [String: Any] else {
            // No battery (desktop Mac)
            data.hasBattery = false
            data.isCharging = false
            data.state = "acPower"
            data.powerSource = "AC Power"
            data.isLowPowerMode = ProcessInfo.processInfo.isLowPowerModeEnabled
            sendResponse(NibServiceResponse(service: "battery", requestId: requestId, data: data))
            return
        }

        data.hasBattery = true

        // Battery level
        if let currentCapacity = description[kIOPSCurrentCapacityKey as String] as? Int,
           let maxCapacity = description[kIOPSMaxCapacityKey as String] as? Int,
           maxCapacity > 0 {
            data.level = Double(currentCapacity) / Double(maxCapacity) * 100.0
            data.currentCapacity = currentCapacity
            data.maxCapacity = maxCapacity
        }

        // Charging state
        if let isCharging = description[kIOPSIsChargingKey as String] as? Bool {
            data.isCharging = isCharging
        }

        // Plugged in?
        if let isPluggedIn = description[kIOPSPowerSourceStateKey as String] as? String {
            data.isPluggedIn = (isPluggedIn == kIOPSACPowerValue as String)
        }

        // Determine state
        data.state = determineBatteryState(description: description, isCharging: data.isCharging ?? false)

        // Time estimates
        if let timeToEmpty = description[kIOPSTimeToEmptyKey as String] as? Int, timeToEmpty > 0 {
            data.timeToEmpty = timeToEmpty
            data.timeToEmptyFormatted = formatMinutes(timeToEmpty)
            data.timeRemaining = timeToEmpty  // For backward compatibility
        }

        if let timeToFullCharge = description[kIOPSTimeToFullChargeKey as String] as? Int, timeToFullCharge > 0 {
            data.timeToFullCharge = timeToFullCharge
            data.timeToFullChargeFormatted = formatMinutes(timeToFullCharge)
        }

        // Power source name
        data.powerSource = description[kIOPSNameKey as String] as? String

        // Hardware info
        data.batteryType = description[kIOPSTypeKey as String] as? String
        data.serialNumber = description[kIOPSHardwareSerialNumberKey as String] as? String

        // Charging states
        data.isCharged = description[kIOPSIsChargedKey as String] as? Bool
        data.isFinishingCharge = description[kIOPSIsFinishingChargeKey as String] as? Bool

        // System states
        data.isLowPowerMode = ProcessInfo.processInfo.isLowPowerModeEnabled
        data.thermalState = getThermalStateName()

        // Amperage and voltage (if available)
        if let amperage = description["Current" as String] as? Int {
            data.amperage = amperage
        }
        if let voltage = description["Voltage" as String] as? Int {
            data.voltage = Double(voltage) / 1000.0 // Convert mV to V
        }

        // Wattage calculation
        if let amperage = data.amperage, let voltage = data.voltage {
            data.wattage = abs(Double(amperage) * voltage / 1000.0)
        }

        sendResponse(NibServiceResponse(service: "battery", requestId: requestId, data: data))
    }

    // MARK: - Battery Health

    private static func handleHealth(requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()

        // Access battery health info via IOKit
        let service = IOServiceGetMatchingService(kIOMainPortDefault, IOServiceMatching("AppleSmartBattery"))
        guard service != 0 else {
            sendError(requestId: requestId, message: "Could not access battery service", sendResponse: sendResponse)
            return
        }
        defer { IOObjectRelease(service) }

        // Cycle count
        if let cycleCount = getIORegistryProperty(service: service, key: "CycleCount") as? Int {
            data.cycleCount = cycleCount
        }

        // Design capacity vs current max capacity
        if let designCapacity = getIORegistryProperty(service: service, key: "DesignCapacity") as? Int {
            data.designCapacity = designCapacity
        }

        if let maxCapacity = getIORegistryProperty(service: service, key: "MaxCapacity") as? Int {
            data.maxCapacity = maxCapacity

            if let designCapacity = data.designCapacity, designCapacity > 0 {
                data.healthPercent = Double(maxCapacity) / Double(designCapacity) * 100.0
            }
        }

        // Temperature (in centi-degrees Celsius)
        if let temperature = getIORegistryProperty(service: service, key: "Temperature") as? Int {
            data.temperatureCelsius = Double(temperature) / 100.0
            data.temperatureFahrenheit = (Double(temperature) / 100.0) * 9.0 / 5.0 + 32.0
        }

        // Manufacture date
        if let manufactureDate = getIORegistryProperty(service: service, key: "ManufactureDate") as? Int {
            // Packed date: (year - 1980) * 512 + month * 32 + day
            let year = (manufactureDate >> 9) + 1980
            let month = (manufactureDate >> 5) & 0xF
            let day = manufactureDate & 0x1F
            data.manufactureDate = String(format: "%04d-%02d-%02d", year, month, day)
        }

        // Manufacturer and model
        data.manufacturer = getIORegistryProperty(service: service, key: "Manufacturer") as? String
        data.deviceName = getIORegistryProperty(service: service, key: "DeviceName") as? String

        // Battery condition (macOS 10.15+)
        if let condition = getIORegistryProperty(service: service, key: "BatteryHealthCondition") as? String {
            data.condition = condition
        } else {
            // Estimate condition from health percent
            if let health = data.healthPercent {
                data.condition = estimateCondition(healthPercent: health)
            }
        }

        // Charging optimizations
        data.optimizedChargingEngaged = getIORegistryProperty(service: service, key: "OptimizedChargingEngaged") as? Bool

        sendResponse(NibServiceResponse(service: "battery", requestId: requestId, data: data))
    }

    // MARK: - Thermal State

    private static func handleThermalState(requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()

        let state = ProcessInfo.processInfo.thermalState
        data.thermalState = getThermalStateName(state)
        data.thermalStateRaw = state.rawValue

        // Recommendations based on thermal state
        data.recommendation = getThermalRecommendation(state)

        sendResponse(NibServiceResponse(service: "battery", requestId: requestId, data: data))
    }

    // MARK: - Sleep Prevention

    private static var sleepAssertionID: IOPMAssertionID = 0

    private static func handlePreventSleep(payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()

        let reason = payload.params?["reason"]?.value as? String ?? "App preventing sleep"
        let type = payload.params?["type"]?.value as? String ?? "idle"

        let assertionType: CFString
        switch type {
        case "display":
            assertionType = kIOPMAssertionTypePreventUserIdleDisplaySleep as CFString
        case "system":
            assertionType = kIOPMAssertionTypePreventSystemSleep as CFString
        default:
            assertionType = kIOPMAssertionTypePreventUserIdleSystemSleep as CFString
        }

        var assertionID: IOPMAssertionID = 0
        let result = IOPMAssertionCreateWithName(
            assertionType,
            IOPMAssertionLevel(kIOPMAssertionLevelOn),
            reason as CFString,
            &assertionID
        )

        if result == kIOReturnSuccess {
            sleepAssertionID = assertionID
            data.success = true
            data.assertionID = Int(assertionID)
        } else {
            data.success = false
            data.errorMessage = "Failed to create sleep assertion"
        }

        sendResponse(NibServiceResponse(service: "battery", requestId: payload.requestId, data: data))
    }

    private static func handleAllowSleep(payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()

        let assertionID: IOPMAssertionID
        if let providedID = payload.params?["assertionID"]?.value as? Int {
            assertionID = IOPMAssertionID(providedID)
        } else {
            assertionID = sleepAssertionID
        }

        if assertionID != 0 {
            let result = IOPMAssertionRelease(assertionID)
            data.success = (result == kIOReturnSuccess)
            if assertionID == sleepAssertionID {
                sleepAssertionID = 0
            }
        } else {
            data.success = false
            data.errorMessage = "No active sleep assertion"
        }

        sendResponse(NibServiceResponse(service: "battery", requestId: payload.requestId, data: data))
    }

    // MARK: - History (simplified - actual implementation would need PrivateFrameworks)

    private static func handleHistory(requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()

        // Note: Full battery history requires private APIs or parsing pmset output
        // This provides what's available through public APIs

        data.note = "Full history requires pmset -g log parsing or private APIs"

        // We can provide current session uptime
        data.systemUptime = ProcessInfo.processInfo.systemUptime
        data.systemUptimeFormatted = formatSeconds(Int(ProcessInfo.processInfo.systemUptime))

        sendResponse(NibServiceResponse(service: "battery", requestId: requestId, data: data))
    }

    // MARK: - Helpers

    private static func getIORegistryProperty(service: io_service_t, key: String) -> Any? {
        IORegistryEntryCreateCFProperty(service, key as CFString, kCFAllocatorDefault, 0)?.takeRetainedValue()
    }

    private static func determineBatteryState(description: [String: Any], isCharging: Bool) -> String {
        if let isCharged = description[kIOPSIsChargedKey as String] as? Bool, isCharged {
            return "full"
        }
        if isCharging {
            return "charging"
        }
        if let powerSource = description[kIOPSPowerSourceStateKey as String] as? String,
           powerSource == kIOPSACPowerValue as String {
            return "pluggedNotCharging"
        }
        return "discharging"
    }

    private static func getThermalStateName(_ state: ProcessInfo.ThermalState? = nil) -> String {
        let thermalState = state ?? ProcessInfo.processInfo.thermalState
        switch thermalState {
        case .nominal: return "nominal"
        case .fair: return "fair"
        case .serious: return "serious"
        case .critical: return "critical"
        @unknown default: return "unknown"
        }
    }

    private static func getThermalRecommendation(_ state: ProcessInfo.ThermalState) -> String {
        switch state {
        case .nominal:
            return "System is running normally"
        case .fair:
            return "Consider reducing intensive tasks"
        case .serious:
            return "Reduce CPU/GPU usage, close unnecessary apps"
        case .critical:
            return "System is throttling - stop intensive tasks immediately"
        @unknown default:
            return "Unknown thermal state"
        }
    }

    private static func estimateCondition(healthPercent: Double) -> String {
        switch healthPercent {
        case 80...: return "Normal"
        case 60..<80: return "Fair"
        case 40..<60: return "Poor"
        default: return "Service Recommended"
        }
    }

    private static func formatMinutes(_ minutes: Int) -> String {
        let hours = minutes / 60
        let mins = minutes % 60
        if hours > 0 {
            return "\(hours)h \(mins)m"
        }
        return "\(mins)m"
    }

    private static func formatSeconds(_ seconds: Int) -> String {
        let hours = seconds / 3600
        let minutes = (seconds % 3600) / 60
        return "\(hours)h \(minutes)m"
    }

    private static func sendError(requestId: String, message: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()
        data.success = false
        data.errorMessage = message
        sendResponse(NibServiceResponse(service: "battery", requestId: requestId, data: data))
    }
}
