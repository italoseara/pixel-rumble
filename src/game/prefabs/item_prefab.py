import pygame as pg

from engine import GameObject, Transform, SpriteRenderer, BoxCollider, RigidBody
from ..scripts import ItemController
from .player import PlayerPrefab


class ItemPrefab(GameObject):
    def __init__(self, player: GameObject, item_type: str, x: int, y: int) -> None:
        super().__init__(f"Gun ({item_type}) - {pg.time.get_ticks()}")

        # Add components for the item
        self.add_component(Transform(x=x, y=y, scale=2, z_index=2))
        self.add_component(SpriteRenderer(f"assets/img/guns/{item_type}.png"))
        self.add_component(RigidBody(mass=1.0, drag=0.5, exceptions=[PlayerPrefab]))
        self.add_component(BoxCollider(width=15, height=15, is_trigger=True))
        self.add_component(ItemController(item_type))
