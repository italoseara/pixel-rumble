from __future__ import annotations

from pygame import Vector2

from connection.util import from_float, to_float, from_uint8, to_uint8
from connection.packets import Packet


class PacketPlayOutAddItem(Packet):
    """Item packet for the play state."""

    id = 0x1B

    item_id: str

    def __init__(self, item_id: str, position : Vector2) -> None:
        self.item_id = item_id
        self.position_x = position.x
        self.position_y = position.y

        data = bytearray()
        data.extend(to_uint8(len(item_id)))
        data.extend(self.item_id.encode())
        data.extend(to_float(self.position_x))
        data.extend(to_float(self.position_y))

        super().__init__(data=data)

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayOutAddItem:
        """Create an item packet from bytes."""

        len_item_id = from_uint8(data[0:1])
        item_id = data[1:1 + len_item_id].decode()
        position_x = from_float(data[1 + len_item_id:5 + len_item_id])
        position_y = from_float(data[5 + len_item_id:9 + len_item_id])

        return cls(item_id, Vector2(position_x, position_y))

    def __repr__(self) -> str:
        return f"<PacketPlayOutItem item_id={self.item_id}>"