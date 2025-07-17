from __future__ import annotations

from connection.util import from_uint8, to_uint8
from connection.packets import Packet


class PacketPlayInChangeCharacter(Packet):
    """Change character packet for the play state."""

    id = 0x0B

    character_index: int

    def __init__(self, character_index: int) -> None:
        self.character_index = character_index

        data = bytearray()
        data.extend(to_uint8(self.character_index))

        super().__init__(data=data)

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayInChangeCharacter:
        """Create a change character packet from bytes."""

        if len(data) != 1:
            raise ValueError("Invalid data length for PacketPlayInChangeCharacter")

        character_index = from_uint8(data[0:1])

        return cls(character_index)

    def __repr__(self) -> str:
        return f"<PacketPlayInChangeCharacter character_index={self.character_index}>"