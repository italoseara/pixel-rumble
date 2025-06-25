import pygame as pg
from pygame.math import Vector2
from typing import Literal, Callable, override

from .component import UIComponent
from ..core.constants import DEFAULT_FONT


class Button(UIComponent):
    text: pg.Surface
    disabled: bool
    on_click: Callable | None

    _spritesheet: pg.Surface
    _sprites: dict[str, pg.Surface]
    _is_clicked: bool

    def __init__(
        self,
        text: str = "Button",
        x: int = 0, y: int = 0,
        size: Literal["sm", "md", "lg"] = "md",
        disabled: bool = False,
        on_click: Callable | None = None
    ) -> None:
        """Initialize a Button UI component.

        Args:
            text (str, optional): The text to display on the button. Defaults to "Button
            x (int, optional): The x position of the button. Defaults to 0.
            y (int, optional): The y position of the button. Defaults to 0.
            size (Literal["sm", "md", "lg"], optional): The size of the button. Defaults to "md".
            disabled (bool, optional): Whether the button is disabled. Defaults to False.
            on_click (Callable | None, optional): The function to call when the button is clicked. Defaults to None.
        """
        
        super().__init__(x, y, 0, 0)

        self._font = pg.font.Font(DEFAULT_FONT, 48)
        self.text = text
        self.disabled = disabled
        self.on_click = on_click

        self._is_clicked = False

        self._load_sprites(size)

    def _load_sprites(self, size: Literal["sm", "md", "lg"], scale: int = 3) -> None:
        """Load the spritesheet and the sprite variantes based on the size.

        Args:
            size (Literal["sm", "md", "lg"]): The size of the button
            scale (int, optional): The scale factor for the button. Defaults to 3.
        """

        # Load the spritesheet
        self._spritesheet = pg.image.load(f"assets/img/ui/button-{size}.png").convert_alpha()
        w, h = self._spritesheet.get_size()
        
        self._spritesheet = pg.transform.scale(self._spritesheet, (w * scale, h * scale))

        # Set the width and height of the button based on the spritesheet size
        self.width = self._spritesheet.get_width()
        self.height = self._spritesheet.get_height() // 2

        # Load the two sprite variants, the one on the top is the default one, the one on the bottom is the clicked one
        self._sprites = {
            "default": self._spritesheet.subsurface((0, 0, self.width, self.height)),
            "clicked": self._spritesheet.subsurface((0, self.height, self.width, self.height))
        }

    @override
    def on_mouse_click(self, mouse_pos: Vector2) -> None:
        if self.disabled or not self.active:
            return

        self._is_clicked = True

    @override
    def on_mouse_release(self, mouse_pos: Vector2) -> None:
        self._is_clicked = False

        if not self.is_mouse_over(mouse_pos):
            return

        if self.on_click:
            self.on_click()

    @override
    def draw(self, surface: pg.Surface) -> None:
        if not self.active:
            return

        # Choose the correct image based on state
        img = self._sprites["clicked" if self._is_clicked else "default"]

        # Draw the button image
        surface.blit(img, self.position)

        # Draw the shadow
        center_x = self.position.x + self.width // 2
        center_y = self.position.y + self.height // 2 - 5 + (3 if self._is_clicked else 0)
        
        shadow = self._font.render(self.text, False, (38, 43, 68))
        surface.blit(shadow, shadow.get_rect(center=(center_x, center_y + 3)))

        # Render the text
        text = self._font.render(self.text, False, (255, 255, 255))
        surface.blit(text, text.get_rect(center=(center_x, center_y)))
