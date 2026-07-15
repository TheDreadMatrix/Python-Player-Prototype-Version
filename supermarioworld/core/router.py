


class SceneManager:
    def onLoad(self, game):
        pass

    def onInitScene(self, game):
        pass

    def _postInitScene(self):
        start_scene = self.game._run_scene or self.START_SCENE

        self.game._scene_name = start_scene
        self._manager_state = start_scene
        self._current_scene = self.scene_dict.get(start_scene)()


    def __init__(self, game):
        self.game = game

        self.START_SCENE = self.game._scene_name

        self._manager_state = ""
        self._current_scene = None
        self.scene_dict = {}

    
    def registerScene(self, name, scene_factory):
        self.scene_dict.update({name: scene_factory})


    def _restartScene(self):
        self._manager_state = self.game.getScene()
        
        self._current_scene.onSave()
        self._current_scene = None
        self._current_scene = self.scene_dict.get(self._manager_state)()


    def save(self):
        pass


    def update(self):
        state_scene = self.game.getScene()
        
        
            
        if state_scene != self._manager_state:
            self._current_scene.onSave()
            self._current_scene.assets.releaseScene()
            self._current_scene = self.scene_dict.get(state_scene)()
            self._manager_state = state_scene


        self._current_scene.onUpdate()


    def event(self, event):
        self._current_scene.onEvent(event)



    def render(self):
        self._current_scene.onRender()   
          



