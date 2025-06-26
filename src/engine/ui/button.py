import pygame as pg
from pygame.math import Vector2
from typing import Literal, Callable, override

from .component import UIComponent
from ..spritesheet import SpriteSheet
from ..constants import DEFAULT_FONT, PIVOT_POINTS

class Button(UIComponent):
    text: pg.Surface
    disabled: bool
    on_click: Callable | None
    pivot: Vector2

    _spritesheet: pg.Surface
    _sprites: dict[str, pg.Surface]
    _is_clicked: bool

    def __init__(
        self,
        text: str = "Button",
        x: int | str = 0, y: int | str = 0,
        size: Literal["sm", "md", "lg"] = "md",
        disabled: bool = False,
        on_click: Callable | None = None,
        pivot: Vector2 | tuple[float, float] | str = (0.5, 0.5)
    ) -> None:
        """Initialize a Button UI component.

        Args:
            text (str, optional): The text to display on the button. Defaults to "Button
            x (int | str, optional): The x position of the button. Can be a percentage of the screen width. Defaults to 0.
            y (int | str, optional): The y position of the button. Can be a percentage of the screen height. Defaults to 0.
            size (Literal["sm", "md", "lg"], optional): The size of the button. Defaults to "md".
            disabled (bool, optional): Whether the button is disabled. Defaults to False.
            on_click (Callable | None, optional): The function to call when the button is clicked. Defaults to None.
            pivot (Vector2 | tuple[float, float] | str, optional): The pivot point of the button. Defaults to (0.5, 0.5).
        """

        super().__init__(
            x=x, y=y, pivot=pivot,
            width=0, height=0  # Width and height will be set based on the sprite size
        )

        self._font = pg.font.Font(DEFAULT_FONT, 48)
        self.text = text
        self.disabled = disabled
        self.on_click = on_click

        self._is_clicked = False

        spritesheet = SpriteSheet("assets/img/ui/buttons.png", (16, 16), scale=3)
        columns = { "sm": 5, "md": "3:4", "lg": "0:2" }

        self._sprites = {
            "default": spritesheet.get_sprite((columns[size], 0)),
            "clicked": spritesheet.get_sprite((columns[size], 1))
        }

        self.width, self.height = self._sprites["default"].get_size()

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

        super().draw(surface)
