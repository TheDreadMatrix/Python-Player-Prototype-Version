class SceneStub:
    def onUpdate(self): ...
    def onEvent(self, event): ...
    def onRender(self): ...
    def onSave(self): ...


class SceneManager:
    def __init__(self, game):
        self.game = game
       
        self.scene_dict = {}

        # Adding scenes to dict
        for name, scene in game.settings.SCENES.items():
            self.registerScene(
                name,
                lambda scene=scene, name=name: scene["class"](
                    game=game, scene_name=name,
                    **scene["kwargs"]
                )
            )

        # Registering START SCENE
        start_scene = game.settings.START_SCENE
        

        self._current_scene_name = start_scene

        self._manager_state = start_scene

        self._current_scene: SceneStub = self.scene_dict[start_scene]()

    
    def registerScene(self, name, scene_factory):
        self.scene_dict.update({name: scene_factory})


    def _restartScene(self):
        self._manager_state = self._current_scene_name
        
        self._current_scene.onSave()
        self.game.assets.releaseScene()
        self.game.renderer.releaseScene()
        self._current_scene = self.scene_dict.get(self._manager_state)()


    def save(self):
        self.game.settings.SAVE_CALLBACK()


    def update(self):
        state_scene = self._current_scene_name
        
        
        if state_scene != self._manager_state:
            self._current_scene.onSave()
            self.game.assets.releaseScene()
            self.game.renderer.releaseScene()
            self._current_scene = self.scene_dict.get(state_scene)()
            
            self._manager_state = state_scene


        self._current_scene.onUpdate()


    def event(self, event):
        self._current_scene.onEvent(event)



    def render(self):
        self._current_scene.onRender()   
          



