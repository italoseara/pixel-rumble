import socket
import threading

from packets import Packet, PacketStatusInPing, PacketStatusOutPong


class Server:
    """A UDP server that listens for incoming connections and handles client requests."""

    _ip: str
    port: int
    buffer_size: int

    sock: socket.socket

    clients: set[tuple[str, int]]
    running: bool

    def __init__(self, port: int, buffer_size: int = 1024) -> None:
        """Initializes the server with the specified host and port.

        Args:
            host (str): The host address to bind the server to.
            port (int): The port number to bind the server to.
            buffer_size (int): The size of the buffer for receiving data.
        """

        self._ip = None
        self.port = port
        self.buffer_size = buffer_size
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.clients = set()
        self.running = False

    @property
    def ip(self) -> str:
        if self._ip is None:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 1))
            self._ip = s.getsockname()[0]
            s.close()

        return self._ip

    def start(self) -> None:
        """Starts the server and begins listening for incoming connections."""
        
        if self.running:
            return

        self.sock.bind(('', self.port))
        self.running = True
        
        threading.Thread(target=self._listen_for_requests, daemon=True).start()
        print(f"[Server] Server started on port {self.port}.")

    def stop(self) -> None:
        """Stops the server and closes the socket."""
        
        if not self.running:
            return

        self.running = False
        self.sock.close()
        print("[Server] Server stopped.")

    def on_packet_received(self, packet: Packet, addr: tuple[str, int]) -> None:
        """Handles a received packet from a client.

        Args:
            packet (Packet): The received packet.
            addr (tuple[str, int]): The address of the client that sent the packet.
        """

        print(f"[Server] Received packet from {addr[0]}:{addr[1]}: {packet}")

        match packet:
            case ping if isinstance(ping, PacketStatusInPing):
                response_packet = PacketStatusOutPong(ip=self.ip, port=self.port)
                self.send(response_packet, addr)
            case _:
                print(f"[Server] Unhandled packet type: {packet.__class__.__name__}")

    def send(self, packet: Packet, addr: tuple[str, int]) -> None:
        """Sends a packet to the specified client address.

        Args:
            packet (Packet): The packet to send.
            client_address (tuple[str, int]): The address of the client to send the packet to.
        """
        
        if not self.running:
            raise RuntimeError("Server is not running.")
        if addr not in self.clients:
            raise ValueError(f"Client {addr[0]}:{addr[1]} is not connected.")

        data = packet.to_bytes()
        self.sock.sendto(data, addr)
        print(f"[Server] Sent packet to {addr[0]}:{addr[1]}: {packet}")

    def broadcast(self, packet: Packet) -> None:
        """Broadcasts a packet to all connected clients."""

        if not self.running:
            raise RuntimeError("Server is not running.")

        print(f"[Server] Broadcasting packet: {packet}")

        data = packet.to_bytes()
        for client in self.clients:
            self.sock.sendto(data, client)

    def _listen_for_requests(self) -> None:
        """Listens for incoming requests from clients."""

        while self.running:
            try:
                data, addr = self.sock.recvfrom(self.buffer_size)
                if addr not in self.clients:
                    self.clients.add(addr)
                    print(f"[Server] New client connected: {addr[0]}:{addr[1]}")

                packet = Packet.from_bytes(data)
                self.on_packet_received(packet, addr)

            except Exception as e:
                print(f"[Server] Error while listening for requests: {e}")

    def __repr__(self) -> str:
        """Return a string representation of the server."""

        return f"<Server address={self.address} running={self.running} clients={len(self.clients)}>"


if __name__ == "__main__":
    server = Server(port=3567)

    try:
        server.start()
        while True:
            pass  # Keep the server running
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()