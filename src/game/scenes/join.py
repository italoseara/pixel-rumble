import pygame as pg
from pygame.math import Vector2
from typing import override, Callable

from engine import Scene, GameObject, Canvas, Game
from engine.ui import Button, InputField, Image, UIComponent
from engine.constants import DEFAULT_FONT, DEBUG_MODE


class ServerListItem(UIComponent):
    name: str
    ip: str
    port: int

    _icon: pg.Surface
    _font: pg.font.Font
    _is_selected: bool

    def __init__(
        self,
        name: str = None,
        ip: str = None, port: int = None,
        x: int | str = 0, y: int | str = 0,
        width: int = 650, height: int = 80,
        pivot: Vector2 | tuple[float, float] | str = (0.0, 0.0)
    ) -> None:
        super().__init__(x, y, width, height, pivot)

        super().__init__(
            x=x, y=y, pivot=pivot,
            width=width, height=height,
        )

        self._is_selected = False
        self._font = pg.font.Font(DEFAULT_FONT, 32)
        self._icon = pg.image.load("assets/img/icons/sword.png").convert_alpha()

        self.name = name
        self.ip = ip
        self.port = port

    @override
    def draw(self, surface: pg.Surface) -> None:
        """Draw the server list item on the given surface."""

        # Draw a dark transparent background
        bg_surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        bg_surface.fill((0, 0, 0, 40)) 
        surface.blit(bg_surface, (self.rect.x, self.rect.y))

        # Draw a border around the input field with 5px thickness
        color = pg.Color(255, 255, 255) if not self._is_selected else pg.Color(0, 200, 0)
        pg.draw.rect(surface, color, self.rect, 5)

        # Draw the icon with a 5x scale
        self._icon = pg.transform.scale(self._icon, (60, 60))
        icon_rect = self._icon.get_rect(center=(self.rect.x + 50, self.rect.y + self.rect.height // 2))
        surface.blit(self._icon, icon_rect)

        # Draw the server name and IP address
        name_text_surface = self._font.render(self.name, True, color)
        ip_text_surface = self._font.render(f"{self.ip}:{self.port}", True, color)

        surface.blit(name_text_surface, (self.rect.x + 90, self.rect.y + (self.rect.height - name_text_surface.get_height()) // 2 - 15))
        surface.blit(ip_text_surface, (self.rect.x + 90, self.rect.y + (self.rect.height - ip_text_surface.get_height()) // 2 + 15))

        if DEBUG_MODE:
            color = (0, 255, 0) if self._is_selected else (255, 0, 0)
            pg.draw.rect(surface, color, self.rect, 1)

        # Here you can handle the selection logic, e.g., joining the server
    @override
    def on_mouse_click(self, mouse_pos: Vector2) -> None:
        """Handle mouse click events on the server list item."""
        if self.is_mouse_over(mouse_pos):
            # Deselect other items in the list
            parent_canvas = self.parent
            if parent_canvas:
                self.deselect_other_items(parent_canvas.get(ServerListItem))

            self._is_selected = True if False else True  # Toggle selection state

    def deselect_other_items(self, items: list['ServerListItem']) -> None:
        for item in items:
            if item is not self and item._is_selected:
                item._is_selected = False

        # Here you can add logic to join the server or perform other actions


class JoinMenu(Scene):
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
            opacity=0.4
        ))

        canvas.add(InputField(
            placeholder="nickname",
            x="50%", y="15%",
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

        server_list = [
            "Server 1:172.0.0.1:8080",
            "Server 2:192.0.0.1:8080",
            "Server 3:172.1.1.1:8080",
            "Server 4:123.0.0.1:8080"
        ]

        for idx, item in enumerate(server_list[:3]):
            y = 200 + idx * 90  # 200 é o valor inicial, 90 é o espaçamento
            name, ip, port = item.split(":")
            canvas.add(ServerListItem(
                name=name, ip=ip, port=int(port),
                x="50%", y=y,
                width=650, height=80,
                pivot="center"
            ))

        self.add(ui)