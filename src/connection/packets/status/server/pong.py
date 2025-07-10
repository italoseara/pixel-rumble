from __future__ import annotations
from packets import Packet


class PacketStatusOutPong(Packet):
    """Pong packet for the status state."""

    id = 0x01

    ip: str
    port: int

    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port

        super().__init__(data=f"{ip}:{port}".encode())

    @classmethod
    def from_bytes(cls, data: bytes) -> PacketStatusOutPong:
        """Create a pong packet from bytes."""

        ip_port = data.decode()
        if ':' not in ip_port:
            raise ValueError("Invalid IP:Port format in PacketStatusOutPong data")

        ip, port_str = ip_port.split(':')

        try:
            port = int(port_str)
        except ValueError:
            raise ValueError("Invalid port number in PacketStatusOutPong data")

        return cls(ip, port)

    def __repr__(self) -> str:
        return f"<PacketStatusOutPong ip={self.ip} port={self.port}>"