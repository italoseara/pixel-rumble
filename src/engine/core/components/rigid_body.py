from __future__ import annotations

import pygame as pg
from typing import override
from pygame.math import Vector2

from .component import Component
from .transform import Transform
from .box_collider import BoxCollider
from ...constants import DEBUG_MODE


class RigidBody(Component):
    mass: float
    drag: float
    gravity: float

    # Calculations
    acceleration: Vector2
    velocity: Vector2

    _transform: Transform | None = None
    _collider: BoxCollider | None = None
    
    def __init__(
        self, 
        mass: float = 1, 
        drag: float = 0.05, 
        gravity: float = 10.0,
    ) -> None:
        """Initialize the RigidBody component.

        Args:
            mass (float, optional): The mass of the object. Defaults to 1.
            drag (float, optional): The drag force to be applied in the X axis. Defaults to 0.05.
            gravity (float, optional): The gravity scale to be applied in the Y axis. Defaults to 10.0.
        """
        
        super().__init__()
        
        self.mass = mass
        self.drag = drag
        self.gravity = gravity

        # Calculations
        self.acceleration = Vector2(0.0, 0.0)
        self.velocity = Vector2(0.0, 0.0)

        self._transform = None
        self._collider = None

        self.is_grounded = False

    @override
    def start(self) -> None:
        """Initialize the RigidBody component.

        Raises:
            RuntimeError: If the parent GameObject does not have a Transform or BoxCollider component.
            NotImplementedError: If the parent GameObject has a parent, as RigidBody can only be added to root GameObjects.
        """
        
        if self.parent.parent:
            raise NotImplementedError("RigidBody cannot be added to a GameObject with a parent. It must be a root GameObject.")
        
        # Cache transform and collider for performance
        self._transform = self.parent.get_component(Transform)
        self._collider = self.parent.get_component(BoxCollider)

        if not self._transform:
            raise RuntimeError("RigidBody requires a Transform component on the owner.")
        if not self._collider:
            raise RuntimeError("RigidBody requires a BoxCollider component on the owner.")

    @override
    def update(self, dt: float) -> None:
        """Update the RigidBody component.

        Args:
            dt (float): The delta time since the last update.
        """
        
        # Apply gravity and drag
        self.acceleration += Vector2(0, 100) * self.gravity
        self.velocity.x *= (1 - self.drag)

        # Integrate acceleration
        self.velocity += self.acceleration * dt
        self.acceleration = Vector2(0.0, 0.0)

        # Predict new position
        new_pos = self._transform.world_position + self.velocity * dt
        self.is_grounded = False

        # Gather other colliders
        scene = self.parent.scene
        colliders = [
            obj.get_component(BoxCollider)
            for obj in scene._game_objects.values()
            if obj is not self.parent and obj.get_component(BoxCollider)
        ] if scene else []

        # Move and resolve X collisions
        self._transform.x = new_pos.x
        for collider in colliders:
            if self._collider.collides_with(collider):
                if self.velocity.x > 0:
                    self._transform.x = collider.get_rect().left - self._collider.width - self._collider.offset.x
                elif self.velocity.x < 0:
                    self._transform.x = collider.get_rect().right - self._collider.offset.x
                self.velocity.x = 0

        # Move and resolve Y collisions
        self._transform.y = new_pos.y
        for collider in colliders:
            if self._collider.collides_with(collider):
                if self.velocity.y > 0:
                    self._transform.y = collider.get_rect().top - self._collider.height - self._collider.offset.y
                    self.is_grounded = True
                elif self.velocity.y < 0:
                    self._transform.y = collider.get_rect().bottom - self._collider.offset.y
                self.velocity.y = 0

    @override
    def draw(self, surface) -> None:
        """Draw the RigidBody component for debugging purposes.

        Args:
            surface (pg.Surface): The surface to draw on.
        """
        
        if DEBUG_MODE:
            # Draw velocity vector
            start_pos = self._transform.screen_position
            end_pos = start_pos + self.velocity * 0.05

            pg.draw.line(surface, (0, 255, 0), start_pos, end_pos, 2)

            # Draw acceleration vector
            if self.acceleration.length() > 0:
                acc_end_pos = start_pos + self.acceleration * 0.05
                pg.draw.line(surface, (0, 0, 255), start_pos, acc_end_pos, 2)

            # Draw grounded state
            font = pg.font.Font(None, 16)
            text = font.render(f"Grounded: {self.is_grounded}", True, (0, 255, 0))
            screen_pos = self._collider.get_screen_rect().topleft
            text_rect = text.get_rect(bottomleft=screen_pos)
            surface.blit(text, text_rect)
            
    def add_force(self, force: Vector2) -> None:
        """Accelerates the RigidBody by adding a force.

        Args:
            force (Vector2): The force to be added.
        """
        
        force = Vector2(force)
        self.acceleration += force / self.mass

    def add_impulse(self, impulse: Vector2) -> None:
        """Add an instantaneous impulse to the RigidBody.

        Args:
            impulse (Vector2): The impulse to be added.
        """
        
        impulse = Vector2(impulse)
        self.velocity += impulse / self.mass

    def __repr__(self) -> str:
        return (f"<{super().__repr__()} mass={self.mass} linear_drag={self.drag} "
                f"gravity_scale={self.gravity} is_grounded={self.is_grounded} "
                f"velocity={self.velocity}>")