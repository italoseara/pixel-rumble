from typing import override

from engine import (
    GameObject, 
    Tilemap, 
    Scene, 
    Transform,
    RigidBody,
    SpriteRenderer,
    BoxCollider,
    Canvas,
)
from engine.ui import Image, Text
from ..scripts import PlayerController

        
class LobbyScene(Scene):
    player_name: str

    def __init__(self, name: str) -> None:
        super().__init__()

        self.player_name = name
    
    @override
    def start(self) -> None:
        map_object = GameObject("Map")
        map_object.add_component(Transform(x=0, y=-100, scale=2.5))
        tilemap = map_object.add_component(Tilemap("assets/maps/mapatestemario.tmx", pivot="center"))
        self.add(map_object)

        ui = GameObject("UI")
        canvas = ui.add_component(Canvas())
        canvas.add(Image(
            "assets/img/background/vignette.png",
            x=0, y=0,
            width="100%", height="100%",
            pivot="topleft",
            opacity=0.4
        ))
        self.add(ui)

        player = GameObject("Player")
        player.add_component(Transform(x=0, y=-100, z_index=1, scale=5))
        player.add_component(SpriteRenderer(
            "assets/img/players.png", 
            pivot="midbottom",
            grid_size=(8, 8),
            sprite_index=(0, 0)
        ))
        
        player.add_component(BoxCollider(width=30))
        player.add_component(RigidBody(drag=0.07, gravity=15))
        player.add_component(PlayerController())
        player_canvas = player.add_component(Canvas())
        player_canvas.add(Text(
            self.player_name,
            x=0, y=-45,
            pivot="midbottom",
            color=(255, 255, 255),
            font_size=18
        ))
        
        self.add(player)

        self.background_color = tilemap.background_color
        self.camera.set_target(player, smooth=True, smooth_speed=10, offset=(0, -100))