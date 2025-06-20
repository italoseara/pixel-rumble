from __future__ import annotations

import pygame as pg
from pygame.math import Vector2

from ..constants import DEBUG_MODE
from .component import Component
from .transform import Transform


class BoxCollider(Component):
    width: float
    height: float
    offset: Vector2
    
    def __init__(self, width: float, height: float, offset: Vector2 | tuple[float, float] = (0, 0)) -> None:
        super().__init__()
        
        self.width = width
        self.height = height
        self.offset = Vector2(offset)

    def start(self) -> None:
        """Initialize the BoxCollider."""
        
        # Ensure the parent has a Transform component
        self._transform = self.parent.get_component(Transform)
        if not self._transform:
            raise RuntimeError("BoxCollider requires a Transform component on the owner.")

    def draw(self, surface) -> None:
        if DEBUG_MODE:
            color = (255, 0, 0) if self.is_colliding() else (0, 255, 0)

            pos = self._transform.screen_position + self.offset
            rect = self.get_screen_rect()
            pg.draw.rect(surface, color, rect, 1)
            

    def get_rect(self) -> pg.Rect:
        """Get the collider's rectangle in world space."""
        
        transform = self.parent.get_component(Transform)
        if not transform:
            raise RuntimeError("BoxCollider requires a Transform component on the owner.")

        pos = transform.world_position + self.offset
        return pg.Rect(pos.x, pos.y, self.width, self.height)

    def get_screen_rect(self) -> pg.Rect:
        """Get the collider's rectangle in screen space."""
        
        transform = self.parent.get_component(Transform)
        if not transform:
            raise RuntimeError("BoxCollider requires a Transform component on the owner.")

        pos = transform.screen_position + self.offset
        return pg.Rect(pos.x, pos.y, self.width, self.height)

    def collides_with(self, other: BoxCollider) -> bool:
        """Check collision with another BoxCollider."""

        transform = self.parent.get_component(Transform)
        other_transform = other.parent.get_component(Transform)
        if not transform or not other_transform:
            raise RuntimeError("Both BoxColliders must have a Transform component on their owners.")

        pos1 = transform.world_position + self.offset
        pos2 = other_transform.world_position + other.offset

        return (
            pos1.x < pos2.x + other.width and
            pos1.x + self.width > pos2.x and
            pos1.y < pos2.y + other.height and
            pos1.y + self.height > pos2.y
        )

    def is_colliding(self) -> bool:
        """Check if this collider is colliding with any other BoxCollider in the scene."""

        for game_object in self.parent._scene._game_objects:
            if game_object is self.parent:
                continue
            
            collider = game_object.get_component(BoxCollider)
            if collider and self.collides_with(collider):
                return True
        
        return False

    def __repr__(self) -> str:
        return f"<{super().__repr__()} width={self.width} height={self.height} offset={self.offset}>"