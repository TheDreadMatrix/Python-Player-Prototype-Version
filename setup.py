from pathlib import Path
from setuptools import Extension, setup
import sys


ROOT = Path(__file__).parent
SOLOUD = ROOT / "MyGame" / "native-code"

sources = [
    SOLOUD / "audio.cpp",
    SOLOUD / "src_audio" / "core" / "soloud.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_audiosource.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_bus.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_core_3d.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_core_basicops.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_core_faderops.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_core_filterops.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_core_getters.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_core_setters.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_core_voicegroup.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_core_voiceops.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_fader.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_fft.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_fft_lut.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_file.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_filter.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_misc.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_queue.cpp",
    SOLOUD / "src_audio" / "core" / "soloud_thread.cpp",
    SOLOUD / "src_audio" / "audiosource" / "wav" / "soloud_wav.cpp",
    SOLOUD / "src_audio" / "audiosource" / "wav" / "soloud_wavstream.cpp",
    SOLOUD / "src_audio" / "audiosource" / "wav" / "dr_impl.cpp",
    SOLOUD / "src_audio" / "audiosource" / "wav" / "stb_vorbis.c",
    SOLOUD / "src_audio" / "backend" / "miniaudio" / "soloud_miniaudio.cpp",
    SOLOUD / "src_audio" / "filter" / "soloud_biquadresonantfilter.cpp",
]

include_dirs = [
    str(SOLOUD / "include_audio"),
    str(SOLOUD / "src_audio"),
    str(SOLOUD / "src_audio" / "audiosource" / "wav"),
    str(SOLOUD / "src_audio" / "backend" / "miniaudio"),
]

define_macros = [
    ("WITH_MINIAUDIO", "1"),
    ("_CRT_SECURE_NO_WARNINGS", "1"),
]

extra_compile_args = []
if sys.platform.startswith("win"):
    extra_compile_args.append("/std:c++17")
else:
    extra_compile_args.append("-std=c++17")

ext_modules = [
    Extension(
        name="MyGame.audio",
        sources=[str(p) for p in sources],
        include_dirs=include_dirs,
        define_macros=define_macros,
        extra_compile_args=extra_compile_args,
        language="c++",
    )
]

setup(
    name="kartoshka-audio",
    version="0.1.0",
    ext_modules=ext_modules,
)
