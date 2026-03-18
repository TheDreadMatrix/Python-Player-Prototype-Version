import typing
from MyGame.requirements import mgl


class ProgramsType(typing.Protocol):
    class ShaderConstant(typing.Protocol):
        IN_POS: str
        IN_UV: str
        IN_TEXT_POS: str
        IN_TEXT_OFFSET: str
    
    GLSL: ShaderConstant
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
