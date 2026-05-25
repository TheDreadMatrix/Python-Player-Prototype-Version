import pygame as pg



class AudioStream:
    def __init__(self, resources):
        self.resources = resources
        self.played = False
        self.passed = False

    def load(self, music_key):
        pg.mixer.music.load(self.resources.musics[music_key])
        self.played = False
        self.passed = False

    def play(self, starts=0, fade_in=0, loops=0):
        if not self.played:
            pg.mixer.music.play(loops, starts, 1000 * fade_in)
            self.played = True


    def fadeOut(self, fade_out):
        if not self.passed:
            pg.mixer.music.fadeout(1000 * fade_out)
            self.passed = True


    def pause(self):
        pg.mixer.music.pause()

    def unpause(self):
        pg.mixer.music.unpause()

    def stop(self):
        pg.mixer.music.stop()

    def setVolume(self, volume):
        pg.mixer.music.set_volume(volume)


    def giveSound(self, sound_key):
        return self.resources.sounds[sound_key]