from __future__ import annotations

import os
import pytmx
import pygame as pg
from pygame.math import Vector2
from pytmx.util_pygame import load_pygame
from typing import override

from .transform import Transform
from .component import Component
from .box_collider import BoxCollider
from ..game_object import GameObject
from ...util import validate_pivot


class Tile(pg.sprite.Sprite):
    """A sprite representing a tile in the tilemap."""

    original_image: pg.Surface
    position: Vector2

    def __init__(self, image: pg.Surface, position: Vector2) -> None:
        super().__init__()
        self.image = image
        self.original_image = image
        self.position = position
        self.rect = self.image.get_rect(topleft=position)

    def update(self, transform: Transform, offset: Vector2) -> None:
        """Update the tile's position based on the transform."""

        self.rect.topleft = (
            transform.screen_position.x + (self.position.x * transform.scale.x) - offset.x,
            transform.screen_position.y + (self.position.y * transform.scale.y) - offset.y
        )
        self.image = pg.transform.scale(self.original_image, (
            int(self.original_image.get_width() * transform.scale.x),
            int(self.original_image.get_height() * transform.scale.y)
        ))

class Tilemap(Component):
    """Tilemap component for rendering Tiled maps in Pygame."""

    group: pg.sprite.Group
    data: pytmx.TiledMap

    _colliders: list[GameObject]

    def __init__(
        self,
        path: str,
        pivot: Vector2 | tuple[float, float] | str = (0.5, 0.5)
    ) -> None:
        """Initialize the Tilemap component.

        Args:
            path (str): Path to the Tiled map file (.tmx).
            pivot (Vector2 | tuple[float, float] | str, optional): Pivot point for the tilemap. Defaults to (0.0, 0.0).
        """

        super().__init__()

        if not os.path.isfile(path):
            raise FileNotFoundError(f"Tilemap file '{path}' does not exist.")

        self._colliders = []
        self.group = pg.sprite.Group()
        self.data = load_pygame(path)
        self.pivot = validate_pivot(pivot)

    @property
    def width(self) -> int:
        """Get the width of the tilemap."""

        transform = self.parent.get_component(Transform)
        if not transform:
            raise RuntimeError("Tilemap requires a Transform component on the owner.")

        return int(self.data.width * self.data.tilewidth * transform.scale.x)

    @property
    def height(self) -> int:
        """Get the height of the tilemap."""

        transform = self.parent.get_component(Transform)
        if not transform:
            raise RuntimeError("Tilemap requires a Transform component on the owner.")

        return int(self.data.height * self.data.tileheight * transform.scale.y)

    @property
    def offset(self) -> Vector2:
        """Get the offset of the tilemap based on its pivot."""

        return Vector2(
            self.width * self.pivot.x,
            self.height * self.pivot.y
        )

    @property
    def background_color(self) -> pg.Color:
        """Get the background color of the tilemap."""

        return pg.Color(self.data.background_color) if self.data.background_color else pg.Color(0, 0, 0)

    def get_position(self, x: int, y: int) -> Vector2:
        """Get the position of a tile in the tilemap.

        Args:
            x (int): The x coordinate of the tile.
            y (int): The y coordinate of the tile.
        
        Returns:
            Vector2: The position of the tile in the tilemap.
        """
        
        transform = self.parent.get_component(Transform)
        if not transform:
            raise RuntimeError("Tilemap requires a Transform component on the owner.")

        position = transform.position
        scale = transform.scale

        return Vector2(
            x * scale.x + position.x - self.offset.x,
            y * scale.y + position.y - self.offset.y
        )

    @override
    def start(self) -> None:
        """Initialize the Tilemap component."""

        transform = self.parent.get_component(Transform)
        if not transform:
            raise RuntimeError("Tilemap requires a Transform component on the owner.")

        collider_layer = self.data.get_layer_by_name("Collider")

        for layer in self.data.visible_layers:
            if not isinstance(layer, pytmx.TiledTileLayer):
                continue

            for x, y, surface in layer.tiles():
                if not surface:
                    continue

                opacity = layer.opacity
                if opacity < 1.0:
                    surface = surface.copy()
                    surface.set_alpha(int(opacity * 255))

                sprite = Tile(surface, Vector2(x * self.data.tilewidth, y * self.data.tileheight))
                self.group.add(sprite)

        if not collider_layer:
            return
        
        for obj in collider_layer:
            obj: pytmx.TiledObject

            x, y = obj.x, obj.y
            width, height = obj.width, obj.height
            is_trigger = obj.properties.get("is_trigger", False)

            if not (width and height):
                continue

            collider = GameObject(name=f"{self.parent.name} (Collider {obj.id})")
            collider.add_component(Transform(position=self.get_position(x, y)))
            collider.add_component(BoxCollider(width=width * transform.scale.x, height=height * transform.scale.y, is_trigger=is_trigger))
            self.parent.scene.add(collider)

            self._colliders.append(collider)

    @override
    def draw(self, surface: pg.Surface) -> None:
        """Draw the tilemap on the given surface."""

        transform = self.parent.get_component(Transform)
        if not transform:
            raise RuntimeError("Tilemap requires a Transform component on the owner.")

        group = self.group.copy()
        group.update(transform, self.offset)
        group.draw(surface)

    @override
    def destroy(self):
        """Destroy the Tilemap component and its colliders."""

        for collider in self._colliders:
            collider.destroy()

        self._colliders.clear()
        self.group.empty()

        super().destroy()