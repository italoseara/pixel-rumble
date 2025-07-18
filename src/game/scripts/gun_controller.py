import time
import math
import random
import pygame as pg
from typing import override
from pygame.math import Vector2

from engine import Component, GameObject, Transform, SpriteRenderer, RigidBody, BoxCollider, Game
from engine.ui import Text


class BulletController(Component):
    """Controls the bullet's behavior, including movement and collision detection."""

    def __init__(self, lifetime: float) -> None:
        super().__init__()
        self.lifetime = lifetime
        self.start_time = time.time()

    @override
    def update(self, dt: float) -> None:
        """Update the bullet's position and check for lifetime expiration."""
        if time.time() - self.start_time > self.lifetime:
            self.parent.destroy()
            return

        box_collider = self.parent.get_component(BoxCollider)
        if box_collider and box_collider.is_colliding():
            self.parent.destroy()

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

    _angle: float
    
    def __init__(
        self,
        player_id: int,
        player: GameObject,
        ammo_counter: Text,
        automatic: bool = False,
        fire_rate: float = 0.5,
        camera_shake: float = 2,
        spread: float = 0.0,
        recoil: float = 0.1,
        damage: int = 10,
        bullet_speed: float = 500,
        bullet_lifetime: float = 2,
        bullet_size: tuple[int, int] = (10, 10),
        max_ammo: int = 30
    ) -> None:
    
        super().__init__()

        self.player_id = player_id
        self.player = player
        self.ammo_counter = ammo_counter
        
        self.automatic = automatic
        self.fire_rate = fire_rate
        self.camera_shake = camera_shake
        self.spread = spread
        self.damage = damage
        self.recoil = recoil
        self.bullet_speed = bullet_speed
        self.bullet_lifetime = bullet_lifetime
        self.bullet_size = bullet_size
        self.max_ammo = max_ammo
        self.ammo_count = max_ammo

        self._last_fire_time = 0.0

    @override
    def handle_event(self, event: pg.event.Event) -> None:
        """Handle input events for firing the gun."""
        
        if event.type == pg.MOUSEBUTTONDOWN and not self.automatic:
            if event.button == pg.BUTTON_LEFT:
                self.fire()

    @override
    def update(self, dt: float) -> None:
        """Update the gun's state, checking for firing input and managing bullets."""

        self.find_angle()
        self.handle_automatic_fire(dt)
        self.update_ammo_counter()

    def update_ammo_counter(self) -> None:
        """Update the ammo counter text."""

        if self.ammo_count > 0:
            self.ammo_counter.text = f"Ammo: {self.ammo_count}"
            self.ammo_counter.active = True
        else:
            self.ammo_counter.text = "Out of Ammo"
            self.ammo_counter.active = False

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
        angle = self._angle + (self.spread * (pg.mouse.get_pos()[0] - window_size[0] // 2) / (window_size[0] // 2))
        
        offset = Vector2(40, -60)
        
        x = transform.x + offset.x * math.cos(math.radians(-angle))
        y = (transform.y - 30) + offset.y * math.sin(math.radians(-angle))
        
        # Create a bullet GameObject
        bullet = GameObject(f"Bullet_{self.player_id} {pg.time.get_ticks()}")
        bullet.add_component(Transform(
            x=x, y=y,
            scale=2,
            rotation=angle,
            z_index=2
        ))
        bullet.add_component(BoxCollider(width=self.bullet_size[0], height=self.bullet_size[1], is_trigger=True))
        bullet_rigid_body = bullet.add_component(RigidBody(gravity=0, drag=0, is_trigger=True))
        bullet.add_component(SpriteRenderer("assets/img/bullet.png"))
        bullet.add_component(BulletController(self.bullet_lifetime))
        self.parent.scene.add(bullet)

        velocity = Vector2(self.bullet_speed, 0).rotate(angle)
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

    def find_angle(self) -> None:
        """Finds the angle the player is aiming at based on mouse position."""

        player_transform = self.player.get_component(Transform)
        if not player_transform:
            return

        mouse_pos = pg.mouse.get_pos()
        player_pos = player_transform.screen_position + Vector2(0, -20)  # Adjust for gun offset
        
        self._angle = -(Vector2(mouse_pos) - Vector2(player_pos)).angle_to(Vector2(1, 0))

        # Update the gun's rotation based on the angle
        transform = self.parent.get_component(Transform)
        sprite_renderer = self.parent.get_component(SpriteRenderer)
        
        transform.rotation = self._angle

        sprite_renderer.flip_y = self._angle > 90 or self._angle < -90