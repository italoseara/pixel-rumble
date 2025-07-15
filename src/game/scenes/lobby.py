import pygame as pg
from pygame.math import Vector2
from typing import override

from engine import (
    GameObject, 
    Tilemap, 
    Scene, 
    Transform,
    Component,
    RigidBody,
    SpriteRenderer,
    BoxCollider,
    Canvas,
)
from engine.ui import Image

class PlayerController(Component):
    def __init__(self, jump_force: float = 700, move_speed: float = 1500) -> None:
        super().__init__()

        self.flip_x = False
        self.jump_force = jump_force  # Adjust jump force as needed
        self.move_speed = move_speed  # Adjust move speed as needed
        self.boost = True
        self.last_boost_time = 0

    @override
    def update(self, dt: float) -> None:
        keys = pg.key.get_pressed()
        transform = self.parent.get_component(Transform)
        rigid_body = self.parent.get_component(RigidBody)

        if keys[pg.K_a]:
            rigid_body.add_force((-self.move_speed, 0))
            self.flip_x = True
        if keys[pg.K_d]:
            rigid_body.add_force((self.move_speed, 0))
            self.flip_x = False
        if (keys[pg.K_SPACE] or keys[pg.K_w]) and rigid_body.is_grounded:
            rigid_body.add_impulse((0, -self.jump_force))
        if keys[pg.K_LSHIFT] and self.boost and self.last_boost_time + 0.5 < pg.time.get_ticks() / 1000:
            impulse_direction = Vector2(-1, 0) if self.flip_x else Vector2(1, 0)
            rigid_body.add_impulse(impulse_direction * self.move_speed / 2)
            self.boost = False
            self.last_boost_time = pg.time.get_ticks() / 1000  # Reset boost timer

        if not self.boost and rigid_body.is_grounded:
            self.boost = True
        
        sprite_renderer = self.parent.get_component(SpriteRenderer)
        if sprite_renderer:
            sprite_renderer.flip_x = self.flip_x

        if transform.y > 1000:
            # Reset position if player falls off the screen
            transform.position = Vector2(0, 100)
            rigid_body.velocity = Vector2(0, 0)
            rigid_body.acceleration = Vector2(0, 0)

        
class LobbyScene(Scene):
    @override
    def start(self) -> None:
        self.background_color = pg.Color(0, 0, 0)


        tilemap = GameObject("Tilemap")
        tilemap.add_component(Transform(x=0, y=-100, scale=2.5))
        tilemap.add_component(Tilemap("assets/maps/mapatestemario.tmx", pivot="center"))
        self.add(tilemap)

        player = GameObject("Player")
        player.add_component(Transform(x=0, y=-100, scale=5))
        player.add_component(SpriteRenderer(
            "assets/img/players.png", 
            pivot="midbottom",
            grid_size=(8, 8),
            sprite_index=(0, 0)
        ))
        player.add_component(BoxCollider(width=30))
        player.add_component(RigidBody(drag=0.07, gravity=15))
        player.add_component(PlayerController())
        self.add(player)

        ui = GameObject("UI")
        canvas = ui.add_component(Canvas())
        canvas.add(Image(
            "assets/img/background/vignette.png",
            x=0, y=0,
            width="100%", height="100%",
            pivot="topleft",
            opacity=0.4
        ))
        self.add(ui)

        self.camera.set_target(tilemap, offset=Vector2(0, 100))