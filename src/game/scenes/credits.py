import pygame as pg
from typing import override

from engine import Scene, GameObject, Canvas, Game
from engine.ui import Image, Button, Text


class CreditsMenu(Scene):
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
            opacity=0.2
        ))
         
        canvas.add(Image(
            "assets/img/logo.png", 
            x="3%", y="15%", 
            pivot="midleft",
            width=150, height=150, 
        ))
        
        canvas.add(Text(
            "CRÉDITOS",
            x="50%", y="15%",
            font_size=70,
            color=pg.Color("white"),
            pivot="midtop"
        ))
        
        canvas.add(Text("DESENVOLVIMENTO", x="50%", y="29%", font_size=35, pivot="midtop"))
        canvas.add(Text("Italo Seara, Lucas Luige, Mateus Soares", x="50%", y="35%", font_size=25, pivot="midtop"))

        canvas.add(Text("ARTE", x="50%", y="46%", font_size=35, pivot="midtop"))
        canvas.add(Text("Italo Seara, Lucas Luige, Mateus Soares", x="50%", y="52%", font_size=25, pivot="midtop"))

        canvas.add(Text("DESIGN", x="50%", y="63%", font_size=35, pivot="midtop"))
        canvas.add(Text("Italo Seara, Lucas Luige, Mateus Soares", x="50%", y="69%", font_size=25, pivot="midtop"))

        canvas.add(Text("PROFESSOR", x="50%", y="80%", font_size=35, pivot="midtop"))
        canvas.add(Text("Jorge Lima", x="50%", y="86%", font_size=25, pivot="midtop"))
        
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
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            Game.instance().pop_scene()