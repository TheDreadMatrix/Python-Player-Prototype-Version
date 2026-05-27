from supermarioworld.core.gl_utils.gl_textures import load_texture, load_texture_cutout
from supermarioworld.package_typing import GameType



class Animation:
    def __init__(self, game: GameType, frame_paths: list[str], durations: list[float], key_images: list[str], repeat: bool=True, tex_filter: int=0, anisotropy: int=0):
        self.game = game


        textures = [load_texture(game.renderer._ctx, game.paths.ImagesPath(path), tex_filter, anisotropy) for path in frame_paths]
        [game.assets._regRawImage(key, textures[i]) for i, key in enumerate(key_images)]

        self.key_images = key_images

        self.durations = durations
        self.repeat = repeat

        self.index = 0
        self.timer = 0.0



    def update(self):
        self.timer += self.game.delta_time

        if self.timer >= self.durations[self.index]:
            self.timer = 0.0
            self.index += 1

            if self.index >= len(self.key_images):
                if self.repeat:
                    self.index = 0
                else:
                    self.index = len(self.key_images) - 1


    def getTextureKey(self):
        return self.key_images[self.index]
    

    def delAnimation(self):
        for key in self.key_images:
            self.game.assets.delImage(key)
    



class AnimationCutOut(Animation):
    def __init__(self, game: GameType, key_atlas: str, frames: list[tuple], durations: list[float], key_images: list[str], repeat: bool=True, tex_filter: int=0, anisotropy: int=0):
        self.game = game

        
        textures = [
            load_texture_cutout(game.renderer._ctx, game.assets.atlas_surfaces[key_atlas], frame[0], frame[1], frame[2], frame[3], tex_filter, anisotropy) for frame in frames
        ]

        [game.assets._regRawImage(key, textures[i]) for i, key in enumerate(key_images)]

        self.key_images = key_images

        self.durations = durations
        self.repeat = repeat

        self.index = 0
        self.timer = 0.0
        