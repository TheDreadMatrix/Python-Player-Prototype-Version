import pygame


class GameRequest:
    def __init__(self, game):
        self.game = game

    def setTitle(self, title):
        pygame.display.set_caption(title)


    @staticmethod
    def isQuiting(event):
        return event.type == pygame.QUIT 
    
    @staticmethod
    def isResized(event):
        return event.type == pygame.VIDEORESIZE
    
    