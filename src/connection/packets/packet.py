from __future__ import annotations


class PacketMeta(type):
    """Metaclass to automatically register Packet subclasses."""

    registry = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        # Only register subclasses of Packet, not Packet itself
        if name != "Packet" and hasattr(cls, "id") and cls.id != -1:
            if cls.id in cls.registry:
                raise ValueError(f"Duplicate packet registration: 0x{cls.id:x}")
            cls.registry[cls.id] = cls

class Packet(metaclass=PacketMeta):
    """Base class for all packets."""

    id: int = -1
    data: bytes

    def __init__(self, data: bytes = b'') -> None:
        """Initialize a packet with an ID, state, binding type, and optional data."""

        self.data = data

    def to_bytes(self) -> bytes:
        """Convert the packet to bytes."""

        return bytes([self.id]) + self.data

    @classmethod
    def from_bytes(cls, data: bytes) -> type[Packet]:
        """Create a packet instance from bytes."""

        if len(data) < 1:
            raise ValueError("Packet data too short")

        id_ = data[0]

        packet_class = cls.registry.get(id_)
        if not packet_class:
            raise ValueError(f"Unknown packet type: 0x{id_:x}")

        return packet_class.from_bytes(data[1:])

    def __repr__(self) -> str:
        """Return a string representation of the packet."""

        data = "0x" + self.data.hex() if self.data else "None"
        return f"<{self.__class__.__name__} id=0x{self.id:x} data={data}>"