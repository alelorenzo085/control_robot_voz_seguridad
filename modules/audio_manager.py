from vosk import Model, KaldiRecognizer
import sounddevice as sd
import soundfile as sf
import json
import numpy as np

samplerate = 16000
# Ruta del modelo Vosk
model = Model("vosk-model-small-es-0.42") 
recognizer = KaldiRecognizer(model, samplerate)

def grabar_audio_autorizado(duracion=4, salida="audio_autorizado.wav"):
    """
    Graba audio de referencia para autenticación.
    """
    print(f"🎤 Grabando audio autorizado ({duracion}s)...")
    audio = sd.rec(int(duracion * samplerate), samplerate=samplerate,
                   channels=1, dtype='float32')
    sd.wait()

    # Guardar archivo WAV
    sf.write(salida, audio, samplerate)
    print(f"✅ Audio guardado en: {salida}")
    return audio.flatten()

def escuchar():
    """
    Graba 4 segundos de audio.
    Devuelve:
    1. El array de audio en numpy (para verificación)
    2. El texto reconocido (para comandos)
    """
    print("🎤 Grabando...")
    # Grabar audio
    audio = sd.rec(int(4 * samplerate), samplerate=samplerate,
                   channels=1, dtype='int16')
    sd.wait()
    
    # Procesar texto con Vosk
    text = ""
    if recognizer.AcceptWaveform(audio.tobytes()):
        result = json.loads(recognizer.Result())
        text = result.get("text", "")
    else:
       
        result = json.loads(recognizer.FinalResult())
        text = result.get("text", "")
        
    audio_flat = audio.flatten()
    
    return audio_flat, text