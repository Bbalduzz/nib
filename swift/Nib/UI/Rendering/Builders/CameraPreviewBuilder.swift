import SwiftUI
import AVFoundation

// MARK: - Camera Preview Builder

extension DynamicView {
    @ViewBuilder
    func buildCameraPreview() -> some View {
        let deviceId = node.props.deviceId

        CameraPreviewView(deviceId: deviceId)
    }
}

// MARK: - Camera Preview View

struct CameraPreviewView: NSViewRepresentable {
    let deviceId: String?

    func makeNSView(context: Context) -> CameraPreviewNSView {
        let view = CameraPreviewNSView()
        view.setupCamera(deviceId: deviceId)
        return view
    }

    func updateNSView(_ nsView: CameraPreviewNSView, context: Context) {
        // Update device if changed
        if nsView.currentDeviceId != deviceId {
            nsView.setupCamera(deviceId: deviceId)
        }
    }
}

// MARK: - Camera Preview NSView

class CameraPreviewNSView: NSView {
    private var captureSession: AVCaptureSession?
    private var previewLayer: AVCaptureVideoPreviewLayer?
    var currentDeviceId: String?

    override init(frame frameRect: NSRect) {
        super.init(frame: frameRect)
        wantsLayer = true
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        wantsLayer = true
    }

    func setupCamera(deviceId: String?) {
        // Clean up existing session
        if let session = captureSession {
            session.stopRunning()
        }
        previewLayer?.removeFromSuperlayer()

        currentDeviceId = deviceId

        // Check authorization
        let authStatus = AVCaptureDevice.authorizationStatus(for: .video)
        if authStatus == .denied || authStatus == .restricted {
            showError("Camera access denied")
            return
        }

        if authStatus == .notDetermined {
            AVCaptureDevice.requestAccess(for: .video) { [weak self] granted in
                DispatchQueue.main.async {
                    if granted {
                        self?.configureSession(deviceId: deviceId)
                    } else {
                        self?.showError("Camera access not granted")
                    }
                }
            }
            return
        }

        configureSession(deviceId: deviceId)
    }

    private func configureSession(deviceId: String?) {
        // Find camera device
        let device: AVCaptureDevice?
        if let deviceId = deviceId {
            device = AVCaptureDevice(uniqueID: deviceId)
        } else {
            device = AVCaptureDevice.default(for: .video)
        }

        guard let captureDevice = device else {
            showError("No camera found")
            return
        }

        // Create session
        let session = AVCaptureSession()
        session.beginConfiguration()

        if session.canSetSessionPreset(.high) {
            session.sessionPreset = .high
        }

        // Add input
        do {
            let input = try AVCaptureDeviceInput(device: captureDevice)
            if session.canAddInput(input) {
                session.addInput(input)
            } else {
                showError("Cannot add camera input")
                return
            }
        } catch {
            showError("Error: \(error.localizedDescription)")
            return
        }

        session.commitConfiguration()

        // Create preview layer
        let preview = AVCaptureVideoPreviewLayer(session: session)
        preview.videoGravity = .resizeAspectFill
        preview.frame = bounds
        preview.autoresizingMask = [.layerWidthSizable, .layerHeightSizable]

        layer?.addSublayer(preview)
        previewLayer = preview
        captureSession = session

        // Start session on background thread
        DispatchQueue.global(qos: .userInitiated).async {
            session.startRunning()
        }
    }

    private func showError(_ message: String) {
        debugPrint("[CameraPreview] \(message)")

        // Show error text in view
        let textLayer = CATextLayer()
        textLayer.string = message
        textLayer.fontSize = 14
        textLayer.foregroundColor = NSColor.secondaryLabelColor.cgColor
        textLayer.alignmentMode = .center
        textLayer.frame = bounds
        textLayer.contentsScale = NSScreen.main?.backingScaleFactor ?? 2.0

        layer?.addSublayer(textLayer)
    }

    override func layout() {
        super.layout()
        previewLayer?.frame = bounds
    }

    deinit {
        captureSession?.stopRunning()
    }
}
