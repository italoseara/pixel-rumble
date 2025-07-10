import time
import socket
import threading

from packets import *


class Client:
    """A UDP client that connects to a server and sends/receives packets."""

    name: str
    address: tuple[str, int]
    buffer_size: int

    sock: socket.socket

    running: bool

    def __init__(self, name: str, server_ip: str, server_port: int, buffer_size: int = 1024) -> None:
        """Initializes the client with the specified IP address and port.

        Args:
            name (str): The name of the client.
            server_ip (str): The IP address of the server to connect to.
            server_port (int): The port number of the server to connect to.
            buffer_size (int): The size of the buffer for receiving data.
        """

        self.name = name
        self.address = (server_ip, server_port)
        self.buffer_size = buffer_size

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = False

    def start(self) -> None:
        """Starts the client and begins listening for incoming packets."""

        if self.running:
            return
        
        self.sock.connect(self.address)
        self.running = True

        threading.Thread(target=self._listen_for_packets, daemon=True).start()
        print(f"[Client] Client started and connected to {self.address}.")

        self.join()

    def stop(self) -> None:
        """Stops the client and closes the socket."""
        if not self.running:
            return

        self.running = False
        self.sock.close()
        print("[Client] Client stopped.")

    def join(self) -> None:
        """Sends a join request to the server with the client's name."""

        if not self.running:
            raise RuntimeError("Client is not running. Start the client before joining.")

        join_packet = PacketPlayInJoin(name=self.name)
        self.send(join_packet)

    def disconnect(self) -> None:
        """Sends a disconnect request to the server."""

        if not self.running:
            raise RuntimeError("Client is not running. Start the client before disconnecting.")

        # disconnect_packet = PacketPlayInDisconnect(name=self.name)
        # self.send(disconnect_packet)

        # self.stop()
        raise NotImplementedError("Disconnect functionality is not implemented yet.")

    def on_packet_received(self, packet: Packet) -> None:
        """Handles a received packet from the server.

        Args:
            packet (Packet): The received packet.
        """

        print(f"[Client] Received packet: {packet}")

        match packet:
            case welcome if isinstance(welcome, PacketPlayOutWelcome):
                if welcome.is_welcome:
                    print(f"[Client] Connection successful: {welcome.message}")
                else:
                    print(f"[Client] Connection failed: {welcome.message}")
                    self.stop()
            case _:
                print(f"[Client] Unhandled packet type: {type(packet).__name__}")

    def send(self, packet: Packet) -> None:
        """Sends a packet to the server.

        Args:
            packet (Packet): The packet to send.
        """

        if not self.running:
            raise RuntimeError("Client is not running. Start the client before sending packets.")

        data = packet.to_bytes()
        self.sock.sendto(data, self.address)
        print(f"[Client] Sent packet: {packet}")

    def _listen_for_packets(self) -> None:
        """Listens for incoming packets from the server and handles them."""
        
        while self.running:
            try:
                data, _ = self.sock.recvfrom(self.buffer_size)

                packet = Packet.from_bytes(data)
                self.on_packet_received(packet)
            except socket.error as e:
                if not self.running:
                    break

                if e.errno == 111:
                    print("[Client] Connection refused by the server. Stopping client.")
                    self.stop()
                else:
                    print(f"[Client] Error receiving packet: {e}")

    def __repr__(self) -> str:
        return f"<Client name={self.name} address={self.address}>"


if __name__ == "__main__":
    client = Client(name="Player1", server_ip="localhost", server_port=3567)

    try:
        client.start()
        while client.running:
            pass  # Keep the client running
    except KeyboardInterrupt:
        pass
    finally:
        client.stop()