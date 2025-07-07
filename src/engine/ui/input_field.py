import pygame as pg
from pygame.math import Vector2
from typing import Literal, Callable, override

from .component import UIComponent
from ..spritesheet import SpriteSheet
from ..constants import DEFAULT_FONT, PIVOT_POINTS

import re as re

class InputField(UIComponent):
    text: str
    placeholder: str
    disabled: bool
    on_submit: Callable | None
    pivot: Vector2
    max_char: int
    allowed_type: str

    _spritesheet: SpriteSheet
    _sprites: dict[str, pg.Surface]
    _is_focused: bool

    def __init__(
        self,
        placeholder: str = "Enter text",
        x: int | str = 0, y: int | str = 0,
        size: Literal["df"] = "df",
        max_char: int = 20,
        allowed_type: str = "str",
        on_submit: Callable | None = None,
        pivot: Vector2 | tuple[float, float] | str = (0.5, 0.5)
    ) -> None:
        """Initialize an InputField UI component.

        Args:
            placeholder (str, optional): The placeholder text for the input field. Defaults to "Enter text".
            x (int | str, optional): The x position of the input field. Can be a percentage of the screen width. Defaults to 0.
            y (int | str, optional): The y position of the input field. Can be a percentage of the screen height. Defaults to 0.
            size (Literal["sm", "md", "lg"], optional): The size of the input field. Defaults to "md".
            disabled (bool, optional): Whether the input field is disabled. Defaults to False.
            on_submit (Callable | None, optional): The function to call when the input is submitted. Defaults to None.
            pivot (Vector2 | tuple[float, float] | str, optional): The pivot point of the input field. Defaults to (0.5, 0.5).
        """

        super().__init__(
            x=x, y=y, pivot=pivot,
            width=0, height=0  # Width and height will be set based on the sprite size
        )

        self._font = pg.font.Font(DEFAULT_FONT, 48)
        self.placeholder = placeholder
        self.on_submit = on_submit
        self.max_char = max_char
        self.allowed_type = allowed_type  # Allowed input types

        self._is_focused = False

        spritesheet = SpriteSheet("assets/img/ui/input.png", (9, 14), scale=4)
        columns = { "df" : "0:4"}
        self.sprites = {
            "default": spritesheet.get_sprite((columns[size], 0))   # Focused and default are the same
        }

        self.width, self.height = self.sprites["default"].get_size()
        self.text = ""


    @override
    def on_mouse_click(self, mouse_pos: Vector2) -> None:
        """Handle mouse click events on the input field.

        Args:
            mouse_pos (Vector2): The position of the mouse click.
        """
        if not self.active:
            return

        # Check if the mouse click is within the input field's rectangle
        if self.rect.collidepoint(mouse_pos):
            self._is_focused = True
        else:
            self._is_focused = False

    @override
    def on_mouse_release(self, mouse_pos: Vector2) -> None:
        """Handle mouse release events.

        Args:
            mouse_pos (Vector2): The position of the mouse release.
        """
        if not self.active:
            return

        # If the input field is clicked, it should be focused
        if self.rect.collidepoint(mouse_pos):
            self._is_focused = True
        else:
            self._is_focused = False

    def verify_input_type(self, key : pg.event) -> bool:
        """Verify if the input is of the allowed type.

        Args:
            input (int | str | float): The input to verify.

        Returns:
            bool: True if the input is of the allowed type, False otherwise.
        """

        if self.allowed_type == "str":
            # verify if the input is a word, digit or a special character
            return bool(re.match(r"^[\w\s!@#$%^&*()_+={}\[\]:;\"'<>?,./\\-]*$", key))
        elif self.allowed_type == "int":
            # verify if the input is an integer
            return bool(re.match(r"^-?\d+$", key))

    @override
    def handle_key_event(self, event: pg.event.Event) -> None:
        """Handle key events for the input field.

        Args:
            event (pg.event.Event): The key event to handle.
        """
        if not self.active or not self._is_focused:
            return

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                # Call the on_submit function if it exists
                if self.on_submit:
                    self.on_submit(self.text)
                self._is_focused = False
            elif event.key == pg.K_BACKSPACE:
                # Remove the last character from the text
                self.text = self.text[:-1]
            elif event.key == pg.K_ESCAPE:
                # Unfocus the input field
                self._is_focused = False
            elif event.unicode and len(self.text) < self.max_char:  # Limit input length to 20 characters
                # Add the character to the text if it's not empty
                if self.verify_input_type(event.unicode):
                    self.text += event.unicode

    @override
    def draw(self, surface: pg.Surface) -> None:
        if not self.active:
            return

        img = self.sprites["default"]
        surface.blit(img, self.position)

        # Show the determined text or placeholder
        display_text = self.text if (self._is_focused or self.text != "") else self.placeholder
        color = (255, 255, 255) if (self._is_focused or self.text != "") else (150, 150, 150)
        text_surface = self._font.render(display_text, True, color)

        # width limit for the text
        max_width = self.width - 16  # optinal margin

        if text_surface.get_width() > max_width:
            # ajust the text to fit within the max width
            text = self.text
            while text:
                rendered = self._font.render(text, True, color)
                if rendered.get_width() <= max_width:
                    break
                # remove from the start or the end based on focus
                text = text[1:] if self._is_focused else text[:-1]
            text_surface = self._font.render(text, True, color)

        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

        super().draw(surface)