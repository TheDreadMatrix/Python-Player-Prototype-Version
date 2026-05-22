from supermarioworld.johnson import Johnson


class PlayerAccountManager:
    def __init__(self, game):
        self.game = game

        self.settings = Johnson(game.paths.CsavesPath("settings.json"))
        self.settings_data = self.settings.readData()

        self.account_hash = {}

        self.loadCurrentPlayer()

    def getCurrentPlayer(self):
        
        return self.account_hash[self.settings_data["current-player"]]

    def getPlayerPath(self, slot: int):
        return self.game.paths.CsavesPath(
            f"player/player{slot}.json"
        )

    def loadPlayer(self, slot: int):
        path = self.getPlayerPath(slot)
        self.settings_data["current-player"] = slot
        self.account_hash.update({slot: PlayerAccount(path)})


    def loadCurrentPlayer(self):
        slot = self.settings_data["current-player"]

        self.loadPlayer(slot)

    
    def save(self):
        self.settings.saveData(self.settings_data)

    def setFps(self, fps):
        self.settings_data["frametime"] = fps

    def getFps(self): return self.settings_data["frametime"]
    def getSoundVolume(self): return self.settings_data["sound"]
    def getMusicVolume(self): return self.settings_data["music"]

    def setSoundVolume(self, volume):
        self.settings_data["sound"] = volume

    def setMusicVolume(self, volume):
        self.settings_data["music"] = volume





class PlayerAccount:
    def __init__(self, path: str):
        self._handler = Johnson(path)
        self.data = self._handler.readData()

    def getSlot(self): return self.data["player"]["slot"] 

    def save(self):
        self._handler.saveData(self.data)

    def hasPassedCutscene(self, name: str) -> bool:
        return self.data["cutscene"].get(name, None)
    
    def setCutsceneAsWatched(self, cutscene_id):
        self.data["cutscene"][cutscene_id] = True


    @property
    def coins(self):
        return self.data["player"]["coins"]
    
    @coins.setter
    def coins(self, value):
        self.data["player"]["coins"] = value
    
    @property
    def rcoins(self):
        return self.data["player"]["rcoins"]
    
    @rcoins.setter
    def rcoins(self, value):
        self.data["player"]["rcoins"] = value
    
    @property
    def points(self):
        return self.data["player"]["points"]
    
    @points.setter
    def points(self, value):
        self.data["player"]["points"] = value
    

    @property
    def lives(self):
        return self.data["player"]["lives"]

    @lives.setter
    def lives(self, value):
        self.data["player"]["lives"] = value

    
    @property
    def time_in_game(self):
        return self.data["player"]["time-in-game"]
    
    @time_in_game.setter
    def time_in_game(self, value):
        self.data["player"]["time-in-game"] = value
    
    @property
    def passed_level_count(self):
        return self.data["player"]["passed-level-count"]
    
    @passed_level_count.setter
    def passed_level_count(self, value):
        self.data["player"]["passed-level-count"] = value
    
    @property
    def current_powerup(self):
        return self.data["player"]["current-form"]
    
    @current_powerup.setter
    def current_powerup(self, value):
        self.data["player"]["current-form"] = value
    
    @property
    def current_character(self):
        return self.data["player"]["current-char"]

    @current_character.setter
    def current_character(self, value):
        self.data["player"]["current-char"] = value
    
    @property
    def current_overworld(self):
        return self.data["overworld"]["current-overworld"]
    
    @current_overworld.setter
    def current_overworld(self, value):
        self.data["overworld"]["current-overworld"] = value
    
    @property
    def current_overworld_level(self):
        return self.data["overworld"]["current-level"]
    
    @current_overworld_level.setter
    def current_overworld_level(self, value):
        self.data["overworld"]["current-level"] = value
    
    @property
    def unlocked_overworld_level_ls(self):
        return self.data["overworld"]["unlocked-level"]
    
    @unlocked_overworld_level_ls.setter
    def unlocked_overworld_level_ls(self, value):
        self.data["overworld"]["unlocked-level"] = value