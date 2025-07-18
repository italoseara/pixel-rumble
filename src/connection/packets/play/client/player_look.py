from __future__ import annotations

from connection.packets import Packet
from connection.util import from_float, to_float


class PacketPlayInPlayerLook(Packet):
    """Player look packet for the play state."""

    id = 0x15

    angle: float

    def __init__(self, angle: float) -> None:
        """Initialize the player look packet."""

        self.angle = angle
        super().__init__(to_float(angle))

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayInPlayerLook:
        """Create a player look packet from bytes."""

        angle = from_float(data[0:4])
        return cls(angle)

    def __repr__(self) -> str:
        return f"<PacketPlayInPlayerLook angle={self.angle}>"