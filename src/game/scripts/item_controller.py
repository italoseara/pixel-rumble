from typing import override

import pygame as pg
from pygame.math import Vector2

from engine import Component, GameObject, Transform, SpriteRenderer, Game
from engine.core.components.box_collider import BoxCollider


class ItemController(Component):
    """Controls the item pickup and usage logic."""

    item_type: str
    position: Vector2

    hint : GameObject

    def __init__(self, item_type: str) -> None:
        """Initialize the ItemController with item type and position."""

        super().__init__()

        self.item_type = item_type
        self.position = Vector2(0, 0)
        self.hint = None

    def start(self) -> None:
        """Initialize the item controller, setting the position of the item."""

        self.hint = GameObject(f"{self.parent.name} - Hint", self.parent)
        self.hint.add_component(Transform(y=-35, scale=1.25, z_index=2))
        self.hint.add_component(SpriteRenderer(
            "assets/img/keyboard/E.png",
            grid_size=(17, 16),
            animation_frames=[(0, 0), (1, 0)],
            animation_duration=1.0,
            loop=True,
        ))
        self.hint.active = False

        Game.instance().current_scene.add(self.hint)

    @override
    def update(self, dt: float) -> None:
        """Update the item state, checking for player interaction."""

        local_player = self.parent.scene.find("Local Player")
        if not local_player:
            return

        player_collider = local_player.get_component(BoxCollider)
        box_collider = self.parent.get_component(BoxCollider)

        self.hint.active = player_collider.collides_with(box_collider)

    @override
    def handle_event(self, event: pg.event.Event) -> None:
        """Handle events related to item interaction."""

        if event.type == pg.KEYDOWN and event.key == pg.K_e and self.hint.active:
            local_player = self.parent.scene.find("Local Player")
            if not local_player:
                return

            if self.parent.scene.find(f"{local_player.name}'s Gun"):
                return
        
            # Add the item to the player's inventory
            self.parent.scene.set_player_gun(self.item_type)

            # Optionally, destroy the item GameObject after pickup
            self.parent.destroy()
            self.hint.destroy()