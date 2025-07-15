import pygame as pg
from typing import override

from engine import Scene, GameObject, Canvas, Game
from engine.ui import Button, InputField, Text


class JoinServerMenu(Scene):
    def __init__(self, ip: str = None, port: int = None) -> None:
        super().__init__()

        self.ip = ip
        self.port = port
    
    @override
    def start(self) -> None:
        self.transparent = True
        self.background_color = pg.Color(0, 0, 0, 160)

        ui = GameObject("UI")
        canvas = ui.add_component(Canvas())

        canvas.add(Text(
            "ENTRAR NA SALA",
            x="50%", y="20%",
            pivot="center",
            font_size=70,
        ))

        canvas.add(InputField(
            placeholder="SEU NOME",
            x="50%", y="50%",
            width=350, height=48,
            pivot="center",
            max_char=15,
        ))

        canvas.add(Button(
            "ENTRAR >",
            x="96%", y="90%",
            pivot="midright",
            font_size=42,
            on_click=lambda: print(canvas.get(InputField)[0].text)
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