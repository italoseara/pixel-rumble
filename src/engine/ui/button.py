import pygame as pg
from pygame.math import Vector2
from typing import Literal, Callable, override

from .component import UIComponent
from ..constants import DEFAULT_FONT, PIVOT_POINTS

class Button(UIComponent):
    text: pg.Surface
    disabled: bool
    on_click: Callable | None
    pivot: Vector2
    color: tuple[int, int, int] | str
    hover_color: tuple[int, int, int] | str

    _font: pg.font.Font
    _is_clicked: bool

    def __init__(
        self,
        text: str = "Button",
        x: int | str = 0, y: int | str = 0,
        width: int | None = None, height: int | None = None,
        font_size: int = 48,
        color: tuple[int, int, int] | str = (255, 255, 255),
        hover_color: tuple[int, int, int] | str = (200, 200, 200),
        disabled: bool = False,
        on_click: Callable | None = None,
        pivot: Vector2 | tuple[float, float] | str = (0.5, 0.5)
    ) -> None:
        """Initialize a Button UI component.

        Args:
            text (str, optional): The text to display on the button. Defaults to "Button
            x (int | str, optional): The x position of the button. Can be a percentage of the screen width. Defaults to 0.
            y (int | str, optional): The y position of the button. Can be a percentage of the screen height. Defaults to 0.
            width (int | None, optional): The width of the button. If None, it will be set based on the text width. Defaults to None.
            height (int | None, optional): The height of the button. If None, it will be set based on the text width. Defaults to None.
            font_size (int, optional): The font size of the button text. Defaults to 48.
            color (tuple[int, int, int] | str, optional): The color of the button text. Defaults to (255, 255, 255).
            hover_color (tuple[int, int, int] | str, optional): The color of the button text when hovered. Defaults to (200, 200, 200).
            disabled (bool, optional): Whether the button is disabled. Defaults to False.
            on_click (Callable | None, optional): The function to call when the button is clicked. Defaults to None.
            pivot (Vector2 | tuple[float, float] | str, optional): The pivot point of the button. Defaults to (0.5, 0.5).
        """

        super().__init__(
            x=x, y=y, pivot=pivot,
            width=width if width is not None else 0,
            height=height if height is not None else 0
        )

        self._font = pg.font.Font(DEFAULT_FONT, font_size)
        self.text = text
        self.disabled = disabled
        self.on_click = on_click
        self.color = color
        self.hover_color = hover_color

        self._is_clicked = False

        # Calculate the size of the button based on the text
        if width is None or height is None:
            text_surface = self._font.render(self.text, True, (255, 255, 255))
            if width is None:
                self.width = text_surface.get_width()
            if height is None:
                self.height = text_surface.get_height()

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

        # Draw the shadow
        center_x = self.position.x + self.width // 2
        center_y = self.position.y + self.height // 2 - 5 + (3 if self._is_clicked else 0)
        
        shadow = self._font.render(self.text, False, (38, 43, 68))
        surface.blit(shadow, shadow.get_rect(center=(center_x, center_y + 3)))

        # Render the text
        color = self.hover_color if self.is_mouse_over(pg.mouse.get_pos()) else self.color
        text = self._font.render(self.text, False, color)
        surface.blit(text, text.get_rect(center=(center_x, center_y)))

        super().draw(surface)
