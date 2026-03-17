from __future__ import annotations

from pathlib import Path
from typing import Iterable, Tuple

from MyGame.requirements import pg


def _resolve_image_path(image_path: str | Path) -> Path:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    return path


def _load_surface(image_path: str | Path) -> "pg.Surface":
    path = _resolve_image_path(image_path)
    surface = pg.image.load(str(path))

    if pg.display.get_init():
        try:
            surface = surface.convert_alpha()
        except pg.error:
            surface = surface.convert()
    return surface


def _surface_to_bytes(
    surface: "pg.Surface",
    components: int,
    flip_y: bool,
) -> bytes:
    if components == 3:
        fmt = "RGB"
    elif components == 4:
        fmt = "RGBA"
    else:
        raise ValueError("components must be 3 or 4")
    return pg.image.tobytes(surface, fmt, flip_y)


def _load_image_bytes(
    image_path: str | Path,
    *,
    components: int,
    flip_y: bool,
) -> Tuple[Tuple[int, int], bytes]:
    surface = _load_surface(image_path)
    size = surface.get_size()
    data = _surface_to_bytes(surface, components=components, flip_y=flip_y)
    return size, data


def _load_images_bytes(
    images_path: Iterable[str | Path],
    *,
    components: int,
    flip_y: bool,
) -> Tuple[Tuple[int, int], list[bytes]]:
    data_list: list[bytes] = []
    size = None
    for image_path in images_path:
        img_size, data = _load_image_bytes(
            image_path, components=components, flip_y=flip_y
        )
        if size is None:
            size = img_size
        elif img_size != size:
            raise ValueError("All images must have the same size")
        data_list.append(data)

    if size is None:
        raise ValueError("images_path is empty")

    return size, data_list
