from supermarioworld.core.gl_utils.gl_textures import load_texture_text, give_font
from supermarioworld.typing.gametype import GameType


class Widget:
    def __init__(self, r, g, b, a):
        self.position = (0, 0)
        self.size = (0, 0)

        self.r = r
        self.g = g
        self.b = b
        self.a = a

        self.flipx = False
        self.flipy = False

        self.visible = True
        self.enabled = True

        self.hovered = False
        self.pressed = False

    def update(self):
        pass

    def render(self):
        pass

    def contains(self, mouse: tuple):
        x, y = self.position
        w, h = self.size

        return (x <= mouse[0] <= x + w and y <= mouse[1] <= y + h)


class FadeLabel:
    def __init__(self, game: GameType):
        self.game = game
        self.renderer = game.renderer

        self.size = (game.width, game.height)
        self.position = (0, 0)

        self.alpha = 0.0

        self.speed = 1.0

        self.fading_in = False
        self.fading_out = False

    def fadeIn(self, speed=1.0):
        self.speed = speed
        self.alpha = 1.0
        self.fading_in = True
        self.fading_out = False

    def fadeOut(self, speed=1.0):
        self.speed = speed
        self.alpha = 0.0
        self.fading_out = True
        self.fading_in = False

    def update(self):
        if self.fading_in:
            self.alpha -= self.speed * self.game.delta_time

            if self.alpha <= 0:
                self.alpha = 0
                self.fading_in = False

        elif self.fading_out:
            self.alpha += self.speed * self.game.delta_time

            if self.alpha >= 1:
                self.alpha = 1
                self.fading_out = False

    def render(self):
        if self.alpha <= 0:
            return

        self.renderer.renderQuad(position=self.position, size=self.size, r=0, g=0, b=0, a=self.alpha)




class TextLabel(Widget):
    _id_count = 0
    def __init__(self, game: GameType, text: str="hello world!", font_key: str=None, size_font: int=20, r=1, g=1, b=1, a=1):
        super().__init__(r=r, g=g, b=b, a=a)
        
        self._ctx = game.renderer._ctx
        self.resources = game.assets
        self.renderer = game.renderer

        self.text = text

        self.texture_id = f"text_label_{TextLabel._id_count}"
        TextLabel._id_count += 1



        font_path = self.resources.font_surfaces.get(font_key)

        self.font = give_font(font_path, size_font)
       

        self.texture_note = None

        self._rebuildText(color_text=(round(self.r * 255), round(self.g * 255), round(self.b * 255)), tex_filter=0, anisotropy=0)


    @property
    def width(self): return self.size[0]

    @property
    def height(self): return self.size[1]
    
    def _rebuildText(self, color_text, tex_filter, anisotropy):
        if self.texture_note is not None:
            self.resources.delImage(self.texture_id)
            self.texture_note.release()
            self.texture_note = None
            
        self.texture_note, self.size = load_texture_text(self._ctx, self.font, self.text, color_text, tex_filter, anisotropy)

        self.resources._regRawImage(self.texture_id, self.texture_note)


    def setText(self, text: str, r_text: float=0, g_text: float=0, b_text: float=0, tex_filter: int=0, anisotropy: int=0):
        if self.text != text:
            self.text = text
            self._rebuildText(color_text=(round(r_text * 255), round(g_text * 255), round(b_text * 255)), tex_filter=tex_filter, anisotropy=anisotropy)


    def render(self):
        self.renderer.render(self.texture_id, size=self.size, position=self.position, r=self.r, g=self.g, b=self.b, a=self.a, flx=self.flipx, fly=self.flipy)

        


    def __repr__(self):
        return f"<TextLabel - {self.texture_id}>"