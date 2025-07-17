import time
import errno
import socket
import threading
from dataclasses import dataclass

from engine import Game
from connection.server import DISCOVERY_PORT
from connection.packets import (
    Packet, 
    PacketPlayInJoin, 
    PacketPlayOutWelcome, 
    PacketPlayInDisconnect,
    PacketStatusInPing,
    PacketStatusOutPong,
    PacketPlayInKeepAlive,
    PacketPlayOutKeepAlive,
    PacketPlayOutPlayerJoin,
    PacketPlayOutPlayerLeave,
    PacketPlayOutPlayerMove
)


TIMEOUT = 2  # seconds
TICK_RATE = 64  # ticks per second


@dataclass(unsafe_hash=True)
class ServerData:
    name: str
    ip: str
    port: int

class Client:
    """A UDP client that connects to a server and sends/receives packets."""

    name: str
    address: tuple[str, int]
    buffer_size: int

    sock: socket.socket

    running: bool

    last_keep_alive: float

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

        self.last_keep_alive = time.time()

    @staticmethod
    def search() -> set[ServerData]:
        """Searches for available servers and returns a set of ServerData objects."""

        print("[Client] Searching for available servers...")

        # Send a ping request using broadcast
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(TIMEOUT)  # Set a timeout for receiving responses

        ping_packet = PacketStatusInPing()
        sock.sendto(ping_packet.to_bytes(), ('<broadcast>', DISCOVERY_PORT))

        servers = set()
        start = time.time()
        while True:            
            try:
                data, addr = sock.recvfrom(1024)
                try:
                    packet = Packet.from_bytes(data)
                    if not isinstance(packet, PacketStatusOutPong):
                        print("[Client] Received packet is not a Pong packet")
                        continue
                    
                    servers.add(ServerData(name=packet.name, ip=packet.ip, port=packet.port))
                    print(f"[Client] Received response from {addr[0]}:{addr[1]}: {packet}")
                except ValueError as e:
                    print(f"[Client] Received invalid packet from {addr[0]}:{addr[1]}: {e}")
                    continue
            except socket.timeout:
                break

            if time.time() - start > TIMEOUT:
                break

        sock.close()
        print(f"[Client] Search completed. Found {len(servers)} servers.")
        return servers

    def on_packet_received(self, packet: Packet) -> None:
        """Handles a received packet from the server.

        Args:
            packet (Packet): The received packet.
        """

        print(f"[Client] Received packet: {packet}")

        match packet:
            case welcome if isinstance(welcome, PacketPlayOutWelcome):
                if welcome.is_welcome:
                    from game.scenes.lobby import LobbyScene
                    
                    Game.instance().clear_scenes()
                    Game.instance().push_scene(LobbyScene(id=welcome.player_id, name=self.name))
                    print(f"[Client] Connection successful: {welcome.message}")
                else:
                    print(f"[Client] Connection failed: {welcome.message}")
                    self.stop()

            case keep_alive if isinstance(keep_alive, PacketPlayOutKeepAlive):
                response_packet = PacketPlayInKeepAlive(value=keep_alive.value)
                self.send(response_packet)
                self.last_keep_alive = time.time()

            case player_join if isinstance(player_join, PacketPlayOutPlayerJoin):
                current_scene = Game.instance().current_scene

                if hasattr(current_scene, 'add_player'):
                    current_scene.add_player(player_join.player_id, player_join.name)
                    print(f"[Client] Player {player_join.name} with ID {player_join.player_id} joined the lobby.")
                else:
                    print("[Client] Current scene does not support adding players.")

            case player_leave if isinstance(player_leave, PacketPlayOutPlayerLeave):
                current_scene = Game.instance().current_scene

                if hasattr(current_scene, 'remove_player'):
                    current_scene.remove_player(player_leave.player_id)
                    print(f"[Client] Player with ID {player_leave.player_id} left the lobby.")
                else:
                    print("[Client] Current scene does not support removing players.")

            case player_move if isinstance(player_move, PacketPlayOutPlayerMove):
                current_scene = Game.instance().current_scene
                if hasattr(current_scene, 'move_player'):
                    current_scene.move_player(
                        player_move.player_id,
                        player_move.position,
                        player_move.acceleration,
                        player_move.velocity
                    )
                    print(f"[Client] Player {player_move.player_id} moved to {player_move.position}.")
            case _:
                print(f"[Client] Unhandled packet type: {packet}")

    def start(self) -> None:
        """Starts the client and begins listening for incoming packets."""

        if self.running:
            return
        
        self.sock.connect(self.address)
        self.running = True

        threading.Thread(target=self._listen_for_packets, daemon=True).start()
        threading.Thread(target=self._wait_for_keep_alive, daemon=True).start()
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

        self.send(PacketPlayInJoin(name=self.name))

    def disconnect(self) -> None:
        """Sends a disconnect request to the server."""

        if not self.running:
            raise RuntimeError("Client is not running. Start the client before disconnecting.")

        self.send(PacketPlayInDisconnect())
        self.stop()

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

    def _wait_for_keep_alive(self) -> None:
        """Waits for keep-alive packets from the server and handles them."""

        while self.running:
            if time.time() - self.last_keep_alive > 20:
                from game.scenes.menu import MainMenu
                
                print("[Client] No keep-alive packets received for 20 seconds. Stopping client.")
                Game.instance().clear_scenes()
                Game.instance().push_scene(MainMenu())
                self.disconnect()
                return

            time.sleep(1)

    def _listen_for_packets(self) -> None:
        """Listens for incoming packets from the server and handles them."""

        tick_interval = 1.0 / TICK_RATE
        while self.running:                
            start_time = time.time()
            try:
                data, _ = self.sock.recvfrom(self.buffer_size)

                packet = Packet.from_bytes(data)
                self.on_packet_received(packet)
            except socket.error as e:
                if not self.running:
                    break

                if e.errno == errno.ECONNREFUSED:
                    from game.scenes.menu import MainMenu
                    
                    print("[Client] Connection refused by the server. Stopping client.")
                    self.stop()

                    Game.instance().clear_scenes()
                    Game.instance().push_scene(MainMenu())
                else:
                    print(f"[Client] Error receiving packet: {e}")

            elapsed = time.time() - start_time
            sleep_time = tick_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    def __repr__(self) -> str:
        return f"<Client name='{self.name}' address={self.address}>"
