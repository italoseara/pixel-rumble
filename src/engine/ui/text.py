from __future__ import annotations

import pygame as pg
from pygame.math import Vector2
from typing import override

from .component import UIComponent
from ..constants import DEFAULT_FONT


class Text(UIComponent):
    _text: str
    color: pg.Color
    shadow: bool
    shadow_color: pg.Color
    _font: pg.font.Font
    
    def __init__(
        self, 
        text: str = "", 
        x: int = 0, y: int = 0,
        pivot: Vector2 | tuple[float, float] | str = (0.0, 0.0),
        *,
        color: pg.Color = pg.Color(255, 255, 255),
        shadow: bool = True,
        shadow_color: pg.Color = pg.Color(38, 43, 68),
        font_size: int = 48,
    ) -> None:
        """Initialize a Text UI component.

        Args:
            text (str, optional): The text to display. Defaults to an empty string.
            x (int, optional): The x position of the text. Defaults to 0.
            y (int, optional): The y position of the text. Defaults to 0.
            color (pg.Color, optional): The color of the text. Defaults to white.
            shadow (bool, optional): Whether to draw a shadow behind the text. Defaults to True.
            shadow_color (pg.Color, optional): The color of the shadow. Defaults to black.
            font_size (int, optional): The size of the font. Defaults to 24.
        """
        
        super().__init__(
            x=x, y=y, pivot=pivot,
            width=0, height=0  # Width and height will be set based on the text size
        )
        
        self._text = text
        self.color = color
        self.shadow = shadow
        self.shadow_color = shadow_color
        self._font = pg.font.Font(DEFAULT_FONT, font_size)
        self._update_size()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value
        self._update_size()

    def _update_size(self) -> None:
        text_surface = self._font.render(self._text, False, self.color)
        self.width, self.height = text_surface.get_size()

    @override
    def draw(self, surface: pg.Surface) -> None:
        if not self.active:
            return

        if self.shadow:
            shadow = self._font.render(self._text, False, self.shadow_color)
            shadow_offset = min(5, self._font.size(self._text)[1] // 5)  # Offset for shadow
            surface.blit(shadow, (self.position.x + shadow_offset, self.position.y + shadow_offset))

        text = self._font.render(self._text, False, self.color)
        surface.blit(text, self.position)

        super().draw(surface)

    @override
    def clone(self) -> Text:
        """Create a copy of this Text component."""
        return Text(
            text=self._text,
            x=self.position.x,
            y=self.position.y,
            pivot=self.pivot,
            color=self.color,
            shadow=self.shadow,
            shadow_color=self.shadow_color,
            font_size=self._font.get_height()
        )