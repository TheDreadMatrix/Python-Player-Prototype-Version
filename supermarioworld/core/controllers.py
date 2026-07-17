import pygame as pg


class Keyboard:
    def __init__(self):
        self._keys = None

    def _update(self):
        self._keys = pg.key.get_pressed()


    def pressed(self, key):
        return self._keys[key]

    def pressedDown(self, key, event):
        pass

    def pressedUp(self, key, event):
        pass




class Mouse:
    def __init__(self):
        pass