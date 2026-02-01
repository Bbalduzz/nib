import SwiftUI
import AVKit
import AppKit

// MARK: - Video View Builder

extension DynamicView {
    @ViewBuilder
    func buildVideo() -> some View {
        let settings = node.props.videoSettings
        let sourceType = node.props.sourceType
        let sourceValue = node.props.sourceValue

        if let urlString = sourceValue {
            let url: URL? = {
                if sourceType == "url" {
                    return URL(string: urlString)
                } else if sourceType == "file" {
                    return URL(fileURLWithPath: urlString)
                }
                return nil
            }()

            if let videoURL = url {
                AppKitVideoPlayer(
                    url: videoURL,
                    autoplay: settings?.autoplay ?? false,
                    loop: settings?.loop ?? false,
                    muted: settings?.muted ?? false,
                    showControls: settings?.controls ?? true
                )
            } else {
                videoPlaceholder("Invalid URL")
            }
        } else {
            videoPlaceholder("No video source")
        }
    }

    @ViewBuilder
    private func videoPlaceholder(_ message: String) -> some View {
        ZStack {
            Rectangle()
                .fill(Color.black)
            VStack(spacing: 8) {
                Image(systemName: "video.slash")
                    .font(.largeTitle)
                    .foregroundColor(.gray)
                Text(message)
                    .font(.caption)
                    .foregroundColor(.gray)
            }
        }
    }
}

// MARK: - AppKit Video Player (works in popovers)

struct AppKitVideoPlayer: NSViewRepresentable {
    let url: URL
    let autoplay: Bool
    let loop: Bool
    let muted: Bool
    let showControls: Bool

    func makeNSView(context: Context) -> AVPlayerView {
        let playerView = AVPlayerView()
        playerView.controlsStyle = showControls ? .inline : .none
        playerView.showsFullScreenToggleButton = false

        // Prevent intrinsic size from affecting popover layout
        playerView.setContentHuggingPriority(.defaultLow, for: .horizontal)
        playerView.setContentHuggingPriority(.defaultLow, for: .vertical)
        playerView.setContentCompressionResistancePriority(.defaultLow, for: .horizontal)
        playerView.setContentCompressionResistancePriority(.defaultLow, for: .vertical)

        // Create player
        let player = AVPlayer(url: url)
        player.isMuted = muted
        playerView.player = player

        // Store for looping
        context.coordinator.player = player
        context.coordinator.loop = loop

        // Setup looping observer
        if loop {
            context.coordinator.setupLoopObserver()
        }

        // Autoplay
        if autoplay {
            DispatchQueue.main.async {
                player.play()
            }
        }

        return playerView
    }

    func updateNSView(_ nsView: AVPlayerView, context: Context) {
        nsView.controlsStyle = showControls ? .inline : .none
        nsView.player?.isMuted = muted
    }

    static func dismantleNSView(_ nsView: AVPlayerView, coordinator: Coordinator) {
        coordinator.cleanup()
        nsView.player?.pause()
        nsView.player = nil
    }

    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    class Coordinator {
        var player: AVPlayer?
        var loop: Bool = false
        var loopObserver: NSObjectProtocol?

        func setupLoopObserver() {
            guard let player = player else { return }
            loopObserver = NotificationCenter.default.addObserver(
                forName: .AVPlayerItemDidPlayToEndTime,
                object: player.currentItem,
                queue: .main
            ) { [weak self] _ in
                self?.player?.seek(to: .zero)
                self?.player?.play()
            }
        }

        func cleanup() {
            if let observer = loopObserver {
                NotificationCenter.default.removeObserver(observer)
            }
            loopObserver = nil
            player = nil
        }
    }
}
