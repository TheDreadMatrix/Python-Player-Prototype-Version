import pygame


class GameRequest:
    def __init__(self, game):
        self.game = game

    def setTitle(self, title):
        pygame.display.set_caption(title)

    def restartScene(self):
        self.game.router._restartScene()

    def redirectScene(self, scene):
        self.game.router._current_scene_name = scene

    def closeGame(self):
        self.game._running = False


    @staticmethod
    def isQuiting(event):
        return event.type == pygame.QUIT 
    
    @staticmethod
    def isResized(event):
        return event.type == pygame.VIDEORESIZE
    
    