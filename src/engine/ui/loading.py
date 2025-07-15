import math

import pygame as pg
from pygame.math import Vector2
from typing import override

from .component import UIComponent


class LoadAnimation(UIComponent):
    pivot: Vector2
    color = tuple[int, int, int] | str

    def __init__(
        self,
        x: int | str = 0, y: int | str = 0,
        width: int = 100, height: int = 100,
        pivot: Vector2 | tuple[float, float] | str = (0.5, 0.5),
        color: tuple[int, int, int] | str = (255, 255, 255)
    ) -> None:
        """Initialize a loading animation UI component.

        Args:
            x (int | str, optional): The x position of the animation. Can be a percentage of the screen width. Defaults to 0.
            y (int | str, optional): The y position of the animation. Can be a percentage of the screen height. Defaults to 0.
            width (int, optional): The width of the animation. Defaults to 100.
            height (int, optional): The height of the animation. Defaults to 100.
            pivot (Vector2 | tuple[float, float] | str, optional): The pivot point of the animation. Defaults to (0.5, 0.5).
            color (tuple[int, int, int] | str, optional): The color of the animation. Defaults to (255, 255, 255).
        """
        super().__init__(x=x, y=y, width=width, height=height, pivot=pivot)
        self.color = color

    @override
    def draw(self, surface: pg.Surface) -> None:
        """Draw a Loading Animation."""

        center = self.rect.center
        radius = min(self.rect.width, self.rect.height) // 2 - 10

        # Radian angle for the arc
        t = pg.time.get_ticks() / 1000.0
        angle = -(t * 2 * math.pi) % (2 * math.pi)
        arc_length = math.pi * 1.2  # Tamanho do arco (em radianos)

        # Rect for the arc
        arc_rect = pg.Rect(
            center[0] - radius,
            center[1] - radius,
            radius * 2,
            radius * 2
        )

        # Draw the rotating arc
        pg.draw.arc(
            surface,
            self.color,
            arc_rect,
            angle,
            angle + arc_length,
            width=8
        )
