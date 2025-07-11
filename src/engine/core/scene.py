import pygame as pg

from .game import Game
from .camera import Camera
from .game_object import GameObject


class Scene:
    camera: Camera
    transparent: bool
    background_color: pg.Color

    _game: Game
    _game_objects: dict[str, GameObject]
    
    def __init__(self) -> None:
        """Initialize the Scene."""
        
        self.camera = Camera()
        self.transparent = False
        self.background_color = None

        self._game = None
        self._game_objects = {}

    def find(self, name: str) -> GameObject | None:
        """Find a GameObject by name in the scene.

        Args:
            name (str): The name of the GameObject to find.
        
        Returns:
            GameObject | None: The found GameObject or None if not found.
        """
        
        return self._game_objects.get(name, None)

    def add(self, game_object: GameObject) -> None:
        """Add a GameObject to the scene.

        Args:
            game_object (GameObject): The GameObject to add to the scene.
        Raises:
            TypeError: If the provided game_object is not an instance of GameObject.
        """
        
        if not isinstance(game_object, GameObject):
            raise TypeError("Expected a GameObject instance")

        if game_object.name in self._game_objects:
            raise ValueError(f"GameObject with name '{game_object.name}' already exists in the scene")

        self._game_objects[game_object.name] = game_object
        game_object._scene = self

    def start(self) -> None:
        """Called once when the scene is pushed."""
        pass

    def handle_event(self, event: pg.event.Event) -> None:
        """Handle an event by forwarding it to all game objects.

        Args:
            event (pg.event.Event): The event to handle.
        """
        
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
        """Forward the event to all game objects.

        Args:
            event (pg.event.Event): The event to handle.
        """

        for game_object in self._game_objects.values():
            game_object.handle_event(event)

        self.handle_event(event)

    def _update(self, dt: float) -> None:
        """Forward the update call to all game objects.

        Args:
            dt (float): The time since the last update in seconds.
        """
        
        for game_object in self._game_objects.values():
            game_object.update(dt)

        self.camera.update(dt)
            

    def _draw(self, surface: pg.Surface) -> None:
        """Forward the draw call to all game objects.

        Args:
            surface (pg.Surface): The surface to draw on.
        """

        if self.background_color is not None:
            if self.background_color.a < 255 and self.transparent:
                s = pg.Surface(surface.get_size(), pg.SRCALPHA)
                s.fill(self.background_color)
                surface.blit(s, (0, 0))
            else:
                surface.fill(self.background_color)
                

        for game_object in self._game_objects.values():
            game_object.draw(surface)
