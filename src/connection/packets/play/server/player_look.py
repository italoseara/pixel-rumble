from __future__ import annotations

from connection.packets import Packet
from connection.util import from_float, to_float, from_uint32, to_uint32


class PacketPlayOutPlayerLook(Packet):
    """Player look packet for the play state."""

    id = 0x16

    angle: float

    def __init__(self, player_id: int, angle: float) -> None:
        """Initialize the player look packet."""

        self.player_id = player_id
        self.angle = angle

        data = bytearray()
        data.extend(to_uint32(self.player_id))
        data.extend(to_float(angle))
        super().__init__(data)

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayOutPlayerLook:
        """Create a player look packet from bytes."""

        player_id = from_uint32(data[:4])
        angle = from_float(data[4:8])
        return cls(player_id=player_id, angle=angle)

    def __repr__(self) -> str:
        return f"<PacketPlayOutPlayerLook player_id={self.player_id} angle={self.angle}>"