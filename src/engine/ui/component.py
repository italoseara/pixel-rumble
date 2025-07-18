from __future__ import annotations

import pygame as pg
from pygame.math import Vector2
from typing import TYPE_CHECKING

from ..core.game import Game
from ..core.components.transform import Transform
from ..util import validate_pivot
from ..constants import DEBUG_MODE

if TYPE_CHECKING:
    from ..core.components.canvas import Canvas

class UIComponent:
    _position: Vector2
    _rel_position: Vector2
    
    width: int
    height: int

    active: bool
    parent: 'Canvas'
    
    def __init__(
        self,
        x: int | str = 0,
        y: int | str = 0,
        width: int = 0,
        height: int = 0,
        pivot: Vector2 | tuple[float, float] | str = (0.0, 0.0)
    ) -> None:
        super().__init__()

        self._position = Vector2(0, 0)
        self._rel_position = Vector2(0, 0)
        self._parse_position(x, y)

        self.width = width
        self.height = height
        self.active = True
        self.parent = None
        self.pivot = validate_pivot(pivot)

    @property
    def rect(self) -> pg.Rect:
        """Get the rectangle representing the component's bounds."""

        return pg.Rect(self.position.x, self.position.y, self.width, self.height)

    @property
    def position(self) -> Vector2:
        """Get the relative position of the component based on the screen size, including offset."""

        pos = Vector2(self._position.x, self._position.y)

        if self._rel_position.x != 0:
            pos.x = self._rel_position.x * pg.display.get_surface().get_width()
            if pos.x < 0:
                pos.x += pg.display.get_surface().get_width()
        if self._rel_position.y != 0:
            pos.y = self._rel_position.y * pg.display.get_surface().get_height()
            if pos.y < 0:
                pos.y += pg.display.get_surface().get_height()

        if self.parent:
            transform = self.parent.parent.get_component(Transform)
            if transform:
                pos += transform.screen_position

        return pos + self.offset

    @property
    def offset(self) -> Vector2:
        """Calculate the offset based on the pivot point."""

        return Vector2(self.width * -self.pivot.x, self.height * -self.pivot.y)

    def _parse_position(self, x: int | str, y: int | str) -> None:
        """Parse the position, allowing for relative positioning."""

        if isinstance(x, str) and x.endswith('%'):
            self._rel_position.x = float(x[:-1]) / 100
            self._position.x = 0
        else:
            self._rel_position.x = 0
            self._position.x = float(x)

        if isinstance(y, str) and y.endswith('%'):
            self._rel_position.y = float(y[:-1]) / 100
            self._position.y = 0
        else:
            self._rel_position.y = 0
            self._position.y = float(y)

    def is_mouse_over(self, mouse_pos: Vector2) -> bool:
        """Check if the mouse position is within the component's bounds."""

        if self.parent is None:
            return False

        scene = self.parent.parent.scene
        current_scene = Game.instance().current_scene
        
        if current_scene != scene:
            return False

        return self.rect.collidepoint(mouse_pos)

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

        if DEBUG_MODE:
            color = (255, 0, 0)
            if not self.active:
                color = (128, 128, 128)
            elif self.is_mouse_over(pg.mouse.get_pos()):
                color = (0, 255, 0)
            
            pg.draw.rect(surface, color, self.rect, 1)

    def clone(self) -> UIComponent:
        """Create a copy of this UIComponent."""
        
        new_component = UIComponent(
            x=self._position.x,
            y=self._position.y,
            width=self.width,
            height=self.height,
            pivot=self.pivot
        )
        new_component._rel_position = self._rel_position.copy()
        new_component.active = self.active
        return new_component