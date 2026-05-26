from supermarioworld.core.gl_utils.gl_textures import load_texture, load_texture_cutout
import pygame as pg





class AssetsResources:
    def __init__(self, game):
        self.game = game



        self.sounds = {}
        self.musics = {}
        self.textures = {}

        self.atlas_surfaces = {}
        self.font_surfaces = {"default": "arial"}

    def pushAtlas(self, atlas_key, atlas_path):
        self.atlas_surfaces.update({atlas_key: pg.image.load(self.game.paths.ImagesPath(atlas_path)).convert_alpha()})

    def pushFont(self, font_key, font_path):
        self.font_surfaces.update({font_key: self.game.paths.FontsPath(font_path)})



    def regImage(self, texture_key, texture_path, texture_filter=0, texture_anisotropy=0):
        self.textures.update({texture_key: load_texture(self.game.renderer._ctx, self.game.paths.ImagesPath(texture_path), texture_filter, texture_anisotropy)})


    def regCutOutImage(self, texture_key, atlas_key, x, y, w, h, texture_filter=0, texture_anisotropy=0):
        self.textures.update({texture_key: 
                              load_texture_cutout(self.game.renderer._ctx, 
                                self.atlas_surfaces[atlas_key], 
                               x, y, w, h, texture_filter, texture_anisotropy)})


    def _regRawImage(self, texture_key, texture):
        self.textures.update({texture_key: texture})



    def regSound(self, sound_key, sound_path):
        self.sounds.update({sound_key: pg.Sound(self.game.paths.SoundPath(sound_path))})


    def regMusic(self, music_key, music_path):
        self.musics.update({music_key: self.game.paths.MusicPath(music_path)})


    def delSound(self, sound_key):
        self.sounds.pop(sound_key)

    def delMusic(self, music_key):
        self.musics.pop(music_key)



    def delImage(self, texture_key):
        tex = self.textures.pop(texture_key, None)
        if tex is not None:
            tex.release()

    


    





