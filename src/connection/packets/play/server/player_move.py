from __future__ import annotations

from pygame.math import Vector2

from connection.util import from_float, to_float, from_uint32, to_uint32
from connection.packets import Packet


class PacketPlayOutPlayerMove(Packet):
    """Player move packet for the play state."""

    id = 0x08

    player_id: int
    position: Vector2
    acceleration: Vector2
    velocity: Vector2

    def __init__(self, player_id: int, position: Vector2, acceleration: Vector2, velocity: Vector2) -> None:
        self.player_id = player_id
        self.position = position
        self.acceleration = acceleration
        self.velocity = velocity

        super().__init__(
            to_uint32(self.player_id) +
            to_float(self.position.x) +
            to_float(self.position.y) +
            to_float(self.acceleration.x) +
            to_float(self.acceleration.y) +
            to_float(self.velocity.x) +
            to_float(self.velocity.y)
        )

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayOutPlayerMove:
        """Create a player move packet from bytes."""

        player_id = from_uint32(data[:4])
        position_x = from_float(data[4:8])
        position_y = from_float(data[8:12])
        acceleration_x = from_float(data[12:16])
        acceleration_y = from_float(data[16:20])
        velocity_x = from_float(data[20:24])
        velocity_y = from_float(data[24:28])

        return cls(
            player_id,
            Vector2(position_x, position_y),
            Vector2(acceleration_x, acceleration_y),
            Vector2(velocity_x, velocity_y)
        )

    def __repr__(self) -> str:
        return (
            f"<PacketPlayOutPlayerMove "
            f"player_id={self.player_id} "
            f"position={self.position} "
            f"acceleration={self.acceleration} "
            f"velocity={self.velocity}>"
        )