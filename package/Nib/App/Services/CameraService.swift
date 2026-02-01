import AVFoundation
import AppKit

/// Camera device information
struct CameraDevice: Codable {
    var id: String
    var name: String
    var position: String      // "front", "back", "external"
    var isBuiltIn: Bool
}

/// Handles camera capture and streaming
class CameraService: NSObject {
    static let shared = CameraService()

    private var captureSession: AVCaptureSession?
    private var photoOutput: AVCapturePhotoOutput?
    private var videoOutput: AVCaptureVideoDataOutput?
    private var currentDevice: AVCaptureDevice?

    // Streaming state
    private var isStreaming = false
    private var streamFPS: Int = 30
    private var lastFrameTime: CFTimeInterval = 0
    private var streamSendResponse: ((NibServiceResponse) -> Void)?
    private var streamRequestId: String?

    // Photo capture state
    private var photoCaptureCompletion: ((Data?, Int, Int) -> Void)?

    private let sessionQueue = DispatchQueue(label: "nib.camera.session")

    private override init() {
        super.init()
    }

    func handle(_ payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        switch payload.action {
        case "listDevices":
            handleListDevices(requestId: payload.requestId, sendResponse: sendResponse)
        case "capturePhoto":
            handleCapturePhoto(payload: payload, sendResponse: sendResponse)
        case "startStream":
            handleStartStream(payload: payload, sendResponse: sendResponse)
        case "stopStream":
            handleStopStream(requestId: payload.requestId, sendResponse: sendResponse)
        default:
            debugPrint("Unknown camera action:", payload.action)
        }
    }

    // MARK: - List Devices

    private func handleListDevices(requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        var devices: [CameraDevice] = []

        // Get all video devices
        var deviceTypes: [AVCaptureDevice.DeviceType] = [.builtInWideAngleCamera]
        if #available(macOS 14.0, *) {
            deviceTypes.append(.external)
        } else {
            deviceTypes.append(.externalUnknown)
        }
        let discoverySession = AVCaptureDevice.DiscoverySession(
            deviceTypes: deviceTypes,
            mediaType: .video,
            position: .unspecified
        )

        for device in discoverySession.devices {
            let position: String
            switch device.position {
            case .front: position = "front"
            case .back: position = "back"
            default: position = "external"
            }

            let cameraDevice = CameraDevice(
                id: device.uniqueID,
                name: device.localizedName,
                position: position,
                isBuiltIn: device.position != .unspecified
            )
            devices.append(cameraDevice)
        }

        var data = NibServiceResponse.ServiceResponseData()
        data.devices = devices

        let response = NibServiceResponse(service: "camera", requestId: requestId, data: data)
        sendResponse(response)
    }

    // MARK: - Capture Photo

    private func handleCapturePhoto(payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        let deviceId = payload.params?["deviceId"]?.value as? String
        let format = payload.params?["format"]?.value as? String ?? "jpeg"
        let quality = payload.params?["quality"]?.value as? Double ?? 0.9

        sessionQueue.async { [weak self] in
            guard let self = self else { return }

            // Set up capture session if needed
            if !self.setupCaptureSession(deviceId: deviceId) {
                DispatchQueue.main.async {
                    var data = NibServiceResponse.ServiceResponseData()
                    data.success = false
                    let response = NibServiceResponse(service: "camera", requestId: payload.requestId, data: data)
                    sendResponse(response)
                }
                return
            }

            // Ensure photo output is configured
            guard let photoOutput = self.photoOutput else {
                DispatchQueue.main.async {
                    var data = NibServiceResponse.ServiceResponseData()
                    data.success = false
                    let response = NibServiceResponse(service: "camera", requestId: payload.requestId, data: data)
                    sendResponse(response)
                }
                return
            }

            // Store completion handler
            self.photoCaptureCompletion = { imageData, width, height in
                DispatchQueue.main.async {
                    var data = NibServiceResponse.ServiceResponseData()
                    if let imageData = imageData {
                        // Convert to requested format
                        let finalData: Data?
                        if format == "png" {
                            if let nsImage = NSImage(data: imageData),
                               let tiffData = nsImage.tiffRepresentation,
                               let bitmapRep = NSBitmapImageRep(data: tiffData) {
                                finalData = bitmapRep.representation(using: .png, properties: [:])
                            } else {
                                finalData = imageData
                            }
                        } else {
                            // JPEG with quality
                            if let nsImage = NSImage(data: imageData),
                               let tiffData = nsImage.tiffRepresentation,
                               let bitmapRep = NSBitmapImageRep(data: tiffData) {
                                finalData = bitmapRep.representation(using: .jpeg, properties: [.compressionFactor: quality])
                            } else {
                                finalData = imageData
                            }
                        }

                        data.imageData = finalData
                        data.imageWidth = width
                        data.imageHeight = height
                        data.imageFormat = format
                        data.success = true
                    } else {
                        data.success = false
                    }

                    let response = NibServiceResponse(service: "camera", requestId: payload.requestId, data: data)
                    sendResponse(response)
                }
            }

            // Capture photo
            let settings = AVCapturePhotoSettings()
            photoOutput.capturePhoto(with: settings, delegate: self)
        }
    }

    // MARK: - Stream Video

    private func handleStartStream(payload: NibMessage.ServicePayload, sendResponse: @escaping (NibServiceResponse) -> Void) {
        let deviceId = payload.params?["deviceId"]?.value as? String
        let fps = payload.params?["fps"]?.value as? Int ?? 30

        sessionQueue.async { [weak self] in
            guard let self = self else { return }

            // Stop existing stream
            self.stopStreamInternal()

            // Set up capture session
            if !self.setupCaptureSession(deviceId: deviceId, forStreaming: true) {
                DispatchQueue.main.async {
                    var data = NibServiceResponse.ServiceResponseData()
                    data.success = false
                    data.isStreaming = false
                    let response = NibServiceResponse(service: "camera", requestId: payload.requestId, data: data)
                    sendResponse(response)
                }
                return
            }

            self.streamFPS = fps
            self.isStreaming = true
            self.streamSendResponse = sendResponse
            self.streamRequestId = payload.requestId
            self.lastFrameTime = 0

            // Send confirmation
            DispatchQueue.main.async {
                var data = NibServiceResponse.ServiceResponseData()
                data.success = true
                data.isStreaming = true
                let response = NibServiceResponse(service: "camera", requestId: payload.requestId, data: data)
                sendResponse(response)
            }
        }
    }

    private func handleStopStream(requestId: String, sendResponse: @escaping (NibServiceResponse) -> Void) {
        sessionQueue.async { [weak self] in
            self?.stopStreamInternal()

            DispatchQueue.main.async {
                var data = NibServiceResponse.ServiceResponseData()
                data.success = true
                data.isStreaming = false
                let response = NibServiceResponse(service: "camera", requestId: requestId, data: data)
                sendResponse(response)
            }
        }
    }

    private func stopStreamInternal() {
        isStreaming = false
        streamSendResponse = nil
        streamRequestId = nil

        if let session = captureSession, session.isRunning {
            session.stopRunning()
        }
        captureSession = nil
        photoOutput = nil
        videoOutput = nil
        currentDevice = nil
    }

    // MARK: - Setup

    private func setupCaptureSession(deviceId: String? = nil, forStreaming: Bool = false) -> Bool {
        // Check camera authorization
        let authStatus = AVCaptureDevice.authorizationStatus(for: .video)
        if authStatus == .denied || authStatus == .restricted {
            debugPrint("Camera access denied")
            return false
        }

        if authStatus == .notDetermined {
            // Request permission synchronously for simplicity
            var granted = false
            let semaphore = DispatchSemaphore(value: 0)
            AVCaptureDevice.requestAccess(for: .video) { result in
                granted = result
                semaphore.signal()
            }
            semaphore.wait()
            if !granted {
                debugPrint("Camera access not granted")
                return false
            }
        }

        // Find camera device
        let device: AVCaptureDevice?
        if let deviceId = deviceId {
            device = AVCaptureDevice(uniqueID: deviceId)
        } else {
            // Use default camera
            device = AVCaptureDevice.default(for: .video)
        }

        guard let captureDevice = device else {
            debugPrint("No camera device found")
            return false
        }

        // Create session
        let session = AVCaptureSession()
        session.beginConfiguration()

        // Set preset
        if session.canSetSessionPreset(.photo) {
            session.sessionPreset = .photo
        }

        // Add input
        do {
            let input = try AVCaptureDeviceInput(device: captureDevice)
            if session.canAddInput(input) {
                session.addInput(input)
            } else {
                debugPrint("Cannot add camera input")
                return false
            }
        } catch {
            debugPrint("Error creating camera input: \(error)")
            return false
        }

        // Add photo output
        let photo = AVCapturePhotoOutput()
        if session.canAddOutput(photo) {
            session.addOutput(photo)
            self.photoOutput = photo
        }

        // Add video output for streaming
        if forStreaming {
            let video = AVCaptureVideoDataOutput()
            video.videoSettings = [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA]
            video.setSampleBufferDelegate(self, queue: sessionQueue)
            video.alwaysDiscardsLateVideoFrames = true

            if session.canAddOutput(video) {
                session.addOutput(video)
                self.videoOutput = video
            }
        }

        session.commitConfiguration()

        self.captureSession = session
        self.currentDevice = captureDevice

        // Start session
        session.startRunning()

        return true
    }
}

// MARK: - AVCapturePhotoCaptureDelegate

extension CameraService: AVCapturePhotoCaptureDelegate {
    func photoOutput(_ output: AVCapturePhotoOutput, didFinishProcessingPhoto photo: AVCapturePhoto, error: Error?) {
        if let error = error {
            debugPrint("Photo capture error: \(error)")
            photoCaptureCompletion?(nil, 0, 0)
            photoCaptureCompletion = nil
            return
        }

        guard let imageData = photo.fileDataRepresentation() else {
            debugPrint("Could not get photo data")
            photoCaptureCompletion?(nil, 0, 0)
            photoCaptureCompletion = nil
            return
        }

        let width = Int(photo.resolvedSettings.photoDimensions.width)
        let height = Int(photo.resolvedSettings.photoDimensions.height)

        photoCaptureCompletion?(imageData, width, height)
        photoCaptureCompletion = nil
    }
}

// MARK: - AVCaptureVideoDataOutputSampleBufferDelegate

extension CameraService: AVCaptureVideoDataOutputSampleBufferDelegate {
    func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        guard isStreaming, let sendResponse = streamSendResponse else { return }

        // Rate limit based on FPS
        let currentTime = CACurrentMediaTime()
        let frameInterval = 1.0 / Double(streamFPS)
        if currentTime - lastFrameTime < frameInterval {
            return
        }
        lastFrameTime = currentTime

        // Convert to JPEG
        guard let imageBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }

        let ciImage = CIImage(cvPixelBuffer: imageBuffer)
        let context = CIContext()

        let width = CVPixelBufferGetWidth(imageBuffer)
        let height = CVPixelBufferGetHeight(imageBuffer)

        guard let cgImage = context.createCGImage(ciImage, from: ciImage.extent) else { return }

        let nsImage = NSImage(cgImage: cgImage, size: NSSize(width: width, height: height))
        guard let tiffData = nsImage.tiffRepresentation,
              let bitmapRep = NSBitmapImageRep(data: tiffData),
              let jpegData = bitmapRep.representation(using: .jpeg, properties: [.compressionFactor: 0.7]) else {
            return
        }

        // Send frame
        var data = NibServiceResponse.ServiceResponseData()
        data.imageData = jpegData
        data.imageWidth = width
        data.imageHeight = height
        data.imageFormat = "jpeg"
        data.isStreamFrame = true

        let response = NibServiceResponse(service: "camera", requestId: streamRequestId ?? "", data: data)
        DispatchQueue.main.async {
            sendResponse(response)
        }
    }
}
