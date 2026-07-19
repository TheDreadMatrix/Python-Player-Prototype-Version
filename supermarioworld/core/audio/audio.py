from supermarioworld.core.audio.soloud import Wav, WavStream, Soloud, BiquadResonantFilter


class AudioStream:
    def __init__(self, game):
        self.game = game
        self.passed = False

        self.engine = Soloud()
        self.engine.init()

        self.low_pass_filter = BiquadResonantFilter()
        self.low_pass_filter.set_params(BiquadResonantFilter.LOWPASS, self.game.settings.LOWPASS_PARAMETR, 1)

        self.engine.set_global_filter(0, self.low_pass_filter)



        self.music_handle = None
        self.music = None


    def setFilterLowPass(self, parametr):
        self.low_pass_filter.set_params(BiquadResonantFilter.LOWPASS, parametr, 1)
        self.engine.set_global_filter(0, self.low_pass_filter)



    def load(self, music_key):
        if self.music_handle is not None:
            self.engine.stop_all()
        path = self.game.assets.musics.get(music_key, "stupid-player-you-put-undefined-key.mp3")

        wav = WavStream()
        wav.load(path)

        self.music_handle = None
        self.music = wav
    
        

    def play(self, loop=True):
        wav = self.music

        self.music_handle = self.engine.play(wav, aVolume=self.game.account.getMusicVolume())

       
        wav.set_looping(loop)
        
        self.passed = False
        


    def fadeOut(self, ms):
        if self.music_handle is not None and not self.passed:
            self.engine.fade_volume(self.music_handle, 0.0, ms / 1000)
            self.passed = True


    def pause(self):
        if self.music_handle is not None:
            self.engine.set_pause(self.music_handle, True)

    def unpause(self):
        if self.music_handle is not None:
            self.engine.set_pause(self.music_handle, False)

    def stop(self):
        if self.music_handle is not None:
            self.engine.stop(self.music_handle)

    def setVolume(self, volume):
        self.engine.set_volume(0, volume)


    def giveSound(self, sound_key):
        return SoundStream(self.game, self.engine, sound_key)
    



class SoundStream:
    def __init__(self, game, audio_stream: Soloud, sound_key):
        self.game = game
        self.audio = audio_stream

        path = self.game.assets.sounds.get(sound_key, "")

        self.sound = Wav()
        self.sound.load(path)

        self.handle = None
            

    def play(self):
        self.handle = self.audio.play(self.sound)
        self.audio.set_volume(self.handle, self.game.account.getSoundVolume())
        


    def setVolume(self, volume):
        if self.handle is not None:
            self.audio.set_volume(self.handle, volume)