from supermarioworld.johnson import Johnson

DEFAULT_PROFILE = {
    "current-character": "martis",
    "current-state": "small",
    "what-in-packet": None,
    "lives": 5,
    "coins": 0,
    "points": 0,
    "datetime": None,
    "time-in-game": 0,
    "passed-levels": 0
}

DEFAULT_OVERWORLD = {
    "active": "overworld-1",
    "worlds": {
        "overworld-1": {
            "current-node": "start",
            "nodes": {}
        },
        
        "overworld-2": {
            "current-node": "start",
            "nodes": {}
        },

        "overworld-3": {
            "current-node": "start",
            "nodes": {}
        },

        "overworld-4": {
            "current-node": "start",
            "nodes": {}
        },

        "overworld-star": {
            "current-node": "start",
            "nodes": {}
        }
    }
}


def apply_defaults(data, defaults):
    for key, value in defaults.items():

        if key not in data:

            if isinstance(value, dict):
                data[key] = value.copy()
            else:
                data[key] = value

        elif isinstance(value, dict) and isinstance(data[key], dict):
            apply_defaults(data[key], value)

    return data


class PlayerAccountManager:
    _MAX_SLOTS = 3

    def __init__(self, game):
        self.game = game

        self.settings = Johnson(game.paths.CsavesPath("settings.json"))
        self.settings_data = self.settings.readData()

        self.current_account = None

        self._account_hashers = {slot:PlayerSlot(game=game, slot=slot) for slot in range(self._MAX_SLOTS)}

        self._loadCurrentPlayer()
        

        
    
    def loadPlayer(self, slot: int):
        if self.current_account is not None:
            self.current_account.save()

        self.settings_data["current-player"] = slot

        self.current_account = self._account_hashers.get(slot, PlayerSlot(game=self.game, slot=0))


    # Save and load
    def _loadCurrentPlayer(self): self.loadPlayer(self.settings_data.get("current-player", 0))

    def save(self): self.settings.saveData(self.settings_data)

    
    # Get
    def getLanguage(self): return self.settings_data.get("language", "ENG")
    def getFps(self): return self.settings_data.get("frametime", 60)
    def getSoundVolume(self): return self.settings_data.get("sound", 1.0)
    def getMusicVolume(self): return self.settings_data.get("music", 1.0)

    # Set
    def setLanguage(self, language): self.settings_data["language"] = language
    def setFps(self, fps): self.settings_data["frametime"] = fps
    def setSoundVolume(self, volume): self.settings_data["sound"] = volume
    def setMusicVolume(self, volume): self.settings_data["music"] = volume

    def __repr__(self):
        return f"{self.settings_data["current-player"]}"



class PlayerSlot:
    def __init__(self, game, slot):

        self._profile = Johnson(game.paths.CsavesPath(f"player/player-{slot}/profile.json"))
        self._profile_data = self._profile.readData()

        self._profile_data = apply_defaults(self._profile_data, DEFAULT_PROFILE)


        self._overworld = Johnson(game.paths.CsavesPath(f"player/player-{slot}/overworld.json"))
        self._overworld_data = self._overworld.readData()

        self._overworld_data = apply_defaults(self._overworld_data, DEFAULT_OVERWORLD)

        # Pushing our slot
        self._profile_data["slot"] = slot

    

    def getSlot(self):
        return self._profile_data["slot"]
    

    # Open nodes 
    def openOverworldNode(self, node_id):
        active_world = self._overworld_data["active"]
        self._overworld_data["worlds"][active_world]["nodes"][node_id] = True

    def hasOverworldNodeOpened(self, node_id):
        active_world = self._overworld_data["active"]
        return self._overworld_data["worlds"][active_world]["nodes"].get(node_id, False)

    # Saving data
    def save(self):
        self._profile.saveData(self._profile_data)
        self._overworld.saveData(self._overworld_data)

    
    # Profile end
    @property
    def coins(self):
        return self._profile_data["coins"]
    
    @coins.setter
    def coins(self, value):
        self._profile_data["coins"] = value
    
    
    @property
    def points(self):
        return self._profile_data["points"]
    
    @points.setter
    def points(self, value):
        self._profile_data["points"] = value
    

    @property
    def lives(self):
        return self._profile_data["lives"]

    @lives.setter
    def lives(self, value):
        self._profile_data["lives"] = value

    
    @property
    def time_in_game(self):
        return self._profile_data["time-in-game"]
    
    @time_in_game.setter
    def time_in_game(self, value):
        self._profile_data["time-in-game"] = value
    
    @property
    def passed_level_count(self):
        return self._profile_data["passed-levels"]
    
    @passed_level_count.setter
    def passed_level_count(self, value):
        self._profile_data["passed-levels"] = value
    
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
    

    # Overworld end
    @property
    def current_overworld(self):
        return self._overworld_data["active"]
    
    @current_overworld.setter
    def current_overworld(self, value):
        self._overworld_data["active"] = value
    
    @property
    def current_overworld_level(self):
        active_world = self._overworld_data["active"]
        return self._overworld_data["worlds"][active_world]["current-node"]
    
    @current_overworld_level.setter
    def current_overworld_level(self, value):
        active_world = self._overworld_data["active"]
        self._overworld_data["worlds"][active_world]["current-node"] = value
    

    @property
    def current_overworld_camera_pos(self):
        active_world = self._overworld_data["active"]
        return self._overworld_data["worlds"][active_world].get("camera-pos", (0, 0))
    
    @current_overworld_camera_pos.setter
    def current_overworld_camera_pos(self, value):
        active_world = self._overworld_data["active"]
        self._overworld_data["worlds"][active_world]["camera-pos"] = value


    def __repr__(self):
        return f"<PlayerSlot - {self._profile_data["slot"]}>"

    
    





class PlayerAccount:
    def __init__(self, path: str):
        self._handler = Johnson(path)
        self.data = self._handler.readData()

    def getSlot(self): return self.data["player"]["slot"] 

    def save(self):
        self._handler.saveData(self.data)


    def openOverworldNode(self, node_id):
        active_world = self.data["overworld"]["active"]
        self.data["overworld"]["worlds"][active_world]["nodes"][node_id] = True

    def hasOverworldNodeOpened(self, node_id):
        active_world = self.data["overworld"]["active"]
        return self.data["overworld"]["worlds"][active_world]["nodes"].get(node_id, False)




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
        return self.data["overworld"]["active"]
    
    @current_overworld.setter
    def current_overworld(self, value):
        self.data["overworld"]["active"] = value
    
    @property
    def current_overworld_level(self):
        active_world = self.data["overworld"]["active"]
        return self.data["overworld"]["worlds"][active_world]["current-level"]
    
    @current_overworld_level.setter
    def current_overworld_level(self, value):
        active_world = self.data["overworld"]["active"]
        self.data["overworld"]["worlds"][active_world]["current-level"] = value
    

    @property
    def current_overworld_camera_pos(self):
        active_world = self.data["overworld"]["active"]
        return self.data["overworld"]["worlds"][active_world].get("camera-pos", [0, 0])
    
    @current_overworld_camera_pos.setter
    def current_overworld_camera_pos(self, value):
        active_world = self.data["overworld"]["active"]
        self.data["overworld"]["worlds"][active_world]["camera-pos"] = value


    def __repr__(self):
        return f"<PlayerAccount - {self.getSlot()}>"