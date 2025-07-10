import socket
import time

from packets import PacketStatusInPing, PacketStatusOutPong, Packet

DISCOVERY_PORT = 3567
BROADCAST_ADDR = '<broadcast>'
TIMEOUT        = 2.0 # seconds

def find_game_servers():
    # Create UDP socket for broadcast
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(TIMEOUT)

    packet = PacketStatusInPing()
    s.sendto(packet.to_bytes(), (BROADCAST_ADDR, DISCOVERY_PORT))
    print("Broadcasted Ping, waiting for replies...")

    servers = set()
    start = time.time()
    while True:
        try:
            data, addr = s.recvfrom(1024)
            try:
                packet = Packet.from_bytes(data)
                if not isinstance(packet, PacketStatusOutPong):
                    raise ValueError("Received packet is not a Pong packet")
                
                servers.add(f"{packet.ip}:{packet.port}")
                print(f"Received response from {addr[0]}:{addr[1]}: {packet.ip}:{packet.port}")
            except ValueError as e:
                print(f"Received invalid packet from {addr[0]}:{addr[1]}: {e}")
                continue
        except socket.timeout:
            break

        if time.time() - start > TIMEOUT:
            break

    return sorted(servers)

if __name__ == '__main__':
    available = find_game_servers()
    if not available:
        print("No game servers found.")
    else:
        print("Found servers:")
        for s in available:
            ip, port = s.split(':')
            print(f" - {ip} on TCP port {port}")
            # now you can do: tcp_sock.connect((ip, int(port)))
