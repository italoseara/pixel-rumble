import pygame as pg

from .game import Game
from .camera import Camera
from .game_object import GameObject


class Scene:
    camera: Camera
    transparent: bool
    background_color: pg.Color

    _game: Game
    _game_objects: list[GameObject]
    
    def __init__(self) -> None:
        self.camera = Camera()
        self.transparent = False
        self.background_color = pg.Color(0, 0, 0, 0)

        self._game = None
        self._game_objects = []

    def add(self, game_object: GameObject) -> None:
        """Add a GameObject to the scene."""
        
        if not isinstance(game_object, GameObject):
            raise TypeError("Expected a GameObject instance")

        self._game_objects.append(game_object)
        game_object._scene = self

    def start(self) -> None:
        """Called once when the scene is pushed."""
        pass

    def pause(self) -> None:
        """Called when another scene is pushed over this one."""
        pass

    def resume(self) -> None:
        """Called when this scene becomes top most again."""
        pass

    def stop(self) -> None:
        """Called when the scene is popped or replaced."""
        pass

    def _handle_event(self, event: pg.event.Event) -> None:
        """Forward the event to all game objects."""

        for game_object in self._game_objects:
            game_object.handle_event(event)

    def _update(self, dt: float) -> None:
        """Forward the update call to all game objects."""
        
        for game_object in self._game_objects:
            game_object.update(dt)

        self.camera.update(dt)
            

    def _draw(self, surface: pg.Surface) -> None:
        """Forward the draw call to all game objects."""

        surface.fill(self.background_color)

        for game_object in self._game_objects:
            game_object.draw(surface)