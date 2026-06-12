import pygame as pg




class AudioStream:
    def __init__(self, game):
        self.game = game
        self.passed = False



    def load(self, music_key):
        try:
            pg.mixer.music.load(self.game.assets.musics[music_key])
            pg.mixer.music.set_volume(self.game.account.getMusicVolume())
        except KeyError:
            raise KeyError(f"Music with key '{music_key}' not found in resources.")
            
        self.passed = False

    def play(self, starts=0, fade_in=0, loops=0):
        pg.mixer.music.play(loops, starts, fade_in)
        


    def fadeOut(self, fade_out):
        if not self.passed:
            pg.mixer.music.fadeout(fade_out)
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
        return SoundStream(self.game, sound_key)
    



class SoundStream:
    def __init__(self, game, sound_key):
        self.game = game

        try:
            self.sound = pg.mixer.Sound(self.game.assets.sounds[sound_key])
            self.sound.set_volume(self.game.account.getSoundVolume())
        except KeyError:
            raise KeyError(f"Sound with key '{sound_key}' not found in resources.")
            

    def play(self, loops=0, fade_ms=0):
        self.sound.play(loops, fade_ms)


    def setVolume(self, volume):
        self.sound.set_volume(volume)