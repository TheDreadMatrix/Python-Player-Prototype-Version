import pygame
import moderngl




TEXTURE_ARRAY_BUILD_PATH = 0
TEXTURE_ARRAY_BUILD_RAW = 0


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



def load_texture_cutout(ctx: moderngl.Context, path: str, x: int, y: int, w: int, h: int, filter: int=0, anisotropy: int=0):
    surface = (pygame.image.load(path).convert_alpha()).subsurface((x, y, w, h)).copy()
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

