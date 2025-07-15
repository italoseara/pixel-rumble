import pytmx
import pygame
from pytmx.util_pygame import load_pygame


pygame.init()
screen = pygame.display.set_mode((800, 600))
tmx_data = load_pygame('assets/maps/mapatestemario.tmx')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

    pygame.display.flip()
    screen.fill((0, 0, 0))  # Clear the screen before drawing the next frame