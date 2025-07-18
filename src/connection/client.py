import time
import errno
import socket
import threading
import logging
from pygame.math import Vector2
from dataclasses import dataclass

from engine import Game
from connection.server import DISCOVERY_PORT
from connection.packets import (
    Packet, 
    PacketPlayInJoin, 
    PacketPlayOutWelcome, 
    PacketPlayInDisconnect,
    PacketStatusInPing,
    PacketStatusOutPong,
    PacketPlayInKeepAlive,
    PacketPlayOutKeepAlive,
    PacketPlayOutPlayerJoin,
    PacketPlayOutPlayerLeave,
    PacketPlayInPlayerMove,
    PacketPlayOutPlayerMove,
    PacketPlayInChangeCharacter,
    PacketPlayOutChangeCharacter,
    PacketPlayInStartGame,
    PacketPlayOutStartGame,
    PacketPlayInItemPickup,
    PacketPlayInAddItem,
    PacketPlayOutItemPickup,
    PacketPlayOutAddItem,
    PacketPlayInItemDrop,
    PacketPlayOutItemDrop,
    PacketPlayInPlayerLook,
    PacketPlayOutPlayerLook
)


TIMEOUT = 2  # seconds
TICK_RATE = 128  # ticks per second


@dataclass(unsafe_hash=True)
class ServerData:
    name: str
    ip: str
    port: int

class Client:
    """A UDP client that connects to a server and sends/receives packets."""

    name: str
    address: tuple[str, int]
    buffer_size: int

    sock: socket.socket

    running: bool

    last_keep_alive: float

    def __init__(self, name: str, server_ip: str, server_port: int, buffer_size: int = 1024) -> None:
        """Initializes the client with the specified IP address and port.

        Args:
            name (str): The name of the client.
            server_ip (str): The IP address of the server to connect to.
            server_port (int): The port number of the server to connect to.
            buffer_size (int): The size of the buffer for receiving data.
        """

        self.name = name
        self.address = (server_ip, server_port)
        self.buffer_size = buffer_size

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = False

        self.last_keep_alive = time.time()

    @staticmethod
    def search() -> set[ServerData]:
        """Searches for available servers and returns a set of ServerData objects."""

        logging.info("[Client] Searching for available servers...")

        # Send a ping request using broadcast
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(TIMEOUT)  # Set a timeout for receiving responses

        ping_packet = PacketStatusInPing()
        sock.sendto(ping_packet.to_bytes(), ('<broadcast>', DISCOVERY_PORT))

        servers = set()
        start = time.time()
        while True:            
            try:
                data, addr = sock.recvfrom(1024)
                try:
                    packet = Packet.from_bytes(data)
                    if not isinstance(packet, PacketStatusOutPong):
                        logging.warning("[Client] Received packet is not a Pong packet")
                        continue
                    
                    servers.add(ServerData(name=packet.name, ip=addr[0], port=packet.port))
                    logging.info(f"[Client] Received response from {addr[0]}:{addr[1]}: {packet}")

                except ValueError as e:
                    logging.warning(f"[Client] Received invalid packet from {addr[0]}:{addr[1]}: {e}")
                    continue
            except socket.timeout:
                break

            if time.time() - start > TIMEOUT:
                break

        sock.close()
        logging.info(f"[Client] Search completed. Found {len(servers)} servers.")
        return servers

    def on_packet_received(self, packet: Packet) -> None:
        """Handles a received packet from the server.

        Args:
            packet (Packet): The received packet.
        """

        logging.info(f"[Client] Received packet: {packet}")

        match packet:
            case welcome if isinstance(welcome, PacketPlayOutWelcome):
                if welcome.is_welcome:
                    from game.scenes.lobby import LobbyScene
                    
                    Game.instance().clear_scenes()
                    Game.instance().push_scene(LobbyScene(id=welcome.player_id, name=self.name))
                    logging.info(f"[Client] Connection successful: {welcome.message}")
                else:
                    logging.info(f"[Client] Connection failed: {welcome.message}")
                    self.stop()

            case keep_alive if isinstance(keep_alive, PacketPlayOutKeepAlive):
                response_packet = PacketPlayInKeepAlive(value=keep_alive.value)
                self.send(response_packet)
                self.last_keep_alive = time.time()

            case player_join if isinstance(player_join, PacketPlayOutPlayerJoin):
                current_scene = Game.instance().current_scene

                if hasattr(current_scene, 'add_player'):
                    current_scene.add_player(player_join.player_id, player_join.name)
                    logging.info(f"[Client] Player {player_join.name} with ID {player_join.player_id} joined the lobby.")
                else:
                    logging.warning("[Client] Current scene does not support adding players.")

            case player_leave if isinstance(player_leave, PacketPlayOutPlayerLeave):
                current_scene = Game.instance().current_scene

                if hasattr(current_scene, 'remove_player'):
                    current_scene.remove_player(player_leave.player_id)
                    logging.info(f"[Client] Player with ID {player_leave.player_id} left the lobby.")
                else:
                    logging.warning("[Client] Current scene does not support removing players.")

            case player_move if isinstance(player_move, PacketPlayOutPlayerMove):
                current_scene = Game.instance().current_scene
                if hasattr(current_scene, 'move_player'):
                    current_scene.move_player(
                        player_move.player_id,
                        player_move.position,
                        player_move.acceleration,
                        player_move.velocity
                    )

            case change_character if isinstance(change_character, PacketPlayOutChangeCharacter):
                current_scene = Game.instance().current_scene
                if hasattr(current_scene, 'change_character'):
                    current_scene.change_character(
                        player_id=change_character.player_id,
                        character_index=change_character.character_index
                    )

            case start_game if isinstance(start_game, PacketPlayOutStartGame):
                current_scene = Game.instance().current_scene
                if hasattr(current_scene, 'start_game'):
                    current_scene.start_game(map_name=start_game.map_name)

            case item if isinstance(item, PacketPlayOutAddItem):
                current_scene = Game.instance().current_scene
                if hasattr(current_scene, 'add_gun_item'):
                    current_scene.add_gun_item(
                        gun_type=item.gun_type,
                        x=int(item.position_x),
                        y=int(item.position_y)
                    )

            case item_pickup if isinstance(item_pickup, PacketPlayOutItemPickup):
                current_scene = Game.instance().current_scene

                if hasattr(current_scene, 'pickup_item'):
                    current_scene.pickup_item(
                        player_id=item_pickup.player_id,
                        gun_type=item_pickup.gun_type,
                        object_id=item_pickup.object_id
                    )

            case item_drop if isinstance(item_drop, PacketPlayOutItemDrop):
                current_scene = Game.instance().current_scene
                if hasattr(current_scene, 'drop_item'):
                    current_scene.drop_item(player_id=item_drop.player_id)

            case player_look if isinstance(player_look, PacketPlayOutPlayerLook):
                current_scene = Game.instance().current_scene
                if hasattr(current_scene, 'player_look'):
                    current_scene.player_look(
                        player_id=player_look.player_id,
                        angle=player_look.angle
                    )

            case _:
                logging.warning(f"[Client] Unhandled packet type: {packet}")

    def start(self) -> None:
        """Starts the client and begins listening for incoming packets."""

        if self.running:
            return
        
        self.sock.connect(self.address)
        self.running = True

        threading.Thread(target=self._listen_for_packets, daemon=True).start()
        threading.Thread(target=self._wait_for_keep_alive, daemon=True).start()
        logging.info(f"[Client] Client started and connected to {self.address}.")

        self.join()

    def stop(self) -> None:
        """Stops the client and closes the socket."""

        if not self.running:
            return

        self.running = False
        self.sock.close()
        logging.info("[Client] Client stopped.")

    def start_game(self, map_name: str) -> None:
        """Sends a request to start the game with the specified map name.

        Args:
            map_name (str): The name of the map to start the game on.
        """

        if not self.running:
            raise RuntimeError("Client is not running. Start the client before starting the game.")

        self.send(PacketPlayInStartGame(map_name=map_name))
        logging.info(f"[Client] Requesting to start game on map '{map_name}'.")

    def spawn_item(self, gun_type: str, x, y) -> None:
        """Sends a request to spawn an item at the specified position.

        Args:
            item_id (str): The ID of the item to spawn.
            x (int): The x-coordinate of the item's position.
            y (int): The y-coordinate of the item's position.
        """

        if not self.running:
            raise RuntimeError("Client is not running. Start the client before spawning items.")

        self.send(PacketPlayInAddItem(gun_type=gun_type, position=Vector2(x, y)))
        logging.info(f"[Client] Requesting to spawn item '{gun_type}' at ({x}, {y}).")

    def pickup_item(self, gun_type: str, object_id: int) -> None:
        """Sends a request to pick up an item.

        Args:
            player_id (int): The ID of the player picking up the item.
            gun_type (str): The type of the gun being picked up.
            object_id (int): The ID of the object being picked up.
        """

        if not self.running:
            raise RuntimeError("Client is not running. Start the client before destroying items.")

        self.send(PacketPlayInItemPickup(gun_type=gun_type, object_id=object_id))
        logging.info(f"[Client] Requesting to pick up item '{gun_type}' with object ID {object_id}.")

    def drop_item(self) -> None:
        """Sends a request to drop the current item."""

        if not self.running:
            raise RuntimeError("Client is not running. Start the client before dropping items.")

        self.send(PacketPlayInItemDrop())
        logging.info("[Client] Requesting to drop the current item.")

    def change_character(self, index: int) -> None:
        """Changes the character of the local player.

        Args:
            index (int): The index of the character to change to.
        """

        if not self.running:
            raise RuntimeError("Client is not running. Start the client before changing character.")

        self.send(PacketPlayInChangeCharacter(index))

    def look(self, angle: float) -> None:
        """Sends a player look packet to the server.

        Args:
            angle (float): The new angle of the player.
        """

        if not self.running:
            raise RuntimeError("Client is not running. Start the client before looking.")

        self.send(PacketPlayInPlayerLook(angle=angle))

    def move(self, position: Vector2, acceleration: Vector2, velocity: Vector2) -> None:
        """Sends a player move packet to the server.

        Args:
            position (Vector2): The new position of the player.
            acceleration (Vector2): The acceleration of the player.
            velocity (Vector2): The velocity of the player.
        """
        
        self.send(PacketPlayInPlayerMove(
            position=position,
            acceleration=acceleration,
            velocity=velocity
        ))

    def join(self) -> None:
        """Sends a join request to the server with the client's name."""

        if not self.running:
            raise RuntimeError("Client is not running. Start the client before joining.")

        self.send(PacketPlayInJoin(name=self.name))

    def disconnect(self) -> None:
        """Sends a disconnect request to the server."""

        if not self.running:
            raise RuntimeError("Client is not running. Start the client before disconnecting.")

        self.send(PacketPlayInDisconnect())
        self.stop()

    def send(self, packet: Packet) -> None:
        """Sends a packet to the server.

        Args:
            packet (Packet): The packet to send.
        """

        if not self.running:
            raise RuntimeError("Client is not running. Start the client before sending packets.")

        data = packet.to_bytes()
        self.sock.sendto(data, self.address)
        logging.info(f"[Client] Sent packet: {packet}")

    def _wait_for_keep_alive(self) -> None:
        """Waits for keep-alive packets from the server and handles them."""

        while self.running:
            if time.time() - self.last_keep_alive > 10:
                from game.scenes.menu import MainMenu
                
                logging.warning("[Client] No keep-alive packets received for 20 seconds. Stopping client.")
                Game.instance().clear_scenes()
                Game.instance().push_scene(MainMenu())
                self.disconnect()
                return

            time.sleep(1)

    def _listen_for_packets(self) -> None:
        """Listens for incoming packets from the server and handles them."""

        tick_interval = 1.0 / TICK_RATE
        while self.running:                
            start_time = time.time()
            try:
                data, _ = self.sock.recvfrom(self.buffer_size)

                packet = Packet.from_bytes(data)
                self.on_packet_received(packet)
            except socket.error as e:
                if not self.running:
                    break

                if e.errno == errno.ECONNREFUSED:
                    from game.scenes.menu import MainMenu
                    
                    logging.warning("[Client] Connection refused by the server. Stopping client.")
                    self.stop()

                    Game.instance().clear_scenes()
                    Game.instance().push_scene(MainMenu())
                else:
                    logging.error(f"[Client] Error receiving packet: {e}")

            elapsed = time.time() - start_time
            sleep_time = tick_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    def __repr__(self) -> str:
        return f"<Client name='{self.name}' address={self.address}>"
