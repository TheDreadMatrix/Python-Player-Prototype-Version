import typing
from supermarioworld.typing.renderer_type import BasicRenderer
from supermarioworld.typing.account_type import BasicAccount, BasicAccountManager
from supermarioworld.typing.runtime_type import BasicApi, BasicPath, BasicEvent, BasicSettings
from supermarioworld.typing.audio_type import BasicAudioEngine
from supermarioworld.typing.assets_type import BasicAssets
from supermarioworld.typing.controllers import BasicKeyboard, BasicMouse






class BasicI18N:
    def gettext(self, word_key: str) -> str: ...


class BasicRouter:
    def redirect(self, scene_name: str, namespace: str="base:") -> None: ...
    def restart(self) -> None: ...

    @property
    def current(self): ...

    @property
    def name(self) -> str: ...




class GameType(typing.Protocol):
    delta_time: float
    tick_time: float

    SCENE_DATA: dict[str, typing.Any]

    DEBUG: bool
    
    width: int
    height: int

    keyboard: BasicKeyboard
    mouse: BasicMouse

    renderer: BasicRenderer
    locale: BasicI18N

    request: BasicApi
    paths: BasicPath
    settings: BasicSettings

    assets: BasicAssets

    account: BasicAccountManager
    player: BasicAccount

    audio: BasicAudioEngine

    router: BasicRouter


    def getFps(self) -> float: ...
    def exit(self) -> None: ...
    def clearColor(self, r: float, g: float, b: float) -> None: ...

