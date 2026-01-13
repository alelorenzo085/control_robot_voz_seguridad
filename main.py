import tkinter as tk
from modules.gui_manager import crear_ventana
from modules.audio_manager import escuchar, grabar_audio_autorizado
from modules.command_processor import procesar_comando
from modules.security import verificar_usuario
from modules.audio_manager import samplerate

def main():
    # Obtenemos widgets y la función de log
    (ventana, canvas, temp, prox, energia, estado_label, 
     resultado_label, agregar_log) = crear_ventana()
    sensores = [temp, prox, energia]

    def ejecutar_reconocimiento():
        estado_label.config(text="Escuchando... 🎤", fg="yellow")
        ventana.update()
        
        # 1. Obtener audio crudo Y texto
        audio_array, text = escuchar()
        
        # 2. Verificar seguridad (MFCC + DTW)
        is_verified, msg_security, score = verificar_usuario(audio_array, samplerate)
        
        if is_verified:
            # --- ACCESO CONCEDIDO ---
            estado_label.config(text=f"✅ Acceso Concedido ({score:.2f})", fg="#00ff00")
            agregar_log(f"AUTH OK: {msg_security}", "seguridad")
            
            # Procesar el comando solo si está verificado
            resultado_label.config(text=f"Texto: {text}")
            
            # Nota: He ajustado la llamada a procesar_comando para coincidir con tu structure
            # Asegúrate que procesar_comando acepte los argumentos correctos
            if text:
                procesar_comando(text, canvas, sensores, resultado_label, estado_label, ventana)
                agregar_log(f"CMD: {text}", "info")
            else:
                agregar_log("Audio ininteligible", "error")
                
        else:
            # --- ACCESO DENEGADO ---
            estado_label.config(text="⛔ ACCESO DENEGADO", fg="red")
            resultado_label.config(text=f"Voz no autorizada ({score:.2f})")
            agregar_log(f"INTRUSO BLOQUEADO: {msg_security}", "error")
            
            # Reset visual de alerta (opcional)
            canvas.itemconfig(sensores[0], fill="grey20")
            canvas.itemconfig(sensores[1], fill="grey20")
            canvas.itemconfig(sensores[2], fill="grey20")

    # Botón principal
    boton = tk.Button(ventana, text="Escuchar 🎤", command=ejecutar_reconocimiento,
                      font=("Arial", 14), bg="#00ffcc", fg="black", width=15, height=2)
    boton.pack(pady=20)

    # Botón para registrar voz autorizada
    def registrar_voz():
        estado_label.config(text="🎤 Registrando voz autorizada...", fg="blue")
        ventana.update()
        try:
            grabar_audio_autorizado(duracion=4)
            estado_label.config(text="✅ Voz registrada correctamente", fg="#00ff00")
            agregar_log("Voz autorizada registrada", "seguridad")
        except Exception as e:
            estado_label.config(text=f"❌ Error: {e}", fg="red")
            agregar_log(f"Error al registrar: {e}", "error")

    boton_registrar = tk.Button(ventana, text="Registrar Voz 🔐", command=registrar_voz,
                                font=("Arial", 12), bg="#ff9900", fg="black", width=15)
    boton_registrar.pack(pady=10)

    # Mensaje inicial en el log
    agregar_log("Sistema iniciado. Esperando usuario...", "info")
    
    ventana.mainloop()

if __name__ == "__main__":
    main()