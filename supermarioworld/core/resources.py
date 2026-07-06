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

    def _set_to_stack(self, owner, resource_type, resource_key):
        self.set_to_destroy.setdefault(owner, [])
        self.set_to_destroy[owner].append((resource_type, resource_key))

    def releaseScene(self, scene):
        for typ, key in self.set_to_destroy.pop(scene, []):

            if typ == "IMAGE":
                self.delImage(key)

            elif typ == "SOUND":
                self.delSound(key)

            elif typ == "MUSIC":
                self.delMusic(key)



    # Registering Atlas Font Textures and Sounds

    # 1. Pygame object
    def regAtlas(self, atlas_key, atlas_path):
        self.atlas_surfaces.update({atlas_key: pg.image.load(self.game.paths.ImagesPath(atlas_path)).convert_alpha()})

    def regFont(self, font_key, font_path):
        self.font_surfaces.update({font_key: self.game.paths.FontsPath(font_path)})



    # 2. Moderngl object
    def regImage(self, owner, texture_key, texture_path, texture_filter=0, texture_anisotropy=0):
        self.textures.update({texture_key: load_texture(self.game.renderer._ctx, self.game.paths.ImagesPath(texture_path), texture_filter, texture_anisotropy)})

        self._set_to_stack(owner, "IMAGE", texture_key)
        

    def regCutOutImage(self, owner, texture_key, atlas_key, x, y, w, h, texture_filter=0, texture_anisotropy=0):
        atlas = self.atlas_surfaces.get(atlas_key)

        if atlas is None:
            raise ValueError(f"Atlas '{atlas_key}' not registered")

        self.textures.update({texture_key: load_texture_cutout(self.game.renderer._ctx, atlas, x, y, w, h, texture_filter, texture_anisotropy)})

        self._set_to_stack(owner, "IMAGE", texture_key)


    def _regRawImage(self, owner, texture_key, texture):
        self.textures.update({texture_key: texture})

        self._set_to_stack(owner, "IMAGE", texture_key)


    # 3. Just string path
    def regSound(self, owner, sound_key, sound_path):
        self.sounds.update({sound_key: self.game.paths.SoundPath(sound_path)})

        self._set_to_stack(owner, "SOUND", sound_key)


    def regMusic(self, owner, music_key, music_path):
        self.musics.update({music_key: self.game.paths.MusicPath(music_path)})

        self._set_to_stack(owner, "MUSIC", music_key)


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

    


    





