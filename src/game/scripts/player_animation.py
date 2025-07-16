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
)

class PlayerAnimation(Component):
    @override
    def update(self, dt: float) -> None:
        transform = self.parent.get_component(Transform)
        rigid_body = self.parent.get_component(RigidBody)

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
