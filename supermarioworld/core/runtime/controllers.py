import pygame as pg


class Keyboard:
    def __init__(self):
        self._keys = None

    def update(self):
        self._keys = pg.key.get_pressed()

    def isPressed(self, key):
        return self._keys[key]

    def isDown(self, key, event):
        return event.type == pg.KEYDOWN and event.key == key
    

    def isUp(self, key, event):
        return event.type == pg.KEYUP and event.key == key




class Mouse:
    def __init__(self):
        pass