import pygame as pg
from pygame.math import Vector2
from typing import Literal, Callable

from .component import UIComponent
from ..core.constants import DEFAULT_FONT


class Button(UIComponent):
    text: pg.Surface
    disabled: bool
    on_click: Callable | None

    _images: list[pg.Surface]
    _is_clicked: bool

    def __init__(
        self,
        text: str = "Button",
        x: int = 0, y: int = 0,
        size: Literal["sm", "md", "lg"] = "md",
        disabled: bool = False,
        on_click: Callable | None = None
    ) -> None:
        super().__init__(x, y, 0, 0)

        font = pg.font.Font(DEFAULT_FONT, 48)
        self.text = font.render(text, False, pg.Color(255, 255, 255))
        self.disabled = disabled
        self.on_click = on_click

        self._is_clicked = False

        self._images = self._get_images(size)

    def _get_images(self, size: Literal["sm", "md", "lg"]) -> list[pg.Surface]:
        """Load and return the button images based on the specified size."""
    
        full_image = pg.image.load(f"assets/img/ui/button-{size}.png").convert_alpha()
        full_image = pg.transform.scale(full_image, (full_image.get_width() * 3, 
                                                     full_image.get_height() * 3))

        self.width = full_image.get_width()
        self.height = full_image.get_height() // 2

        return [
            full_image.subsurface((0, 0, self.width, self.height)),  # normal
            full_image.subsurface((0, self.height, self.width, self.height)),  # pressed
        ]

    def on_mouse_click(self, mouse_pos: Vector2) -> None:
        if self.disabled or not self.active:
            return

        self._is_clicked = True

    def on_mouse_release(self, mouse_pos: Vector2) -> None:
        self._is_clicked = False

        if self.on_click:
            self.on_click()

    def draw(self, surface: pg.Surface) -> None:
        if not self.active:
            return

        # Choose the correct image based on state
        img = self._images[1] if self._is_clicked else self._images[0]

        surface.blit(img, self.position)
        center_x = self.position.x + self.width // 2
        center_y = self.position.y + self.height // 2 - 5 + (3 if self._is_clicked else 0)
        surface.blit(self.text, self.text.get_rect(center=(center_x, center_y)))