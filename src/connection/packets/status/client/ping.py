from __future__ import annotations
from connection.packets import Packet


class PacketStatusInPing(Packet):
    """Ping packet for the status state."""

    id = 0x00

    def __init__(self) -> None:
        """Initialize a ping packet."""
        super().__init__(data=b'')

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketStatusInPing:
        """Create a ping packet from bytes."""

        return cls()

    def __repr__(self) -> str:
        return f"<PacketStatusInPing>"