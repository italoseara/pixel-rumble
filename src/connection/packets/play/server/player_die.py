from __future__ import annotations

from connection.packets import Packet
from connection.util import from_uint32, to_uint32


class PacketPlayOutPlayerDie(Packet):
    """Player die packet for the play state."""

    id = 0x1A

    player_id: int

    def __init__(self, player_id: int) -> None:
        self.player_id = player_id

        super().__init__(to_uint32(self.player_id))

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayOutPlayerDie:
        """Create a player die packet from bytes."""

        player_id = from_uint32(data[:4])

        return cls(player_id)

    def __repr__(self) -> str:
        return f"<PacketPlayOutPlayerDie player_id={self.player_id}>"