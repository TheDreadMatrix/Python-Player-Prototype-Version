import pygame



def load_texture(game, path):
    surface = pygame.image.load(path).convert_alpha()
    texture = game._ctx.texture(surface.size(), 4, pygame.image.tobytes(surface))
    return texture



