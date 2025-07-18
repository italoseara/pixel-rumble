from __future__ import annotations

from pygame.math import Vector2
from connection.util import from_uint8, to_uint8, from_float, to_float, from_uint32, to_uint32
from connection.packets import Packet


class PacketPlayOutShoot(Packet):
    """Shoot packet for the play state."""

    id = 0x18

    player_id: int
    gun_type: str
    angle: float
    position: Vector2

    def __init__(self, player_id: int, gun_type: str, angle: float, position: Vector2) -> None:
        self.player_id = player_id
        self.gun_type = gun_type
        self.angle = angle
        self.position = position

        data = bytearray()
        data.extend(to_uint32(self.player_id))
        data.extend(to_uint8(len(self.gun_type)))
        data.extend(self.gun_type.encode())
        data.extend(to_float(self.angle))
        data.extend(to_float(self.position.x))
        data.extend(to_float(self.position.y))
        super().__init__(data)

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayOutShoot:
        """Create a shoot packet from bytes."""

        player_id = from_uint32(data[0:4])
        gun_type_length = from_uint8(data[4:5])
        gun_type = data[5:5 + gun_type_length].decode()
        angle = from_float(data[5 + gun_type_length:9 + gun_type_length])
        position_x = from_float(data[9 + gun_type_length:13 + gun_type_length])
        position_y = from_float(data[13 + gun_type_length:17 + gun_type_length])
        position = Vector2(position_x, position_y)

        return cls(player_id, gun_type, angle, position)

    def __repr__(self) -> str:
        return f"<PacketPlayOutShoot player_id={self.player_id} gun_type={self.gun_type} angle={self.angle} position={self.position}>"