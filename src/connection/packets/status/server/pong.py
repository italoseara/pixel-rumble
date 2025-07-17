from __future__ import annotations

from connection.packets import Packet
from connection.util import from_uint32, to_uint32

class PacketStatusOutPong(Packet):
    """Pong packet for the status state."""

    id = 0x01

    name: str
    ip: str
    port: int

    def __init__(self, name: str, ip: str, port: int) -> None:
        self.name = name
        self.ip = ip
        self.port = port

        super().__init__(data=f"{name}\0{ip}".encode() + to_uint32(port))

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketStatusOutPong:
        """Create a pong packet from bytes."""

        header, port_bytes = data.rsplit(b'\0', 2)[0:2], data[-4:]
        decoded = header[0].decode()
        parts = decoded.split("\0")

        if len(parts) != 2:
            raise ValueError("Invalid data format for PacketStatusOutPong")

        name, ip = parts
        if not name or not ip:
            raise ValueError("Name and IP cannot be empty in PacketStatusOutPong")

        port = from_uint32(port_bytes)

        return cls(name, ip, port)

    def __repr__(self) -> str:
        return f"<PacketStatusOutPong name='{self.name}' ip={self.ip} port={self.port}>"