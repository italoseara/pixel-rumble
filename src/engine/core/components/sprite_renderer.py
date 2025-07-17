from __future__ import annotations

import os
import pygame as pg
import logging
from typing import override
from pygame.math import Vector2

from .component import Component
from .transform import Transform
from ...util import validate_pivot
from ...constants import DEBUG_MODE
from ...spritesheet import SpriteSheet


class SpriteRenderer(Component):
    color: pg.Color
    flip_x: bool
    flip_y: bool
    pivot: Vector2

    sprite_sheet: SpriteSheet | None
    sprite_size: tuple[int, int] | None
    sprite_index: tuple[int | str, int | str] | None

    animation_frames: list[tuple[int | str, int | str]] | None
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
        grid_size: tuple[int, int] | None = None,
        sprite_index: tuple[int | str, int | str] | None = None,
        animation_frames: list[tuple[int | str, int | str]] | None = None,
        animation_duration: float | None = None,
        loop: bool = True
    ) -> None:
        """Initialize the SpriteRenderer component.

        Args:
            path (str): Path to the image file or sprite sheet.
            color (pg.Color, optional): Color filter for the image. Defaults to pg.Color(255, 255, 255).
            flip_x (bool, optional): Flip the image in the X axi. Defaults to False.
            flip_y (bool, optional): Flip the image in the Y axis. Defaults to False.
            pivot (Vector2 | tuple[float, float] | str, optional): The pivot point of the image. Defaults to (0.5, 0.5).
            sprite_size (tuple[int, int], optional): The size of the sprite image. Defaults to None.
            sprite_index (tuple[int, int], optional): The index of the sprite in the spritesheet. Defaults to None.
            animation_frames (list[tuple[int, int]], optional): A list of indexes for each frame of the animation. Defaults to None.
            animation_duration (float, optional): The total duration of the animation in seconds. Defaults to None.
            loop (bool, optional): Whether the animation should loop. Defaults to True.

        Raises:
            ValueError: If the image path is empty or invalid.
            FileNotFoundError: If the image file does not exist at the specified path.
            TypeError: If the pivot is not a Vector2, tuple, or valid string.
            RuntimeError: If the SpriteRenderer requires a Transform component on the owner.
            ValueError: If the pivot string is invalid.
        """
        
        super().__init__()

        # Validate and set image path
        if not path:
            raise ValueError("Image path cannot be empty")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Image file not found at {path}")
        self._path = path

        # Sprite and animation state
        self.sprite_sheet = None
        self.sprite_size = grid_size
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
        self.pivot = validate_pivot(pivot)

    @property
    def width(self) -> int:
        """Get the width of the current sprite."""

        sprite = self._get_current_sprite()
        if sprite:
            transform = self.parent.get_component(Transform)
            return int(sprite.get_width() * transform.scale.x)
        return 0

    @property
    def height(self) -> int:
        """Get the height of the current sprite."""

        sprite = self._get_current_sprite()
        if sprite:
            transform = self.parent.get_component(Transform)
            return int(sprite.get_height() * transform.scale.y)
        return 0

    @property
    def offset(self) -> Vector2:
        """Calculate the offset based on the pivot point."""

        return Vector2(self.width * -(self.pivot.x - 0.5), 
                       self.height * -(self.pivot.y - 0.5))

    def _get_current_sprite(self) -> pg.Surface | None:
        if not self.sprite_sheet:
            return None

        if self.animation_frames and self.sprite_size:
            index_x, index_y = self.animation_frames[self._current_frame]
            return self._extract_sprite(index_x, index_y)
        elif self.sprite_index and self.sprite_size:
            index_x, index_y = self.sprite_index
            return self._extract_sprite(index_x, index_y)
        elif self.sprite_size:
            # fallback: first sprite
            return self._extract_sprite(0, 0)
        else:
            # fallback: full image
            return self.sprite_sheet._spritesheet.copy()

    def _extract_sprite(self, index_x: int | str, index_y: int | str) -> pg.Surface:
        """Extract a sprite using SpriteSheet.get_sprite."""
        
        if not self.sprite_sheet or not self.sprite_size:
            raise RuntimeError("SpriteSheet or sprite_size not set.")

        return self.sprite_sheet.get_sprite((index_x, index_y))

    @override
    def start(self) -> None:
        """Initialize the SpriteRenderer component.

        Raises:
            RuntimeError: If the SpriteRenderer requires a Transform component on the owner.
            RuntimeError: If the image cannot be loaded from the specified path.
        """

        transform = self.parent.get_component(Transform)
        if transform is None:
            raise RuntimeError("SpriteRenderer requires a Transform component on the owner.")

        try:
            if self.sprite_size:
                self.sprite_sheet = SpriteSheet(self._path, self.sprite_size)
            else:
                logging.info(f"[Game] Loading image from {self._path}")
                self.sprite_sheet = SpriteSheet(self._path)
        except pg.error as e:
            raise RuntimeError(f"Failed to load image at {self._path}: {e}")

    @override
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

    @override
    def draw(self, surface: pg.Surface) -> None:
        """Draw the sprite on the given surface.

        Args:
            surface (pg.Surface): The surface to draw the sprite on.
        """

        sprite = self._get_current_sprite()
        if sprite is None:
            raise RuntimeError("SpriteRenderer sprite not loaded.")
        
        transform = self.parent.get_component(Transform)
        
        image = pg.transform.flip(sprite, self.flip_x, self.flip_y)
        image = pg.transform.scale(image, (self.width, self.height))
        
        rotated_image = pg.transform.rotate(image, -transform.rotation)
        rotated_offset = self.offset.rotate(transform.rotation)
        
        width, height = rotated_image.get_size()
        center = Vector2(width / 2, height / 2)
        position = transform.screen_position + rotated_offset - center
        
        surface.blit(rotated_image, position)
        
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