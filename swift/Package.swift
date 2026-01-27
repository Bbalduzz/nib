// swift-tools-version:5.9
import PackageDescription
import Foundation

let packageDir = URL(fileURLWithPath: #file).deletingLastPathComponent().path
let infoPlistPath = "\(packageDir)/Nib/Info.plist"

let package = Package(
    name: "Nib",
    platforms: [
        .macOS(.v14)  // Required for @Observable macro
    ],
    products: [
        .executable(name: "nib-runtime", targets: ["Nib"])
    ],
    dependencies: [
        .package(url: "https://github.com/Flight-School/MessagePack.git", from: "1.2.4")
    ],
    targets: [
        .executableTarget(
            name: "Nib",
            dependencies: ["MessagePack"],
            path: "Nib",
            exclude: ["Info.plist"],
            linkerSettings: [
                .unsafeFlags([
                    "-Xlinker", "-sectcreate",
                    "-Xlinker", "__TEXT",
                    "-Xlinker", "__info_plist",
                    "-Xlinker", infoPlistPath
                ])
            ]
        )
    ]
)
