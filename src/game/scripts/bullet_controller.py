import time
from typing import override

from engine import Component, BoxCollider
from .player_controller import PlayerController, PlayerAnimation, RigidBody, Transform

class BulletController(Component):
    """Controls the bullet's behavior, including movement and collision detection."""

    def __init__(self, lifetime: float, damage: int) -> None:
        super().__init__()
        self.lifetime = lifetime
        self.damage = damage

        self.start_time = time.time()

    @override
    def update(self, dt: float) -> None:
        """Update the bullet's position and check for lifetime expiration."""
        if time.time() - self.start_time > self.lifetime:
            self.parent.destroy()
            return

        box_collider = self.parent.get_component(BoxCollider)
        if box_collider and (colliding := box_collider.is_colliding()):

            local_player = self.parent.scene.find("Local Player")
            local_player_collider = local_player.get_component(BoxCollider)
            if colliding == local_player_collider:
                player_controller = local_player.get_component(PlayerController)
                rigid_body = local_player.get_component(RigidBody)
                player_transform = local_player.get_component(Transform)
                transform = self.parent.get_component(Transform)

                if not player_controller or not rigid_body or not player_transform or not transform:
                    return

                player_controller.take_damage(self.damage)

                knockback_force = 300
                direction = (player_transform.position - transform.position).normalize()
                rigid_body.add_impulse(direction * knockback_force)

            player_animation = colliding.parent.get_component(PlayerAnimation)
            if player_animation:
                player_animation.play_hit_animation()

            self.parent.destroy()