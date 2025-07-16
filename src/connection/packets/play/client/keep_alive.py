from __future__ import annotations

from connection.packets import Packet
from connection.util import to_uint32, from_uint32


class PacketPlayInKeepAlive(Packet):
    """Keep alive packet for the play state."""

    id = 0x05

    value: int

    def __init__(self, value: str) -> None:
        self.value = value

        super().__init__(data=to_uint32(value))

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayInKeepAlive:
        """Create a keep alive packet from bytes."""

        if len(data) != 4:
            raise ValueError("Invalid data length for PacketPlayInKeepAlive")

        value = from_uint32(data)

        return cls(value)

    def __repr__(self) -> str:
        return f"<PacketPlayInKeepAlive value={self.value}>"