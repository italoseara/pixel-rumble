import math
import logging
import pygame as pg
from typing import override

from pygame.math import Vector2

from engine.ui import Image, Text
from engine import GameObject, Tilemap, Scene, Transform, Canvas, RigidBody, BoxCollider, SpriteRenderer, Game
from game.prefabs import PlayerPrefab, GunPrefab, ItemPrefab

from ..scripts import PlayerController, PlayerAnimation, GunController, GameLogic, VisualGunController, BulletController
from ..consts import GUN_ATTRIBUTES


class GameScene(Scene):
    player_id: int
    player_name: str
    character_index: tuple[int, int]
    players: dict[int, GameObject]

    def __init__(
        self, 
        id: int, 
        name: str, 
        character_index: tuple[int, int],
        players: dict[int, GameObject],
        map_name: str
    ) -> None:
        super().__init__()

        self.player_id = id
        self.player_name = name
        self.character_index = character_index
        self.players = players.copy()
        self.map_name = map_name

        self.local_player: GameObject | None = None
        self.ammo_counter: Text | None = None
        self.items: list[GameObject] = []

    @override
    def start(self) -> None:
        map_object = GameObject("Map")
        map_object.add_component(GameLogic())
        map_object.add_component(Transform(x=0, y=0, scale=2.5))
        tilemap = map_object.add_component(Tilemap(f"assets/maps/{self.map_name}.tmx", pivot="center"))
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

        canvas.add(Image(
            "assets/img/icons/heart.png",
            x="5%", y="-6%",
            width=40, height=40,
            pivot="center",
        ))
        self.health_text = canvas.add(Text(
            "100",
            x="9%", y="-6%",
            font_size=40, 
            color=(255, 255, 255),
            pivot="midleft",
        ))

        canvas.add(Image(
            "assets/img/icons/ammo.png",
            x="5%", y="-13%",
            width=18, height=36,
            pivot="center",
        ))
        self.ammo_counter = canvas.add(Text(
            "--",
            x="9%", y="-13%",
            font_size=40, 
            color=(255, 255, 255),
            pivot="midleft",
        ))
        self.add(ui)

        self.local_player = PlayerPrefab(
            self.player_id, 
            self.player_name, 
            character_index=self.character_index, 
            is_local=True
        )
        self.local_player.add_component(PlayerController(self.health_text))
        self.local_player.add_component(PlayerAnimation())
        self.add(self.local_player)

        for player in self.players.values():
            self.add(player)
        
        self.background_color = tilemap.background_color
        self.camera.set_target(self.local_player, smooth=True, smooth_speed=10, offset=(0, -100))

    def shoot(self, player_id: int, gun_type: str, angle: float, position: Vector2) -> None:
        """Handles shooting logic for the player.

        Args:
            player_id (int): The unique ID of the player.
            gun_type (str): The type of gun being used.
            angle (float): The angle at which the player is shooting.
            position (Vector2): The position from where the shot is fired.
        """

        bullet = GameObject(f"Bullet_{player_id} {pg.time.get_ticks()}")
        bullet.add_component(Transform(
            x=position.x, y=position.y,
            scale=2,
            rotation=angle,
            z_index=2
        ))
        bullet.add_component(BoxCollider(width=10, height=10, is_trigger=True))
        bullet_rigid_body = bullet.add_component(RigidBody(gravity=0, drag=0, is_trigger=True))
        bullet.add_component(SpriteRenderer("assets/img/bullet.png"))
        bullet.add_component(BulletController(
            GUN_ATTRIBUTES[gun_type]["bullet_lifetime"],
            GUN_ATTRIBUTES[gun_type]["damage"]
        ))
        self.add(bullet)

        bullet_speed = GUN_ATTRIBUTES[gun_type]["bullet_speed"]

        velocity = Vector2(bullet_speed, 0).rotate(angle)
        bullet_rigid_body.add_impulse(velocity)

    def add_gun_item(self, gun_type: str, x: int = 0, y: int = 0) -> None:
        """Adds a gun item to the local player.

        Args:
            gun_type (str): The type of gun to add.
        """

        if gun_type not in GUN_ATTRIBUTES:
            logging.warning(f"[Game] Gun '{gun_type}' not found.")
            return

        item = ItemPrefab(self.local_player, gun_type, x=x, y=y)
        self.items.append(item)
        self.add(item)

    def pickup_item(self, player_id: int, gun_type: str, object_id: int) -> None:
        """Removes an item from the scene.

        Args:
            gun_type (str): The type of gun to remove.
            object_id (int): The unique identifier of the item to remove.
        """

        item_name = f"Gun ({gun_type}) - {object_id}"
        if item := self.find(item_name):
            self.remove(item)

        self.give_item(gun_type, player_id)

    def give_item(self, gun_type: str, player_id: int = None) -> None:
        """Sets the gun for the local player.

        Args:
            gun_name (str): The name of the gun to set.
        """

        if gun_type not in GUN_ATTRIBUTES:
            logging.warning(f"[Game] Gun '{gun_type}' not found.")
            return

        if player_id is None:
            if self.find(f"{self.local_player.name}'s Gun"):
                logging.warning(f"[Game] Player already has a gun.")
                return
        
            gun = GunPrefab(self.local_player, gun_type)
            gun.add_component(GunController( self.player_id, self.local_player, self.ammo_counter, gun_type))
            gun.add_component(VisualGunController(self.local_player))
        else:
            if self.find(f"Player ({player_id})'s Gun"):
                logging.warning(f"[Game] Player {player_id} already has a gun.")
                return
            
            player = self.find(f"Player ({player_id})")
            if not player:
                logging.warning(f"[Game] Player with ID {player_id} not found.")
                return

            gun = GunPrefab(player, gun_type)
            gun.add_component(VisualGunController(player))
            
        self.add(gun)
    
    def drop_item(self, player_id: int) -> None:
        """Drops the gun item for the specified player.

        Args:
            player_id (int): The unique ID of the player.
        """

        player = self.find(f"Player ({player_id})")
        if not player:
            logging.warning(f"[Game] Player with ID {player_id} not found.")
            return

        gun = self.find(f"{player.name}'s Gun")
        if not gun:
            logging.warning(f"[Game] Player {player.name} does not have a gun to drop.")
            return

        gun.destroy()

    def remove_player(self, player_id: int) -> None:
        """Removes a player from the lobby scene.

        Args:
            player_id (int): The unique ID of the player to remove.
        """

        player = self.find(f"Player ({player_id})")
        if player:
            self.remove(player)
            logging.info(f"[Game] Player with ID {player_id} removed.")
        else:
            logging.warning(f"[Game] Player with ID {player_id} not found.")

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
            logging.warning(f"[Game] Player with ID {player_id} not found.")

    def player_look(self, player_id: int, angle: float) -> None:
        """Updates the look direction of a player.

        Args:
            player_id (int): The unique ID of the player.
            angle (float): The angle to look at.
        """

        player = self.find(f"Player ({player_id})")
        if player:
            player_animation = player.get_component(PlayerAnimation)
            player_animation.look_angle = angle
        else:
            logging.warning(f"[Game] Player with ID {player_id} not found.")

    def player_die(self, player_id: int) -> None:
        """Handles the death of a player.

        Args:
            player_id (int): The unique ID of the player.
        """

        player = self.find(f"Player ({player_id})")
        if player:
            logging.info(f"[Game] Player with ID {player_id} has died.")
        else:
            logging.warning(f"[Game] Player with ID {player_id} not found for death handling.")