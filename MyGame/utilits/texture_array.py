from __future__ import annotations

from MyGame.requirements import mgl
from MyGame.utilits.texture_io import _load_images_bytes
from MyGame.utilits.texture import _apply_filter, _apply_repeat, _apply_anisotropy


def create_texture_array(
    ctx: "mgl.Context",
    images_path: list[str] | tuple[str, ...],
    *,
    components: int = 4,
    filter: int | tuple[int, int] = (mgl.NEAREST, mgl.NEAREST),
    use_mipmap: bool = False,
    flip_y: bool = True,
    repeat_x: bool = True,
    repeat_y: bool = True,
    anisotropy: float | None = None,
) -> "mgl.TextureArray":
    (width, height), data_list = _load_images_bytes(
        images_path, components=components, flip_y=flip_y
    )

    layers = len(data_list)
    data = b"".join(data_list)
    texture = ctx.texture_array((width, height, layers), components, data)

    _apply_filter(texture, filter)
    _apply_repeat(texture, repeat_x, repeat_y)
    _apply_anisotropy(texture, anisotropy)

    if use_mipmap:
        texture.build_mipmaps()

    return texture
