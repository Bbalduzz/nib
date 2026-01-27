import AppKit

// Handle --version flag
if CommandLine.arguments.contains("--version") || CommandLine.arguments.contains("-v") {
    print("nib-runtime \(NibVersion.version)")
    exit(0)
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate

// Don't show in dock (LSUIElement equivalent)
app.setActivationPolicy(.accessory)

app.run()
