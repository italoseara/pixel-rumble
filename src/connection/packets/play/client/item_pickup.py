from __future__ import annotations

from connection.util import from_uint32, to_uint32, from_uint8, to_uint8
from connection.packets import Packet


class PacketPlayInItemPickup(Packet):
    """Destroy item packet for the play state."""

    id = 0x10

    gun_type: str
    object_id: int

    def __init__(self, gun_type: str, object_id: int) -> None:
        self.gun_type = gun_type
        self.object_id = object_id

        data = bytearray()
        data.extend(to_uint8(len(self.gun_type)))
        data.extend(self.gun_type.encode())
        data.extend(to_uint32(self.object_id))
        super().__init__(data)

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayInItemPickup:
        """Create a destroy item packet from bytes."""

        gun_type_length = from_uint8(data[0:1])
        gun_type = data[1:1 + gun_type_length].decode()
        object_id = from_uint32(data[1 + gun_type_length:5 + gun_type_length])

        return cls(gun_type, object_id)

    def __repr__(self) -> str:
        return f"<PacketPlayInItemPickup gun_type={self.gun_type} object_id={self.object_id}>"