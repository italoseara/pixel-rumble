from __future__ import annotations
from packets import Packet


class PacketPlayOutWelcome(Packet):
    """Welcome packet for the play state."""

    id = 0x03

    is_welcome: bool
    message: str

    def __init__(self, is_welcome: bool, message: str = "") -> None:
        self.is_welcome = is_welcome
        self.message = message

        super().__init__(data=bytes([(is_welcome & 1)]) + message.encode())

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketPlayOutWelcome:
        """Create a welcome packet from bytes."""

        if len(data) < 1:
            raise ValueError("Data must contain at least one byte")

        is_welcome = bool(data[0])
        message = data[1:].decode()

        return cls(is_welcome, message)

    def __repr__(self) -> str:
        return f"<PacketPlayOutWelcome is_welcome={self.is_welcome} message='{self.message}'>"