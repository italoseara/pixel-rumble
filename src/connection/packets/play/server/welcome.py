from __future__ import annotations

from connection.util import from_uint32, to_uint32
from connection.packets import Packet


class PacketPlayOutWelcome(Packet):
    """Welcome packet for the play state."""

    id = 0x03

    is_welcome: bool
    player_id: int
    message: str

    def __init__(self, is_welcome: bool, player_id: int = 0, message: str = "") -> None:
        self.is_welcome = is_welcome
        self.player_id = player_id
        self.message = message

        super().__init__(data=bytes([(is_welcome & 1)]) + to_uint32(player_id) + message.encode())

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayOutWelcome:
        """Create a welcome packet from bytes."""

        if len(data) < 1:
            raise ValueError("Data must contain at least one byte")

        is_welcome = bool(data[0])
        player_id = from_uint32(data[1:5])
        message = data[5:].decode()

        return cls(is_welcome, player_id, message)

    def __repr__(self) -> str:
        return f"<PacketPlayOutWelcome is_welcome={self.is_welcome} player_id={self.player_id} message='{self.message}'>"