from __future__ import annotations

import pygame as pg
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .scene import Scene
    from connection.client import Client
    from connection.server import Server


class Game:
    width: int
    height: int
    screen: pg.Surface
    clock: pg.time.Clock
    fps: int

    client: Client | None
    server: Server | None

    _scenes: list['Scene']
    _running: bool
    _instance: Game = None

    def __init__(
        self,
        title: str,
        width: int = 800,
        height: int = 600,
        fps: int = 60,
        icon: str = None
    ) -> None:
        """Initialize the Game instance.

        Args:
            title (str): The title of the game window.
            width (int, optional): The width of the game window. Defaults to 800.
            height (int, optional): The height of the game window. Defaults to 600.
            fps (int, optional): The frames per second for the game loop. Defaults to 60.
            icon (str, optional): Path to the icon image file. Defaults to None.
        Raises:
            RuntimeError: If an instance of Game already exists.
        """
        
        if Game._instance is not None:
            raise RuntimeError("Game instance already exists.")
        Game._instance = self

        self.width = width
        self.height = height
        self.fps = fps
        self._running = False

        pg.init()
        pg.display.set_caption(title)
        if icon:
            pg.display.set_icon(pg.image.load(icon))

        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()

        self._scenes = []

        self.client = None
        self.server = None

    @classmethod
    def instance(cls) -> Game:
        """Returns the singleton instance of the Game class."""
        
        if cls._instance is None:
            raise RuntimeError("Game instance has not been created yet.")
        return cls._instance

    @property
    def current_scene(self) -> "Scene":
        """Returns the current scene or None if no scenes are available."""
        
        if not self._scenes:
            return None
        return self._scenes[-1]

    def clear_scenes(self) -> None:
        """Clear all scenes from the stack."""
        
        while self._scenes:
            self._scenes.pop().stop()
        print("[Game] All scenes cleared from stack.")

    def push_scene(self, scene: "Scene") -> None:
        """Pause current and push a new one on top.

        Args:
            scene (Scene): The scene to push onto the stack.
        """
        
        if self.current_scene:
            self.current_scene.pause()

        scene._game = self
        self._scenes.append(scene)
        scene.start()

        print(f"[Game] Scene {type(scene).__name__} pushed onto stack. Total scenes: {len(self._scenes)}")

    def pop_scene(self) -> None:
        """End current scene and resume the one below."""
        
        if not self._scenes:
            return
        
        top = self._scenes.pop()
        top.stop()
        if self.current_scene:
            self.current_scene.resume()

        print(f"[Game] Scene {type(top).__name__} popped from stack. Remaining scenes: {len(self._scenes)}")

    def replace_scene(self, scene: "Scene") -> None:
        """Remove current scene, then push the new one.

        Args:
            scene (Scene): The scene to replace the current one with.
        """
        
        self.pop_scene()
        self.push_scene(scene)

        print(f"[Game] Scene replaced with {type(scene).__name__}. Remaining scenes: {len(self._scenes)}")

    def run(self) -> None:
        """Enter the main loop until no scenes remain or quit is called."""

        print(f"[Game] Starting game loop at {self.width}x{self.height} with {self.fps} FPS")
        self.running = True
        while self.running and self.current_scene:
            dt = self.clock.tick(self.fps) / 1000.0  # seconds since last frame

            # 1) Event handling
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                    break
                else:
                    # give scene a chance to consume it
                    self.current_scene._handle_event(event)
            else:
                # 2) Update
                self.current_scene._update(dt)

                # 3) Draw
                def draw_scene(scene: "Scene", surface: pg.Surface) -> None:
                    if scene.transparent and len(self._scenes) > 1:
                        draw_scene(self._scenes[-2], surface)
                    scene._draw(surface)
                self.screen.fill((0, 0, 0))
                draw_scene(self.current_scene, self.screen)
                
                pg.display.flip()

        pg.quit()

    def quit(self) -> None:
        """Exit the main loop and clear all scenes."""
        
        self.running = False
        while self._scenes:
            self._scenes.pop().stop()

        if self.server:
            self.server.stop()
            self.server = None

        if self.client:
            self.client.disconnect()
            self.client = None

    def notify(self, gameObject : str, compType, addType, **kwargs) -> None:
        """Display a notification message in the console."""
        self.current_scene.find(gameObject).get_component(compType).add(addType(**kwargs))
