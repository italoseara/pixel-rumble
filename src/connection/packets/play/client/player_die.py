from __future__ import annotations

from connection.packets import Packet


class PacketPlayInPlayerDie(Packet):
    """Player die packet for the play state."""

    id = 0x19

    def __init__(self) -> None:
        super().__init__(data=b"")

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayInPlayerDie:
        """Create a player die packet from bytes."""

        return cls()

    def __repr__(self) -> str:
        return f"<PacketPlayInPlayerDie>"