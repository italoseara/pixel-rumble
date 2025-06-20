import pygame as pg
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game_object import GameObject

class Component:
    """
    Base class for all components. 
    You'll subclass this to create Sprite, PhysicsBody, Script, etc.
    """

    parent: 'GameObject'
    
    def __init__(self):
        pass

    def start(self):
        """Called once when the component is added to a GameObject."""
        pass

    def update(self, dt: float):
        """Called every frame; dt is seconds since last frame."""
        pass

    def draw(self, surface: pg.Surface):
        """Called every frame after update, to render visuals."""
        pass

    def handle_event(self, event: pg.event.Event):
        """Called to handle events like mouse clicks or key presses."""
        pass

    def destroy(self):
        """Called when the component is removed from the GameObject."""
        pass

    def __repr__(self):
        return f"{self.__class__.__name__} parent=\"{self.parent.name}\","