import pygame
import moderngl



def load_texture(game, path: str):
    surface = pygame.image.load(path).convert_alpha()
    texture = game._ctx.texture(surface.size, 4, pygame.image.tobytes(surface, "RGBA"))
    texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
    return texture


def create_error_texture(ctx):
    size = 256
    tile = 32

    data = bytearray()

    purple = (255, 0, 255, 255)
    black = (0, 0, 0, 255)

    for y in range(size):
        for x in range(size):
            if ((x // tile) + (y // tile)) % 2 == 0:
                data.extend(purple)
            else:
                data.extend(black)

    texture = ctx.texture((size, size), 4, bytes(data))
    texture.build_mipmaps()

    return texture



def load_texture_text(game, path: str, text: str):
    surface = pygame.font.Font(path, 48).render(text)
    texture = game._ctx.texture(surface.size, 4, pygame.image.tobytes(surface, "RGBA"))
    return texture

