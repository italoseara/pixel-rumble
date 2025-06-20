from __future__ import annotations

import pygame as pg
from typing import Type, TypeVar, TYPE_CHECKING

from .components.component import Component
if TYPE_CHECKING:
    from .scene import Scene


T = TypeVar("T", bound=Component)

class GameObject:
    name: str
    active: bool  # skip update/draw if False
    visible: bool  # skip draw if False
    parent: GameObject | None

    _scene: "Scene" | None
    _components: dict[Type[Component], Component]

    _all: dict[str, GameObject] = {}

    def __init__(self, name: str, parent: GameObject | None = None) -> None:
        if not name:
            raise ValueError("GameObject name cannot be empty")
        if name in GameObject._all:
            raise ValueError(f"GameObject with name {name} already exists")
        
        self.name = name
        self.active = True
        self.visible = True
        self.parent = parent

        self._scene = None
        self._components = {}

        GameObject._all[name] = self

    @classmethod
    def find(cls, name: str) -> GameObject | None:
        """Finds a GameObject by name."""
        
        return cls._all.get(name, None)

    def add_component(self, component: T) -> T:
        """Adds a component to the GameObject."""
        
        if not isinstance(component, Component):
            raise TypeError(f"Expected a Component, got {type(component).__name__}")

        ctype = type(component)
        if ctype in self._components:
            raise ValueError(f"Component {ctype.__name__} already exists in GameObject {self.name}")

        component.parent = self
        self._components[ctype] = component
        component.start()
        return component

    def get_component(self, ctype: Type[T]) -> T | None:
        """Returns the first component of the specified type."""
        
        return self._components.get(ctype, None)

    def remove_component(self, ctype: Type[Component]) -> bool:
        """Removes the first component of the specified type."""
        
        comp = self._component_map.pop(ctype, None)
        return comp is not None

    def update(self, dt: float) -> None:
        """Forward the update call to each component."""
        
        if not self.active:
            return
        
        for comp in list(self._components.values()):
            comp.update(dt)

    def draw(self, surface: pg.Surface) -> None:
        """Forward the draw call to each component."""
        
        if not self.visible or not self.active:
            return
        
        for comp in list(self._components.values()):
            comp.draw(surface)

    def handle_event(self, event: pg.event.Event) -> None:
        """Forward the event to each component."""
        
        if not self.active:
            return
        
        for comp in list(self._components.values()):
            comp.handle_event(event)

    def destroy(self) -> None:
        """Clean up the GameObject and its components."""
        
        for comp in list(self._components):
            comp.parent = None
            comp.destroy()
            del self._components[type(comp)]
            
        self._components.clear()
        self.name = ""
        self.active = False
        self.visible = False

        if self.name in GameObject._all:
            del GameObject._all[self.name]

    def has_component(self, ctype: Type[Component]) -> bool:
        return ctype in self._component_map

    def __repr__(self) -> str:
        return f"<GameObject {self.name!r} active={self.active} visible={self.visible} components={list(self._components.keys())}>"