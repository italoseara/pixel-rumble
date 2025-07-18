import time
from typing import override

from engine import Component, BoxCollider

class BulletController(Component):
    """Controls the bullet's behavior, including movement and collision detection."""

    def __init__(self, lifetime: float) -> None:
        super().__init__()
        self.lifetime = lifetime
        self.start_time = time.time()

    @override
    def update(self, dt: float) -> None:
        """Update the bullet's position and check for lifetime expiration."""
        if time.time() - self.start_time > self.lifetime:
            self.parent.destroy()
            return

        box_collider = self.parent.get_component(BoxCollider)
        if box_collider and box_collider.is_colliding():
            self.parent.destroy()