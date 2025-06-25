import pygame as pg
from pygame.math import Vector2
from typing import TYPE_CHECKING

from ..constants import DEBUG_MODE
from ..core.components.component import Component
if TYPE_CHECKING:
    from ..core.components.canvas import Canvas

class UIComponent(Component):
    position: Vector2
    width: int
    height: int
    active: bool
    parent: 'Canvas'
    
    def __init__(self, x=0, y=0, width=0, height=0) -> None:
        super().__init__()
        self.position = Vector2(x, y)
        self.width = width
        self.height = height
        self.active = True
        self.parent = None
        
    def is_mouse_over(self, mouse_pos: Vector2) -> bool:
        """Check if the mouse position is within the component's bounds."""

        x, y = self.position
        return x <= mouse_pos.x <= x + self.width and y <= mouse_pos.y <= y + self.height

    def on_mouse_click(self, mouse_pos: Vector2) -> None:
        pass

    def on_mouse_release(self, mouse_pos: Vector2) -> None:
        pass

    def handle_key_event(self, event: pg.event.Event) -> None:
        pass

    def start(self) -> None:
        """Called once when the component is added to a Canvas."""
        pass

    def update(self, dt: float) -> None:
        """Called every frame; dt is seconds since last frame."""
        pass

    def draw(self, surface: pg.Surface) -> None:
        """Called every frame after update, to render visuals."""
        pass