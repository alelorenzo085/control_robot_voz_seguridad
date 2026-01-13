from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json
import numpy as np

samplerate = 16000
# Asegúrate que la ruta al modelo sea correcta
model = Model("vosk-model-small-es-0.42") 
recognizer = KaldiRecognizer(model, samplerate)

def escuchar():
    """
    Graba 4 segundos de audio.
    Devuelve:
    1. El array de audio en numpy (para verificación)
    2. El texto reconocido (para comandos)
    """
    print("🎤 Grabando...")
    # Grabamos en int16
    audio = sd.rec(int(4 * samplerate), samplerate=samplerate,
                   channels=1, dtype='int16')
    sd.wait()
    
    # Procesar texto con Vosk
    text = ""
    if recognizer.AcceptWaveform(audio.tobytes()):
        result = json.loads(recognizer.Result())
        text = result.get("text", "")
    else:
        # A veces el texto queda en FinalResult
        result = json.loads(recognizer.FinalResult())
        text = result.get("text", "")
        
    # Aplanar el audio para que sea un array 1D (necesario para librosa)
    audio_flat = audio.flatten()
    
    return audio_flat, text