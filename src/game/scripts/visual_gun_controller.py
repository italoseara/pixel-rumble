import time
import math
import random
import pygame as pg
from typing import override
from pygame.math import Vector2

from engine import Component, GameObject, Transform, SpriteRenderer, RigidBody, BoxCollider, Game
from engine.ui import Text
from .player_animation import PlayerAnimation

class VisualGunController(Component):
    """Controls the gun's visual representation."""

    player: GameObject

    def __init__(self, player: GameObject) -> None:
        super().__init__()

        self.player = player

    @override
    def update(self, dt: float) -> None:
        """Update the gun's state, checking for firing input and managing bullets."""

        self.handle_look_angle()

    def handle_look_angle(self) -> None:        
        # Update the gun's rotation based on the angle
        transform = self.parent.get_component(Transform)
        sprite_renderer = self.parent.get_component(SpriteRenderer)
        player_animation = self.player.get_component(PlayerAnimation)

        if not transform or not sprite_renderer or not player_animation:
            return

        look_angle = player_animation.look_angle
        transform.rotation = look_angle

        sprite_renderer.flip_y = look_angle > 90 or look_angle < -90
