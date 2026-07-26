from pathlib import Path
import sys

from supermarioworld.core.app import SuperMariWorldApplication


if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

MODS_DIR = BASE_DIR / "mods"

smw = SuperMariWorldApplication(__file__, "supermarioworld_config")


MODS_DIR.mkdir(exist_ok=True)


for mod_file in sorted(MODS_DIR.glob("*.py")):
    print(f"Loading mod: {mod_file.name}")

    environment = {
        "game": smw,
        "trace": print,
        "__file__": str(mod_file),
        "__name__": mod_file.stem
    }

    try:
        exec(compile(mod_file.read_text("utf-8"), str(mod_file), "exec"), environment)

        for event in ("preUpdate", "onUpdate", "preRender", "onRender"):
            func = environment.get(event)
            if callable(func):
                getattr(smw, event)(func)

    except Exception as e:
        print(f"Ошибка в моде {mod_file.name}:")
        print(e)

smw._run()