import typing
from MyGame.requirements import mgl


class ProgramsType(typing.Protocol):
    

    shader_textures: mgl.Program    
    shader_text: mgl.Program
    shader_pp: mgl.Program





class GameType(typing.Protocol):
    scene_name: str
    delta_time: float
    ctx: mgl.Context
    programs: ProgramsType 

    ebo: typing.Any
    vbo: typing.Any

    width: int
    height: int
    def __init__(self): ...

    def getFps(self) -> float: ...

    def closeGame(self) -> None: ...
    def switchScene(self, scene_name: str) -> None: ...
    def setMode(self) -> None: ...
    def setCRTPP(self, flag: bool): ...
