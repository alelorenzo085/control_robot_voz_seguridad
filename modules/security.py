import os
import numpy as np
import librosa
from scipy.spatial.distance import cdist
from scipy.io import wavfile

# Ruta del audio de referencia (DEBES CREARLO PRIMERO)
AUDIO_REF_PATH = "audio_autorizado.wav"
UMBRAL_SEGURIDAD = 0.65  # Ajusta este valor (0.60 a 0.80) según pruebas

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
        # 1. Cargar referencia
        sr_ref, data_ref = wavfile.read(AUDIO_REF_PATH)
        
        # Convertir a float32 normalizado (como en el notebook)
        if data_ref.dtype == 'int16':
            data_ref = data_ref.astype(np.float32) / 32768.0
        
        # Audio actual ya viene como array int16, convertir a float
        audio_act = audio_actual_array.astype(np.float32) / 32768.0

        # 2. Extraer MFCCs (Librosa)
        # Nota: librosa carga lento la primera vez
        mfcc_ref = librosa.feature.mfcc(y=data_ref, sr=sr_ref, n_mfcc=13)
        mfcc_act = librosa.feature.mfcc(y=audio_act, sr=samplerate, n_mfcc=13)

        # 3. Normalización y Comparación (DTW)
        A = zscore_per_coef(mfcc_ref)
        B = zscore_per_coef(mfcc_act)

        cost = cdist(A.T, B.T, metric='cosine')
        D, wp = librosa.sequence.dtw(C=cost)

        distancia_acumulada = float(D[-1, -1])
        distancia_promedio = distancia_acumulada / len(wp)
        similitud = float(np.exp(-distancia_promedio))

        is_authorized = similitud >= UMBRAL_SEGURIDAD
        return is_authorized, f"Similitud: {similitud:.2f}", similitud

    except Exception as e:
        print(f"Error en verificación: {e}")
        return False, "Error técnico", 0.0