from __future__ import annotations

from connection.util import from_uint32, to_uint32, from_uint8, to_uint8
from connection.packets import Packet


class PacketPlayOutItemPickup(Packet):
    """Destroy item packet for the play state."""

    id = 0x12

    player_id: int
    gun_type: str
    object_id: int

    def __init__(self, player_id: int, gun_type: str, object_id: int) -> None:
        self.player_id = player_id
        self.gun_type = gun_type
        self.object_id = object_id

        data = bytearray()
        data.extend(to_uint32(self.player_id))
        data.extend(to_uint8(len(self.gun_type)))
        data.extend(self.gun_type.encode())
        data.extend(to_uint32(self.object_id))
        super().__init__(data)

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayOutItemPickup:
        """Create a destroy item packet from bytes."""

        player_id = from_uint32(data[0:4])
        gun_type_length = from_uint8(data[4:5])
        gun_type = data[5:5 + gun_type_length].decode()
        object_id = from_uint32(data[5 + gun_type_length:9 + gun_type_length])

        return cls(player_id, gun_type, object_id)

    def __repr__(self) -> str:
        return f"<PacketPlayOutItemPickup player_id={self.player_id} gun_type={self.gun_type} object_id={self.object_id}>"