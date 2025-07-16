from __future__ import annotations

from connection.util import from_uint32, to_uint32
from connection.packets import Packet


class PacketPlayOutPlayerJoin(Packet):
    """Join packet for the play state."""

    id = 0x07

    player_id: int
    name: str

    def __init__(self, player_id: int, name: str) -> None:
        self.player_id = player_id
        self.name = name

        super().__init__(
            to_uint32(self.player_id) +
            name.encode()
        )

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayOutPlayerJoin:
        """Create a join packet from bytes."""

        player_id = from_uint32(data[:4])
        name = data[4:].decode()

        return cls(player_id, name)

    def __repr__(self) -> str:
        return f"<PacketPlayInJoin player_id={self.player_id} name='{self.name}'>"