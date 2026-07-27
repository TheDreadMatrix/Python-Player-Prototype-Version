import pygame


class GameRequest:

    @staticmethod
    def setTitle(title): pygame.display.set_caption(title)


    @staticmethod
    def isQuiting(event):
        return event.type == pygame.QUIT 
    
    @staticmethod
    def isResized(event):
        return event.type == pygame.VIDEORESIZE
    
    