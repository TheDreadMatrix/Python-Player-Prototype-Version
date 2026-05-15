from supermarioworld.rendering._moderngl import pygame, load_texture_text






class TextLabel:
    def __init__(self, game, renderer, text_id: str, text: str, font_path: str|None=None, size_font: int=20, color_text: tuple=(255, 255, 255)):
        self._ctx = game._ctx
        self.renderer = renderer

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

        self.font = pygame.font.Font(font_path, size_font) if font_path else pygame.font.SysFont('arial', size_font) 
       

        self.texture_note = None

        self._rebuildText(color_text, 0, 0)
    
    def _rebuildText(self, color_text, filter, anisotropy):
        self.texture_note, self.size = load_texture_text(self._ctx, self.font, self.text, color_text, filter, anisotropy)
        self.renderer._pushStraightTexture(self.texture_id, self.texture_note)


    def setText(self, text: str, color_text: tuple=(255, 255, 255), filter: int=0, anisotropy: int=0):
        if self.text != text:
            self.text = text
            self._rebuildText(color_text, filter, anisotropy)

            

    def render(self):
        self.renderer.submitSprite(
            self.texture_id,
            position=self.position,
            size=self.size,
            layer=self.layer,
            rgb=self.rgb,
            alpha=self.alpha,
            flipx=self.flipx,
            flipy=self.flipy,
            shader=self.shader_id
        )