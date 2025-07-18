from __future__ import annotations

from connection.packets import Packet
from connection.util import from_uint32, to_uint32

class PacketStatusOutPong(Packet):
    """Pong packet for the status state."""

    id = 0x01

    name: str
    port: int

    def __init__(self, name: str, port: int) -> None:
        self.name = name
        self.port = port

        super().__init__(data=f"{name}".encode() + to_uint32(port))

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketStatusOutPong:
        """Create a pong packet from bytes."""

        if len(data) < 4:
            raise ValueError("Data is too short to contain a valid Pong packet.")

        name = data[:-4].decode()
        port = from_uint32(data[-4:])

        return cls(name=name, port=port)

    def __repr__(self) -> str:
        return f"<PacketStatusOutPong name='{self.name}' port={self.port}>"