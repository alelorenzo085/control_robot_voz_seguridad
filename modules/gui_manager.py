import tkinter as tk
import datetime

def crear_ventana():
    """Crea la ventana principal con robot y devuelve los widgets principales."""
    ventana = tk.Tk()
    ventana.title("Robot industrial 4.0 - Seguridad del hablante")
    ventana.geometry("550x650") # Un poco más alto para el log
    ventana.config(bg="#1e1e1e")

    # Título
    titulo = tk.Label(ventana, text="CONTROL DE ACCESO POR VOZ - ROBOT INDUSTRIAL 4.0",
             font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#00ffcc")
    titulo.pack(pady=10)

    # Canvas donde se dibujarán los sensores del robot
    canvas = tk.Canvas(ventana, width=400, height=150, bg="#111", highlightthickness=0)
    canvas.pack(pady=20)

    # Crear sensores (óvalos) apagados inicialmente
    temp = canvas.create_oval(25, 30, 125, 130, fill="grey20")
    prox = canvas.create_oval(145, 30, 245, 130, fill="grey20")
    energia = canvas.create_oval(265, 30, 365, 130, fill="grey20")


    # Label Estado
    estado_label = tk.Label(ventana, text="Esperando...", font=("Arial", 12), bg="#1e1e1e", fg="white")
    estado_label.pack(pady=5)
    
    resultado_label = tk.Label(ventana, text="...", font=("Arial", 11), bg="#1e1e1e", fg="gray")
    resultado_label.pack(pady=5)

    # --- NUEVO: LISTBOX PARA LOG DE EVENTOS ---
    tk.Label(ventana, text="📜 Registro de Eventos:", bg="#1e1e1e", fg="white").pack(anchor="w", padx=20)
    log_box = tk.Listbox(ventana, height=8, width=60, bg="#2d2d2d", fg="#00ff00", font=("Consolas", 9))
    log_box.pack(pady=5)

    def agregar_log(mensaje, tipo="info"):
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        icono = "🔒" if tipo == "seguridad" else "🤖"
        if tipo == "error": icono = "❌"
        log_box.insert(0, f"[{hora}] {icono} {mensaje}") # Insertar al principio

    return ventana, canvas, temp, prox, energia, estado_label, resultado_label, agregar_log