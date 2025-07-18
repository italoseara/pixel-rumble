import pygame as pg
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game_object import GameObject

class Component:
    """Base class for all components."""

    parent: 'GameObject'

    def __init__(self) -> None:
        pass

    def start(self) -> None:
        """Called once when the component is added to a GameObject."""
        pass

    def update(self, dt: float) -> None:
        """Called every frame; dt is seconds since last frame."""
        pass

    def draw(self, surface: pg.Surface) -> None:
        """Called every frame after update, to render visuals."""
        pass

    def handle_event(self, event: pg.event.Event) -> None:
        """Called to handle events like mouse clicks or key presses."""
        pass

    def destroy(self) -> None:
        """Called when the component is removed from the GameObject."""
        pass

    def clone(self) -> 'Component':
        """Create a copy of this component."""
        raise NotImplementedError(f"{self.__class__.__name__} does not implement clone method.")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} parent=\"{self.parent.name}\","