import pygame
import moderngl


TEXTURE_BUILD_PATH = 0
TEXTURE_BUILD_RAW = 1
TEXTURE_BUILD_TEXT = 2

TEXTURE_ARRAY_BUILD_PATH = 0
TEXTURE_ARRAY_BUILD_RAW = 1


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


def load_texture_array(ctx: moderngl.Texture, paths: list[str], filter: int=0, anisotropy: int=0):
    surfaces = b""
    for path in paths:
        surface = pygame.image.load(path).convert_alpha()
        


    _build_texture_attribute(0, filter, anisotropy)




def load_texture(ctx: moderngl.Texture, path: str, filter: int=0, anisotropy: int=0):
    surface = pygame.image.load(path).convert_alpha()
    texture: moderngl.Texture = ctx.texture(surface.size, 4, pygame.image.tobytes(surface, "RGBA"))

    _build_texture_attribute(texture, filter, anisotropy)
    return texture




def load_texture_text(ctx: moderngl.Context, font: pygame.Font, text: str, color: tuple=(255, 255, 255), filter: int=0, anisotropy: int=0):
    surface: pygame.Surface = font.render(text, True, color)
    texture = ctx.texture(surface.size, 4, pygame.image.tobytes(surface, "RGBA"))

    _build_texture_attribute(texture, filter, anisotropy)

    return (texture, surface.get_size())

