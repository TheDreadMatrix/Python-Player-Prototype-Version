from pathlib import Path
import sys, os


class CorePath:
    def __init__(self, file_execution):
        
        if getattr(sys, "frozen", False):
            self._runtime_dir = Path(os.getenv("APPDATA")) / ".superkartoshkaworld"
        else:
            self._runtime_dir = Path(file_execution).resolve().parent / "assets"

        if hasattr(sys, "_MEIPASS"):
            self._resource_dir = Path(sys._MEIPASS) / "assets"
        else:
            self._resource_dir = self._runtime_dir 


        self._fonts_dir = self._resource_dir / "fonts"
        self._assets_dir = self._resource_dir / "images"
        self._shaders_dir = self._resource_dir / "shaders"
        self._music_dir = self._resource_dir / "music"
        self._sound_dir = self._resource_dir / "sounds"

        
        self._config_dir = self._runtime_dir / "config"
        self._csaves_dir = self._runtime_dir / "csaves"


    def _ensure_file(self, path: Path, kind: str) -> Path:
        if not path.exists():
            raise FileNotFoundError(f"{kind} file not found: {path}")
        if not path.is_file():
            raise FileNotFoundError(f"{kind} is not a file: {path}")
        return path

    def _ensure_folder(self, path: Path, kind: str) -> Path:
        if not path.exists():
            raise FileNotFoundError(f"{kind} folder not found: {path}")

        if not path.is_dir():
            raise NotADirectoryError(f"{kind} is not a directory: {path}")
        
        return path
    

    
    def ConfigFolder(self, folders):
        return str(self._ensure_folder(self._config_dir / folders, "Config"))
    
    def CsavesFolder(self, folders):
        return str(self._ensure_folder(self._csaves_dir / folders, "Csaves"))


    def findGlobal(self, folder: str, file_category: str) -> list[str]:
        root = Path(folder)

        if not root.exists():
            raise FileNotFoundError(f"Folder not found: {root}")

        files = []

        for file in root.glob(file_category):
            if file.is_file():
                files.append(str(file))

        return files
    
    
    

    

    # Work with file path
    def ConfigPath(self, filename):
        return str(self._ensure_file(self._config_dir / filename, "Config"))
    
    def CsavesPath(self, filename):
        return str(self._ensure_file(self._csaves_dir / filename, "Csaves"))
    

    def FontsPath(self, filename):
        return str(self._ensure_file(self._fonts_dir / filename, "Fonts"))
    
    def AssetPath(self, filename):
        return str(self._ensure_file(self._resource_dir / filename, "Assets"))

    def ShaderPath(self, filename):
        return str(self._ensure_file(self._shaders_dir / filename, "Shader"))

    def ImagesPath(self, filename):
        return str(self._ensure_file(self._assets_dir / filename, "Images"))

    def MusicPath(self, filename):
        return str(self._ensure_file(self._music_dir / filename, "Music"))

    def SoundPath(self, filename):
        return str(self._ensure_file(self._sound_dir / filename, "Sound"))

    def ShaderText(self, filename):
        path = self._ensure_file(self._shaders_dir / filename, "Shader")
        return path.read_text(encoding="utf-8")