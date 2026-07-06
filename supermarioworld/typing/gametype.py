import typing
from supermarioworld.typing.renderer_type import BasicRenderer
from supermarioworld.typing.account_type import BasicAccount, BasicAccountManager
from supermarioworld.typing.runtime_type import BasicApi, BasicPath
from supermarioworld.typing.audio_type import BasicAudioEngine
from supermarioworld.typing.assets_type import BasicAssets






class BasicI18N:
    def gettext(self, word_key: str) -> str: ...


class BasicEvent(typing.Protocol):
    type: typing.Any
    key: int




class GameType(typing.Protocol):
    delta_time: float
    tick_time: float
    SCENE_DATA: dict[str, typing.Any]
    DEBUG: bool
    
    width: int
    height: int

    renderer: BasicRenderer
    locale: BasicI18N

    request: BasicApi
    paths: BasicPath
    assets: BasicAssets

    account: BasicAccountManager
    player: BasicAccount

    audio: BasicAudioEngine


    def getFps(self) -> float: ...
    def getScene(self) -> str: ...
    def clearColor(self, r: float, g: float, b: float) -> None: ...

