import pygame as pg
from typing import override

from engine import Scene, GameObject, Canvas, Game
from engine.ui import Text, Button, InputField, Image


class JoinMenu(Scene):
    @override
    def start(self) -> None:
        self.transparent = True
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
            "assets/img/background/creditos.png",
            x=0, y=0,
            width="100%", height="100%",
            pivot="topleft",
            opacity=1.0
        ))

        canvas.add(Image(
            "assets/img/background/vignette.png",
            x=0, y=0,
            width="100%", height="100%",
            pivot="topleft",
            opacity=0.4
        ))

        canvas.add(Text(
            "DIGITE O NICKNAME",
            x="50%", y="10%",
            pivot="center",
        ))

        canvas.add(InputField(
            placeholder="nickname",
            x="50%", y="20%",
            width=250, height=48,
            pivot="center",
            max_char=15,
        ))

        canvas.add(Button(
            "< VOLTAR",
            x="5%", y="-10%",
            pivot="midleft",
            font_size=42,
            on_click=lambda: Game.instance().pop_scene()
        ))

        canvas.add(Button(
            "ENTRAR >",
            x="-15%", y="-10%",
            pivot="center",
            font_size=42,
            on_click=lambda: print("Joining game...")
        ))

        self.add(ui)