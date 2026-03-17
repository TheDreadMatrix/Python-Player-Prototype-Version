import typing
from MyGame.requirements import mgl




class GameType(typing.Protocol):
    scene_name: str
    delta_time: float
    ctx: mgl.Context

    vertices: list
    indices: list

    width: int
    height: int
    def __init__(self): ...

    def getFps(self) -> float: ...

    def closeGame(self) -> None: ...
    def switchScene(self, scene_name: str) -> None: ...
    def setMode(self) -> None: ...
    def setCRTPP(self, flag: bool): ...
