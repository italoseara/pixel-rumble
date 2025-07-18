from __future__ import annotations

import pygame as pg
from pygame.math import Vector2
from typing import Literal, override

from .component import UIComponent

class Image(UIComponent):
    _original_image: pg.Surface
    _image: pg.Surface
    _width_is_percent: bool = False
    _height_is_percent: bool = False
    _width_value: int | float | str
    _height_value: int | float | str
    _image_path: str
    _opacity: float

    def __init__(
        self,
        image_path: str,
        x: int | str = 0,
        y: int | str = 0,
        width: int | str | None = None,
        height: int | str | None = None,
        pivot: Vector2 | tuple[float, float] | str = (0.5, 0.5),
        opacity: float = 1.0
    ) -> None:
        """Initialize an Image UI component.

        Args:
            image_path (str): The path to the image file.
            x (int | str, optional): The x position of the image. Can be a percentage of the screen width. Defaults to 0.
            y (int | str, optional): The y position of the image. Can be a percentage of the screen height. Defaults to 0.
            width (int | str | None, optional): The width of the image. Can be a percentage of the screen width. Defaults to None.
            height (int | str | None, optional): The height of the image. Can be a percentage of the screen height. Defaults to None.
            pivot (Vector2 | tuple[float, float] | str, optional): The pivot point of the image. Defaults to (0, 0).
            opacity (float, optional): The opacity of the image (0.0-1.0). Defaults to 1.0.
        """
        self._image_path = image_path
        self._original_image = pg.image.load(image_path).convert_alpha()
        img_width, img_height = self._original_image.get_size()
        self._opacity = max(0.0, min(1.0, opacity))

        # Store width/height as passed for later recalculation
        self._width_value = width if width is not None else img_width
        self._height_value = height if height is not None else img_height
        self._width_is_percent = isinstance(self._width_value, str) and self._width_value.endswith('%')
        self._height_is_percent = isinstance(self._height_value, str) and self._height_value.endswith('%')

        # Calculate initial width/height
        calc_width = self._calculate_dimension(self._width_value, img_width, axis='x')
        calc_height = self._calculate_dimension(self._height_value, img_height, axis='y')
        super().__init__(x=x, y=y, width=calc_width, height=calc_height, pivot=pivot)
        self._update_scaled_image()

    def _calculate_dimension(self, value: int | str, default: int, axis: Literal['x', 'y']) -> int:
        if isinstance(value, str) and value.endswith('%'):
            percent = float(value[:-1]) / 100
            if axis == 'x':
                return int(percent * pg.display.get_surface().get_width())
            else:
                return int(percent * pg.display.get_surface().get_height())
        elif value is None:
            return default
        else:
            return int(value)

    def _update_scaled_image(self) -> None:
        width = self.width
        height = self.height
        img_width, img_height = self._original_image.get_size()
        if (width, height) != (img_width, img_height):
            img = pg.transform.scale(self._original_image, (width, height))
        else:
            img = self._original_image.copy()
        alpha_value = int(self._opacity * 255)
        img.set_alpha(alpha_value)
        self._image = img

    def set_opacity(self, opacity: float) -> None:
        """Set the opacity of the image (0.0-1.0)."""
        self._opacity = max(0.0, min(1.0, opacity))
        self._update_scaled_image()

    @override
    def update(self, dt: float) -> None:
        # Recalculate width/height if they are percent-based
        updated = False
        if self._width_is_percent:
            new_width = self._calculate_dimension(self._width_value, self._original_image.get_width(), axis='x')
            if new_width != self.width:
                self.width = new_width
                updated = True
        if self._height_is_percent:
            new_height = self._calculate_dimension(self._height_value, self._original_image.get_height(), axis='y')
            if new_height != self.height:
                self.height = new_height
                updated = True
        if updated:
            self._update_scaled_image()

    @override
    def draw(self, surface: pg.Surface) -> None:
        if not self.active:
            return
        surface.blit(self._image, self.position)
        super().draw(surface)

    @override
    def clone(self) -> Image:
        """Create a copy of this Image component."""
        new_image = Image(
            image_path=self._image_path,
            x=self._position.x,
            y=self._position.y,
            width=self._width_value,
            height=self._height_value,
            pivot=self.pivot,
            opacity=self._opacity
        )
        new_image._original_image = self._original_image.copy()
        new_image._image = self._image.copy()
        return new_image