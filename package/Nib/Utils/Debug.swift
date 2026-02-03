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

    var minLevel: LogLevel = .debug
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

    private let dateFormatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd HH:mm:ss.SSS"
        return formatter
    }()

    private init() {}

    private func log(_ level: LogLevel, _ message: String, file: String = #file, function: String = #function, line lineNum: Int = #line) {
        guard level >= LogConfig.shared.minLevel else { return }

        let timestamp = dateFormatter.string(from: Date())
        let levelName = level.name.padding(toLength: 8, withPad: " ", startingAt: 0)
        let fileName = (file as NSString).lastPathComponent.replacingOccurrences(of: ".swift", with: "")
        let location = "\(fileName):\(function):\(lineNum)"
        let line = "\(timestamp) | \(levelName) | swift  | \(location) - \(message)\n"

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

    func debug(_ message: String, file: String = #file, function: String = #function, line: Int = #line) {
        log(.debug, message, file: file, function: function, line: line)
    }

    func info(_ message: String, file: String = #file, function: String = #function, line: Int = #line) {
        log(.info, message, file: file, function: function, line: line)
    }

    func warn(_ message: String, file: String = #file, function: String = #function, line: Int = #line) {
        log(.warn, message, file: file, function: function, line: line)
    }

    func error(_ message: String, file: String = #file, function: String = #function, line: Int = #line) {
        log(.error, message, file: file, function: function, line: line)
    }
}

// MARK: - Global Functions (Convenience)

/// Global logger instance
let log = Logger.shared

/// Legacy debugPrint - now routes through structured logger at DEBUG level
func debugPrint(_ items: Any..., separator: String = " ", terminator: String = "", file: String = #file, function: String = #function, line: Int = #line) {
    let message = items.map { String(describing: $0) }.joined(separator: separator)
    log.debug(message, file: file, function: function, line: line)
}

/// Clear the log file
func clearLog() {
    try? FileManager.default.removeItem(atPath: logPath)
}
