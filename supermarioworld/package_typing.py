import typing


class _RequestType(typing.Protocol):
    def showMouse(self, flag: bool) -> None: ...
    def closeGame(self) -> None: ...
    def redirectScene(self, scene: str) -> None: ...


class _PathsType(typing.Protocol):
    def ShaderPath(self, filename: str) -> str: ...
    def AssetPath(self, filename: str) -> str: ...
    def DataPath(self, filename: str) -> str: ...
    def MusicPath(self, filename: str) -> str: ...
    def SoundPath(Self, filename: str) -> str: ...
    def ShaderText(self, filename: str) -> str: ...


class GameType(typing.Protocol):
    delta_time: float
    
    width: int
    height: int

    request: _RequestType
    paths: _PathsType

    def getFps(self) -> float: ...
    def getScene(self) -> str: ...
    def setColorScreen(self, r: float, g: float, b: float) -> None: ...


class EmptyScene:
    def __init__(self, game: "GameType"):
        self.game = game

    def onUpdate(self): pass
    def onEvent(self, event): pass
    def onRender(self): pass
    def onSave(self): pass