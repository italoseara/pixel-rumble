import struct


def to_uint32(value: int) -> bytes:
    """Convert an integer to a 4-byte unsigned integer."""

    return struct.pack('>I', value)

def from_uint32(data: bytes) -> int:
    """Convert a 4-byte unsigned integer to an integer."""

    if len(data) != 4:
        raise ValueError("Data must be exactly 4 bytes long.")

    return struct.unpack('>I', data)[0]

def to_uint8(value: int) -> bytes:
    """Convert an integer to a 1-byte unsigned integer."""

    if not (0 <= value <= 255):
        raise ValueError("Value must be between 0 and 255.")

    return struct.pack('>B', value)

def from_uint8(data: bytes) -> int:
    """Convert a 1-byte unsigned integer to an integer."""

    if len(data) != 1:
        raise ValueError("Data must be exactly 1 byte long.")

    return struct.unpack('>B', data)[0]