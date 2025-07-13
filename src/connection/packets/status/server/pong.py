from __future__ import annotations
from packets import Packet


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

        super().__init__(data=f"{name}:{ip}:{port}".encode())

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketStatusOutPong:
        """Create a pong packet from bytes."""

        decoded = data.decode()
        parts = decoded.split(":")
        if len(parts) != 3:
            raise ValueError("Invalid data format for PacketStatusOutPong")

        name, ip, port_str = parts
        if not name or not ip:
            raise ValueError("Name and IP cannot be empty in PacketStatusOutPong")

        try:
            port = int(port_str)
        except ValueError:
            raise ValueError("Invalid port number in PacketStatusOutPong data")

        return cls(name, ip, port)

    def __repr__(self) -> str:
        return f"<PacketStatusOutPong name={self.name} ip={self.ip} port={self.port}>"