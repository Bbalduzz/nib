import AppKit
import CoreText

/// Manages runtime font registration from file paths and URLs
class FontManager {
    static let shared = FontManager()

    /// Registered fonts by file path
    private var registeredPaths: Set<String> = []

    /// Mapping of custom font names to their actual font family names
    private var fontNameMapping: [String: String] = [:]

    /// Cache directory for downloaded fonts
    private lazy var cacheDirectory: URL = {
        let cacheDir = FileManager.default.urls(for: .cachesDirectory, in: .userDomainMask).first!
        let fontCacheDir = cacheDir.appendingPathComponent("nib-fonts")
        try? FileManager.default.createDirectory(at: fontCacheDir, withIntermediateDirectories: true)
        return fontCacheDir
    }()

    private init() {}

    /// Register fonts from a dictionary of name -> path/URL mappings
    /// - Parameter fonts: Dictionary mapping font names to paths or URLs
    func registerFonts(_ fonts: [String: String]) {
        for (name, source) in fonts {
            registerFont(name: name, source: source)
        }
    }

    /// Register a font with a custom name from a path or URL
    /// - Parameters:
    ///   - name: The name to use when referencing this font
    ///   - source: File path or URL to the font file
    func registerFont(name: String, source: String) {
        // Check if it's a URL
        if source.hasPrefix("http://") || source.hasPrefix("https://") {
            registerFontFromURL(name: name, urlString: source)
        } else {
            registerFontFromPath(name: name, path: source)
        }
    }

    /// Register a font from a local file path
    private func registerFontFromPath(name: String, path: String) {
        // Skip if already registered
        guard !registeredPaths.contains(path) else { return }

        let url = URL(fileURLWithPath: path)

        // Check if file exists
        guard FileManager.default.fileExists(atPath: path) else {
            print("[FontManager] Font file not found: \(path)")
            return
        }

        if registerFontFile(at: url, customName: name) {
            registeredPaths.insert(path)
        }
    }

    /// Register a font from a URL (downloads to cache)
    private func registerFontFromURL(name: String, urlString: String) {
        guard let url = URL(string: urlString) else {
            print("[FontManager] Invalid URL: \(urlString)")
            return
        }

        // Create a cache filename based on the URL
        let cacheFileName = url.lastPathComponent
        let cachedPath = cacheDirectory.appendingPathComponent(cacheFileName)

        // Check if already cached
        if FileManager.default.fileExists(atPath: cachedPath.path) {
            if !registeredPaths.contains(cachedPath.path) {
                if registerFontFile(at: cachedPath, customName: name) {
                    registeredPaths.insert(cachedPath.path)
                }
            }
            return
        }

        // Download font synchronously (for simplicity)
        print("[FontManager] Downloading font from: \(urlString)")
        do {
            let data = try Data(contentsOf: url)
            try data.write(to: cachedPath)
            print("[FontManager] Font cached at: \(cachedPath.path)")

            if registerFontFile(at: cachedPath, customName: name) {
                registeredPaths.insert(cachedPath.path)
            }
        } catch {
            print("[FontManager] Failed to download font: \(error)")
        }
    }

    /// Register a font file with CoreText and extract its family name
    private func registerFontFile(at url: URL, customName: String) -> Bool {
        var error: Unmanaged<CFError>?

        // Register font for this process only
        if CTFontManagerRegisterFontsForURL(url as CFURL, .process, &error) {
            // Extract the actual font family name from the file
            if let fontFamilyName = extractFontFamilyName(from: url) {
                fontNameMapping[customName] = fontFamilyName
                print("[FontManager] Registered '\(customName)' -> '\(fontFamilyName)' from \(url.path)")
            } else {
                // Fallback: use custom name as-is
                fontNameMapping[customName] = customName
                print("[FontManager] Registered '\(customName)' from \(url.path)")
            }
            return true
        }

        if let error = error?.takeRetainedValue() {
            print("[FontManager] Failed to register font: \(error)")
        }
        return false
    }

    /// Extract the font family name from a font file
    private func extractFontFamilyName(from url: URL) -> String? {
        guard let fontDataProvider = CGDataProvider(url: url as CFURL),
              let cgFont = CGFont(fontDataProvider) else {
            return nil
        }

        // Try to get the family name
        if let familyName = cgFont.postScriptName as String? {
            // PostScript name is usually available
            // But we want the family name, so let's try CTFont
            let ctFont = CTFontCreateWithGraphicsFont(cgFont, 12, nil, nil)
            if let familyName = CTFontCopyFamilyName(ctFont) as String? {
                return familyName
            }
            return familyName
        }

        return nil
    }

    /// Get the actual font family name for a custom name
    /// - Parameter customName: The custom name used when registering
    /// - Returns: The actual font family name, or the input if not found
    func resolvedFontName(_ customName: String) -> String {
        return fontNameMapping[customName] ?? customName
    }

    /// Register a font from a file path (legacy method)
    /// - Parameter path: Path to the .ttf or .otf font file
    /// - Returns: true if registration succeeded or font was already registered
    func registerFont(at path: String) -> Bool {
        // Skip if already registered
        guard !registeredPaths.contains(path) else { return true }

        let url = URL(fileURLWithPath: path)

        // Check if file exists
        guard FileManager.default.fileExists(atPath: path) else {
            print("[FontManager] Font file not found: \(path)")
            return false
        }

        var error: Unmanaged<CFError>?

        // Register font for this process only
        if CTFontManagerRegisterFontsForURL(url as CFURL, .process, &error) {
            registeredPaths.insert(path)
            print("[FontManager] Successfully registered font: \(path)")
            return true
        }

        if let error = error?.takeRetainedValue() {
            print("[FontManager] Failed to register font: \(error)")
        }
        return false
    }

    /// Get a font by name after registration
    /// - Parameters:
    ///   - name: Font family name (or custom registered name)
    ///   - size: Font size in points
    /// - Returns: NSFont if available, nil otherwise
    func font(named name: String, size: CGFloat) -> NSFont? {
        let resolvedName = resolvedFontName(name)
        return NSFont(name: resolvedName, size: size)
    }

    /// Check if a font is available by name
    func isFontAvailable(_ name: String) -> Bool {
        let resolvedName = resolvedFontName(name)
        return NSFont(name: resolvedName, size: 12) != nil
    }
}
