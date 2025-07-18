import time
import math
import random
import pygame as pg
from typing import override
from pygame.math import Vector2

from engine import Component, GameObject, Transform, SpriteRenderer, RigidBody, BoxCollider, Game
from engine.ui import Text

from .player_animation import PlayerAnimation
from .bullet_controller import BulletController
from ..consts import GUN_ATTRIBUTES

class GunController(Component):
    """Controls the gun's firing logic and bullet management."""

    player_id: int
    player: GameObject
    automatic: bool
    fire_rate: float
    camera_shake: float
    spread: float
    recoil: float
    damage: int
    bullet_speed: float
    bullet_lifetime: float
    bullet_size: tuple[int, int]
    ammo_count: int
    max_ammo: int

    _gun_type: str

    def __init__(self, player_id: int, player: GameObject, ammo_counter: Text, gun_type: str) -> None:
        self._gun_type = gun_type

        self.player_id = player_id
        self.player = player
        self.ammo_counter = ammo_counter
        
        self.automatic = GUN_ATTRIBUTES[gun_type]["automatic"]
        self.fire_rate = GUN_ATTRIBUTES[gun_type]["fire_rate"]
        self.camera_shake = GUN_ATTRIBUTES[gun_type]["camera_shake"]
        self.spread = GUN_ATTRIBUTES[gun_type]["spread"]
        self.damage = GUN_ATTRIBUTES[gun_type]["damage"]
        self.recoil = GUN_ATTRIBUTES[gun_type]["recoil"]
        self.bullet_speed = GUN_ATTRIBUTES[gun_type]["bullet_speed"]
        self.bullet_lifetime = GUN_ATTRIBUTES[gun_type]["bullet_lifetime"]
        self.max_ammo = GUN_ATTRIBUTES[gun_type]["max_ammo"]
        self.ammo_count = self.max_ammo

        self._last_fire_time = 0.0

    @override
    def handle_event(self, event: pg.event.Event) -> None:
        """Handle input events for firing the gun."""
        
        if event.type == pg.MOUSEBUTTONDOWN and not self.automatic:
            if event.button == pg.BUTTON_LEFT:
                self.fire()

        if event.type == pg.KEYDOWN and event.key == pg.K_g:
            self.drop()

    @override
    def update(self, dt: float) -> None:
        """Update the gun's state, checking for firing input and managing bullets."""

        self.handle_automatic_fire(dt)
        self.update_ammo_counter()

    def update_ammo_counter(self) -> None:
        """Update the ammo counter text."""

        if self.ammo_count > 0:
            self.ammo_counter.text = f"{self.ammo_count}"
        else:
            self.ammo_counter.text = "--"

    def handle_automatic_fire(self, dt: float) -> None:
        """Handle automatic firing logic based on the fire rate."""
        
        if self.automatic and pg.mouse.get_pressed()[0]:
            current_time = pg.time.get_ticks() / 1000.0
            if current_time - self._last_fire_time >= self.fire_rate:
                self.fire()
                self._last_fire_time = current_time

    def fire(self) -> None:
        """Fires a bullet from the gun."""

        # check for cooldown
        current_time = pg.time.get_ticks() / 1000.0
        if current_time - self._last_fire_time < self.fire_rate:
            return

        if self.ammo_count <= 0:
            self.update_ammo_counter()
            self.drop()
            return

        transform = self.player.get_component(Transform)

        window_size = pg.display.get_window_size()

        look_angle = self.player.get_component(PlayerAnimation).look_angle
        spread_angle = look_angle + (self.spread * (pg.mouse.get_pos()[0] - window_size[0] // 2) / (window_size[0] // 2))
        
        offset = Vector2(40, -60)
        
        x = transform.x + offset.x * math.cos(math.radians(-spread_angle))
        y = (transform.y - 30) + offset.y * math.sin(math.radians(-spread_angle))
        
        # Create a bullet GameObject
        bullet = GameObject(f"Bullet_{self.player_id} {pg.time.get_ticks()}")
        bullet.add_component(Transform(
            x=x, y=y,
            scale=2,
            rotation=spread_angle,
            z_index=2
        ))
        bullet.add_component(BoxCollider(width=10, height=10, is_trigger=True))
        bullet_rigid_body = bullet.add_component(RigidBody(gravity=0, drag=0, is_trigger=True))
        bullet.add_component(SpriteRenderer("assets/img/bullet.png"))
        bullet.add_component(BulletController(self.bullet_lifetime, self.damage))
        self.parent.scene.add(bullet)

        velocity = Vector2(self.bullet_speed, 0).rotate(spread_angle)
        bullet_rigid_body.add_impulse(velocity)

        # Apply recoil
        rigid_body = self.player.get_component(RigidBody)
        rigid_body.add_impulse(velocity * -self.recoil)  # Apply a small recoil effect

        # Apply camera shake
        camera = self.parent.scene.camera
        camera.position += Vector2(
            -random.random() * self.camera_shake,
            -random.random() * self.camera_shake
        )

        Game.instance().client.shoot(
            self._gun_type,
            spread_angle,
            Vector2(x, y)
        )

        # Update the last fire time
        self._last_fire_time = current_time
        self.ammo_count -= 1
        if self.ammo_count == 0:
            self.update_ammo_counter()
            self.drop()

    def drop(self) -> None:
        """Drops the gun item."""
        
        self.parent.destroy()
        Game.instance().client.drop_item()
