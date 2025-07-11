import pygame as pg
from pygame.math import Vector2

from .game_object import GameObject
from .components.transform import Transform


class Camera:
    position: Vector2
    viewport: pg.Rect
    target: GameObject | None
    offset: Vector2
    smooth: bool
    smooth_speed: float

    def __init__(self, x: float = 0, y: float = 0, width: int = 800, height: int = 600) -> None:
        """Initialize the Camera with a position and viewport size.

        Args:
            x (float, optional): The initial X position of the camera. Defaults to 0
            y (float, optional): The initial Y position of the camera. Defaults to 0
            width (int, optional): The width of the camera viewport. Defaults to 800.
            height (int, optional): The height of the camera viewport. Defaults to 600.
        """
        
        self.position = Vector2(x, y)
        self.viewport = pg.Rect(x, y, width, height)
        self.target = None
        self.offset = Vector2(0, 0)
        self.smooth = False
        self.smooth_speed = 10

    def set_target(self, target: GameObject, smooth: bool = False, smooth_speed: float = 10, offset: Vector2 = (0, 0)) -> None:
        """Set the target GameObject for the camera to follow.

        Args:
            target (GameObject): The GameObject to follow.
            smooth (bool, optional): Whether to smoothly follow the target. Defaults to False.
            smooth_speed (float, optional): The speed of the smooth follow. Defaults to 10.
            offset (Vector2 | tuple[float, float], optional): The offset from the target's position. Defaults to (0, 0).
        """
        
        self.target = target
        self.offset = Vector2(offset)
        self.smooth = smooth
        self.smooth_speed = smooth_speed

    def update(self, dt: float) -> None:
        """Update the camera position based on the target's position or smooth follow.

        Args:
            dt (float): The delta time since the last update.
        """

        self.viewport.size = pg.display.get_surface().get_size()

        if not self.target:
            return
        
        target_transform = self.target.get_component(Transform)
        if not target_transform:
            return

        if self.smooth:
            # Smooth follow with interpolation
            direction = target_transform.position - self.position + self.offset
            self.position += direction * (self.smooth_speed * dt)
        else:
            # Direct follow
            self.position = Vector2(target_transform.position) + self.offset

    def world_to_screen(self, world_pos: Vector2) -> Vector2:
        """Convert world coordinates to screen coordinates.

        Args:
            world_pos (Vector2): The world position to convert.
        Returns:
            Vector2: The screen position corresponding to the world position.
        """
        
        # Calculate relative position to camera
        rel_pos = Vector2(world_pos) - self.position
        
        # Apply zoom
        # rel_pos *= self.zoom
        
        # Center on screen
        return rel_pos + Vector2(self.viewport.width / 2, self.viewport.height / 2)

    def screen_to_world(self, screen_pos: Vector2) -> Vector2:
        """Convert screen coordinates to world coordinates.

        Args:
            screen_pos (Vector2): The screen position to convert.
        Returns:
            Vector2: The world position corresponding to the screen position.
        """
        
        # Reverse of world_to_screen
        rel_pos = Vector2(screen_pos) - Vector2(self.viewport.width / 2, self.viewport.height / 2)
        
        # Apply inverse zoom
        # rel_pos /= self.zoom
        
        # Offset by camera position
        return rel_pos + self.position