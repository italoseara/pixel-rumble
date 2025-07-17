import pygame as pg
from typing import override

from connection.client import Client
from engine import Scene, GameObject, Canvas, Game
from engine.ui import Button, InputField, Text


class DirectConnectionMenu(Scene):
    @override
    def start(self) -> None:
        self.transparent = True
        self.background_color = pg.Color(0, 0, 0, 160)

        ui = GameObject("UI")
        canvas = ui.add_component(Canvas())

        canvas.add(Text(
            "CONEXÃO DIRETA",
            x="50%", y="20%",
            pivot="center",
            font_size=70,
        ))

        canvas.add(InputField(
            placeholder="SEU NOME",
            x="50%", y="40%",
            width=350, height=48,
            pivot="center",
            max_char=15,
        ))

        canvas.add(InputField(
            placeholder="IP",
            x="50%", y="50%",
            width=350, height=48,
            pivot="center",
            max_char=20,
        ))

        canvas.add(InputField(
            placeholder="PORTA",
            x="50%", y="60%",
            width=350, height=48,
            pivot="center",
            max_char=5,
            allowed_type=int,
        ))

        canvas.add(Button(
            "ENTRAR >",
            x="96%", y="90%",
            pivot="midright",
            font_size=42,
            on_click=lambda: self.connect()
        ))

        canvas.add(Button(
            "< VOLTAR",
            x="5%", y="-10%",
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

    def connect(self) -> None:
        """Connect to the server using the provided IP and port."""

        name = self.find("UI").get_component(Canvas).get(InputField)[0].text
        ip = self.find("UI").get_component(Canvas).get(InputField)[1].text
        port = self.find("UI").get_component(Canvas).get(InputField)[2].value

        Game.instance().client = Client(name=name, server_ip=ip, server_port=port)
        Game.instance().client.start()