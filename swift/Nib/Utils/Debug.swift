import Foundation

private let logPath = "/tmp/nib.log"

/// Print to log file (like Python's print) - SYNCHRONOUS for debugging
func debugPrint(_ items: Any..., separator: String = " ", terminator: String = "\n") {
    let message = items.map { String(describing: $0) }.joined(separator: separator) + terminator
    let timestamp = ISO8601DateFormatter().string(from: Date())
    let line = "[\(timestamp)] \(message)"

    if let handle = FileHandle(forWritingAtPath: logPath) {
        handle.seekToEndOfFile()
        handle.write(line.data(using: .utf8)!)
        try? handle.synchronize()
        handle.closeFile()
    } else {
        FileManager.default.createFile(atPath: logPath, contents: line.data(using: .utf8))
    }
}

/// Clear the log file
func clearLog() {
    try? FileManager.default.removeItem(atPath: logPath)
}
