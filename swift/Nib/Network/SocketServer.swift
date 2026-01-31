import Foundation
import MessagePack

class SocketServer {
    private let path: String
    private var serverSocket: Int32 = -1
    private var clientSocket: Int32 = -1
    private var isRunning = false
    private let queue = DispatchQueue(label: "nib.socket", qos: .userInteractive)

    private let encoder = MessagePackEncoder()
    private let decoder = MessagePackDecoder()

    var onMessage: ((NibMessage) -> Void)?

    init(path: String) {
        self.path = path
    }

    func start() {
        queue.async { [weak self] in
            self?.setupServer()
        }
    }

    func stop() {
        isRunning = false

        if clientSocket >= 0 {
            close(clientSocket)
            clientSocket = -1
        }
        if serverSocket >= 0 {
            close(serverSocket)
            serverSocket = -1
        }
        unlink(path)
    }

    func sendEvent(nodeId: String, event: String) {
        debugPrint("SocketServer.sendEvent called - nodeId:", nodeId, "event:", event)
        debugPrint("clientSocket:", clientSocket)

        guard clientSocket >= 0 else {
            debugPrint("No client socket, cannot send event")
            return
        }

        debugPrint("Creating NibEvent...")
        let eventData = NibEvent(nodeId: nodeId, event: event)
        debugPrint("NibEvent created, encoding...")

        do {
            let packed = try encoder.encode(eventData)
            debugPrint("Event packed, size:", packed.count, "bytes")
            sendMessage(packed)
            debugPrint("Event sent successfully")
        } catch {
            debugPrint("Failed to pack event:", error)
        }
    }

    private func setupServer() {
        // Remove existing socket file
        unlink(path)

        // Create socket
        serverSocket = socket(AF_UNIX, SOCK_STREAM, 0)
        guard serverSocket >= 0 else {
            print("Failed to create socket")
            return
        }

        // Bind to path
        var addr = sockaddr_un()
        addr.sun_family = sa_family_t(AF_UNIX)
        withUnsafeMutablePointer(to: &addr.sun_path.0) { ptr in
            path.utf8CString.withUnsafeBufferPointer { buffer in
                _ = memcpy(ptr, buffer.baseAddress!, min(buffer.count, 104))
            }
        }

        let bindResult = withUnsafePointer(to: &addr) { ptr in
            ptr.withMemoryRebound(to: sockaddr.self, capacity: 1) { sockaddrPtr in
                bind(serverSocket, sockaddrPtr, socklen_t(MemoryLayout<sockaddr_un>.size))
            }
        }

        guard bindResult == 0 else {
            print("Failed to bind socket: \(errno)")
            return
        }

        // Listen
        guard listen(serverSocket, 1) == 0 else {
            print("Failed to listen on socket")
            return
        }

        isRunning = true
        print("Socket server listening on \(path)")

        // Accept connections in loop
        acceptLoop()
    }

    private func acceptLoop() {
        while isRunning {
            var clientAddr = sockaddr_un()
            var clientAddrLen = socklen_t(MemoryLayout<sockaddr_un>.size)

            let newSocket = withUnsafeMutablePointer(to: &clientAddr) { ptr in
                ptr.withMemoryRebound(to: sockaddr.self, capacity: 1) { sockaddrPtr in
                    accept(serverSocket, sockaddrPtr, &clientAddrLen)
                }
            }

            guard newSocket >= 0 else {
                if isRunning {
                    print("Accept failed: \(errno)")
                }
                continue
            }

            print("Client connected")
            clientSocket = newSocket
            handleClient(newSocket)
        }
    }

    private func handleClient(_ socket: Int32) {
        var buffer = Data()
        let readBuffer = UnsafeMutablePointer<UInt8>.allocate(capacity: 4096)
        defer { readBuffer.deallocate() }

        while isRunning && clientSocket >= 0 {
            let bytesRead = read(socket, readBuffer, 4096)

            if bytesRead <= 0 {
                print("Client disconnected")
                clientSocket = -1
                break
            }

            buffer.append(readBuffer, count: bytesRead)

            debugPrint("Received \(bytesRead) bytes, buffer now \(buffer.count) bytes")

            while let message = extractMessage(from: &buffer) {
                debugPrint("Extracted message of \(message.count) bytes, processing...")
                processMessage(message)
                debugPrint("Message processed, buffer now \(buffer.count) bytes")
            }
            debugPrint("No more complete messages in buffer")
        }
    }

    private func extractMessage(from buffer: inout Data) -> Data? {
        debugPrint("extractMessage: buffer size =", buffer.count)

        // MessagePack messages with length prefix: 4 bytes big-endian length + msgpack data
        guard buffer.count >= 4 else {
            debugPrint("extractMessage: buffer too small for length prefix")
            return nil
        }

        debugPrint("extractMessage: reading length prefix...")
        let lengthBytes = [UInt8](buffer.prefix(4))
        let length =
            UInt32(lengthBytes[0]) << 24 | UInt32(lengthBytes[1]) << 16 | UInt32(lengthBytes[2])
            << 8 | UInt32(lengthBytes[3])
        debugPrint("extractMessage: length =", length)

        let totalNeeded = 4 + Int(length)
        guard buffer.count >= totalNeeded else {
            debugPrint("extractMessage: buffer too small for message, need", totalNeeded)
            return nil
        }

        debugPrint("extractMessage: extracting message data...")
        // avoid threading issues
        let messageData = Data(buffer[4..<totalNeeded])
        debugPrint("extractMessage: got message data, size =", messageData.count)

        debugPrint("extractMessage: creating new buffer without message...")
        buffer = Data(buffer[totalNeeded...])
        debugPrint("extractMessage: done, returning", messageData.count, "bytes")

        return messageData
    }

    private func processMessage(_ data: Data) {
        debugPrint("Processing message of \(data.count) bytes")
        do {
            let raw = try decoder.decode(RawMessage.self, from: data)
            debugPrint("Decoded message type:", raw.type)
            if let root = raw.payload?.root {
                debugPrint("Root view type:", root.type)
            }
            if let patches = raw.payload?.patches {
                debugPrint("Patches count:", patches.count)
            }
            let message = parseMessage(raw)
            onMessage?(message)
            debugPrint("Message dispatched to handler")
        } catch {
            debugPrint("Failed to process message:", error)
        }
    }

    private func parseMessage(_ raw: RawMessage) -> NibMessage {
        debugPrint("parseMessage: type =", raw.type)
        switch raw.type {
        case "render":
            let payload = NibMessage.RenderPayload(
                root: raw.payload?.root,
                statusBar: raw.payload?.statusBar.map {
                    NibMessage.RenderPayload.StatusBarConfig(icon: $0.icon, title: $0.title)
                },
                window: raw.payload?.window.map {
                    NibMessage.WindowConfig(width: $0.width, height: $0.height)
                },
                menu: raw.payload?.menu,
                hotkeys: raw.payload?.hotkeys,
                fonts: raw.payload?.fonts
            )
            return .render(payload)
        case "patch":
            debugPrint("parseMessage: parsing patch, patches count =", raw.payload?.patches?.count ?? 0)
            let payload = NibMessage.PatchPayload(
                patches: raw.payload?.patches ?? [],
                statusBar: raw.payload?.statusBar.map {
                    NibMessage.PatchPayload.StatusBarConfig(icon: $0.icon, title: $0.title)
                },
                window: raw.payload?.window.map {
                    NibMessage.WindowConfig(width: $0.width, height: $0.height)
                }
            )
            return .patch(payload)
        case "notify":
            let payload = NibMessage.NotifyPayload(
                title: raw.payload?.title ?? "Notification",
                body: raw.payload?.body,
                subtitle: raw.payload?.subtitle,
                sound: raw.payload?.sound,
                identifier: raw.payload?.identifier
            )
            return .notify(payload)
        case "clipboard":
            let payload = NibMessage.ClipboardPayload(
                action: raw.payload?.action ?? "read",
                content: raw.payload?.content,
                requestId: raw.payload?.requestId
            )
            return .clipboard(payload)
        case "fileDialog":
            let payload = NibMessage.FileDialogPayload(
                action: raw.payload?.action ?? "open",
                title: raw.payload?.title,
                types: raw.payload?.types,
                multiple: raw.payload?.multiple,
                directory: raw.payload?.directory,
                defaultName: raw.payload?.defaultName,
                requestId: raw.payload?.requestId ?? ""
            )
            return .fileDialog(payload)
        case "service":
            let payload = NibMessage.ServicePayload(
                service: raw.payload?.service ?? "",
                action: raw.payload?.action ?? "",
                requestId: raw.payload?.requestId ?? "",
                params: raw.payload?.params
            )
            return .service(payload)
        case "action":
            let payload = NibMessage.ActionPayload(
                nodeId: raw.payload?.nodeId ?? "",
                action: raw.payload?.action ?? "",
                params: raw.payload?.params
            )
            return .action(payload)
        case "quit":
            return .quit
        default:
            print("Unknown message type: \(raw.type)")
            return .quit
        }
    }

    private func sendMessage(_ data: Data) {
        guard clientSocket >= 0 else { return }

        // Length prefix
        var length = UInt32(data.count).bigEndian
        let lengthData = Data(bytes: &length, count: 4)

        var fullMessage = lengthData
        fullMessage.append(data)

        _ = fullMessage.withUnsafeBytes { ptr in
            write(clientSocket, ptr.baseAddress!, fullMessage.count)
        }
    }

    func sendServiceResponse(_ response: NibServiceResponse) {
        debugPrint("Sending service response for:", response.service)
        guard clientSocket >= 0 else {
            debugPrint("No client connected for service response")
            return
        }

        do {
            let packed = try encoder.encode(response)
            sendMessage(packed)
            debugPrint("Service response sent successfully")
        } catch {
            debugPrint("Failed to encode service response:", error)
        }
    }
}
