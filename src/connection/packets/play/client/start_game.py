from __future__ import annotations
from connection.packets import Packet


class PacketPlayInStartGame(Packet):
    """Start game packet for the play state."""

    id = 0x0D

    map_name: str

    def __init__(self, map_name: str) -> None:
        self.map_name = map_name
        
        super().__init__(data=map_name.encode())

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayInStartGame:
        """Create a start game packet from bytes."""

        map_name = data.decode()

        if not map_name:
            raise ValueError("Map name cannot be empty in PacketPlayInStartGame data")

        return cls(map_name)

    def __repr__(self) -> str:
        return f"<PacketPlayInStartGame map_name='{self.map_name}'>"