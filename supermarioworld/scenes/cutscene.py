from supermarioworld.package_typing import EmptyScene, GameType
from supermarioworld.johnson import Johnson


class CutsceneScene(EmptyScene):
    def __init__(self, game: GameType):
        self.game = game

        self.account = Johnson(game.paths.CsavesPath(f"{game.settings_read["current-player"]}.json"))
        self.account_read = self.account.readData()

        if self.account_read["cutscene"]["cutscene-1"]:
            self.game.request.redirectScene(self.account_read["overworld"]["current-overworld"])

        self.account_read["cutscene"]["cutscene-1"] = True
        self.account.saveData(self.account_read)
            
        



    def onUpdate(self):
        return super().onUpdate()
    

    def onEvent(self, event):
        return super().onEvent(event)
    

    def onRender(self):
        return super().onRender()
    

    def onSave(self):
        return super().onSave()