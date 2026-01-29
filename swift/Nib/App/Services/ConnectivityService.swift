import Foundation
import SystemConfiguration

/// Handles network connectivity status queries
struct ConnectivityService {
    static func handleStatus(requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var data = NibServiceResponse.ServiceResponseData()
        data.isConnected = false
        data.connectionType = "none"
        data.isExpensive = false
        data.isConstrained = false

        // Use SystemConfiguration to check network reachability
        var zeroAddress = sockaddr()
        zeroAddress.sa_len = UInt8(MemoryLayout<sockaddr>.size)
        zeroAddress.sa_family = sa_family_t(AF_INET)

        if let reachability = withUnsafePointer(to: &zeroAddress, {
            $0.withMemoryRebound(to: sockaddr.self, capacity: 1) {
                SCNetworkReachabilityCreateWithAddress(nil, $0)
            }
        }) {
            var flags = SCNetworkReachabilityFlags()
            if SCNetworkReachabilityGetFlags(reachability, &flags) {
                let isReachable = flags.contains(.reachable)
                let needsConnection = flags.contains(.connectionRequired)

                if isReachable && !needsConnection {
                    data.isConnected = true
                    // On macOS, we don't have cellular - it's either WiFi or Ethernet
                    data.connectionType = "wifi"  // Default assumption
                }
            }
        }

        let response = NibServiceResponse(service: "connectivity", requestId: requestId, data: data)
        sendResponse(response)
    }
}
