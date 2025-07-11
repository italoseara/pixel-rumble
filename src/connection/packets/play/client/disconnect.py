from __future__ import annotations
from packets import Packet


class PacketPlayInDisconnect(Packet):
    """Disconnect packet for the play state."""

    id = 0x04

    def __init__(self) -> None:
        super().__init__(data=b"")

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayInDisconnect:
        """Create a disconnect packet from bytes."""

        return cls()

    def __repr__(self) -> str:
        return f"<PacketPlayInDisconnect>"
