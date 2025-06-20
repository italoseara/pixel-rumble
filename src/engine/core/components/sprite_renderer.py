from __future__ import annotations

import os
import pygame as pg
from pygame.math import Vector2

from .component import Component
from .transform import Transform


class SpriteRenderer(Component):
    image: pg.Surface | None
    color: pg.Color
    flip_x: bool
    flip_y: bool
    pivot: Vector2

    _path: str

    def __init__(
        self,
        path: str, 
        color: pg.Color = pg.Color(255, 255, 255), 
        flip_x: bool = False, flip_y: bool = False,
        pivot: Vector2 | tuple[float, float] = (0.5, 0.5)
    ) -> None:
        super().__init__()

        if not path:
            raise ValueError("Image path cannot be empty")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Image file not found at {path}")

        self._path = path
        self.image = None
        self.color = color
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.pivot = Vector2(pivot)

    def start(self) -> None:
        """Load the image from the specified path."""

        try:
            self.image = pg.image.load(self._path).convert_alpha()
            self.image.fill(self.color, special_flags=pg.BLEND_RGBA_MULT)
        except pg.error as e:
            raise RuntimeError(f"Failed to load image at {self._path}: {e}")

    def draw(self, surface: pg.Surface) -> None:
        """Draw the sprite on the given surface."""

        if self.image is None:
            raise RuntimeError("SpriteRenderer image not loaded.")

        # Apply flipping if necessary
        image = pg.transform.flip(self.image, self.flip_x, self.flip_y)
        
        transform = self.parent.get_component(Transform)
        if transform is None:
            raise RuntimeError("SpriteRenderer requires a Transform component on the owner.")

        # Scale the image based on the transform's scale
        scaled_width = int(image.get_width() * transform.scale.x)
        scaled_height = int(image.get_height() * transform.scale.y)
        image = pg.transform.scale(image, (scaled_width, scaled_height))

        # Calculate the position to draw the image
        offset = Vector2(scaled_width * -(self.pivot.x - 0.5), scaled_height * -(self.pivot.y - 0.5))
        position = transform.screen_position - offset

        # Rotate the image around the pivot point
        rotated_image = pg.transform.rotate(image, -transform.rotation)
        rotated_offset = offset.rotate(transform.rotation)
        rect = rotated_image.get_rect(center=position + offset + rotated_offset)
        
        # Draw the image on the surface
        surface.blit(rotated_image, rect.topleft)

    def __repr__(self) -> str:
        return f"<{super().__repr__()} path={self._path}, color={self.color}, flip_x={self.flip_x}, flip_y={self.flip_y}, pivot={self.pivot}>"