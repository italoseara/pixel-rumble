from __future__ import annotations

from pygame import Vector2

from connection.util import from_float, to_float, from_uint8, to_uint8
from connection.packets import Packet


class PacketPlayInAddItem(Packet):
    """Add item packet for the play state."""

    id = 0x0F

    gun_type: str

    def __init__(self, gun_type: str, position: Vector2) -> None:
        self.gun_type = gun_type
        self.position_x = position.x
        self.position_y = position.y

        data = bytearray()
        data.extend(to_uint8(len(gun_type)))
        data.extend(self.gun_type.encode())
        data.extend(to_float(self.position_x))
        data.extend(to_float(self.position_y))

        super().__init__(data=data)

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayInAddItem:
        """Create an add item packet from bytes."""

        len_gun_type = from_uint8(data[0:1])
        gun_type = data[1:1 + len_gun_type].decode()
        position_x = from_float(data[1 + len_gun_type:5 + len_gun_type])
        position_y = from_float(data[5 + len_gun_type:9 + len_gun_type])

        return cls(gun_type, Vector2(position_x, position_y))

    def __repr__(self) -> str:
        return f"<PacketPlayInAddItem gun_type={self.gun_type}>"