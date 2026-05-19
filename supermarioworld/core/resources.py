from supermarioworld.core._moderngl import (
    load_texture, load_texture_cutout, 
    _DEFAULT_FRAGMENT_SOURCE, _DEFAULT_VERTEX_SOURCE
    )
import pygame as pg


class ShaderEntry:
    def __init__(self, game, custom_shader, default=False):
        self.program = custom_shader._program if not default else game._ctx.program(_DEFAULT_VERTEX_SOURCE, _DEFAULT_FRAGMENT_SOURCE)
        self.vao = game._ctx.vertex_array(self.program, [(game._vbo, "2f 2f", "inPos", "inCoord")], index_buffer=game._ebo)
        self.program["DM_Texture"] = 0


class AssetsResources:
    def __init__(self, game):
        self.game = game

        
        self.shaders = {"default": ShaderEntry(game=game, custom_shader=0, default=True)}
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


    