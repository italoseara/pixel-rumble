import pygame as pg
from typing import override

from engine import Component, GameObject, SpriteRenderer, BoxCollider, Game


class CharacterSelector(Component):
    character_index: int
    hint: GameObject
    
    def __init__(self, character_index: int, hint: GameObject) -> None:
        super().__init__()
        self.character_index = character_index
        self.hint = hint

        print(f"[CharacterSelector] Initialized with character index {self.character_index}.")

    @override
    def update(self, dt: float) -> None:
        local_player = self.parent.scene.find("Local Player")

        if not local_player:
            return

        player_collider = local_player.get_component(BoxCollider)
        box_collider = self.parent.get_component(BoxCollider)

        self.hint.active = player_collider.collides_with(box_collider)

    @override
    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_e and self.hint.active:
            local_player = self.parent.scene.find("Local Player")
            if not local_player:
                return

            sprite_renderer = local_player.get_component(SpriteRenderer)
            if not sprite_renderer:
                return

            index = self.character_index % 16
            sprite_renderer.set_index((index % 4, index // 4))

            Game.instance().client.change_character(index)
            print(f"[Game] Character changed to index {index}.")
