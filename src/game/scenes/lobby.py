import pytmx
from typing import override
from pygame.math import Vector2

from game.prefabs import PlayerPrefab
from engine import GameObject, Tilemap, Scene, Transform, Canvas, RigidBody, SpriteRenderer, Game
from engine.ui import Image, Button

from .menu import MainMenu
from ..scripts import PlayerAnimation, CharacterSelector, PlayerController


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
        tilemap = map_object.add_component(Tilemap("assets/maps/lobby.tmx", pivot="center"))
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
        canvas.add(Button(
            "< SAIR",
            x="5%", y="-10%",
            pivot="midleft",
            font_size=42,
            on_click=lambda: self.exit()
        ))

        if Game.instance().is_admin:
            canvas.add(Button(
                "INICIAR >",
                x="96%", y="90%",
                pivot="midright",
                font_size=42,
                on_click=lambda: print("[Game] Starting game... (This should be replaced with actual game start logic)"
            )))

        self.add(ui)

        local_player = PlayerPrefab(self.player_id, self.player_name, is_local=True)
        local_player.add_component(PlayerController())
        local_player.add_component(PlayerAnimation())
        self.add(local_player)

        self.add_character_selector(tilemap)
        
        self.background_color = tilemap.background_color
        self.camera.set_target(local_player, smooth=True, smooth_speed=10, offset=(0, -100))

    def add_character_selector(self, tilemap: Tilemap) -> None:
        """Adds the character selector to the lobby scene.

        Args:
            tilemap (Tilemap): The tilemap component of the map object.
        """

        collider_layer = tilemap.data.get_layer_by_name("Collider")

        for obj in collider_layer:
            obj: pytmx.TiledObject

            if obj.name != "CharacterSelect":
                continue
            
            game_object = self.find(f"{tilemap.parent.name} (Collider {obj.id})")
            if not game_object:
                continue

            character_index = obj.properties.get("character", 0)

            hint = GameObject(f"{game_object.name} - Hint", game_object)
            hint.add_component(Transform(x=10, y=-25, scale=1.25))
            hint.add_component(SpriteRenderer(
                "assets/img/keyboard/E.png",
                grid_size=(17, 16),
                animation_frames=[(0, 0), (1, 0)],
                animation_duration=1.0,
                loop=True,
            ))
            hint.active = False
            self.add(hint)

            character_selector = game_object.add_component(CharacterSelector(character_index, hint))

            print(f"[Game] Character selector initialized with index {character_selector.character_index}.")

    def change_character(self, player_id: int, character_index: int) -> None:
        """Changes the character of a player in the lobby.

        Args:
            player_id (int): The unique ID of the player.
            character_index (int): The index of the character to change to.
        """

        player = self.find(f"Player ({player_id})")
        if not player:
            print(f"[Game] Player with ID {player_id} not found.")
            return

        sprite_renderer = player.get_component(SpriteRenderer)
        if not sprite_renderer:
            print(f"[Game] Player {player_id} does not have a SpriteRenderer component.")
            return

        index = character_index % 16
        sprite_renderer.set_index((index % 4, index // 4))
        print(f"[Game] Player {player_id} changed character to index {index}.")

    def add_player(self, player_id: int, name: str) -> None:
        """Adds a player to the lobby scene.

        Args:
            player_id (int): The unique ID of the player.
            name (str): The name of the player.
        """

        player = PlayerPrefab(player_id, name)
        player.add_component(PlayerAnimation())
        self.add(player)

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

    def exit(self):
        """Exits the lobby scene and returns to the main menu."""
        Game.instance().client.disconnect()

        if Game.instance().is_admin:
            Game.instance().server.stop()
            Game.instance().is_admin = False

        Game.instance().clear_scenes()
        Game.instance().push_scene(MainMenu())