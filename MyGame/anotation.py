import typing


class _RequestType(typing.Protocol):
    def showMouse(self) -> None: ...
    def closeGame(self) -> None: ...
    def redirectScene(self, scene: str) -> None: ...



class GameType(typing.Protocol):
    delta_time: float
    
    width: int
    height: int

    request: _RequestType

    def getFps(self) -> float: ...
