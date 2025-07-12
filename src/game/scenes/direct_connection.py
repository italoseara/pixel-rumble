import pygame as pg
from pygame.math import Vector2
from typing import override
import time as tm

from engine import Scene, GameObject, Canvas, Game
from engine.ui import Button, InputField, Image, UIComponent, Text
from engine.constants import DEFAULT_FONT, DEBUG_MODE


class DirectConnection(Scene):
    @override
    def start(self) -> None:
        self.transparent = False
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
            "CONEXÃO DIRETA",
            x="50%", y="30%",
            pivot="center",
            font_size=48,
        ))

        canvas.add(InputField(
            placeholder="nickname",
            x="50%", y="40%",
            width=250, height=48,
            pivot="center",
            max_char=15,
        ))

        canvas.add(InputField(
            placeholder="IP",
            x="50%", y="50%",
            width=250, height=48,
            pivot="center",
            max_char=9,
        ))

        canvas.add(InputField(
            placeholder="PORTA",
            x="50%", y="60%",
            width=250, height=48,
            pivot="center",
            max_char=5,
            allowed_type=int,
        ))

        canvas.add(Button(
            "ENTRAR >",
            x="50%", y="90%",
            pivot="center",
            font_size=42,
            on_click=lambda: print("Entrar na sala")
        ))

        canvas.add(Button(
            "< VOLTAR",
            x="5%", y="10%",
            pivot="midleft",
            font_size=42,
            on_click=lambda: Game.instance().pop_scene()
        ))

        self.add(ui)

    @override
    def handle_event(self, event: pg.event.Event) -> None:
        """Handle an event by forwarding it to all game objects.

        Args:
            event (pg.event.Event): The event to handle.
        """

        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            Game.instance().pop_scene()