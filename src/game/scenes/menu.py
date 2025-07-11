import pygame as pg
from typing import override

from .host import HostMenu
from .credits import CreditsMenu


from engine import Scene, GameObject, Canvas, Game
from engine.ui import Image, Button


class MainMenu(Scene):
    @override
    def start(self) -> None:
        self.background_color = pg.Color(54, 78, 109, 255)

        ui = GameObject("UI")
        canvas = ui.add_component(Canvas())
        canvas.add(Image(
            "assets/img/background/texture.png",
            x=0, y=0,
            width="100%", height="100%",
            pivot="topleft",
            opacity=0.25
        ))

        canvas.add(Image(
            "assets/img/logo.png", 
            x="0%", y="25%", 
            pivot="midleft",
            width=350, height=350, 
        ))

        canvas.add(Button(
            "ENTRAR",
            x="5%", y="65%",
            font_size=60,
            pivot="midleft",
            on_click=lambda: print("Join button clicked!"),
        ))
        canvas.add(Button(
            "CRIAR SALA",
            x="5%", y="75%",
            font_size=60,
            pivot="midleft",
            on_click=lambda: Game.instance().push_scene(HostMenu())
        ))
        canvas.add(Button(
            "CRÉDITOS",
            x="5%", y="85%",
            font_size=60,
            pivot="midleft",
            on_click=lambda: Game.instance().push_scene(CreditsMenu()),
        ))

        canvas.add(Image(
            "assets/img/background/menu.png",
            x=0, y=0,
            width="100%", height="100%",
            pivot="topleft",
        ))

        canvas.add(Image(
            "assets/img/background/vignette.png",
            x=0, y=0,
            width="100%", height="100%",
            pivot="topleft",
            opacity=0.2
        ))

        self.add(ui)
