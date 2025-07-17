import pytmx
import random
import pygame as pg
from pygame.math import Vector2
from typing import override

from engine import Game, Tilemap, Transform, Component, RigidBody
from .player_animation import PlayerAnimation

class PlayerController(Component):
    def __init__(self, jump_force: float = 700, move_speed: float = 1700) -> None:
        super().__init__()

        self.jump_force = jump_force
        self.move_speed = move_speed
        self.boost = True
        self.last_boost_time = 0

        self.last_position_update = Vector2(0, 0)
        self.last_position_update_time = 0  # Track last forced update time

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
        self.reset_if_fallen(transform, rigid_body)
        self.handle_position_packet(transform, rigid_body)

    def handle_movement(self, keys: pg.key.ScancodeWrapper, rigid_body: RigidBody) -> None:
        if keys[pg.K_a]:
            rigid_body.add_force((-self.move_speed, 0))
        if keys[pg.K_d]:
            rigid_body.add_force((self.move_speed, 0))

    def handle_jump(self, keys: pg.key.ScancodeWrapper, rigid_body: RigidBody) -> None:
        if (keys[pg.K_SPACE] or keys[pg.K_w]) and rigid_body.is_grounded:
            rigid_body.add_impulse((0, -self.jump_force))

    def handle_boost(self, keys: pg.key.ScancodeWrapper, rigid_body: RigidBody) -> None:
        current_time = pg.time.get_ticks() / 1000
        if keys[pg.K_LSHIFT] and self.boost and self.last_boost_time + 0.5 < current_time:
            player_animation = self.parent.get_component(PlayerAnimation)
            impulse_direction = Vector2(-1, 0) if player_animation.flip_x else Vector2(1, 0)
            rigid_body.add_impulse(impulse_direction * self.move_speed / 2)
            self.boost = False
            self.last_boost_time = current_time

        if not self.boost and rigid_body.is_grounded:
            self.boost = True

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

    def handle_position_packet(self, transform: Transform, rigid_body: RigidBody) -> None:
        """Send a position update packet if the player has moved significantly or every 0.5 seconds."""

        current_time = pg.time.get_ticks() / 1000  # seconds
            
        if self.last_position_update.distance_to(transform.position) > 10 or \
            current_time - self.last_position_update_time >= 0.5:

            self.last_position_update = transform.position.copy()
            self.last_position_update_time = current_time

            Game.instance().client.move(
                position=transform.position,
                acceleration=rigid_body.acceleration,
                velocity=rigid_body.velocity
            )