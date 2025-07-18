from __future__ import annotations

import pygame as pg
from pygame.math import Vector2
from typing import TypeVar, override

from .component import Component
from ...ui.component import UIComponent


T = TypeVar("T", bound=UIComponent)

class Canvas(Component):
    _components: list[UIComponent]

    def __init__(self) -> None:
        """Initialize the Canvas component.

        The Canvas is a container for UI components and handles their updates, events, and drawing.
        """
        
        super().__init__()
        self._components = []

    def add(self, component: T) -> T:
        self._components.append(component)
        component.parent = self
        component.start()
        return component

    @override
    def update(self, dt: float) -> None:
        for component in self._components:
            if component.active:
                component.update(dt)

    @override
    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = Vector2(pg.mouse.get_pos())
            for component in reversed(self._components):  # Process from top to bottom
                if component.active and component.is_mouse_over(mouse_pos):
                    component.on_mouse_click(mouse_pos)
        elif event.type == pg.MOUSEBUTTONUP:
            mouse_pos = Vector2(pg.mouse.get_pos())
            for component in reversed(self._components):
                if component.active:
                    component.on_mouse_release(mouse_pos)

        for component in self._components:
            if component.active:
                component.handle_key_event(event)

    @override
    def draw(self, surface: pg.Surface) -> None:
        for component in self._components:
            component.draw(surface)

    @override
    def clone(self) -> Canvas:
        """Create a copy of this Canvas component."""

        new_canvas = Canvas()
        new_canvas.parent = self.parent
        new_canvas._components = [comp.clone() for comp in self._components]
        return new_canvas

    def get(self, component_type: type[T]) -> list[T]:
        """Return a list of components of the specified type."""
        return [comp for comp in self._components if isinstance(comp, component_type)]