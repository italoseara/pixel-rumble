from __future__ import annotations

from pygame import Vector2

from connection.util import from_float, to_float

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
        data.extend(self.item_id.encode())
        data.extend(to_float(self.position_x))
        data.extend(to_float(self.position_y))

        super().__init__(data=data)

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayOutAddItem:
        """Create an item packet from bytes."""

        if len(data) < 10:
            raise ValueError("Invalid data length for PacketPlayOutAddItem")

        item_id = data[:6].decode()
        position_x = from_float(data[6:10])
        position_y = from_float(data[10:14])

        return cls(item_id, Vector2(position_x, position_y))

    def __repr__(self) -> str:
        return f"<PacketPlayOutItem item_id={self.item_id}>"