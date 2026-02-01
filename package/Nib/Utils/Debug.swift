import Foundation

// MARK: - Log Configuration

private let logPath = "/tmp/nib.log"

/// Log levels matching Python implementation
enum LogLevel: Int, Comparable {
    case debug = 0
    case info = 1
    case warn = 2
    case error = 3

    var name: String {
        switch self {
        case .debug: return "DEBUG"
        case .info: return "INFO"
        case .warn: return "WARN"
        case .error: return "ERROR"
        }
    }

    static func < (lhs: LogLevel, rhs: LogLevel) -> Bool {
        lhs.rawValue < rhs.rawValue
    }
}

/// Global log configuration
final class LogConfig {
    static let shared = LogConfig()

    var minLevel: LogLevel = .info
    var fileEnabled: Bool = true
    var consoleEnabled: Bool = false  // Disabled by default for Swift (uses file)

    private init() {
        // Read from environment
        if let levelStr = ProcessInfo.processInfo.environment["NIB_LOG_LEVEL"]?.lowercased() {
            switch levelStr {
            case "debug": minLevel = .debug
            case "info": minLevel = .info
            case "warn", "warning": minLevel = .warn
            case "error": minLevel = .error
            default: break
            }
        }

        if let fileStr = ProcessInfo.processInfo.environment["NIB_LOG_FILE_ENABLED"]?.lowercased() {
            fileEnabled = !["0", "false", "no"].contains(fileStr)
        }

        if let consoleStr = ProcessInfo.processInfo.environment["NIB_LOG_CONSOLE"]?.lowercased() {
            consoleEnabled = ["1", "true", "yes"].contains(consoleStr)
        }
    }
}

// MARK: - Logger

/// Structured logger for nib framework
final class Logger {
    static let shared = Logger()

    private let dateFormatter: ISO8601DateFormatter = {
        let formatter = ISO8601DateFormatter()
        formatter.formatOptions = [.withInternetDateTime]
        return formatter
    }()

    private init() {}

    private func log(_ level: LogLevel, _ message: String, file: String = #file, function: String = #function) {
        guard level >= LogConfig.shared.minLevel else { return }

        let timestamp = dateFormatter.string(from: Date())
        let line = "[\(timestamp)] [\(level.name)] [Swift] \(message)\n"

        // Write to file
        if LogConfig.shared.fileEnabled {
            if let handle = FileHandle(forWritingAtPath: logPath) {
                handle.seekToEndOfFile()
                if let data = line.data(using: .utf8) {
                    handle.write(data)
                }
                try? handle.synchronize()
                handle.closeFile()
            } else {
                FileManager.default.createFile(atPath: logPath, contents: line.data(using: .utf8))
            }
        }

        // Write to console (stderr)
        if LogConfig.shared.consoleEnabled {
            fputs(line, stderr)
        }
    }

    func debug(_ message: String, file: String = #file, function: String = #function) {
        log(.debug, message, file: file, function: function)
    }

    func info(_ message: String, file: String = #file, function: String = #function) {
        log(.info, message, file: file, function: function)
    }

    func warn(_ message: String, file: String = #file, function: String = #function) {
        log(.warn, message, file: file, function: function)
    }

    func error(_ message: String, file: String = #file, function: String = #function) {
        log(.error, message, file: file, function: function)
    }
}

// MARK: - Global Functions (Convenience)

/// Global logger instance
let log = Logger.shared

/// Legacy debugPrint - now routes through structured logger at DEBUG level
func debugPrint(_ items: Any..., separator: String = " ", terminator: String = "") {
    let message = items.map { String(describing: $0) }.joined(separator: separator)
    log.debug(message)
}

/// Clear the log file
func clearLog() {
    try? FileManager.default.removeItem(atPath: logPath)
}
