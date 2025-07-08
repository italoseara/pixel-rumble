import pygame as pg
from typing import override

from engine import Scene, GameObject, Canvas
from engine.ui import Image


class MainMenu(Scene):

    @override
    def start(self) -> None:
        self.background_color = pg.Color(54, 78, 109, 255)
        
        ui = GameObject("UI")
        canvas = ui.add_component(Canvas())
        canvas.add(Image(
            "assets/img/logo.png", 
            x="50%", y="25%", 
            width=350, height=350, 
            pivot="center"
        ))
        canvas.add(Image(
            "assets/img/vignette.png",
            x=0, y=0,
            width="100%", height="100%",
            pivot="topleft",
            opacity=0.2
        ))

        self.add(ui)

    @override
    def draw(self, surface: pg.Surface) -> None:
        pass