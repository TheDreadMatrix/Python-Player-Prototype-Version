from __future__ import annotations

from MyGame.requirements import mgl
from MyGame.utilits.texture_io import _load_images_bytes
from MyGame.utilits.texture import _apply_filter, _apply_repeat, _apply_anisotropy


def create_cubemap(
    ctx: "mgl.Context",
    images_path: list[str] | tuple[str, ...],
    *,
    components: int = 4,
    filter: int | tuple[int, int] = (mgl.NEAREST, mgl.NEAREST),
    use_mipmap: bool = False,
    flip_y: bool = False,
    repeat_x: bool = False,
    repeat_y: bool = False,
    repeat_z: bool = False,
    anisotropy: float | None = None,
) -> "mgl.TextureCube":
    if len(images_path) != 6:
        raise ValueError("Cubemap requires 6 images in order: +X, -X, +Y, -Y, +Z, -Z")

    (width, height), data_list = _load_images_bytes(
        images_path, components=components, flip_y=flip_y
    )

    if width != height:
        raise ValueError("Cubemap images must be square")

    data = b"".join(data_list)
    texture = ctx.texture_cube((width, height), components, data)

    _apply_filter(texture, filter)
    _apply_repeat(texture, repeat_x, repeat_y, repeat_z)
    _apply_anisotropy(texture, anisotropy)

    if use_mipmap:
        texture.build_mipmaps()

    return texture
