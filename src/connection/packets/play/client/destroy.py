from __future__ import annotations

from connection.packets import Packet


class PacketPlayInDestroyItem(Packet):
    """Destroy item packet for the play state."""

    id = 0x1C

    item_id: str

    def __init__(self, item_id: str) -> None:
        self.item_id = item_id

        super().__init__(data=item_id.encode())

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayInDestroyItem:
        """Create a destroy item packet from bytes."""

        if len(data) < 10:
            raise ValueError("Data must be at least 10 bytes long in PacketPlayInDestroyItem")

        item_id = data.decode()

        return cls(item_id)

    def __repr__(self) -> str:
        return f"<PacketPlayInDestroyItem item_id={self.item_id}>"