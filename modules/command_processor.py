def procesar_comando(text, canvas, sensores, resultado_label, estado_label, ventana):
    """
    Procesa el comando de voz y actualiza el estado del robot.
    sensores: tupla (temp, prox, energia)
    """
    temp, prox, energia = sensores
    text = text.lower()

    if "activar" in text and "robot" in text:
        canvas.itemconfig(temp, fill="red")
        canvas.itemconfig(prox, fill="green")
        canvas.itemconfig(energia, fill="yellow")
        resultado_label.config(text="Comando: activar robot")
        estado_label.config(text="🟢 Robot activo")

    elif "detener" in text and "robot" in text:
        canvas.itemconfig(temp, fill="grey20")
        canvas.itemconfig(prox, fill="grey20")
        canvas.itemconfig(energia, fill="grey20")
        resultado_label.config(text="Comando: detener robot")
        estado_label.config(text="⚪ Detenido")

    elif "temperatura" in text and "alta" in text:
        canvas.itemconfig(temp, fill="red")
        resultado_label.config(text="⚠️ ALERTA: ¡¡Temperatura alta!!")
        estado_label.config(text="❌ Error")

    elif "revisar" in text and "sensores" in text:
        resultado_label.config(text="Sensores en perfecto estado:\nTemperatura | Proximidad | Energía")
        estado_label.config(text="🆗 Revisión completa")

    elif "salir" in text:
        resultado_label.config(text="👋 Cerrando programa...")
        ventana.after(1000, ventana.destroy)

    else:
        resultado_label.config(text="❓ No le entiendo. ¿Podría repetir?")
