class SceneStub:
    def onInitialization(self, game, **kwargs): ...
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
                    **scene.get("kwargs", {})
                )
            )


    def _post_init(self):

        # Registering START SCENE
        start_scene = self.game.settings.START_SCENE
        

        self._current_scene_name = start_scene

        self._manager_state = start_scene

        self._current_scene: SceneStub = self.scene_dict[start_scene]()
        self._current_scene.onInitialization(self.game, **self._current_scene._kwargs)

    @property
    def current(self):
        return self._current_scene

    @property
    def name(self):
        return self._current_scene_name

    
    def registerScene(self, name, scene_factory):
        self.scene_dict.update({name: scene_factory})


    def redirect(self, scene_name, namespace="base:"):
        self._current_scene_name = namespace + scene_name


    def restart(self):
        self._manager_state = self._current_scene_name
        
        self._current_scene.onSave()
        self.game.assets.releaseScene()
        self.game.renderer.releaseScene()

        self._current_scene = self.scene_dict.get(self._manager_state)()
        self._current_scene.onInitialization(self.game, **self._current_scene._kwargs)


    def save(self):
        self.game.settings.SAVE_CALLBACK()


    def update(self):
        state_scene = self._current_scene_name
        
        
        if state_scene != self._manager_state:
            self._current_scene.onSave()
            self.game.assets.releaseScene()
            self.game.renderer.releaseScene()
            
            self._current_scene = self.scene_dict.get(state_scene)()
            self._current_scene.onInitialization(self.game, **self._current_scene._kwargs)
            
            self._manager_state = state_scene


        self._current_scene.onUpdate()


    def event(self, event):
        self._current_scene.onEvent(event)



    def render(self):
        self._current_scene.onRender()   
          



