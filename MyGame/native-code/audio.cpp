
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "soloud.h"
#include "soloud_wav.h"
#include "soloud_biquadresonantfilter.h"

#include <string>
#include <cstring>

namespace
{
	constexpr unsigned int kLowpassSlot = 0;

	static PyObject *raise_runtime(const char *msg)
	{
		PyErr_SetString(PyExc_RuntimeError, msg);
		return nullptr;
	}

	static PyObject *raise_value(const char *msg)
	{
		PyErr_SetString(PyExc_ValueError, msg);
		return nullptr;
	}

	struct PyAudioEngine
	{
		PyObject_HEAD
		SoLoud::Soloud *engine;
		bool alive;
	};

	struct PySound
	{
		PyObject_HEAD
		SoLoud::Wav *wav;
		SoLoud::BiquadResonantFilter *lowpass;
	};

	struct PyVoice
	{
		PyObject_HEAD
		PyAudioEngine *engine;
		SoLoud::handle handle;
		bool valid;
	};

	static PyTypeObject PyAudioEngine_Type;
	static PyTypeObject PySound_Type;
	static PyTypeObject PyVoice_Type;

	static bool ensure_engine_alive(PyAudioEngine *self)
	{
		if (!self->engine || !self->alive)
		{
			PyErr_SetString(PyExc_RuntimeError, "AudioEngine is not initialized");
			return false;
		}
		return true;
	}

	static bool ensure_voice_valid(PyVoice *self)
	{
		if (!self->engine || !self->valid || !self->engine->engine)
		{
			PyErr_SetString(PyExc_RuntimeError, "Voice is not valid");
			return false;
		}
		if (!self->engine->engine->isValidVoiceHandle(self->handle))
		{
			PyErr_SetString(PyExc_RuntimeError, "Voice handle is no longer valid");
			return false;
		}
		return true;
	}
}

// AudioEngine ---------------------------------------------------------

static PyObject *AudioEngine_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
	PyAudioEngine *self = reinterpret_cast<PyAudioEngine *>(type->tp_alloc(type, 0));
	if (!self)
		return nullptr;
	self->engine = nullptr;
	self->alive = false;
	return reinterpret_cast<PyObject *>(self);
}

static int AudioEngine_init(PyAudioEngine *self, PyObject *args, PyObject *kwargs)
{
	static const char *kwlist[] = {"sample_rate", "buffer_size", "channels", "backend", nullptr};
	unsigned int sample_rate = 44100;
	unsigned int buffer_size = 512;
	unsigned int channels = 2;
	const char *backend = "miniaudio";

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|IIIs", const_cast<char **>(kwlist),
									 &sample_rate, &buffer_size, &channels, &backend))
	{
		return -1;
	}

	if (channels == 0 || channels > 8)
	{
		PyErr_SetString(PyExc_ValueError, "channels must be in range 1..8");
		return -1;
	}

	self->engine = new SoLoud::Soloud();
	unsigned int backend_id = SoLoud::Soloud::AUTO;
	if (backend && strcmp(backend, "miniaudio") == 0)
	{
		backend_id = SoLoud::Soloud::MINIAUDIO;
	}

	const unsigned int flags = SoLoud::Soloud::CLIP_ROUNDOFF;
	SoLoud::result res = self->engine->init(flags, backend_id, sample_rate, buffer_size, channels);
	if (res != SoLoud::SO_NO_ERROR)
	{
		delete self->engine;
		self->engine = nullptr;
		PyErr_Format(PyExc_RuntimeError, "SoLoud init failed (code %u)", res);
		return -1;
	}

	self->alive = true;
	return 0;
}

static void AudioEngine_dealloc(PyAudioEngine *self)
{
	if (self->engine)
	{
		self->engine->deinit();
		delete self->engine;
		self->engine = nullptr;
	}
	self->alive = false;
	Py_TYPE(self)->tp_free(reinterpret_cast<PyObject *>(self));
}

static PyObject *AudioEngine_play(PyAudioEngine *self, PyObject *args, PyObject *kwargs)
{
	static const char *kwlist[] = {"sound", "volume", "pan", "speed", "paused", nullptr};
	PyObject *sound_obj = nullptr;
	float volume = 1.0f;
	float pan = 0.0f;
	float speed = 1.0f;
	int paused = 0;

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|fffi", const_cast<char **>(kwlist),
									 &sound_obj, &volume, &pan, &speed, &paused))
	{
		return nullptr;
	}

	if (!ensure_engine_alive(self))
		return nullptr;

	if (!PyObject_TypeCheck(sound_obj, &PySound_Type))
		return raise_value("sound must be a Sound instance");

	PySound *sound = reinterpret_cast<PySound *>(sound_obj);
	if (!sound->wav)
		return raise_runtime("Sound is not loaded");

	SoLoud::handle handle = self->engine->play(*sound->wav, volume, pan, paused != 0);
	if (speed != 1.0f)
	{
		self->engine->setRelativePlaySpeed(handle, speed);
	}

	PyVoice *voice = PyObject_New(PyVoice, &PyVoice_Type);
	if (!voice)
		return nullptr;
	Py_INCREF(self);
	voice->engine = self;
	voice->handle = handle;
	voice->valid = true;
	return reinterpret_cast<PyObject *>(voice);
}

static PyObject *AudioEngine_stop_all(PyAudioEngine *self, PyObject *args)
{
	(void)args;
	if (!ensure_engine_alive(self))
		return nullptr;
	self->engine->stopAll();
	Py_RETURN_NONE;
}

static PyObject *AudioEngine_set_global_volume(PyAudioEngine *self, PyObject *args)
{
	float volume = 1.0f;
	if (!PyArg_ParseTuple(args, "f", &volume))
		return nullptr;
	if (!ensure_engine_alive(self))
		return nullptr;
	self->engine->setGlobalVolume(volume);
	Py_RETURN_NONE;
}

static PyObject *AudioEngine_fade_global_volume(PyAudioEngine *self, PyObject *args)
{
	float target = 1.0f;
	float time_sec = 0.0f;
	if (!PyArg_ParseTuple(args, "ff", &target, &time_sec))
		return nullptr;
	if (!ensure_engine_alive(self))
		return nullptr;
	self->engine->fadeGlobalVolume(target, time_sec);
	Py_RETURN_NONE;
}

static PyMethodDef AudioEngine_methods[] = {
	{"play", reinterpret_cast<PyCFunction>(AudioEngine_play), METH_VARARGS | METH_KEYWORDS, "Play a Sound and return a Voice"},
	{"stop_all", reinterpret_cast<PyCFunction>(AudioEngine_stop_all), METH_VARARGS, "Stop all voices"},
	{"set_global_volume", reinterpret_cast<PyCFunction>(AudioEngine_set_global_volume), METH_VARARGS, "Set global volume"},
	{"fade_global_volume", reinterpret_cast<PyCFunction>(AudioEngine_fade_global_volume), METH_VARARGS, "Fade global volume"},
	{nullptr, nullptr, 0, nullptr}};

// Sound ---------------------------------------------------------------

static PyObject *Sound_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
	PySound *self = reinterpret_cast<PySound *>(type->tp_alloc(type, 0));
	if (!self)
		return nullptr;
	self->wav = nullptr;
	self->lowpass = nullptr;
	return reinterpret_cast<PyObject *>(self);
}

static int Sound_init(PySound *self, PyObject *args, PyObject *kwargs)
{
	static const char *kwlist[] = {"path", "loop", "volume", nullptr};
	const char *path = nullptr;
	int loop = 0;
	float volume = 1.0f;

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|if", const_cast<char **>(kwlist),
									 &path, &loop, &volume))
	{
		return -1;
	}

	self->wav = new SoLoud::Wav();
	SoLoud::result res = self->wav->load(path);
	if (res != SoLoud::SO_NO_ERROR)
	{
		delete self->wav;
		self->wav = nullptr;
		PyErr_Format(PyExc_RuntimeError, "Failed to load audio file: %s (code %u)", path, res);
		return -1;
	}

	self->wav->setLooping(loop != 0);
	self->wav->setVolume(volume);

	self->lowpass = new SoLoud::BiquadResonantFilter();
	self->lowpass->setParams(SoLoud::BiquadResonantFilter::LOWPASS, 1000.0f, 1.0f);
	self->lowpass->setFilterParameter(SoLoud::BiquadResonantFilter::WET, 0.0f);
	self->wav->setFilter(kLowpassSlot, self->lowpass);

	return 0;
}

static void Sound_dealloc(PySound *self)
{
	if (self->wav)
	{
		delete self->wav;
		self->wav = nullptr;
	}
	if (self->lowpass)
	{
		delete self->lowpass;
		self->lowpass = nullptr;
	}
	Py_TYPE(self)->tp_free(reinterpret_cast<PyObject *>(self));
}

static PyObject *Sound_set_looping(PySound *self, PyObject *args)
{
	int loop = 0;
	if (!PyArg_ParseTuple(args, "p", &loop))
		return nullptr;
	if (!self->wav)
		return raise_runtime("Sound is not loaded");
	self->wav->setLooping(loop != 0);
	Py_RETURN_NONE;
}

static PyObject *Sound_set_volume(PySound *self, PyObject *args)
{
	float volume = 1.0f;
	if (!PyArg_ParseTuple(args, "f", &volume))
		return nullptr;
	if (!self->wav)
		return raise_runtime("Sound is not loaded");
	self->wav->setVolume(volume);
	Py_RETURN_NONE;
}

static PyObject *Sound_set_lowpass(PySound *self, PyObject *args, PyObject *kwargs)
{
	static const char *kwlist[] = {"freq", "resonance", "wet", nullptr};
	float freq = 1000.0f;
	float resonance = 1.0f;
	float wet = 1.0f;

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "f|ff", const_cast<char **>(kwlist),
									 &freq, &resonance, &wet))
	{
		return nullptr;
	}

	if (!self->lowpass)
		return raise_runtime("Lowpass filter is not initialized");

	self->lowpass->setParams(SoLoud::BiquadResonantFilter::LOWPASS, freq, resonance);
	self->lowpass->setFilterParameter(SoLoud::BiquadResonantFilter::WET, wet);
	Py_RETURN_NONE;
}

static PyObject *Sound_clear_lowpass(PySound *self, PyObject *args)
{
	(void)args;
	if (!self->lowpass)
		return raise_runtime("Lowpass filter is not initialized");
	self->lowpass->setFilterParameter(SoLoud::BiquadResonantFilter::WET, 0.0f);
	Py_RETURN_NONE;
}

static PyObject *Sound_length(PySound *self, PyObject *args)
{
	(void)args;
	if (!self->wav)
		return raise_runtime("Sound is not loaded");
	return PyFloat_FromDouble(self->wav->getLength());
}

static PyMethodDef Sound_methods[] = {
	{"set_looping", reinterpret_cast<PyCFunction>(Sound_set_looping), METH_VARARGS, "Enable or disable looping"},
	{"set_volume", reinterpret_cast<PyCFunction>(Sound_set_volume), METH_VARARGS, "Set default volume"},
	{"set_lowpass", reinterpret_cast<PyCFunction>(Sound_set_lowpass), METH_VARARGS | METH_KEYWORDS, "Configure lowpass filter"},
	{"clear_lowpass", reinterpret_cast<PyCFunction>(Sound_clear_lowpass), METH_VARARGS, "Disable lowpass filter"},
	{"length", reinterpret_cast<PyCFunction>(Sound_length), METH_VARARGS, "Return sound length in seconds"},
	{nullptr, nullptr, 0, nullptr}};

// Voice ---------------------------------------------------------------

static PyObject *Voice_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
	(void)args;
	(void)kwargs;
	PyVoice *self = reinterpret_cast<PyVoice *>(type->tp_alloc(type, 0));
	if (!self)
		return nullptr;
	self->engine = nullptr;
	self->handle = 0;
	self->valid = false;
	return reinterpret_cast<PyObject *>(self);
}

static void Voice_dealloc(PyVoice *self)
{
	if (self->engine)
	{
		Py_DECREF(self->engine);
		self->engine = nullptr;
	}
	self->valid = false;
	Py_TYPE(self)->tp_free(reinterpret_cast<PyObject *>(self));
}

static PyObject *Voice_stop(PyVoice *self, PyObject *args)
{
	(void)args;
	if (!ensure_voice_valid(self))
		return nullptr;
	self->engine->engine->stop(self->handle);
	Py_RETURN_NONE;
}

static PyObject *Voice_pause(PyVoice *self, PyObject *args)
{
	int paused = 1;
	if (!PyArg_ParseTuple(args, "|p", &paused))
		return nullptr;
	if (!ensure_voice_valid(self))
		return nullptr;
	self->engine->engine->setPause(self->handle, paused != 0);
	Py_RETURN_NONE;
}

static PyObject *Voice_set_volume(PyVoice *self, PyObject *args)
{
	float volume = 1.0f;
	if (!PyArg_ParseTuple(args, "f", &volume))
		return nullptr;
	if (!ensure_voice_valid(self))
		return nullptr;
	self->engine->engine->setVolume(self->handle, volume);
	Py_RETURN_NONE;
}

static PyObject *Voice_set_pan(PyVoice *self, PyObject *args)
{
	float pan = 0.0f;
	if (!PyArg_ParseTuple(args, "f", &pan))
		return nullptr;
	if (!ensure_voice_valid(self))
		return nullptr;
	self->engine->engine->setPan(self->handle, pan);
	Py_RETURN_NONE;
}

static PyObject *Voice_set_speed(PyVoice *self, PyObject *args)
{
	float speed = 1.0f;
	if (!PyArg_ParseTuple(args, "f", &speed))
		return nullptr;
	if (!ensure_voice_valid(self))
		return nullptr;
	self->engine->engine->setRelativePlaySpeed(self->handle, speed);
	Py_RETURN_NONE;
}

static PyObject *Voice_fade_volume(PyVoice *self, PyObject *args)
{
	float target = 1.0f;
	float time_sec = 0.0f;
	if (!PyArg_ParseTuple(args, "ff", &target, &time_sec))
		return nullptr;
	if (!ensure_voice_valid(self))
		return nullptr;
	self->engine->engine->fadeVolume(self->handle, target, time_sec);
	Py_RETURN_NONE;
}

static PyObject *Voice_fade_pan(PyVoice *self, PyObject *args)
{
	float target = 0.0f;
	float time_sec = 0.0f;
	if (!PyArg_ParseTuple(args, "ff", &target, &time_sec))
		return nullptr;
	if (!ensure_voice_valid(self))
		return nullptr;
	self->engine->engine->fadePan(self->handle, target, time_sec);
	Py_RETURN_NONE;
}

static PyObject *Voice_fade_speed(PyVoice *self, PyObject *args)
{
	float target = 1.0f;
	float time_sec = 0.0f;
	if (!PyArg_ParseTuple(args, "ff", &target, &time_sec))
		return nullptr;
	if (!ensure_voice_valid(self))
		return nullptr;
	self->engine->engine->fadeRelativePlaySpeed(self->handle, target, time_sec);
	Py_RETURN_NONE;
}

static PyObject *Voice_set_lowpass(PyVoice *self, PyObject *args, PyObject *kwargs)
{
	static const char *kwlist[] = {"freq", "resonance", "wet", nullptr};
	float freq = 1000.0f;
	float resonance = 1.0f;
	float wet = 1.0f;

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "f|ff", const_cast<char **>(kwlist),
									 &freq, &resonance, &wet))
	{
		return nullptr;
	}

	if (!ensure_voice_valid(self))
		return nullptr;

	self->engine->engine->setFilterParameter(self->handle, kLowpassSlot, SoLoud::BiquadResonantFilter::FREQUENCY, freq);
	self->engine->engine->setFilterParameter(self->handle, kLowpassSlot, SoLoud::BiquadResonantFilter::RESONANCE, resonance);
	self->engine->engine->setFilterParameter(self->handle, kLowpassSlot, SoLoud::BiquadResonantFilter::WET, wet);
	Py_RETURN_NONE;
}

static PyObject *Voice_set_lowpass_wet(PyVoice *self, PyObject *args)
{
	float wet = 0.0f;
	if (!PyArg_ParseTuple(args, "f", &wet))
		return nullptr;
	if (!ensure_voice_valid(self))
		return nullptr;
	self->engine->engine->setFilterParameter(self->handle, kLowpassSlot, SoLoud::BiquadResonantFilter::WET, wet);
	Py_RETURN_NONE;
}

static PyObject *Voice_is_valid(PyVoice *self, PyObject *args)
{
	(void)args;
	if (!self->engine || !self->engine->engine)
		Py_RETURN_FALSE;
	if (!self->engine->engine->isValidVoiceHandle(self->handle))
		Py_RETURN_FALSE;
	Py_RETURN_TRUE;
}

static PyObject *Voice_is_paused(PyVoice *self, PyObject *args)
{
	(void)args;
	if (!ensure_voice_valid(self))
		return nullptr;
	if (self->engine->engine->getPause(self->handle))
		Py_RETURN_TRUE;
	Py_RETURN_FALSE;
}

static PyObject *Voice_get_volume(PyVoice *self, PyObject *args)
{
	(void)args;
	if (!ensure_voice_valid(self))
		return nullptr;
	return PyFloat_FromDouble(self->engine->engine->getVolume(self->handle));
}

static PyObject *Voice_get_pan(PyVoice *self, PyObject *args)
{
	(void)args;
	if (!ensure_voice_valid(self))
		return nullptr;
	return PyFloat_FromDouble(self->engine->engine->getPan(self->handle));
}

static PyObject *Voice_get_speed(PyVoice *self, PyObject *args)
{
	(void)args;
	if (!ensure_voice_valid(self))
		return nullptr;
	return PyFloat_FromDouble(self->engine->engine->getRelativePlaySpeed(self->handle));
}

static PyMethodDef Voice_methods[] = {
	{"stop", reinterpret_cast<PyCFunction>(Voice_stop), METH_VARARGS, "Stop this voice"},
	{"pause", reinterpret_cast<PyCFunction>(Voice_pause), METH_VARARGS, "Pause or resume this voice"},
	{"set_volume", reinterpret_cast<PyCFunction>(Voice_set_volume), METH_VARARGS, "Set voice volume"},
	{"set_pan", reinterpret_cast<PyCFunction>(Voice_set_pan), METH_VARARGS, "Set voice pan"},
	{"set_speed", reinterpret_cast<PyCFunction>(Voice_set_speed), METH_VARARGS, "Set relative play speed"},
	{"fade_volume", reinterpret_cast<PyCFunction>(Voice_fade_volume), METH_VARARGS, "Fade voice volume"},
	{"fade_pan", reinterpret_cast<PyCFunction>(Voice_fade_pan), METH_VARARGS, "Fade voice pan"},
	{"fade_speed", reinterpret_cast<PyCFunction>(Voice_fade_speed), METH_VARARGS, "Fade voice speed"},
	{"set_lowpass", reinterpret_cast<PyCFunction>(Voice_set_lowpass), METH_VARARGS | METH_KEYWORDS, "Set lowpass filter for this voice"},
	{"set_lowpass_wet", reinterpret_cast<PyCFunction>(Voice_set_lowpass_wet), METH_VARARGS, "Set lowpass wet value"},
	{"is_valid", reinterpret_cast<PyCFunction>(Voice_is_valid), METH_VARARGS, "Check if voice is valid"},
	{"is_paused", reinterpret_cast<PyCFunction>(Voice_is_paused), METH_VARARGS, "Check if voice is paused"},
	{"get_volume", reinterpret_cast<PyCFunction>(Voice_get_volume), METH_VARARGS, "Get current volume"},
	{"get_pan", reinterpret_cast<PyCFunction>(Voice_get_pan), METH_VARARGS, "Get current pan"},
	{"get_speed", reinterpret_cast<PyCFunction>(Voice_get_speed), METH_VARARGS, "Get current speed"},
	{nullptr, nullptr, 0, nullptr}};

// Module --------------------------------------------------------------

static PyTypeObject PyAudioEngine_Type = {
	PyVarObject_HEAD_INIT(nullptr, 0)
};

static PyTypeObject PySound_Type = {
	PyVarObject_HEAD_INIT(nullptr, 0)
};

static PyTypeObject PyVoice_Type = {
	PyVarObject_HEAD_INIT(nullptr, 0)
};

static PyModuleDef audio_module = {
	PyModuleDef_HEAD_INIT,
	"audio",
	"SoLoud audio bindings",
	-1,
	nullptr,
};

PyMODINIT_FUNC PyInit_audio(void)
{
	PyAudioEngine_Type.tp_name = "MyGame.audio.AudioEngine";
	PyAudioEngine_Type.tp_basicsize = sizeof(PyAudioEngine);
	PyAudioEngine_Type.tp_dealloc = reinterpret_cast<destructor>(AudioEngine_dealloc);
	PyAudioEngine_Type.tp_flags = Py_TPFLAGS_DEFAULT;
	PyAudioEngine_Type.tp_doc = "Audio engine based on SoLoud";
	PyAudioEngine_Type.tp_methods = AudioEngine_methods;
	PyAudioEngine_Type.tp_init = reinterpret_cast<initproc>(AudioEngine_init);
	PyAudioEngine_Type.tp_new = AudioEngine_new;

	PySound_Type.tp_name = "MyGame.audio.Sound";
	PySound_Type.tp_basicsize = sizeof(PySound);
	PySound_Type.tp_dealloc = reinterpret_cast<destructor>(Sound_dealloc);
	PySound_Type.tp_flags = Py_TPFLAGS_DEFAULT;
	PySound_Type.tp_doc = "Loaded sound (wav/ogg/mp3/flac)";
	PySound_Type.tp_methods = Sound_methods;
	PySound_Type.tp_init = reinterpret_cast<initproc>(Sound_init);
	PySound_Type.tp_new = Sound_new;

	PyVoice_Type.tp_name = "MyGame.audio.Voice";
	PyVoice_Type.tp_basicsize = sizeof(PyVoice);
	PyVoice_Type.tp_dealloc = reinterpret_cast<destructor>(Voice_dealloc);
	PyVoice_Type.tp_flags = Py_TPFLAGS_DEFAULT;
	PyVoice_Type.tp_doc = "Playing voice handle";
	PyVoice_Type.tp_methods = Voice_methods;
	PyVoice_Type.tp_new = Voice_new;

	if (PyType_Ready(&PyAudioEngine_Type) < 0)
		return nullptr;
	if (PyType_Ready(&PySound_Type) < 0)
		return nullptr;
	if (PyType_Ready(&PyVoice_Type) < 0)
		return nullptr;

	PyObject *module = PyModule_Create(&audio_module);
	if (!module)
		return nullptr;

	Py_INCREF(&PyAudioEngine_Type);
	if (PyModule_AddObject(module, "AudioEngine", reinterpret_cast<PyObject *>(&PyAudioEngine_Type)) < 0)
	{
		Py_DECREF(&PyAudioEngine_Type);
		Py_DECREF(module);
		return nullptr;
	}

	Py_INCREF(&PySound_Type);
	if (PyModule_AddObject(module, "Sound", reinterpret_cast<PyObject *>(&PySound_Type)) < 0)
	{
		Py_DECREF(&PySound_Type);
		Py_DECREF(module);
		return nullptr;
	}

	Py_INCREF(&PyVoice_Type);
	if (PyModule_AddObject(module, "Voice", reinterpret_cast<PyObject *>(&PyVoice_Type)) < 0)
	{
		Py_DECREF(&PyVoice_Type);
		Py_DECREF(module);
		return nullptr;
	}

	return module;
}
