from supermarioworld.package_typing import EmptyScene, GameType
from supermarioworld.johnson import Johnson


class Cutscene_1(EmptyScene):
    def __init__(self, game: GameType):
        self.game = game

        self.account = Johnson(game.paths.DataPath(f"{game.data_settings_read["current-player-account-path"]}.json"))
        self.account_read = self.account.readData()
        if self.account_read["player"]["cutscened-1"]:
            self.game.request.redirectScene(self.account_read["overworld"]["current-overworld"])
        self.account_read["player"]["cutscened-1"] = True
        self.account.saveData(self.account_read)
            
        



    def onUpdate(self):
        return super().onUpdate()
    

    def onEvent(self, event):
        return super().onEvent(event)
    

    def onRender(self):
        return super().onRender()
    

    def onSave(self):
        return super().onSave()