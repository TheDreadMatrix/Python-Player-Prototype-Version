from supermarioworld.core.gl_utils.gl_textures import pygame, load_texture_text
from supermarioworld.package_typing import GameType



class FadeLabel:
    def __init__(self, game: GameType):
        self.game = game

        self.renderer = game.renderer

        self.size = (game.width, game.height)
        self.position = (0, 0)
        self.layer = 1


    def render(self):
        self.renderer.submitQuad()




class TextLabel:
    def __init__(self, game: GameType, text_id: str, text: str="SOME-TEXT", font_key: str=None, size_font: int=20):
        self._ctx = game.renderer._ctx
        self.resources = game.assets

        self.text = text

        self.texture_id = text_id

        self.position = (0, 0)

        self.size = (200, 80)
      
        self.r = 1
        self.g = 1
        self.b = 1
        self.a = 1

        self.flipx = False
        self.flipy = False


        font_path = self.resources.font_surfaces.get(font_key)

        if font_path:
            self.font = pygame.font.Font(font_path, size_font)
        else:
            self.font = pygame.font.SysFont("arial", size_font)
       

        self.texture_note = None

        self._rebuildText(color_text=(0, 0, 0), tex_filter=0, anisotropy=0)
    
    def _rebuildText(self, color_text, tex_filter, anisotropy):
        if self.texture_note is not None:
            self.resources.delImage(self.texture_id)
            
        self.texture_note, self.size = load_texture_text(self._ctx, self.font, self.text, color_text, tex_filter, anisotropy)
        self.resources._regRawImage(self.texture_id, self.texture_note)


    def setText(self, text: str, r_text: float=0, g_text: float=0, b_text: float=0, tex_filter: int=0, anisotropy: int=0):
        if self.text != text:
            self.text = text
            self._rebuildText(color_text=(round(r_text * 255), round(g_text * 255), round(b_text * 255)), tex_filter=tex_filter, anisotropy=anisotropy)

            