import pygame as pg
from typing import override

from engine import Scene, GameObject, Canvas
from engine.ui import Text, Button, InputField

class HostMenu(Scene):
    @override
    def start(self) -> None:
        self.transparent = True
        self.background_color = pg.Color(0, 0, 0, 80)

        ui = GameObject("UI")
        canvas = ui.add_component(Canvas())

        canvas.add(Button(
            "X",
            x="-2%", y="2%",
            pivot="topright",
            font_size=32,
            on_click=lambda: self._game.pop_scene(),
        ))

        canvas.add(Text(
            "ENTER PORT",
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
            "HOST GAME",
            x="50%", y="62%",
            pivot="center",
            on_click=lambda: print(input_field.text)
        ))

        self.add(ui)

    @override
    def handle_event(self, event: pg.event.Event) -> None:
        """Handle an event by forwarding it to all game objects.

        Args:
            event (pg.event.Event): The event to handle.
        """

        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self._game.pop_scene()