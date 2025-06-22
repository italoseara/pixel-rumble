from __future__ import annotations

import os
import pygame as pg
from pygame.math import Vector2

from .component import Component
from .transform import Transform
from ..constants import PIVOT_POINTS, DEBUG_MODE


class SpriteRenderer(Component):
    image: pg.Surface | None
    color: pg.Color
    flip_x: bool
    flip_y: bool
    pivot: Vector2

    sprite_sheet: pg.Surface | None
    sprite_size: tuple[int, int] | None
    sprite_index: tuple[int, int] | None

    animation_frames: list[tuple[int, int]] | None
    animation_duration: float | None
    loop: bool

    _path: str
    _current_frame: int
    _animation_timer: float

    def __init__(
        self,
        path: str,
        color: pg.Color = pg.Color(255, 255, 255),
        flip_x: bool = False,
        flip_y: bool = False,
        pivot: Vector2 | tuple[float, float] | str = (0.5, 0.5),
        sprite_size: tuple[int, int] | None = None,
        sprite_index: tuple[int, int] | None = None,
        animation_frames: list[tuple[int, int]] | None = None,
        animation_duration: float | None = None,
        loop: bool = True
    ) -> None:
        super().__init__()

        # Validate and set image path
        if not path:
            raise ValueError("Image path cannot be empty")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Image file not found at {path}")
        self._path = path

        # Sprite and animation state
        self.image = None
        self.sprite_sheet = None
        self.sprite_size = sprite_size
        self.sprite_index = sprite_index
        self.animation_frames = animation_frames
        self.animation_duration = animation_duration
        self.loop = loop
        self._current_frame = 0
        self._animation_timer = 0.0

        # Visual properties
        self.color = color
        self.flip_x = flip_x
        self.flip_y = flip_y

        # Pivot validation and assignment
        self.pivot = self._validate_pivot(pivot)

    @property
    def width(self) -> int:
        """Get the width of the sprite."""

        if self.image:
            transform = self.parent.get_component(Transform)
            return int(self.image.get_width() * transform.scale.x)
        return 0

    @property
    def height(self) -> int:
        """Get the height of the sprite."""
        
        if self.image:
            transform = self.parent.get_component(Transform)
            return int(self.image.get_height() * transform.scale.y)
        return 0

    @property
    def offset(self) -> Vector2:
        return Vector2(self.width * -(self.pivot.x - 0.5), 
                       self.height * -(self.pivot.y - 0.5))

    def _validate_pivot(self, pivot) -> Vector2:
        """Validate and assign the pivot value."""
        if isinstance(pivot, str):
            if pivot not in PIVOT_POINTS:
                raise ValueError(f"Invalid pivot string: {pivot}. Must be one of {list(PIVOT_POINTS.keys())}.")
            return Vector2(PIVOT_POINTS[pivot])
        elif isinstance(pivot, tuple):
            if len(pivot) != 2:
                raise ValueError("Pivot tuple must be of length 2.")
            return Vector2(pivot)
        elif isinstance(pivot, Vector2):
            return pivot
        else:
            raise TypeError("Pivot must be a Vector2, tuple of two floats, or a valid pivot string.")

    def _extract_sprite(self, index_x: int, index_y: int) -> pg.Surface:
        """Extract a sprite from the sprite sheet at the given indices."""

        sprite_w, sprite_h = self.sprite_size
        rect = pg.Rect(index_x * sprite_w, index_y * sprite_h, sprite_w, sprite_h)
        sprite = self.sprite_sheet.subsurface(rect).copy()
        sprite.fill(self.color, special_flags=pg.BLEND_RGBA_MULT)
        return sprite

    def _set_initial_image(self) -> None:
        """Set the initial image based on sprite/animation settings."""

        if self.sprite_size and self.animation_frames:
            index_x, index_y = self.animation_frames[0]
            self.image = self._extract_sprite(index_x, index_y)
        elif self.sprite_size and self.sprite_index:
            index_x, index_y = self.sprite_index
            self.image = self._extract_sprite(index_x, index_y)
        else:
            self.image = self.sprite_sheet.copy()
            self.image.fill(self.color, special_flags=pg.BLEND_RGBA_MULT)

    def start(self) -> None:
        """Load the image from the specified path. If using a sprite sheet,
        extract the correct sprite or animation frame."""

        transform = self.parent.get_component(Transform)
        if transform is None:
            raise RuntimeError("SpriteRenderer requires a Transform component on the owner.")

        try:
            print(f"Loading image from {self._path}")
            self.sprite_sheet = pg.image.load(self._path).convert_alpha()
            self._set_initial_image()
        except pg.error as e:
            raise RuntimeError(f"Failed to load image at {self._path}: {e}")

    def update(self, dt: float) -> None:
        """Update the animation frame based on delta time (dt in seconds)."""

        if self.animation_frames and self.animation_duration and self.sprite_sheet and self.sprite_size:
            self._animation_timer += dt
            frame_duration = self.animation_duration / len(self.animation_frames)
            while self._animation_timer >= frame_duration:
                self._animation_timer -= frame_duration
                self._current_frame += 1
                if self._current_frame >= len(self.animation_frames):
                    if self.loop:
                        self._current_frame = 0
                    else:
                        self._current_frame = len(self.animation_frames) - 1
            # Update the image to the current frame
            index_x, index_y = self.animation_frames[self._current_frame]
            self.image = self._extract_sprite(index_x, index_y)

    def _get_transformed_image(self, image: pg.Surface, transform: Transform) -> tuple[pg.Surface, pg.Rect, Vector2]:
        """Apply flipping, scaling, and rotation to the image and
        return the transformed image, rect, and offset."""

        # Apply flipping if necessary
        image = pg.transform.flip(image, self.flip_x, self.flip_y)

        # Scale the image based on the transform's scale
        image = pg.transform.scale(image, (self.width, self.height))

        # Rotate the image around the pivot point
        rotated_image = pg.transform.rotate(image, -transform.rotation)
        rotated_offset = self.offset.rotate(transform.rotation)
        # rect = rotated_image.get_rect(center=position + offset + rotated_offset)

        # We are doing this because rect coordinates are integer-based,
        # while we want to use floating-point for more precise positioning
        width, height = rotated_image.get_size()
        center = Vector2(width / 2, height / 2)
        position = transform.screen_position + rotated_offset - center

        return rotated_image, position

    def draw(self, surface: pg.Surface) -> None:
        """Draw the sprite on the given surface, applying flipping,
        scaling, rotation, and pivot alignment."""

        if self.image is None:
            raise RuntimeError("SpriteRenderer image not loaded.")

        transform = self.parent.get_component(Transform)
        rotated_image, pos = self._get_transformed_image(self.image, transform)
        surface.blit(rotated_image, pos)

        if DEBUG_MODE:
            debug_pos = transform.screen_position + Vector2(0, 30)

            font = pg.font.Font(None, 16)
            path_text = font.render(f"path: {self._path}", True, (0, 255, 0))
            flip_text = font.render(f"flip X: {self.flip_x}, flip Y: {self.flip_y}", True, (0, 255, 0))
            animation_text = font.render(
                f"frame: {self._current_frame + 1}/{len(self.animation_frames) if self.animation_frames else 1}",
                True, (0, 255, 0)
            )

            surface.blit(path_text, debug_pos)
            surface.blit(flip_text, debug_pos + Vector2(0, 10))
            surface.blit(animation_text, debug_pos + Vector2(0, 20))

    def __repr__(self) -> str:
        return (
            f"<{super().__repr__()} path={self._path}, color={self.color}, flip_x={self.flip_x}, "
            f"flip_y={self.flip_y}, pivot={self.pivot}, sprite_size={self.sprite_size}, "
            f"sprite_index={self.sprite_index}, animation_frames={self.animation_frames}, "
            f"animation_speed={self.animation_duration}, loop={self.loop}>"
        )