from __future__ import annotations

from MyGame.requirements import mgl
from MyGame.utilits.textures.texture_io import _load_image_bytes


def _apply_filter(texture: "mgl.Texture", tex_filter):
    if isinstance(tex_filter, int):
        texture.filter = (tex_filter, tex_filter)
    else:
        texture.filter = tex_filter


def _apply_repeat(texture, repeat_x: bool, repeat_y: bool, repeat_z: bool | None = None):
    if hasattr(texture, "repeat_x"):
        texture.repeat_x = repeat_x
    if hasattr(texture, "repeat_y"):
        texture.repeat_y = repeat_y
    if repeat_z is not None and hasattr(texture, "repeat_z"):
        texture.repeat_z = repeat_z


def _apply_anisotropy(texture, anisotropy: float | None):
    if anisotropy is None:
        return
    if hasattr(texture, "anisotropy"):
        texture.anisotropy = float(anisotropy)


def create_texture(
    ctx: "mgl.Context",
    image_path: str,
    *,
    components: int = 4,
    filter: int | tuple[int, int] = (mgl.NEAREST, mgl.NEAREST),
    use_mipmap: bool = False,
    flip_y: bool = True,
    repeat_x: bool = True,
    repeat_y: bool = True,
    anisotropy: float | None = None,
) -> "mgl.Texture":
    size, data = _load_image_bytes(image_path, components=components, flip_y=flip_y)
    texture = ctx.texture(size, components, data)

    _apply_filter(texture, filter)
    _apply_repeat(texture, repeat_x, repeat_y)
    _apply_anisotropy(texture, anisotropy)

    if use_mipmap:
        texture.build_mipmaps()

    return texture
