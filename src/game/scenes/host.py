import pygame as pg
from typing import override

from engine import Scene, GameObject, Canvas, Game
from engine.ui import Text, Button, InputField

class HostMenu(Scene):
    @override
    def start(self) -> None:
        self.transparent = True
        self.background_color = pg.Color(0, 0, 0, 128)

        ui = GameObject("UI")
        canvas = ui.add_component(Canvas())

        canvas.add(Text(
            "DIGITE A PORTA",
            x="50%", y="40%",
            pivot="center",
        ))

        input_field = canvas.add(InputField(
            placeholder="25565",
            x="50%", y="50%",
            width=250, height=48,
            pivot="center",
            max_char=5,
            allowed_type=int,
        ))

        canvas.add(Button(
            "CRIAR PARTIDA",
            x="50%", y="65%",
            pivot="center",
            on_click=lambda: print(input_field.text)
        ))

        canvas.add(Button(
            text="< VOLTAR",
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