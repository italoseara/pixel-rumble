from __future__ import annotations

from connection.packets import Packet
from connection.util import from_uint32, to_uint32


class PacketPlayOutItemDrop(Packet):
    """Item drop packet for the play state."""

    id = 0x14

    player_id: int

    def __init__(self, player_id: int) -> None:
        """Initialize the item drop packet.

        Args:
            player_id (int, optional): The ID of the player dropping the item. Defaults to None.
        """
        
        self.player_id = player_id

        super().__init__(to_uint32(player_id))

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayOutItemDrop:
        """Create a item drop packet from bytes."""

        if len(data) != 4:
            raise ValueError("Invalid data length for PacketPlayOutItemDrop")

        player_id = from_uint32(data[0:4])
        return cls(player_id)

    def __repr__(self) -> str:
        return f"<PacketPlayOutItemDrop player_id={self.player_id}>"