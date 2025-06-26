import pygame as pg


class SpriteSheet:
    """A class to handle spritesheets in Pygame."""
    
    _spritesheet: pg.Surface
    size: tuple[int, int]
    spacing: tuple[int, int]
    scale: int
    
    def __init__(
        self, 
        filename: str, 
        size: tuple[int, int] | None = None, 
        spacing: tuple[int, int] = (0, 0), 
        scale: int = 1
    ) -> None:
        """Initialize a SpriteSheet.

        Args:
            filename (str): The path to the spritesheet image file.
            size (tuple[int, int]): The size of each sprite in the spritesheet.
            spacing (tuple[int, int], optional): The spacing between sprites. Defaults to (0, 0).
            scale (int, optional): The scale factor for the sprites. Defaults to 1.
        """

        print("Loading spritesheet:", filename)

        self._spritesheet = pg.image.load(filename).convert_alpha()
        self.size = size if size else (self._spritesheet.get_width(), self._spritesheet.get_height())
        self.spacing = spacing
        self.scale = scale

    def get_sprite(self, index: tuple[int | str, int | str], colorkey: pg.Color | None = None) -> pg.Surface:
        """Get a sprite or a rectangle of sprites from the spritesheet.

        Args:
            index (tuple[int | str, int | str]): The (row, column) index or range of the sprite(s) in the spritesheet. Use a string like "0:2" for a range.
            colorkey (pg.Color | None, optional): The color key for transparency. Defaults to None.

        Returns:
            pg.Surface: The sprite surface.
        """
        
        def parse_range(val, size):
            if isinstance(val, int):
                return val * size, size
            
            if isinstance(val, str) and ":" in val:
                start, end = map(int, val.split(":"))
                pos = start * size
                length = (end - start + 1) * size
                return pos, length
            
            raise ValueError(f"Invalid index value: {val}")

        x, width = parse_range(index[0], self.size[0])
        y, height = parse_range(index[1], self.size[1])

        sprite = self._spritesheet.subsurface(pg.Rect(x, y, width, height))

        if colorkey is not None:
            sprite.set_colorkey(colorkey)

        return pg.transform.scale(sprite, (width * self.scale, height * self.scale))

    def get_sprites(self, indexes: tuple[int | str, int | str] | None = None, colorkey: pg.Color | None = None) -> list[pg.Surface]:
        """Get multiple sprites from the spritesheet.

        Args:
            indexes (tuple[int | str, int | str] | None, optional): A list of (row, column) indices for the sprites. If None, all sprites are returned. Defaults to None.
            colorkey (pg.Color | None, optional): The color key for transparency. Defaults to None.

        Returns:
            list[pg.Surface]: A list of sprite surfaces.
        """

        if indexes is None:
            rows = self._spritesheet.get_height() // (self.size[1] + self.spacing[1])
            cols = self._spritesheet.get_width() // (self.size[0] + self.spacing[0])
            indexes = [(row, col) for row in range(rows) for col in range(cols)]

        return [self.get_sprite(index, colorkey) for index in indexes]