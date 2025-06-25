import pygame as pg
from pygame.math import Vector2

from engine import *
from engine.ui import Text, Button


class PlayerController(Component):
    def __init__(self, jump_force: float = 800, move_speed: float = 1500) -> None:
        super().__init__()

        self.flip_x = False
        self.jump_force = jump_force  # Adjust jump force as needed
        self.move_speed = move_speed  # Adjust move speed as needed
        self.boost = True
        self.last_boost_time = 0
    
    def start(self) -> None:
        self.flip_x = False
    
    def update(self, dt: float) -> None:
        keys = pg.key.get_pressed()
        transform = self.parent.get_component(Transform)
        rigid_body = self.parent.get_component(RigidBody)

        if keys[pg.K_a]:
            rigid_body.add_force((-self.move_speed, 0))
            self.flip_x = True
        if keys[pg.K_d]:
            rigid_body.add_force((self.move_speed, 0))
            self.flip_x = False
        if (keys[pg.K_SPACE] or keys[pg.K_w]) and rigid_body.is_grounded:
            rigid_body.add_impulse((0, -self.jump_force))
        if keys[pg.K_LSHIFT] and self.boost and self.last_boost_time + 0.5 < pg.time.get_ticks() / 1000:
            impulse_direction = Vector2(-1, 0) if self.flip_x else Vector2(1, 0)
            rigid_body.add_impulse(impulse_direction * self.move_speed)
            self.boost = False
            self.last_boost_time = pg.time.get_ticks() / 1000  # Reset boost timer

        if not self.boost and rigid_body.is_grounded:
            self.boost = True
        
        sprite_renderer = self.parent.get_component(SpriteRenderer)
        if sprite_renderer:
            sprite_renderer.flip_x = self.flip_x

        if transform.y > 1000:
            # Reset position if player falls off the screen
            transform.position = Vector2(0, 25)
            rigid_body.velocity = Vector2(0, 0)
            rigid_body.acceleration = Vector2(0, 0)


class MainScene(Scene):
    def start(self) -> None:
        player = GameObject("Player")
        player.add_component(Transform(x=0, y=20, scale=5))
        player.add_component(SpriteRenderer(
            "assets/img/players.png", 
            pivot="midbottom",
            sprite_size=(8, 8),
            sprite_index=(2, 1),
        ))
        player.add_component(BoxCollider(width=30))
        player.add_component(RigidBody(drag=0.07, gravity=15))
        player.add_component(PlayerController())
        self.add(player)

        platform = GameObject("Platform")
        platform.add_component(Transform(x=-400, y=0, scale=5))
        platform.add_component(BoxCollider(width=800, height=20))
        self.add(platform)

        platform2 = GameObject("Platform2")
        platform2.add_component(Transform(x=50, y=-200, scale=5))
        platform2.add_component(BoxCollider(width=20, height=200))
        self.add(platform2)

        platform3 = GameObject("Platform3")
        platform3.add_component(Transform(x=-300, y=-150, scale=5))
        platform3.add_component(BoxCollider(width=200, height=20))
        self.add(platform3)

        button = GameObject("Button")
        button.add_component(Transform(x=200, y=-100, scale=2))
        button.add_component(SpriteRenderer(
            "assets/img/keyboard/W.png",
            pivot="midbottom",
            sprite_size=(17, 16),
            animation_frames=[(0, 0), (1, 0)],
            animation_duration=1,
            loop=True,
        ))
        button.add_component(BoxCollider())
        self.add(button)

        ui = GameObject("UI")
        canvas = ui.add_component(Canvas())
        canvas.add(Text("Press A/D to move, Space/W to jump", x=10, y=10))
        canvas.add(Button(
            "Click Me", 
            x=10, y=50, 
            size="lg",
            on_click=lambda: print("Button clicked!")
        ))
        self.add(ui)

        self.camera.set_target(player, smooth=True, smooth_speed=10, offset=(0, -100))
        self.background_color = pg.Color(60, 60, 60)  # Sky blue background


def main() -> None:
    game = Game(title="Pixel Rumble - Demo", icon="assets/img/logo.png")
    game.push_scene(MainScene())
    game.run()


if __name__ == "__main__":
    main()