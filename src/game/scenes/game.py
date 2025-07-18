from typing import override
from pygame.math import Vector2

from engine.ui import Image, Text
from engine import GameObject, Tilemap, Scene, Transform, Canvas, RigidBody, Game
from game.prefabs import PlayerPrefab, GunPrefab, ItemPrefab
from ..scripts import PlayerController, PlayerAnimation, GunController, GameLogic


GUN_ATTRIBUTES = {
    "uzi___": {
        "automatic": True,
        "fire_rate": 0.05,
        "camera_shake": 5,
        "spread": 0.1,
        "recoil": 0.05,
        "damage": 10,
        "bullet_speed": 1000,
        "bullet_lifetime": 2,
        "bullet_size": (10, 10),
        "max_ammo": 60
    },
    "pistol": {
        "automatic": False,
        "fire_rate": 0.2,
        "camera_shake": 5,
        "spread": 0.0,
        "recoil": 0.1,
        "damage": 20,
        "bullet_speed": 1000,
        "bullet_lifetime": 2,
        "bullet_size": (10, 10),
        "max_ammo": 20
    },
    "awm___": {
        "automatic": False,
        "fire_rate": 2.0,
        "camera_shake": 50,
        "spread": 0.0,
        "recoil": 0.5,
        "damage": 100,
        "bullet_speed": 1500,
        "bullet_lifetime": 3,
        "bullet_size": (15, 15),
        "max_ammo": 5
    }
}


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

        self.local_player = PlayerPrefab(
            self.player_id, 
            self.player_name, 
            character_index=self.character_index, 
            is_local=True
        )
        self.local_player.add_component(PlayerController())
        self.local_player.add_component(PlayerAnimation())
        self.add(self.local_player)

        ui = GameObject("UI")
        canvas = ui.add_component(Canvas())
        canvas.add(Image(
            "assets/img/background/vignette.png",
            x=0, y=0,
            width="100%", height="100%",
            pivot="topleft",
            opacity=0.4
        ))
        self.ammo_counter = canvas.add(Text(
            f"Ammo: 0",
            x="1%", y="-1%",
            font_size=24, 
            color=(255, 255, 255),
            pivot="bottomleft"
        ))
        self.add(ui)

        for player in self.players.values():
            self.add(player)
        
        self.background_color = tilemap.background_color
        self.camera.set_target(self.local_player, smooth=True, smooth_speed=10, offset=(0, -100))

    def add_gun_item(self, gun_type: str, x: int = 0, y: int = 0) -> None:
        """Adds a gun item to the local player.

        Args:
            gun_type (str): The type of gun to add.
        """

        if gun_type not in GUN_ATTRIBUTES:
            print(f"[Game] Gun '{gun_type}' not found.")
            return

        item = ItemPrefab(self.local_player, gun_type, x=x, y=y)
        self.items.append(item)
        self.add(item)

    def remove_item(self, item_name: str) -> None:
        """Removes an item from the scene.

        Args:
            item_name (str): The name of the item to remove.
        """
        item = self.find(item_name)
        if item:
            self.remove(item)
            print(f"[Game] Item '{item_name}' removed.")
        else:
            print(f"[Game] Item '{item_name}' not found.")

    def set_player_gun(self, gun_type: str) -> None:
        """Sets the gun for the local player.

        Args:
            gun_name (str): The name of the gun to set.
        """

        if gun_type not in GUN_ATTRIBUTES:
            print(f"[Game] Gun '{gun_type}' not found.")
            return

        if self.find(f"{self.local_player.name}'s Gun"):
            print(f"[Game] Player already has a gun.")
            return

        gun = GunPrefab(self.local_player, gun_type)
        gun.add_component(GunController(
            self.player_id,
            self.local_player,
            self.ammo_counter,
            **GUN_ATTRIBUTES[gun_type]
        ))
        self.add(gun)


    def add_player(self, player_id: int, name: str) -> None:
        """Adds a player to the lobby scene.

        Args:
            player_id (int): The unique ID of the player.
            name (str): The name of the player.
        """

        player = PlayerPrefab(player_id, name)
        player.add_component(PlayerAnimation())
        self.add(player)

        self.players[player_id] = player

    def remove_player(self, player_id: int) -> None:
        """Removes a player from the lobby scene.

        Args:
            player_id (int): The unique ID of the player to remove.
        """

        player = self.find(f"Player ({player_id})")
        if player:
            self.remove(player)
            print(f"[Game] Player with ID {player_id} removed.")
        else:
            print(f"[Game] Player with ID {player_id} not found.")

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
            print(f"[Game] Player with ID {player_id} not found.")