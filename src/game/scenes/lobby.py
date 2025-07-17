from typing import override
from pygame.math import Vector2
import logging

from ..scripts import PlayerAnimation
from game.prefabs import PlayerPrefab
from engine import GameObject, Tilemap, Scene, Transform, Canvas, RigidBody
from engine.ui import Image


class LobbyScene(Scene):
    player_id: int
    player_name: str

    def __init__(self, id: int, name: str) -> None:
        super().__init__()

        self.player_id = id
        self.player_name = name
    
    @override
    def start(self) -> None:
        map_object = GameObject("Map")
        map_object.add_component(Transform(x=0, y=0, scale=2.5))
        tilemap = map_object.add_component(Tilemap("assets/maps/mario.tmx", pivot="center"))
        self.add(map_object)

        ui = GameObject("UI")
        canvas = ui.add_component(Canvas())
        canvas.add(Image(
            "assets/img/background/vignette.png",
            x=0, y=0,
            width="100%", height="100%",
            pivot="topleft",
            opacity=0.4
        ))
        self.add(ui)

        local_player = PlayerPrefab(self.player_id, self.player_name, is_local=True)
        self.add(local_player)

        self.background_color = tilemap.background_color
        self.camera.set_target(local_player, smooth=True, smooth_speed=10, offset=(0, -100))

    def add_player(self, player_id: int, name: str) -> None:
        """Adds a player to the lobby scene.

        Args:
            player_id (int): The unique ID of the player.
            name (str): The name of the player.
        """

        player = PlayerPrefab(player_id, name)
        self.add(player)

    def remove_player(self, player_id: int) -> None:
        """Removes a player from the lobby scene.

        Args:
            player_id (int): The unique ID of the player to remove.
        """

        player = self.find(f"Player ({player_id})")
        if player:
            self.remove(player)
            logging.info(f"[LobbyScene] Player with ID {player_id} removed.")
        else:
            logging.warning(f"[LobbyScene] Player with ID {player_id} not found.")

    def move_player(self, player_id: int, position: Vector2, acceleration: Vector2, velocity: Vector2) -> None:
        """Updates the position and movement of a player in the lobby.

        Args:
            player_id (int): The unique ID of the player.
            position (Vector2): The new position of the player.
            acceleration (Vector2): The acceleration vector of the player.
            velocity (Vector2): The velocity vector of the player.
        """

        player = self.find(f"Player ({player_id})")
        if player:
            player_animation = player.get_component(PlayerAnimation)
            player_animation.desired_position = position

            rigid_body = player.get_component(RigidBody)
            rigid_body.acceleration = acceleration
            rigid_body.velocity = velocity
        else:
            logging.warning(f"[LobbyScene] Player with ID {player_id} not found.")
