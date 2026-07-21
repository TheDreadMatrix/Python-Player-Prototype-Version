from supermarioworld.core.gl_utils.gl_textures import load_texture, load_texture_cutout
from supermarioworld.typing.gametype import GameType



class Animation:
    _id = 0
    def __init__(self, game: GameType, frame_paths: list[str], durations: list[float], repeat: bool=True, tex_filter: int=0, anisotropy: int=0):
        self.game = game

        anim_id = Animation._id
        Animation._id += 1

        textures = [load_texture(game.renderer._ctx, game.paths.ImagesPath(path), tex_filter, anisotropy) for path in frame_paths]
        self.key_images = []

        for i, texture in enumerate(textures):
            key = f"animation_{anim_id}_frame_{i}"
            self.key_images.append(key)
            game.assets._regRawImage(key, texture)

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
    
    



class AnimationCutOut(Animation):
    def __init__(self, game: GameType, key_atlas: str, frames: list[tuple], durations: list[float], repeat: bool=True, tex_filter: int=0, anisotropy: int=0):
        self.game = game

        anim_id = Animation._id
        Animation._id += 1

        
        textures = [
            load_texture_cutout(game.renderer._ctx, game.assets.atlas_surfaces[key_atlas], frame[0], frame[1], frame[2], frame[3], tex_filter, anisotropy) for frame in frames
        ]

        self.key_images = []

        for i, texture in enumerate(textures):
            key = f"animation_{anim_id}_frame_{i}"
            self.key_images.append(key)
            game.assets._regRawImage(key, texture)

        self.durations = durations
        self.repeat = repeat

        self.index = 0
        self.timer = 0.0
        