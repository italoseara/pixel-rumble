from __future__ import annotations

from connection.packets import Packet


class PacketPlayInItemDrop(Packet):
    """Item drop packet for the play state."""

    id = 0x13

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayInItemDrop:
        """Create a item drop packet from bytes."""

        return cls()

    def __repr__(self) -> str:
        return f"<PacketPlayInItemDrop>"
