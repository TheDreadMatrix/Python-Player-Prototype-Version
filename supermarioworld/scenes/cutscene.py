from supermarioworld.package_typing import GameType
from supermarioworld.scenes.base import EmptyScene



class CutsceneScene(EmptyScene):
    def __init__(self, game: GameType, cutscene_id: str, redirect_scene: str):
        super().__init__(game=game)
        CURRENT_PLAYER = self.account.getCurrentPlayer()
        

        if CURRENT_PLAYER.hasPassedCutscene(cutscene_id):
            self.request.redirectScene(redirect_scene if not isinstance(redirect_scene, int) else CURRENT_PLAYER.current_overworld)
        else:
            CURRENT_PLAYER.setCutsceneAsWatched("cutscene-1")
            CURRENT_PLAYER.save()
            
        

    


    def onUpdate(self):
        return super().onUpdate()
    

    def onEvent(self, event):
        return super().onEvent(event)
    

    def onRender(self):
        self.game.clearColor(1, 0, 0)
    

    def onSave(self):
        return super().onSave()