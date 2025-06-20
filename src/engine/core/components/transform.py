import pygame as pg
from pygame.math import Vector2

from .component import Component
from ..constants import DEBUG_MODE


class Transform(Component):
    position: Vector2
    rotation: float
    scale: Vector2

    def __init__(
        self, 
        position: Vector2 | tuple[float, float] = (0, 0), 
        rotation: float = 0.0, scale: Vector2 | float = 1, 
        *, 
        x: float = 0.0, y: float = 0.0
    ) -> None:
        super().__init__()

        self.position = Vector2(position) or Vector2(x, y)
        self.rotation = rotation
        self.scale = scale if isinstance(scale, Vector2) else Vector2(scale, scale)

    @property
    def world_position(self) -> Vector2:
        """Get the world position of the transform."""

        parent = self.parent.parent
        if parent and (transform := parent.get_component(Transform)):
            return transform.world_position + self.position
        return self.position

    @property
    def screen_position(self) -> Vector2:
        """Get the screen position of the transform."""
        
        if self.parent:
            return self.parent._scene.camera.world_to_screen(self.world_position)
        return self.world_position

    @property
    def x(self) -> float:
        """Get the x position."""
        
        return self.position.x

    @x.setter
    def x(self, value: float) -> None:
        """Set the x position."""
        
        self.position.x = value

    @property
    def y(self) -> float:
        """Get the y position."""
        
        return self.position.y

    @y.setter
    def y(self, value: float) -> None:
        """Set the y position."""
        self.position.y = value

    def draw(self, surface) -> None:
        """Draw the transform's position as a debug point."""
        
        if DEBUG_MODE:
            pg.draw.circle(surface, (0, 255, 0), self.screen_position, 2)
            pg.draw.line(surface, (0, 255, 0), self.screen_position, self.screen_position + Vector2(10, 0).rotate(self.rotation), 1)

            font = pg.font.Font(None, 16)

            pos_text = font.render(f"pos: (x: {self.x:.1f}, y: {self.y:.1f})", True, (0, 255, 0))
            pos_text_rect = pos_text.get_rect(topleft=self.screen_position)
            surface.blit(pos_text, pos_text_rect)

            scale_text = font.render(f"scale: (x: {self.scale.x:.1f}, y: {self.scale.y:.1f})", True, (0, 255, 0))
            scale_text_rect = scale_text.get_rect(topleft=self.screen_position + Vector2(0, 10))
            surface.blit(scale_text, scale_text_rect)

            rot_text = font.render(f"rot: {self.rotation:.1f}°", True, (0, 255, 0))
            rot_text_rect = rot_text.get_rect(topleft=self.screen_position + Vector2(0, 20))
            surface.blit(rot_text, rot_text_rect)

    def __repr__(self) -> str:
        return f"<{super().__repr__()} position={self.world_position}, rotation={self.rotation}, scale={self.scale}>"