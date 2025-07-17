from __future__ import annotations

from connection.util import from_uint32, to_uint32, from_uint8, to_uint8
from connection.packets import Packet


class PacketPlayOutChangeCharacter(Packet):
    """Change character packet for the play state."""

    id = 0x0C

    player_id: int
    character_index: int

    def __init__(self, player_id: int, character_index: int) -> None:
        self.player_id = player_id
        self.character_index = character_index

        data = bytearray()
        data.extend(to_uint32(self.player_id))
        data.extend(to_uint8(self.character_index))

        super().__init__(data=data)

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayOutChangeCharacter:
        """Create a change character packet from bytes."""

        if len(data) != 5:
            raise ValueError("Invalid data length for PacketPlayOutChangeCharacter")

        player_id = from_uint32(data[:4])
        character_index = from_uint8(data[4:5])

        return cls(player_id, character_index)

    def __repr__(self) -> str:
        return f"<PacketPlayOutChangeCharacter player_id={self.player_id} character_index={self.character_index}>"