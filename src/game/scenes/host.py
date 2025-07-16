import pygame as pg
from typing import override

from connection.client import Client
from connection.server import Server
from engine import Scene, GameObject, Canvas, Game
from engine.ui import Text, Button, InputField


class HostMenu(Scene):
    @override
    def start(self) -> None:
        self.transparent = True
        self.background_color = pg.Color(0, 0, 0, 160)

        ui = GameObject("UI")
        canvas = ui.add_component(Canvas())

        canvas.add(Text(
            "CRIAR SALA",
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
            placeholder="NOME DA SALA",
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
            on_click=lambda: self.open_server()
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
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            Game.instance().pop_scene()

    def open_server(self) -> None:
        """Handle the server operation logic."""
        parent_canvas = self.find("UI").get_component(Canvas)

        name = parent_canvas.get(InputField)[0].text
        room_name = parent_canvas.get(InputField)[1].text
        port = parent_canvas.get(InputField)[2].value

        Game.instance().server = Server(name=room_name, port=port)
        Game.instance().server.start()

        Game.instance().client = Client(name=name, server_ip="localhost", server_port=port)
        Game.instance().client.start()