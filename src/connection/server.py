import time
import socket
import threading
import random
from typing import override
from abc import ABC, abstractmethod
from dataclasses import dataclass

from connection.packets import (
    Packet,
    PacketStatusInPing,
    PacketStatusOutPong,
    PacketPlayInJoin,
    PacketPlayOutWelcome,
    PacketPlayInDisconnect,
    PacketPlayInKeepAlive,
    PacketPlayOutKeepAlive,
    PacketPlayOutPlayerJoin,
    PacketPlayInPlayerMove,
    PacketPlayOutPlayerMove
)

DISCOVERY_PORT = 1337  # Fixed port for discovery server
BUFFER_SIZE = 1024  # bytes
TICK_RATE = 64  # ticks per second

class BaseUDPServer(ABC):
    port: int
    buffer_size: int
    sock: socket.socket
    running: bool
    
    def __init__(self, port: int, buffer_size: int = BUFFER_SIZE) -> None:
        self.port = port
        self.buffer_size = buffer_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = False

    def start(self) -> None:
        if self.running:
            return
        
        self.sock.bind(('', self.port))
        self.running = True

        threading.Thread(target=self._listen_for_requests, daemon=True).start()
        print(f"[{type(self).__name__}] Started on port {self.port}.")

    def stop(self) -> None:
        if not self.running:
            return

        self.running = False
        self.sock.close()
        print(f"[{type(self).__name__}] Stopped.")

    def send(self, packet: Packet, addr: tuple[str, int]) -> None:
        if not self.running:
            raise RuntimeError(f"{type(self).__name__} is not running.")

        data = packet.to_bytes()
        self.sock.sendto(data, addr)
        print(f"[{type(self).__name__}] Sent packet to {addr[0]}:{addr[1]}: {packet}")

    def _listen_for_requests(self) -> None:
        tick_interval = 1.0 / TICK_RATE

        while self.running:
            start_time = time.time()
            try:
                data, addr = self.sock.recvfrom(self.buffer_size)
                packet = Packet.from_bytes(data)
                self.on_packet_received(packet, addr)
            except Exception as e:
                print(f"[{type(self).__name__}] Error while listening for requests: {e}")

            elapsed = time.time() - start_time
            sleep_time = tick_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    @abstractmethod
    def on_packet_received(self, packet: Packet, addr: tuple[str, int]) -> None:
        raise NotImplementedError


class DiscoveryServer(BaseUDPServer):
    name: str
    ip: str
    target_port: int
    
    def __init__(self, name: str, ip: str, port: int, buffer_size: int = BUFFER_SIZE) -> None:
        super().__init__(DISCOVERY_PORT, buffer_size)
        self.name = name
        self.ip = ip
        self.target_port = port
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    @override
    def on_packet_received(self, packet: Packet, addr: tuple[str, int]) -> None:
        print(f"[DiscoveryServer] Received packet from {addr[0]}:{addr[1]}: {packet}")
        if isinstance(packet, PacketStatusInPing):
            response_packet = PacketStatusOutPong(self.name, self.ip, self.target_port)
            self.send(response_packet, addr)
        else:
            print(f"[DiscoveryServer] Unhandled packet type: {type(packet).__name__}")

    def __repr__(self) -> str:
        return f"<DiscoveryServer name={self.name} ip={self.ip} port={self.port} target_port={self.target_port} running={self.running}>"


@dataclass
class ClientData:
    id: int
    name: str
    ip: str
    port: int
    last_active: float = time.time()
    keep_alive_id: int = 0
    missed_keep_alive: int = 0

class Server(BaseUDPServer):
    name: str
    ip: str
    clients: dict[tuple[str, int], ClientData]
    discovery_server: DiscoveryServer

    _keep_alive_thread: threading.Thread

    def __init__(self, name: str, port: int, buffer_size: int = BUFFER_SIZE) -> None:
        super().__init__(port, buffer_size)
        self.name = name
        self.ip = self._get_ip()
        self.clients = {}
        self.discovery_server = DiscoveryServer(name=self.name, ip=self.ip, port=self.port)
        self._keep_alive_thread = threading.Thread(target=self._send_keep_alive_loop, daemon=True)

    def _get_ip(self) -> str:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 1))
        ip = sock.getsockname()[0]
        sock.close()
        return ip

    @override
    def start(self) -> None:
        super().start()
        self.discovery_server.start()
        self._keep_alive_thread.start()

    @override
    def stop(self) -> None:
        super().stop()
        self.discovery_server.stop()
        self.clients.clear()

    def _send_keep_alive_loop(self):
        while self.running:
            for addr, client in list(self.clients.items()):
                client.missed_keep_alive += 1
                if client.missed_keep_alive >= 4:
                    # TODO: Handle disconnect or removal of unresponsive client
                    print(f"[Server] Client {addr[0]}:{addr[1]} missed too many keep-alives. Disconnecting.")
                    self.clients.pop(addr, None)
                    continue

                keep_alive_id = random.randint(1, 1_000_000)
                client.keep_alive_id = keep_alive_id
                
                packet = PacketPlayOutKeepAlive(keep_alive_id)
                self.send(packet, addr)
            time.sleep(5)

    @override
    def on_packet_received(self, packet: Packet, addr: tuple[str, int]) -> None:
        print(f"[Server] Received packet from {addr[0]}:{addr[1]}: {packet}")
        match packet:
            case join if isinstance(join, PacketPlayInJoin):
                if addr not in self.clients:
                    client_id = random.randint(1, 1_000_000)

                    # Ensure the 1 in a million chance of duplicate client IDs is handled
                    while any(client.id == client_id for client in self.clients.values()):
                        client_id = random.randint(1, 1_000_000)
                    
                    self.clients[addr] = ClientData(
                        id=client_id,
                        name=join.name,
                        ip=addr[0],
                        port=addr[1]
                    )

                    print(f"[Server] Client {addr[0]}:{addr[1]} joined with name: {join.name}")
                    welcome_packet = PacketPlayOutWelcome(True, client_id, "Welcome to the server!")
                    self.send(welcome_packet, addr)

                    player_join_packet = PacketPlayOutPlayerJoin(player_id=client_id, name=join.name)
                    self.broadcast(player_join_packet, exclude=addr)

                    for client_addr, client_data in self.clients.items():
                        if client_addr != addr:
                            player_join_packet = PacketPlayOutPlayerJoin(player_id=client_data.id, name=client_data.name)
                            self.send(player_join_packet, addr)
                else:
                    print(f"[Server] Client {addr[0]}:{addr[1]} already connected.")
                    welcome_packet = PacketPlayOutWelcome(False, 0, "You are already connected.")
                    self.send(welcome_packet, addr)
                return

            case disconnect if isinstance(disconnect, PacketPlayInDisconnect):
                if addr in self.clients:
                    self.clients.pop(addr)
                    print(f"[Server] Client {addr[0]}:{addr[1]} disconnected.")
                else:
                    print(f"[Server] Client {addr[0]}:{addr[1]} is not connected.")
                return

        if addr not in self.clients:
            print(f"[Server] Client {addr[0]}:{addr[1]} is not connected. Ignoring packet.")
            return

        match packet:
            case keep_alive if isinstance(keep_alive, PacketPlayInKeepAlive):
                client = self.clients.get(addr)
                if keep_alive.value == client.keep_alive_id:
                    client.missed_keep_alive = 0
                    client.last_active = time.time()
                else:
                    print(f"[Server] Invalid keep-alive response from {addr[0]}:{addr[1]}")
                return

            case player_move if isinstance(player_move, PacketPlayInPlayerMove):
                client = self.clients.get(addr)
                move_packet = PacketPlayOutPlayerMove(
                    player_id=client.id, 
                    position=player_move.position,
                    acceleration=player_move.acceleration,
                    velocity=player_move.velocity
                )
                self.broadcast(move_packet, exclude=addr)

            case _:
                print(f"[Server] Unhandled packet type: {type(packet).__name__}")

    def broadcast(self, packet: Packet, exclude: tuple[str, int] = None) -> None:
        if not self.running:
            raise RuntimeError("Server is not running.")

        print(f"[Server] Broadcasting packet: {packet}")
        data = packet.to_bytes()
        for client in self.clients:
            if exclude and client == exclude:
                continue
            self.sock.sendto(data, client)

    def send(self, packet: Packet, addr: tuple[str, int]) -> None:
        if not self.running:
            raise RuntimeError("Server is not running.")

        if addr not in self.clients:
            raise ValueError(f"Client {addr[0]}:{addr[1]} is not connected.")

        super().send(packet, addr)

    def __repr__(self) -> str:
        return f"<Server name='{self.name}' ip={self.ip} port={self.port} running={self.running} clients={len(self.clients)}>"
