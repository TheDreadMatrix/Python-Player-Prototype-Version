import pygame
import moderngl








BASE_FILTER_DICT = {
    0: (moderngl.NEAREST, moderngl.NEAREST, False),
    1: (moderngl.LINEAR, moderngl.LINEAR, False),
    2: (moderngl.NEAREST_MIPMAP_NEAREST, moderngl.NEAREST, True),
    3: (moderngl.LINEAR_MIPMAP_NEAREST, moderngl.LINEAR, True),
    4: (moderngl.NEAREST_MIPMAP_LINEAR, moderngl.NEAREST, True),
    5: (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR, True)
}

def _build_texture_attribute(texture, filter, anisotropy):
    min_filter, mag_filter, use_mipmap = BASE_FILTER_DICT.get(filter, BASE_FILTER_DICT[0])

    texture.filter = (min_filter, mag_filter)

    if use_mipmap:
        texture.build_mipmaps()

    if anisotropy:
        texture.anisotropy = anisotropy



def load_texture_cutout(ctx: moderngl.Context, surface: pygame.Surface, x: int, y: int, w: int, h: int, filter: int=0, anisotropy: int=0):
    surface = surface.subsurface((x, y, w, h)).copy()
    texture: moderngl.Texture = ctx.texture(surface.size, 4, pygame.image.tobytes(surface, "RGBA"))

    _build_texture_attribute(texture, filter, anisotropy)
    return texture


def load_texture(ctx: moderngl.Context, path: str, filter: int=0, anisotropy: int=0):
    surface = pygame.image.load(path).convert_alpha()
    texture: moderngl.Texture = ctx.texture(surface.size, 4, pygame.image.tobytes(surface, "RGBA"))

    _build_texture_attribute(texture, filter, anisotropy)
    return texture




def load_texture_text(ctx: moderngl.Context, font: pygame.Font, text: str, color: tuple=(255, 255, 255), filter: int=0, anisotropy: int=0):
    surface: pygame.Surface = font.render(text, True, color)
    texture = ctx.texture(surface.size, 4, pygame.image.tobytes(surface, "RGBA"))

    _build_texture_attribute(texture, filter, anisotropy)

    return (texture, surface.get_size())


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



