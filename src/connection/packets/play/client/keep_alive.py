from __future__ import annotations

import struct
from connection.packets import Packet


class PacketPlayInKeepAlive(Packet):
    """Join packet for the play state."""

    id = 0x05

    value: int

    def __init__(self, value: str) -> None:
        self.value = value

        

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayInKeepAlive:
        """Create a keep alive packet from bytes."""

        

    def __repr__(self) -> str:
        return f"<PacketPlayInKeepAlive value={self.name}>"