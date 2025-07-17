from __future__ import annotations

from connection.util import from_uint32, to_uint32
from connection.packets import Packet


class PacketPlayOutPlayerLeave(Packet):
    """Player Leave packet for the play state."""

    id = 0x0A

    player_id: int

    def __init__(self, player_id: int) -> None:
        self.player_id = player_id

        super().__init__(to_uint32(self.player_id))

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayOutPlayerLeave:
        """Create a leave packet from bytes."""

        if len(data) != 4:
            raise ValueError("Data must be 4 bytes long for player leave packet")

        player_id = from_uint32(data[:4])

        return cls(player_id)

    def __repr__(self) -> str:
        return f"<PacketPlayOutPlayerLeave player_id={self.player_id}>"