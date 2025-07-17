from engine.ui import Text
from engine import (
    GameObject,
    Transform,
    SpriteRenderer,
    BoxCollider,
    RigidBody,
    Canvas
)
from game.scripts import PlayerAnimation


class PlayerPrefab(GameObject):
    """A prefab for the player character in the game."""

    def __init__(self, id: int, name: str, x: float = 0, y: float = 0, is_local: bool = False) -> None:
        """Initializes the player prefab with a name and position.

        Args:
            id (int): The unique ID of the player.
            name (str): The name of the player.
            x (float): The x-coordinate of the player.
            y (float): The y-coordinate of the player.
        """

        super().__init__("Local Player" if is_local else f"Player ({id})")

        self.add_component(Transform(x=x, y=y, z_index=1, scale=5))
        self.add_component(SpriteRenderer(
            "assets/img/players.png",
            pivot="midbottom",
            grid_size=(8, 8),
            sprite_index=(0, 0)
        ))
        self.add_component(BoxCollider(width=30))
        self.add_component(RigidBody(drag=0.07, gravity=15, is_kinematic=is_local))
        self.add_component(PlayerAnimation())
        
        # Add a text component for the player's name
        self.add_component(Canvas()).add(Text(
            name,
            x=0, y=-45,
            pivot="midbottom",
            color=(255, 255, 255),
            font_size=18
        ))