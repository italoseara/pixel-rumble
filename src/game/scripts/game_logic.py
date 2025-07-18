import time
import pytmx
import random
from engine import Component, Tilemap, Game

from ..consts import GUN_ATTRIBUTES


class GameLogic(Component):
    """Base class for game logic components."""

    def __init__(self) -> None:
        super().__init__()

        self.last_spawn = 0

    def start(self) -> None:
        """Initialize the game logic component."""
        pass

    def update(self, dt: float) -> None:
        """Update the game logic component."""

        if not Game.instance().is_admin:
            return
        
        current_time = time.time()
        if current_time - self.last_spawn > 10:
            self.spawn_random_weapon()
            self.last_spawn = current_time

    def spawn_random_weapon(self) -> None:
        """Initialize the PlayerController component."""

        tilemap = self.parent.get_component(Tilemap)

        spawn_points = []
        for spawn in tilemap.data.get_layer_by_name("Spawn"):
            spawn: pytmx.TiledObject

            if spawn.name == "ItemSpawnPoint":
                spawn_points.append((spawn.x, spawn.y))

        if not spawn_points:
            raise RuntimeError("No spawn points found in the Tilemap")

        x, y = random.choice(spawn_points)
        position = tilemap.get_position(x, y)
        gun_type= random.choice(list(GUN_ATTRIBUTES.keys()))
        self.parent.scene.add_gun_item(
            gun_type= gun_type,
            x=position[0],
            y=position[1]
        )

        Game.instance().client.spawn_item(
            gun_type=gun_type,
            x=position[0],
            y=position[1]
        )