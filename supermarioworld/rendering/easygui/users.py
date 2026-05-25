from supermarioworld.core.gl_utils import pygame, load_texture_text



class FadeLabel:
    def __init__(self, game, renderer):
        self.game = game

        self.renderer = renderer

        self.size = (game.width, game.height)
        self.position = (0, 0)
        self.layer = 1


    def render(self):
        self.renderer.submitQuad()




class TextLabel:
    def __init__(self, game, renderer, text_id: str, text: str, font_key: str=None, size_font: int=20, color_text: tuple=(255, 255, 255)):
        self._ctx = game._ctx
        self.renderer = renderer
        self.resources = game.assets

        self.text = text
        self.texture_id = text_id
        self.position = (0, 0)
        self.size = (200, 80)
        self.layer = 1
        self.rgb = (1, 1, 1)
        self.alpha = 1
        self.flipx = False
        self.flipy = False

        self.shader_id = "default"

        self.font = pygame.font.Font(self.resources.font_surfaces[font_key], size_font) if font_key else pygame.font.SysFont('arial', size_font) 
       

        self.texture_note = None

        self._rebuildText(color_text, 0, 0)
    
    def _rebuildText(self, color_text, filter, anisotropy):
        if self.texture_note is not None:
            self.texture_note.release()
            
        self.texture_note, self.size = load_texture_text(self._ctx, self.font, self.text, color_text, filter, anisotropy)
        self.resources._regRawImage(self.texture_id, self.texture_note)


    def setText(self, text: str, color_text: tuple=(255, 255, 255), filter: int=0, anisotropy: int=0):
        if self.text != text:
            self.text = text
            self._rebuildText(color_text, filter, anisotropy)

            