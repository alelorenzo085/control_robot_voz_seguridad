import os
import numpy as np
import librosa
import soundfile as sf
from scipy.spatial.distance import cdist

# Ruta del audio de referencia
AUDIO_REF_PATH = "audio_autorizado.wav"
UMBRAL_SEGURIDAD = 0.50  # Ajusta este valor 

def zscore_per_coef(mfcc):
    """Normaliza los coeficientes MFCC (Del Notebook)"""
    mu = mfcc.mean(axis=1, keepdims=True)
    sigma = mfcc.std(axis=1, keepdims=True)
    sigma[sigma == 0] = 1.0
    return (mfcc - mu) / sigma

def verificar_usuario(audio_actual_array, samplerate):
    """
    Compara el audio grabado en vivo con el audio de referencia.
    Retorna: (Booleano, Mensaje, Similitud)
    """
    if not os.path.exists(AUDIO_REF_PATH):
        return False, "⚠️ Falta archivo 'audio_autorizado.wav'", 0.0

    try:
        # 1. Cargar referencia con soundfile
        data_ref, sr_ref = sf.read(AUDIO_REF_PATH)
        
        # Normalizar si es necesario
        if data_ref.dtype == 'int16':
            data_ref = data_ref.astype(np.float32) / 32768.0
        elif isinstance(data_ref[0], (int, np.integer)):
            data_ref = data_ref.astype(np.float32) / 32768.0
        
        # Normalizar audio actual si es necesario
        audio_act = audio_actual_array.astype(np.float32) / 32768.0

        mfcc_ref = librosa.feature.mfcc(y=data_ref, sr=sr_ref, n_mfcc=13)
        mfcc_act = librosa.feature.mfcc(y=audio_act, sr=samplerate, n_mfcc=13)

        # 3. Normalización y Comparación 
        A = zscore_per_coef(mfcc_ref)
        B = zscore_per_coef(mfcc_act)

        cost = cdist(A.T, B.T, metric='cosine')
        D, wp = librosa.sequence.dtw(C=cost)

        distancia_acumulada = float(D[-1, -1])
        distancia_promedio = distancia_acumulada / len(wp)
        similitud = float(np.exp(-distancia_promedio))

        print(f"[DEBUG] Distancia promedio: {distancia_promedio:.4f} | Similitud: {similitud:.4f} | Umbral: {UMBRAL_SEGURIDAD}")

        is_authorized = similitud >= UMBRAL_SEGURIDAD
        return is_authorized, f"Similitud: {similitud:.2f}", similitud

    except Exception as e:
        print(f"Error en verificación: {e}")
        import traceback
        traceback.print_exc()
        return False, "Error técnico", 0.0