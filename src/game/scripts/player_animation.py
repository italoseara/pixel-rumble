import math
import pytmx
import random
import pygame as pg
from pygame.math import Vector2
from typing import override

from engine import (
    Transform,
    Component,
    RigidBody,
    SpriteRenderer,
)

class PlayerAnimation(Component):
    def __init__(self) -> None:
        super().__init__()

        self.flip_x = False  # Indicates if the player is facing left
        self.desired_position = None  # Position to move towards, if any
    
    @override
    def update(self, dt: float) -> None:
        transform = self.parent.get_component(Transform)
        rigid_body = self.parent.get_component(RigidBody)

        self.handle_desired_position(transform)
        self.handle_sprite_flip(rigid_body)

        if rigid_body.acceleration.length() > 0:
            self.handle_walk_animation(transform)   
        else:
            self.handle_idle_animation(transform)

    def handle_idle_animation(self, transform: Transform) -> None:
        transform.scale = Vector2(5, 5 + math.sin(pg.time.get_ticks() / 200) / 7)
        transform.rotation *= 0.8

    def handle_walk_animation(self, transform: Transform) -> None:
        transform.scale = Vector2(5, 5 + math.sin(pg.time.get_ticks() / 40) / 5)
        transform.rotation = math.sin(pg.time.get_ticks() / 80) * 5

    def handle_sprite_flip(self, rigid_body: RigidBody) -> None:
        if rigid_body.acceleration.x < 0:
            self.flip_x = True
        elif rigid_body.acceleration.x > 0:
            self.flip_x = False
        
        sprite_renderer = self.parent.get_component(SpriteRenderer)
        if sprite_renderer:
            sprite_renderer.flip_x = self.flip_x

    def handle_desired_position(self, transform: Transform) -> None:
        """Interpolate from the current position to the desired position."""
        
        if self.desired_position is not None:
            transform.position = transform.position.lerp(self.desired_position, 0.2)
            transform.position.x = int(transform.position.x)
            transform.position.y = int(transform.position.y)