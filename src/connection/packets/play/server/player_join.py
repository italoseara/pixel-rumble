from __future__ import annotations
from connection.packets import Packet


class PacketPlayInJoin(Packet):
    """Join packet for the play state."""

    id = 0x07

    name: str

    def __init__(self, name: str) -> None:
        self.name = name

        super().__init__(data=name.encode())

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayInJoin:
        """Create a join packet from bytes."""

        name = data.decode()

        if not name:
            raise ValueError("Name cannot be empty in PacketPlayInJoin data")

        return cls(name)

    def __repr__(self) -> str:
        return f"<PacketPlayInJoin name='{self.name}'>"