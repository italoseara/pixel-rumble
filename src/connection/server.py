import socket
import threading

from packets import PacketStatusInPing, PacketStatusOutPong, Packet

DISCOVERY_PORT = 3567
PACKET_SIZE    = 1024

class DiscoveryServer:
    """A UDP server that allows clients to discover the game server via broadcast."""
    
    def __init__(self, port: int) -> None:
        """Initializes the DiscoveryServer.

        Args:
            port (int): The port on which the original game server is running.
        """
        
        self.port = port
        self.running = False
        self.server_socket = None

    def start(self) -> None:
        if self.running:
            return

        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of the address
        
        self.server_socket.bind(('', DISCOVERY_PORT))
        threading.Thread(target=self._listen_for_requests, daemon=True).start()
        self.log(f"UDP server started on port {DISCOVERY_PORT}.")

    def stop(self) -> None:
        if not self.running:
            return

        self.running = False
        if self.server_socket:
            self.server_socket.close()
        self.server_socket = None

        self.log("UDP server stopped.")

    def log(self, message: str) -> None:
        """Logs a message to the console."""

        print(f"[Discovery] {message}")

    def send_packet(self, packet: Packet, address: tuple[str, int]) -> None:
        """Sends a packet to the specified address.

        Args:
            packet (Packet): The packet to send.
            address (tuple[str, int]): The address to send the packet to (IP, port).
        """
        
        if not self.running:
            raise RuntimeError("Server is not running.")
        
        self.server_socket.sendto(packet.to_bytes(), address)
        self.log(f"Sent packet to {address[0]}:{address[1]}")

    def _listen_for_requests(self) -> None:
        while self.running:
            try:
                data, addr = self.server_socket.recvfrom(PACKET_SIZE)
                packet = Packet.from_bytes(data)

                if isinstance(packet, PacketStatusInPing):
                    self.log(f"Received ping from {addr[0]}:{addr[1]}")
                    response_packet = PacketStatusOutPong(ip=addr[0], port=self.port)
                    self.send_packet(response_packet, addr)
                else:
                    self.log(f"Received unknown packet type from {addr[0]}:{addr[1]}")
            except Exception as e:
                self.log(f"Error processing packet: {e}")
                if not self.running:  # Ignore exceptions on shutdown
                    break


if __name__ == "__main__":
    # Replace with the actual game server port
    discovery_server = DiscoveryServer(port=5555)
    
    try:
        discovery_server.start()
        while True:
            pass  # Keep the server running
    except KeyboardInterrupt:
        pass
    finally:
        discovery_server.stop()