from __future__ import annotations

import time
import math
import pygame as pg
from pygame.math import Vector2
from typing import override

from engine import (
    Transform,
    Component,
    RigidBody,
    SpriteRenderer,
    Game
)

class PlayerAnimation(Component):
    flip_x: bool
    desired_position: Vector2 | None
    look_angle: float

    _hit_time: float

    def __init__(self) -> None:
        super().__init__()

        self.flip_x = False
        self.desired_position = None
        self.look_angle = 0.0

        self._hit_time = 0

    @override
    def update(self, dt: float) -> None:
        transform = self.parent.get_component(Transform)
        rigid_body = self.parent.get_component(RigidBody)
        sprite_renderer = self.parent.get_component(SpriteRenderer)

        self.handle_look_angle()
        self.handle_desired_position(transform)
        self.handle_sprite_flip(rigid_body, sprite_renderer)
        self.handle_hit_animation(sprite_renderer)

        if rigid_body.acceleration.length() > 0:
            self.handle_walk_animation(transform)   
        else:
            self.handle_idle_animation(transform)

    def handle_hit_animation(self, sprite_renderer: SpriteRenderer) -> None:
        """Handle hit animation logic."""
        
        if self._hit_time > 0 and time.time() - self._hit_time < 0.1:
            sprite_renderer.color = (255, 128, 128)
        else:
            sprite_renderer.color = (255, 255, 255)
            self._hit_time = 0

    def handle_idle_animation(self, transform: Transform) -> None:
        transform.scale = Vector2(5, 5 + math.sin(pg.time.get_ticks() / 200) / 7)
        transform.rotation *= 0.8

    def handle_walk_animation(self, transform: Transform) -> None:
        transform.scale = Vector2(5, 5 + math.sin(pg.time.get_ticks() / 40) / 5)
        transform.rotation = math.sin(pg.time.get_ticks() / 80) * 5

    def handle_sprite_flip(self, rigid_body: RigidBody, sprite_renderer: SpriteRenderer) -> None:
        if rigid_body.acceleration.x < 0:
            self.flip_x = True
        elif rigid_body.acceleration.x > 0:
            self.flip_x = False
        
        sprite_renderer.flip_x = self.flip_x

    def handle_desired_position(self, transform: Transform) -> None:
        """Interpolate from the current position to the desired position."""
        
        if self.desired_position is not None:
            transform.position = transform.position.lerp(self.desired_position, 0.3)
            transform.position.x = int(transform.position.x)
            transform.position.y = int(transform.position.y)

    def handle_look_angle(self) -> None:
        """Rotate the player to face the look angle."""

        if self.parent.name != "Local Player":
            return

        transform = self.parent.get_component(Transform)
        if not transform:
            return

        mouse_pos = pg.mouse.get_pos()
        player_pos = transform.screen_position + Vector2(0, -20)  # Adjust for gun offset
        
        new_look_angle = -(Vector2(mouse_pos) - Vector2(player_pos)).angle_to(Vector2(1, 0))

        if abs(new_look_angle - self.look_angle) > 1:
            Game.instance().client.look(angle=new_look_angle)

        self.look_angle = new_look_angle

    def play_hit_animation(self) -> None:
        """Play hit animation when the player is hit by a bullet."""

        self._hit_time = time.time()

    @override
    def clone(self) -> PlayerAnimation:
        """Create a copy of this PlayerAnimation component."""
        
        new_animation = PlayerAnimation()
        new_animation.flip_x = self.flip_x
        new_animation.desired_position = self.desired_position
        return new_animation