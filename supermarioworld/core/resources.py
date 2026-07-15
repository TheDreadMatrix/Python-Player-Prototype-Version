from supermarioworld.core.gl_utils.gl_textures import load_texture, load_texture_cutout
import pygame as pg





class AssetsResources:
    def __init__(self, game):
        self.game = game

        self.sounds = {} 
        self.musics = {}
        self.textures = {}

        self.atlas_surfaces: dict[str, pg.Surface] = {}
        self.font_surfaces: dict[str, str] = {}

        self.set_to_destroy = {}
        self._owner = None


    def beginScene(self, scene_name):
        self._owner = scene_name

    def _set_to_stack(self, owner, resource_type, resource_key):
        self.set_to_destroy.setdefault(owner, [])
        self.set_to_destroy[owner].append((resource_type, resource_key))

    def releaseScene(self):
        for typ, key in self.set_to_destroy.pop(self._owner, []):

            if typ == "image":
                self.delImage(key)

            elif typ == "atlas":
                self.delAtlas(key)

            elif typ == "font":
                self.delFont(key)

            elif typ == "sound":
                self.delSound(key)

            elif typ == "music":
                self.delMusic(key)



    # Registering Atlas Font Textures and Sounds

    # 1. Pygame object
    def regAtlas(self, atlas_key, atlas_path):
        self.atlas_surfaces.update({atlas_key: pg.image.load(self.game.paths.ImagesPath(atlas_path)).convert_alpha()})
        self._set_to_stack(self._owner, "atlas", atlas_key)

    def regFont(self, font_key, font_path):
        self.font_surfaces.update({font_key: self.game.paths.FontsPath(font_path)})
        self._set_to_stack(self._owner, "font", font_key)


    # 2. Moderngl object
    def regImage(self, texture_key, texture_path, texture_filter=0, texture_anisotropy=0):
        self.textures.update({texture_key: load_texture(self.game.renderer._ctx, self.game.paths.ImagesPath(texture_path), texture_filter, texture_anisotropy)})

        self._set_to_stack(self._owner, "image", texture_key)
        

    def regCutOutImage(self,  texture_key, atlas_key, x, y, w, h, texture_filter=0, texture_anisotropy=0):
        atlas = self.atlas_surfaces.get(atlas_key)

        if atlas is None:
            raise ValueError(f"Atlas '{atlas_key}' not registered")

        self.textures.update({texture_key: load_texture_cutout(self.game.renderer._ctx, atlas, x, y, w, h, texture_filter, texture_anisotropy)})

        self._set_to_stack(self._owner, "image", texture_key)


    def _regRawImage(self, texture_key, texture):
        self.textures.update({texture_key: texture})
        self._set_to_stack(self._owner, "image", texture_key)

    


    # 3. Just string path
    def regSound(self, sound_key, sound_path):
        self.sounds.update({sound_key: self.game.paths.SoundPath(sound_path)})
        self._set_to_stack(self._owner, "sound", sound_key)

    


    def regMusic(self, music_key, music_path):
        self.musics.update({music_key: self.game.paths.MusicPath(music_path)})
        self._set_to_stack(self._owner, "music", music_key)



    # Clear
    def delSound(self, sound_key):
        self.sounds.pop(sound_key, None)

    def delMusic(self, music_key):
        self.musics.pop(music_key, None)

    def delAtlas(self, atlas_key):
        self.atlas_surfaces.pop(atlas_key, None)

    def delFont(self, font_key):
        self.font_surfaces.pop(font_key, None)



    def delImage(self, texture_key):
        tex = self.textures.pop(texture_key, None)
        if tex is not None:
            tex.release()

    


    





