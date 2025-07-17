import pygame
from typing import override
from pygame.math import Vector2

from engine import Component, GameObject


class GunController(Component):
    """Controls the gun's firing logic and bullet management."""

    player: GameObject
    automatic: bool
    fire_rate: float
    damage: int
    bullet_speed: float
    bullet_lifetime: float
    bullet_size: tuple[int, int]

    _angle: float
    
    def __init__(
        self,
        player: GameObject,
        automatic: bool = False,
        fire_rate: float = 0.5,
        damage: int = 10,
        bullet_speed: float = 500,
        bullet_lifetime: float = 2,
        bullet_size: tuple[int, int] = (10, 10)
    ) -> None:
    
        super().__init__()

        self.player = player
        self.automatic = automatic
        self.fire_rate = fire_rate
        self.damage = damage
        self.bullet_speed = bullet_speed
        self.bullet_lifetime = bullet_lifetime
        self.bullet_size = bullet_size

    @override
    def update(self, dt: float) -> None:
        """Update the gun's state, checking for firing input and managing bullets."""

        self.find_angle()

    def find_angle(self) -> None:
        """Finds the angle the player is aiming at based on mouse position."""

        scene = self.parent.scene
        mouse_pos = pygame.mouse.get_pos()
        
        self._angle = (Vector2(mouse_pos) - Vector2(player_pos)).angle_to(Vector2(1, 0))

        # Update the gun's rotation based on the angle
        self.game_object.transform.rotation = self._angle