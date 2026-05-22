from supermarioworld.core._moderngl import (
    load_texture, load_texture_cutout, create_error_texture,
    _DEFAULT_FRAGMENT_SOURCE, _DEFAULT_VERTEX_SOURCE
    )
import pygame as pg


class ShaderEntry:
    def __init__(self, game, custom_shader, default=False):
        self.program = custom_shader._program if not default else game._ctx.program(_DEFAULT_VERTEX_SOURCE, _DEFAULT_FRAGMENT_SOURCE)
        self.vao = game._ctx.vertex_array(self.program, [(game._vbo, "2f 2f", "inPos", "inCoord")], index_buffer=game._ebo)
        self.program["DM_Texture"] = 0
        self.uniforms = {
            "unPos": self.program["unPos"],
            "unSize": self.program["unSize"],
            "unLayer": self.program["unLayer"],
            "alpha": self.program["alpha"],
            "rgb": self.program["rgb"],
            "unFlx": self.program["unFlx"],
            "unFly": self.program["unFly"],
        }


class AssetsResources:
    def __init__(self, game):
        self.game = game

        self.default_texture = create_error_texture(game._ctx)
        self.default_shader = ShaderEntry(game, 0, True)


        self.sounds = {}
        self.musics = {}
        self.shaders = {}
        self.textures = {}

        self.atlas_surfaces = {}
        self.font_surfaces = {"default": "arial"}

    def pushAtlas(self, atlas_key, atlas_path):
        self.atlas_surfaces.update({atlas_key: pg.image.load(self.game.paths.ImagesPath(atlas_path)).convert_alpha()})

    def pushFont(self, font_key, font_path):
        self.font_surfaces.update({font_key: self.game.paths.FontsPath(font_path)})


    def regShader(self, shader_key, your_shader):
        self.shaders.update({shader_key: your_shader})


    def regImage(self, texture_key, texture_path, texture_filter=0, texture_anisotropy=0):
        self.textures.update({texture_key: load_texture(self.game._ctx, self.game.paths.ImagesPath(texture_path), texture_filter, texture_anisotropy)})


    def regCutOutImage(self, texture_key, atlas_key, x, y, w, h, texture_filter=0, texture_anisotropy=0):
        self.textures.update({texture_key: 
                              load_texture_cutout(self.game._ctx, 
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

    def delShader(self, shader_key):
        shader = self.shaders.pop(shader_key, None)
        if shader is not None:
            shader.program.release()
            shader.vao.release()


    

class AudioStream:
    def __init__(self, resources: AssetsResources):
        self.resources = resources
        self.played = False
        self.passed = False

    def load(self, music_key):
        pg.mixer.music.load(self.resources.musics[music_key])
        self.played = False
        self.passed = False

    def play(self, starts=0, fade_in=0, loops=0):
        if not self.played:
            pg.mixer.music.play(loops, starts, 1000 * fade_in)
            self.played = True


    def fadeOut(self, fade_out):
        if not self.passed:
            pg.mixer.music.fadeout(1000 * fade_out)
            self.passed = True


    def pause(self):
        pg.mixer.music.pause()

    def unpause(self):
        pg.mixer.music.unpause()

    def stop(self):
        pg.mixer.music.stop()

    def setVolume(self, volume):
        pg.mixer.music.set_volume(volume)


    def giveSound(self, sound_key):
        return self.resources.sounds[sound_key]



