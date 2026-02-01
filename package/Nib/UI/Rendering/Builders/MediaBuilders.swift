import SwiftUI

// MARK: - Media View Builders

extension DynamicView {
    @ViewBuilder
    func buildImage() -> some View {
        let styles = node.props.imageStyles
        let sourceType = node.props.sourceType
        let sourceValue = node.props.sourceValue
        let systemName = node.props.systemName

        Group {
            // SF Symbol (used by SFSymbol class)
            if let symbolName = systemName {
                Image(systemName: symbolName)
                    .applySFSymbolStyles(styles)
            }
            // URL image
            else if sourceType == "url", let urlString = sourceValue, let url = URL(string: urlString) {
                AsyncImage(url: url) { phase in
                    switch phase {
                    case .empty:
                        ProgressView()
                    case .success(let image):
                        image
                            .applyAsyncImageStyles(styles)
                    case .failure:
                        Image(systemName: "photo")
                            .foregroundColor(.secondary)
                    @unknown default:
                        Image(systemName: "photo")
                    }
                }
            }
            // File image
            else if sourceType == "file", let path = sourceValue {
                if let nsImage = NSImage(contentsOfFile: path) {
                    Image(nsImage: nsImage)
                        .applyImageStyles(styles)
                } else {
                    // Debug: log why image failed to load
                    let _ = {
                        let exists = FileManager.default.fileExists(atPath: path)
                        debugPrint("[Image] Failed to load file: \(path), exists: \(exists)")
                    }()
                    Image(systemName: "photo")
                        .foregroundColor(.secondary)
                }
            }
            // Base64 data image
            else if sourceType == "data",
                    let base64String = sourceValue,
                    let data = Data(base64Encoded: base64String),
                    let nsImage = NSImage(data: data) {
                Image(nsImage: nsImage)
                    .applyImageStyles(styles)
            }
            // Fallback
            else {
                let _ = {
                    if sourceType != nil {
                        debugPrint("[Image] Unknown sourceType: \(sourceType ?? "nil"), value: \(sourceValue ?? "nil")")
                    }
                }()
                Image(systemName: "photo")
                    .foregroundColor(.secondary)
            }
        }
    }

    @ViewBuilder
    func buildLink() -> some View {
        if let urlString = node.props.url, let url = URL(string: urlString) {
            // Check for custom content
            if let children = node.children, !children.isEmpty {
                Link(destination: url) {
                    ForEach(children) { child in
                        DynamicView(node: child, onEvent: onEvent)
                    }
                }
            } else {
                Link(node.props.label ?? urlString, destination: url)
            }
        } else {
            Text(node.props.label ?? "Invalid URL")
        }
    }
}

// MARK: - Image Styling

extension View {
    @ViewBuilder
    func applyImageStyles(_ styles: ViewNode.ImageStyles?) -> some View {
        if let styles = styles {
            self
                .applyResizable(styles)
                .applyScaling(styles)
                .applyAntialiased(styles)
                .applyBlur(styles)
        } else {
            self
        }
    }

    /// Apply SF Symbol-specific styles
    @ViewBuilder
    func applySFSymbolStyles(_ styles: ViewNode.ImageStyles?) -> some View {
        if let styles = styles {
            self
                .applySymbolRenderingMode(styles)
                .applySymbolConfiguration(styles)
        } else {
            self
        }
    }

    @ViewBuilder
    private func applySymbolRenderingMode(_ styles: ViewNode.ImageStyles) -> some View {
        if let mode = styles.symbolRenderingMode {
            switch mode.lowercased() {
            case "monochrome":
                self.symbolRenderingMode(.monochrome)
            case "hierarchical":
                self.symbolRenderingMode(.hierarchical)
            case "palette":
                self.symbolRenderingMode(.palette)
            case "multicolor":
                self.symbolRenderingMode(.multicolor)
            default:
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applySymbolConfiguration(_ styles: ViewNode.ImageStyles) -> some View {
        if let scale = styles.symbolScale, let s = Image.Scale.nib(scale) {
            self.imageScale(s)
                .fontWeight(Font.Weight.nib(styles.symbolWeight))
        } else if let weight = styles.symbolWeight {
            self.fontWeight(Font.Weight.nib(weight))
        } else {
            self
        }
    }

    /// Apply styles to an AsyncImage result (SwiftUI Image from async loading)
    @ViewBuilder
    func applyAsyncImageStyles(_ styles: ViewNode.ImageStyles?) -> some View {
        if let styles = styles {
            applyAsyncImageStylesInternal(styles)
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyAsyncImageStylesInternal(_ styles: ViewNode.ImageStyles) -> some View {
        // For async images, we need to handle resizable differently
        if let image = self as? SwiftUI.Image {
            let resizedImage = styles.resizable == true ? image.resizable(resizingMode: .stretch) : image

            if styles.scaledToFit == true {
                resizedImage.scaledToFit()
                    .applyAntialiased(styles)
                    .applyBlur(styles)
            } else if styles.scaledToFill == true {
                resizedImage.scaledToFill()
                    .applyAntialiased(styles)
                    .applyBlur(styles)
            } else {
                resizedImage
                    .applyAntialiased(styles)
                    .applyBlur(styles)
            }
        } else {
            let _ = debugPrint("[AsyncImage] Cast to Image failed, self type: \(type(of: self))")
            self
        }
    }

    @ViewBuilder
    private func applyResizable(_ styles: ViewNode.ImageStyles) -> some View {
        if styles.resizable == true {
            if let image = self as? Image {
                AnyView(image.resizable(resizingMode: .stretch))
            } else {
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyScaling(_ styles: ViewNode.ImageStyles) -> some View {
        if styles.scaledToFit == true {
            self.scaledToFit()
        } else if styles.scaledToFill == true {
            self.scaledToFill()
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyAntialiased(_ styles: ViewNode.ImageStyles) -> some View {
        if styles.antialiased == false {
            if let image = self as? Image {
                AnyView(image.interpolation(.none))
            } else {
                self
            }
        } else {
            self
        }
    }

    @ViewBuilder
    private func applyBlur(_ styles: ViewNode.ImageStyles) -> some View {
        if let blur = styles.blur, blur > 0 {
            self.blur(radius: blur)
        } else {
            self
        }
    }
}

// MARK: - Type Conversions
// Note: Font.Weight.nib is defined in FontModifiers.swift

extension Image.Scale {
    static func nib(_ value: String?) -> Image.Scale? {
        switch value?.lowercased() {
        case "small": return .small
        case "medium": return .medium
        case "large": return .large
        default: return nil
        }
    }
}
