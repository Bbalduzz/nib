import Foundation
import UserNotifications

/// Service for handling macOS notifications using UserNotifications framework.
class NotificationService: NSObject, UNUserNotificationCenterDelegate {

    private var sendResponse: ((NotificationResponse) -> Void)?
    private var sendEvent: ((String, String) -> Void)?
    private var registeredCategories: Set<String> = []

    struct NotificationResponse: Codable {
        let type: String
        let requestId: String?
        let data: ResponseData

        struct ResponseData: Codable {
            var granted: Bool?
            var notifications: [[String: Any]]?
            var notification: [String: Any]?
            var success: Bool?
            var error: String?

            // Custom encoding to handle [String: Any]
            func encode(to encoder: Encoder) throws {
                var container = encoder.container(keyedBy: CodingKeys.self)
                if let granted = granted {
                    try container.encode(granted, forKey: .granted)
                }
                if let success = success {
                    try container.encode(success, forKey: .success)
                }
                if let error = error {
                    try container.encode(error, forKey: .error)
                }
                // notifications and notification are handled separately via MessagePack
            }

            enum CodingKeys: String, CodingKey {
                case granted, notifications, notification, success, error
            }

            init(from decoder: Decoder) throws {
                let container = try decoder.container(keyedBy: CodingKeys.self)
                granted = try container.decodeIfPresent(Bool.self, forKey: .granted)
                success = try container.decodeIfPresent(Bool.self, forKey: .success)
                error = try container.decodeIfPresent(String.self, forKey: .error)
            }

            init(granted: Bool? = nil, notifications: [[String: Any]]? = nil, notification: [String: Any]? = nil, success: Bool? = nil, error: String? = nil) {
                self.granted = granted
                self.notifications = notifications
                self.notification = notification
                self.success = success
                self.error = error
            }
        }
    }

    override init() {
        super.init()
    }

    func configure(sendResponse: @escaping (NotificationResponse) -> Void, sendEvent: @escaping (String, String) -> Void) {
        self.sendResponse = sendResponse
        self.sendEvent = sendEvent
    }

    func setupNotificationCenter() {
        // Only set up if running from a proper app bundle
        guard isRunningFromAppBundle else {
            debugPrint("NotificationService: Skipping setup (not running from .app bundle)")
            return
        }

        let center = UNUserNotificationCenter.current()
        center.delegate = self
    }

    private var isRunningFromAppBundle: Bool {
        let bundlePath = Bundle.main.bundlePath
        let executablePath = Bundle.main.executablePath ?? ""
        return bundlePath.hasSuffix(".app") && executablePath.contains("/Contents/MacOS/")
    }

    // MARK: - Handle Notification Actions

    func handle(_ payload: NibMessage.NotificationPayload) {
        switch payload.action {
        case "requestPermission":
            requestPermission(requestId: payload.requestId)
        case "push":
            if let notification = payload.notification {
                push(notification: notification)
            }
        case "schedule":
            if let notification = payload.notification, let trigger = payload.trigger {
                schedule(notification: notification, trigger: trigger)
            }
        case "cancel":
            if let id = payload.notificationId {
                cancel(id: id)
            }
        case "cancelAll":
            cancelAll()
        case "getScheduled":
            getScheduled(requestId: payload.requestId)
        case "getDelivered":
            getDelivered(requestId: payload.requestId)
        case "getScheduledById":
            if let id = payload.notificationId {
                getScheduledById(id: id, requestId: payload.requestId)
            }
        case "getDeliveredById":
            if let id = payload.notificationId {
                getDeliveredById(id: id, requestId: payload.requestId)
            }
        default:
            debugPrint("NotificationService: Unknown action: \(payload.action)")
        }
    }

    // MARK: - Permission

    private func requestPermission(requestId: String?) {
        guard isRunningFromAppBundle else {
            // In dev mode, always report as granted (we'll use AppleScript fallback)
            if let requestId = requestId {
                sendResponse?(NotificationResponse(
                    type: "notificationResponse",
                    requestId: requestId,
                    data: .init(granted: true)
                ))
            }
            return
        }

        let center = UNUserNotificationCenter.current()
        center.requestAuthorization(options: [.alert, .sound, .badge]) { [weak self] granted, error in
            if let error = error {
                debugPrint("NotificationService: Authorization error: \(error)")
            }

            if let requestId = requestId {
                self?.sendResponse?(NotificationResponse(
                    type: "notificationResponse",
                    requestId: requestId,
                    data: .init(granted: granted)
                ))
            }
        }
    }

    // MARK: - Push

    private func push(notification: NibMessage.NotificationConfig) {
        guard isRunningFromAppBundle else {
            // Fall back to AppleScript for dev mode
            pushViaAppleScript(notification: notification)
            return
        }

        let content = buildNotificationContent(from: notification)

        // Register category if notification has actions
        if let actions = notification.actions, !actions.isEmpty {
            registerCategory(for: notification)
        }

        let request = UNNotificationRequest(
            identifier: notification.id,
            content: content,
            trigger: nil  // nil = immediate delivery
        )

        UNUserNotificationCenter.current().add(request) { error in
            if let error = error {
                debugPrint("NotificationService: Failed to push notification: \(error)")
            } else {
                debugPrint("NotificationService: Notification pushed: \(notification.id)")
            }
        }
    }

    private func pushViaAppleScript(notification: NibMessage.NotificationConfig) {
        let title = notification.title.replacingOccurrences(of: "\"", with: "\\\"")
        let body = (notification.body ?? "").replacingOccurrences(of: "\"", with: "\\\"")
        let subtitle = notification.subtitle?.replacingOccurrences(of: "\"", with: "\\\"")

        var script = "display notification \"\(body)\" with title \"\(title)\""
        if let sub = subtitle {
            script += " subtitle \"\(sub)\""
        }
        // Add sound if configured
        if let sound = notification.sound {
            if sound.custom == true {
                script += " sound name \"\(sound.name)\""
            } else if sound.name == "default" {
                script += " sound name \"default\""
            }
        }

        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/osascript")
        process.arguments = ["-e", script]
        try? process.run()
        debugPrint("NotificationService: Notification pushed via AppleScript: \(notification.id)")
    }

    // MARK: - Schedule

    private func schedule(notification: NibMessage.NotificationConfig, trigger: NibMessage.NotificationTrigger) {
        guard isRunningFromAppBundle else {
            debugPrint("NotificationService: Scheduling not available in dev mode")
            return
        }

        debugPrint("NotificationService: Scheduling notification - trigger type: \(trigger.type)")
        if let interval = trigger.interval {
            debugPrint("NotificationService: Interval: \(interval) seconds")
        }

        let content = buildNotificationContent(from: notification)

        // Register category if notification has actions
        if let actions = notification.actions, !actions.isEmpty {
            registerCategory(for: notification)
        }

        let unTrigger = buildTrigger(from: trigger)
        debugPrint("NotificationService: Built trigger: \(String(describing: unTrigger))")

        if unTrigger == nil {
            debugPrint("NotificationService: WARNING - trigger is nil, notification will fire immediately!")
        }

        let request = UNNotificationRequest(
            identifier: notification.id,
            content: content,
            trigger: unTrigger
        )

        UNUserNotificationCenter.current().add(request) { error in
            if let error = error {
                debugPrint("NotificationService: Failed to schedule notification: \(error)")
            } else {
                debugPrint("NotificationService: Notification scheduled: \(notification.id)")
            }
        }
    }

    // MARK: - Cancel

    private func cancel(id: String) {
        guard isRunningFromAppBundle else { return }

        let center = UNUserNotificationCenter.current()
        center.removePendingNotificationRequests(withIdentifiers: [id])
        center.removeDeliveredNotifications(withIdentifiers: [id])
        debugPrint("NotificationService: Notification cancelled: \(id)")
    }

    private func cancelAll() {
        guard isRunningFromAppBundle else { return }

        let center = UNUserNotificationCenter.current()
        center.removeAllPendingNotificationRequests()
        center.removeAllDeliveredNotifications()
        debugPrint("NotificationService: All notifications cancelled")
    }

    // MARK: - Query

    private func getScheduled(requestId: String?) {
        guard isRunningFromAppBundle else {
            if let requestId = requestId {
                sendResponse?(NotificationResponse(
                    type: "notificationResponse",
                    requestId: requestId,
                    data: .init(notifications: [])
                ))
            }
            return
        }

        UNUserNotificationCenter.current().getPendingNotificationRequests { [weak self] requests in
            let notifications = requests.map { self?.convertRequest($0) ?? [:] }
            if let requestId = requestId {
                self?.sendResponse?(NotificationResponse(
                    type: "notificationResponse",
                    requestId: requestId,
                    data: .init(notifications: notifications)
                ))
            }
        }
    }

    private func getDelivered(requestId: String?) {
        guard isRunningFromAppBundle else {
            if let requestId = requestId {
                sendResponse?(NotificationResponse(
                    type: "notificationResponse",
                    requestId: requestId,
                    data: .init(notifications: [])
                ))
            }
            return
        }

        UNUserNotificationCenter.current().getDeliveredNotifications { [weak self] notifications in
            let notificationDicts = notifications.map { self?.convertDelivered($0) ?? [:] }
            if let requestId = requestId {
                self?.sendResponse?(NotificationResponse(
                    type: "notificationResponse",
                    requestId: requestId,
                    data: .init(notifications: notificationDicts)
                ))
            }
        }
    }

    private func getScheduledById(id: String, requestId: String?) {
        guard isRunningFromAppBundle else {
            if let requestId = requestId {
                sendResponse?(NotificationResponse(
                    type: "notificationResponse",
                    requestId: requestId,
                    data: .init(notification: nil)
                ))
            }
            return
        }

        UNUserNotificationCenter.current().getPendingNotificationRequests { [weak self] requests in
            let notification = requests.first { $0.identifier == id }.map { self?.convertRequest($0) ?? [:] }
            if let requestId = requestId {
                self?.sendResponse?(NotificationResponse(
                    type: "notificationResponse",
                    requestId: requestId,
                    data: .init(notification: notification)
                ))
            }
        }
    }

    private func getDeliveredById(id: String, requestId: String?) {
        guard isRunningFromAppBundle else {
            if let requestId = requestId {
                sendResponse?(NotificationResponse(
                    type: "notificationResponse",
                    requestId: requestId,
                    data: .init(notification: nil)
                ))
            }
            return
        }

        UNUserNotificationCenter.current().getDeliveredNotifications { [weak self] notifications in
            let notification = notifications.first { $0.request.identifier == id }.map { self?.convertDelivered($0) ?? [:] }
            if let requestId = requestId {
                self?.sendResponse?(NotificationResponse(
                    type: "notificationResponse",
                    requestId: requestId,
                    data: .init(notification: notification)
                ))
            }
        }
    }

    // MARK: - Helpers

    private func buildNotificationContent(from config: NibMessage.NotificationConfig) -> UNMutableNotificationContent {
        let content = UNMutableNotificationContent()
        content.title = config.title

        if let body = config.body {
            content.body = body
        }
        if let subtitle = config.subtitle {
            content.subtitle = subtitle
        }

        // Sound
        if let sound = config.sound {
            if sound.name == "defaultCritical" {
                // Critical sound (requires entitlement)
                content.sound = UNNotificationSound.defaultCriticalSound(withAudioVolume: Float(sound.volume ?? 1.0))
            } else if sound.custom == true {
                // Custom sound
                content.sound = UNNotificationSound(named: UNNotificationSoundName(sound.name))
            } else {
                // Default sound
                content.sound = .default
            }
        }

        // Category for actions
        if let actions = config.actions, !actions.isEmpty {
            content.categoryIdentifier = "nib.\(config.id)"
        }

        return content
    }

    private func buildTrigger(from trigger: NibMessage.NotificationTrigger) -> UNNotificationTrigger? {
        debugPrint("NotificationService.buildTrigger: type=\(trigger.type), interval=\(String(describing: trigger.interval)), date=\(String(describing: trigger.date))")

        switch trigger.type {
        case "date":
            if let dateString = trigger.date {
                let formatter = ISO8601DateFormatter()
                formatter.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
                if let date = formatter.date(from: dateString) {
                    let components = Calendar.current.dateComponents([.year, .month, .day, .hour, .minute, .second], from: date)
                    debugPrint("NotificationService.buildTrigger: Parsed date successfully: \(date)")
                    return UNCalendarNotificationTrigger(dateMatching: components, repeats: trigger.repeats ?? false)
                } else {
                    debugPrint("NotificationService.buildTrigger: Failed to parse date: \(dateString)")
                }
            }
        case "interval":
            if let interval = trigger.interval {
                debugPrint("NotificationService.buildTrigger: Creating interval trigger for \(interval) seconds")
                if interval > 0 {
                    return UNTimeIntervalNotificationTrigger(timeInterval: interval, repeats: trigger.repeats ?? false)
                } else {
                    debugPrint("NotificationService.buildTrigger: Interval <= 0, skipping")
                }
            } else {
                debugPrint("NotificationService.buildTrigger: Interval is nil")
            }
        case "calendar":
            if let fromTime = trigger.fromTime {
                let components = parseTimeString(fromTime)
                return UNCalendarNotificationTrigger(dateMatching: components, repeats: trigger.repeats ?? true)
            }
        default:
            debugPrint("NotificationService.buildTrigger: Unknown trigger type: \(trigger.type)")
            break
        }
        return nil
    }

    private func parseTimeString(_ time: String) -> DateComponents {
        let parts = time.split(separator: ":")
        var components = DateComponents()
        if parts.count >= 2 {
            components.hour = Int(parts[0])
            components.minute = Int(parts[1])
        }
        return components
    }

    private func registerCategory(for notification: NibMessage.NotificationConfig) {
        guard let actions = notification.actions, !actions.isEmpty else { return }

        let categoryId = "nib.\(notification.id)"
        guard !registeredCategories.contains(categoryId) else { return }

        let unActions = actions.map { action -> UNNotificationAction in
            var options: UNNotificationActionOptions = []
            if let opts = action.options {
                if opts.contains("foreground") {
                    options.insert(.foreground)
                }
                if opts.contains("destructive") {
                    options.insert(.destructive)
                }
                if opts.contains("authenticationRequired") {
                    options.insert(.authenticationRequired)
                }
            }

            if let textInput = action.textInput {
                return UNTextInputNotificationAction(
                    identifier: action.id,
                    title: action.title,
                    options: options,
                    textInputButtonTitle: textInput.buttonTitle ?? "Send",
                    textInputPlaceholder: textInput.placeholder ?? ""
                )
            } else {
                return UNNotificationAction(
                    identifier: action.id,
                    title: action.title,
                    options: options
                )
            }
        }

        let category = UNNotificationCategory(
            identifier: categoryId,
            actions: unActions,
            intentIdentifiers: [],
            options: []
        )

        // Get existing categories and add new one
        UNUserNotificationCenter.current().getNotificationCategories { [weak self] existing in
            var categories = existing
            categories.insert(category)
            UNUserNotificationCenter.current().setNotificationCategories(categories)
            self?.registeredCategories.insert(categoryId)
        }
    }

    private func convertRequest(_ request: UNNotificationRequest) -> [String: Any] {
        let content = request.content
        return [
            "id": request.identifier,
            "title": content.title,
            "body": content.body,
            "subtitle": content.subtitle
        ]
    }

    private func convertDelivered(_ notification: UNNotification) -> [String: Any] {
        let content = notification.request.content
        return [
            "id": notification.request.identifier,
            "title": content.title,
            "body": content.body,
            "subtitle": content.subtitle
        ]
    }

    // MARK: - Legacy Notification API (NibMessage.NotifyPayload)

    /// Send a notification using the legacy API (simple title/body).
    /// Routes to modern or AppleScript fallback based on app bundle status.
    func sendLegacyNotification(_ payload: NibMessage.NotifyPayload) {
        if isRunningFromAppBundle {
            sendLegacyNotificationModern(payload)
        } else {
            sendLegacyNotificationViaAppleScript(payload)
        }
    }

    private func sendLegacyNotificationModern(_ payload: NibMessage.NotifyPayload) {
        let content = UNMutableNotificationContent()
        content.title = payload.title

        if let body = payload.body {
            content.body = body
        }
        if let subtitle = payload.subtitle {
            content.subtitle = subtitle
        }
        if payload.sound ?? true {
            content.sound = .default
        }

        let identifier = payload.identifier ?? UUID().uuidString

        let request = UNNotificationRequest(
            identifier: identifier,
            content: content,
            trigger: nil
        )

        UNUserNotificationCenter.current().add(request) { error in
            if let error = error {
                debugPrint("Failed to send notification: \(error)")
            } else {
                debugPrint("Notification sent: \(payload.title)")
            }
        }
    }

    private func sendLegacyNotificationViaAppleScript(_ payload: NibMessage.NotifyPayload) {
        let title = payload.title.replacingOccurrences(of: "\"", with: "\\\"")
        let body = (payload.body ?? "").replacingOccurrences(of: "\"", with: "\\\"")
        let subtitle = payload.subtitle?.replacingOccurrences(of: "\"", with: "\\\"")

        var script = "display notification \"\(body)\" with title \"\(title)\""
        if let sub = subtitle {
            script += " subtitle \"\(sub)\""
        }
        if payload.sound ?? true {
            script += " sound name \"default\""
        }

        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/osascript")
        process.arguments = ["-e", script]
        try? process.run()
        debugPrint("Notification sent (AppleScript): \(payload.title)")
    }

    // MARK: - UNUserNotificationCenterDelegate

    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification,
        withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void
    ) {
        // Show notification even when app is in foreground
        completionHandler([.banner, .sound])
    }

    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        didReceive response: UNNotificationResponse,
        withCompletionHandler completionHandler: @escaping () -> Void
    ) {
        let notificationId = response.notification.request.identifier
        let actionId = response.actionIdentifier

        // Check for text input
        var userText: String? = nil
        if let textResponse = response as? UNTextInputNotificationResponse {
            userText = textResponse.userText
        }

        // Map default actions
        var event = "action:\(actionId)"
        if actionId == UNNotificationDefaultActionIdentifier {
            event = "action:default"
        } else if actionId == UNNotificationDismissActionIdentifier {
            event = "action:dismiss"
        }

        if let text = userText {
            event += ":\(text)"
        }

        sendEvent?(notificationId, event)
        completionHandler()
    }
}
