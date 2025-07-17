from __future__ import annotations

from pygame.math import Vector2

from connection.util import from_float, to_float
from connection.packets import Packet


class PacketPlayInPlayerMove(Packet):
    """Player move packet for the play state."""

    id = 0x09

    position: Vector2
    acceleration: Vector2
    velocity: Vector2

    def __init__(self, position: Vector2, acceleration: Vector2, velocity: Vector2) -> None:
        self.position = position
        self.acceleration = acceleration
        self.velocity = velocity

        super().__init__(
            to_float(self.position.x) +
            to_float(self.position.y) +
            to_float(self.acceleration.x) +
            to_float(self.acceleration.y) +
            to_float(self.velocity.x) +
            to_float(self.velocity.y)
        )

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayInPlayerMove:
        """Create a player move packet from bytes."""

        position_x = from_float(data[0:4])
        position_y = from_float(data[4:8])
        acceleration_x = from_float(data[8:12])
        acceleration_y = from_float(data[12:16])
        velocity_x = from_float(data[16:20])
        velocity_y = from_float(data[20:24])

        return cls(
            Vector2(position_x, position_y),
            Vector2(acceleration_x, acceleration_y),
            Vector2(velocity_x, velocity_y)
        )

    def __repr__(self) -> str:
        return (
            f"<PacketPlayInPlayerMove "
            f"position={self.position} "
            f"acceleration={self.acceleration} "
            f"velocity={self.velocity}>"
        )
