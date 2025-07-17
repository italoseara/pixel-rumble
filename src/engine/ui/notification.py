import pygame as pg
from pygame.math import Vector2

from typing import override
from ..ui.component import UIComponent
from ..constants import DEFAULT_FONT


class NotificationText(UIComponent):
    """A Text component that automatically deactivates after a specified duration."""
    _text: str
    color: pg.Color
    shadow: bool
    shadow_color: pg.Color
    _font: pg.font.Font

    def __init__(
            self,
            text: str = "",
            x: int = 400, y: int = 300,
            lifespan: int = 3000,  # Duration in milliseconds
            pivot: Vector2 | tuple[float, float] | str = (0.0, 0.0),
            color: pg.Color = pg.Color(255, 255, 255),
            font_size: int = 24,
    ) -> None:
        super().__init__(
            x=x, y=y,
            pivot=pivot,
            width=0, height=0
        )  # Width and height will be set based on the text size

        self.lifespan = lifespan
        self._start_time = pg.time.get_ticks()

        self._text = text
        self._color = color
        self._font = pg.font.Font(DEFAULT_FONT, font_size)
        self._opacity = 255  # Full opacity by default
        self._update_size()

    def _update_size(self) -> None:
        text_surface = self._font.render(self._text, False, self._color)
        self.width, self.height = text_surface.get_size()

    @override
    def update(self, dt):
        elapsed = (pg.time.get_ticks() - self._start_time)  # em ms
        if elapsed > self.lifespan:
            # Começa o fade-out nos últimos 1000ms
            fade_duration = 1000
            fade_elapsed = elapsed - self.lifespan
            if fade_elapsed < fade_duration:
                self._opacity = int(255 * (1 - fade_elapsed / fade_duration))
            else:
                self.active = False  # Desativa o componente após o fade-out completo
        else:
            self._opacity = 255

    @override
    def draw(self, surface):
        # Renderiza o texto com a opacidade atual
        text_surface = self._font.render(self._text, True, self._color)
        text_surface.set_alpha(self._opacity)
        surface.blit(text_surface, self.rect)

        super().draw(surface)