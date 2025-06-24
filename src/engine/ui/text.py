import pygame as pg
from .component import UIComponent

class Text(UIComponent):
    _text: str
    color: pg.Color
    font: pg.font.Font
    
    def __init__(
        self, 
        text: str = "", 
        x: int = 0, y: int = 0, 
        *,
        color: pg.Color = pg.Color(255, 255, 255), 
        font_size: int = 24,
    ) -> None:
        """Initialize a Text UI component.

        Args:
            text (str, optional): The text to display. Defaults to an empty string.
            x (int, optional): The x position of the text. Defaults to 0.
            y (int, optional): The y position of the text. Defaults to 0.
            color (pg.Color, optional): The color of the text. Defaults to white.
            font_size (int, optional): The size of the font. Defaults to 24.
        """
        
        super().__init__(x, y, 0, 0)
        self._text = text
        self.color = color
        self.font = pg.font.Font(None, font_size)
        self._update_size()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value
        self._update_size()
        
    def _update_size(self) -> None:
        text_surface = self.font.render(self._text, True, self.color)
        self.width, self.height = text_surface.get_size()
        
    def draw(self, surface: pg.Surface) -> None:
        if not self.active:
            return

        text_surface = self.font.render(self._text, True, self.color)
        surface.blit(text_surface, self.position)
