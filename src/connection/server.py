import socket
import threading
from typing import override
from abc import ABC, abstractmethod

from connection.packets import (
    Packet,
    PacketStatusInPing,
    PacketStatusOutPong,
    PacketPlayInJoin,
    PacketPlayOutWelcome,
    PacketPlayInDisconnect
)

DISCOVERY_PORT = 1337
BUFFER_SIZE = 1024


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
        while self.running:
            try:
                data, addr = self.sock.recvfrom(self.buffer_size)
                packet = Packet.from_bytes(data)
                self.on_packet_received(packet, addr)
            except Exception as e:
                print(f"[{type(self).__name__}] Error while listening for requests: {e}")

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


class Server(BaseUDPServer):
    name: str
    ip: str
    clients: set[tuple[str, int]]
    discovery_server: DiscoveryServer

    def __init__(self, name: str, port: int, buffer_size: int = BUFFER_SIZE) -> None:
        super().__init__(port, buffer_size)

        self.name = name
        self.ip = self._get_ip()
        self.clients: set[tuple[str, int]] = set()
        self.discovery_server = DiscoveryServer(name=self.name, ip=self.ip, port=self.port)

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

    @override
    def stop(self) -> None:
        super().stop()
        self.discovery_server.stop()
        self.clients.clear()

    @override
    def on_packet_received(self, packet: Packet, addr: tuple[str, int]) -> None:
        print(f"[Server] Received packet from {addr[0]}:{addr[1]}: {packet}")
        match packet:
            case join if isinstance(join, PacketPlayInJoin):
                if addr not in self.clients:
                    self.clients.add(addr)
                    print(f"[Server] Client {addr[0]}:{addr[1]} joined with name: {join.name}")
                    welcome = PacketPlayOutWelcome(True, "Welcome to the server!")
                else:
                    print(f"[Server] Client {addr[0]}:{addr[1]} already connected.")
                    welcome = PacketPlayOutWelcome(False, "You are already connected.")
                self.send(welcome, addr)
                return

            case disconnect if isinstance(disconnect, PacketPlayInDisconnect):
                if addr in self.clients:
                    self.clients.remove(addr)
                    print(f"[Server] Client {addr[0]}:{addr[1]} disconnected.")
                else:
                    print(f"[Server] Client {addr[0]}:{addr[1]} is not connected.")
                return

        if addr not in self.clients:
            print(f"[Server] Client {addr[0]}:{addr[1]} is not connected. Ignoring packet.")
            return

        match packet:
            case _:
                print(f"[Server] Unhandled packet type: {type(packet).__name__}")

    def broadcast(self, packet: Packet) -> None:
        if not self.running:
            raise RuntimeError("Server is not running.")

        print(f"[Server] Broadcasting packet: {packet}")
        data = packet.to_bytes()
        for client in self.clients:
            self.sock.sendto(data, client)

    def send(self, packet: Packet, addr: tuple[str, int]) -> None:
        if not self.running:
            raise RuntimeError("Server is not running.")

        if addr not in self.clients:
            raise ValueError(f"Client {addr[0]}:{addr[1]} is not connected.")

        super().send(packet, addr)

    def __repr__(self) -> str:
        return f"<Server ip={self.ip} port={self.port} running={self.running} clients={len(self.clients)}>"


if __name__ == "__main__":
    server = Server(name="TestServer", port=25565)
    try:
        server.start()
        while server.running:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
