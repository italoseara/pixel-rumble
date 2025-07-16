import math
import pytmx
import random
import pygame as pg
from pygame.math import Vector2
from typing import override

from engine import (
    Tilemap,
    Transform,
    Component,
    RigidBody,
    SpriteRenderer,
)

class PlayerController(Component):
    def __init__(self, jump_force: float = 700, move_speed: float = 1700) -> None:
        super().__init__()

        self.flip_x = False
        self.jump_force = jump_force
        self.move_speed = move_speed
        self.boost = True
        self.last_boost_time = 0

    @override
    def start(self) -> None:
        """Initialize the PlayerController component.

        Raises:
            RuntimeError: If the Map object or Tilemap component is not found in the scene.
        """

        # Set random position for the player
        self.set_random_pos()

    @override
    def update(self, dt: float) -> None:
        keys = pg.key.get_pressed()
        transform = self.parent.get_component(Transform)
        rigid_body = self.parent.get_component(RigidBody)

        self.handle_movement(keys, rigid_body)
        self.handle_jump(keys, rigid_body)
        self.handle_boost(keys, rigid_body)
        self.handle_sprite_flip()
        self.reset_if_fallen(transform, rigid_body)

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

    def handle_movement(self, keys: pg.key.ScancodeWrapper, rigid_body: RigidBody) -> None:
        if keys[pg.K_a]:
            rigid_body.add_force((-self.move_speed, 0))
            self.flip_x = True
        if keys[pg.K_d]:
            rigid_body.add_force((self.move_speed, 0))
            self.flip_x = False

    def handle_jump(self, keys: pg.key.ScancodeWrapper, rigid_body: RigidBody) -> None:
        if (keys[pg.K_SPACE] or keys[pg.K_w]) and rigid_body.is_grounded:
            rigid_body.add_impulse((0, -self.jump_force))

    def handle_boost(self, keys: pg.key.ScancodeWrapper, rigid_body: RigidBody) -> None:
        current_time = pg.time.get_ticks() / 1000
        if keys[pg.K_LSHIFT] and self.boost and self.last_boost_time + 0.5 < current_time:
            impulse_direction = Vector2(-1, 0) if self.flip_x else Vector2(1, 0)
            rigid_body.add_impulse(impulse_direction * self.move_speed / 2)
            self.boost = False
            self.last_boost_time = current_time

        if not self.boost and rigid_body.is_grounded:
            self.boost = True

    def handle_sprite_flip(self) -> None:
        sprite_renderer = self.parent.get_component(SpriteRenderer)
        if sprite_renderer:
            sprite_renderer.flip_x = self.flip_x

    def reset_if_fallen(self, transform: Transform, rigid_body: RigidBody) -> None:
        if transform.y > 1000:
            self.set_random_pos()
            rigid_body.velocity = Vector2(0, 0)
            rigid_body.acceleration = Vector2(0, 0)

    def set_random_pos(self) -> None:
        """Initialize the PlayerController component."""

        map_object = self.parent.scene.find("Map")
        tilemap = map_object.get_component(Tilemap)

        spawn_points = []
        for spawn in tilemap.data.get_layer_by_name("Spawn"):
            spawn: pytmx.TiledObject

            if spawn.name == "PlayerSpawnPoint":
                spawn_points.append((spawn.x, spawn.y))

        if not spawn_points:
            raise RuntimeError("No spawn points found in the Tilemap")

        x, y = random.choice(spawn_points)
        transform = self.parent.get_component(Transform)
        transform.position = tilemap.get_position(x, y)