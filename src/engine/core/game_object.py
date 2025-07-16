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

    def __init__(self, name: str, parent: GameObject | None = None) -> None:
        """Initialize a GameObject with a name and an optional parent.

        Args:
            name (str): The name of the GameObject.
            parent (GameObject | None): The parent GameObject, if any. Defaults to None
        Raises:
            ValueError: If the name is empty or already exists.
        """
        
        if not name:
            raise ValueError("GameObject name cannot be empty")
        
        self.name = name
        self.active = True
        self.visible = True
        self.parent = parent

        self._scene = None
        self._components = {}

    def add_component(self, component: T) -> T:
        """Adds a component to the GameObject.

        Args:
            component (Component): The component to add.
        Returns:
            T: The added component.
        Raises:
            TypeError: If the component is not an instance of Component.
            ValueError: If a component of the same type already exists in the GameObject.
        """
        
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
        """Returns the first component of the specified type.

        Args:
            ctype (Type[Component]): The type of the component to retrieve.
        Returns:
            T | None: The component if found, otherwise None.
        """
        
        return self._components.get(ctype, None)

    def remove_component(self, ctype: Type[Component]) -> bool:
        """Removes the first component of the specified type.

        Args:
            ctype (Type[Component]): The type of the component to remove.
        Returns:
            bool: True if the component was removed, False if it was not found.
        """
        
        comp = self._component_map.pop(ctype, None)
        return comp is not None

    def update(self, dt: float) -> None:
        """Forward the update call to each component.

        Args:
            dt (float): The time since the last update in seconds.
        """
        
        if not self.active:
            return
        
        for comp in list(self._components.values()):
            comp.update(dt)

    def draw(self, surface: pg.Surface) -> None:
        """Forward the draw call to each component.

        Args:
            surface (pg.Surface): The surface to draw on.
        """
        
        if not self.visible or not self.active:
            return
        
        for comp in list(self._components.values()):
            comp.draw(surface)

    def handle_event(self, event: pg.event.Event) -> None:
        """Forward the event to each component.

        Args:
            event (pg.event.Event): The event to handle.
        """
        
        if not self.active:
            return
        
        for comp in list(self._components.values()):
            comp.handle_event(event)

    def destroy(self) -> None:
        """Clean up the GameObject and its components."""

        for comp in self._components.values():
            comp.parent = None
            comp.destroy()

        self._components.clear()
        self.name = ""
        self.active = False
        self.visible = False

    def has_component(self, ctype: Type[Component]) -> bool:
        """Check if the GameObject has a component of the specified type.

        Args:
            ctype (Type[Component]): The type of the component to check.
        Returns:
            bool: True if the component exists, False otherwise.
        """
        
        return ctype in self._component_map

    def __repr__(self) -> str:
        return f"<GameObject {self.name!r} active={self.active} visible={self.visible} components={list(self._components.keys())}>"