from __future__ import annotations

import re
import pygame as pg
from pygame.math import Vector2
from typing import Callable, override, Any

from .component import UIComponent
from ..constants import DEFAULT_FONT

class InputField(UIComponent):
    _text: str
    placeholder: str
    disabled: bool
    on_submit: Callable | None
    pivot: Vector2
    max_char: int
    allowed_type: type | str

    _is_focused: bool

    def __init__(
        self,
        placeholder: str = "Enter text",
        x: int | str = 0, y: int | str = 0,
        width: int = 200, height: int = 48,
        max_char: int = 20,
        allowed_type: type | str = str,
        on_submit: Callable | None = None,
        pivot: Vector2 | tuple[float, float] | str = (0.5, 0.5)
    ) -> None:
        """Initialize an InputField UI component.

        Args:
            placeholder (str, optional): The placeholder text for the input field. Defaults to "Enter text".
            x (int | str, optional): The x position of the input field. Can be a percentage of the screen width. Defaults to 0.
            y (int | str, optional): The y position of the input field. Can be a percentage of the screen height. Defaults to 0.
            max_char (int, optional): The max amount of characters you can type. Defaults to 20.
            allowed_type (type | str, optional): The allowed type of the text input, it can be a type or a regex. Defaults to str.
            on_submit (Callable | None, optional): The function to call when the input is submitted. Defaults to None.
            pivot (Vector2 | tuple[float, float] | str, optional): The pivot point of the input field. Defaults to (0.5, 0.5).
        """

        super().__init__(
            x=x, y=y, pivot=pivot,
            width=width, height=height,
        )

        self._font = pg.font.Font(DEFAULT_FONT, 48)
        self.placeholder = placeholder
        self.on_submit = on_submit
        self.max_char = max_char
        self.allowed_type = allowed_type  # Allowed input types

        self._is_focused = False

        self._text = ""

    @property
    def text(self) -> str:
        return self._text

    @property
    def value(self) -> Any:
        return self.allowed_type(self._text) if self._text else self.allowed_type()

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

    def verify_input_type(self, key: str) -> bool:
        """Verify if the input is of the allowed type.

        Args:
            key (str): The input string to verify.

        Returns:
            bool: True if the input is of the allowed type, False otherwise.
        """

        new_text = self._text + key

        if isinstance(self.allowed_type, str):
            return bool(re.match(self.allowed_type, new_text))

        if self.allowed_type == str:
            return bool(re.match(r"^[\w\s!@#$%^&*()_+={}\[\]:;\"'<>?,./\\-]*$", new_text))
        elif self.allowed_type == int:
            return bool(re.match(r"^-?\d+$", new_text))
        elif self.allowed_type == float:
            return bool(re.match(r"^-?\d*(\.\d*)?$", new_text))
        
        return False

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
                    self.on_submit(self._text)
                self._is_focused = False
            elif event.key == pg.K_BACKSPACE:
                # Remove the last character from the text
                self._text = self._text[:-1]
            elif event.key == pg.K_ESCAPE:
                # Unfocus the input field
                self._is_focused = False
            elif event.unicode and len(self._text) < self.max_char:  # Limit input length to 20 characters
                # Add the character to the text if it's not empty
                if self.verify_input_type(event.unicode):
                    self._text += event.unicode

    @override
    def draw(self, surface: pg.Surface) -> None:
        if not self.active:
            return

        # Draw a dark transparent background
        bg_surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        bg_surface.fill((0, 0, 0, 40)) 
        surface.blit(bg_surface, (self.rect.x, self.rect.y))

        # Draw a border around the input field with 5px thickness
        border_color = (255, 255, 255) if self._is_focused else (150, 150, 150)
        pg.draw.rect(surface, border_color, self.rect, 5)

        # Show the determined text or placeholder
        display_text = self._text if (self._is_focused or self._text != "") else self.placeholder
        color = (255, 255, 255) if (self._is_focused or self._text != "") else (150, 150, 150)
        text_surface = self._font.render(display_text, True, color)

        # width limit for the text
        max_width = self.width - 8  # optional margin

        if text_surface.get_width() > max_width:
            # ajust the text to fit within the max width
            text = self._text
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

    @override
    def clone(self) -> InputField:
        """Create a copy of this InputField component."""
        
        new_input_field = InputField(
            placeholder=self.placeholder,
            x=self._position.x,
            y=self._position.y,
            width=self.width,
            height=self.height,
            max_char=self.max_char,
            allowed_type=self.allowed_type,
            on_submit=self.on_submit,
            pivot=self.pivot
        )
        new_input_field._text = self._text
        new_input_field._is_focused = self._is_focused
        return new_input_field