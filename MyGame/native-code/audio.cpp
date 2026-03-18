
#include <soloud.h>




class AudioEngine{
    public:
        SoLoud::Soloud AEngine;

        AudioEngine(){
            AEngine.init();
        }

        ~AudioEngine(){
            AEngine.deinit();
        }


        int play(){}
};
