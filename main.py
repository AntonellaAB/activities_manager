import sys
import os
import tkinter as tk
from tkinter import messagebox

# Aseguramos que Python reconozca la raíz del proyecto para todas las importaciones
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from ui.login import LoginApp
from database.conection import obtener_conexion

def verificar_sistema():
    """Valida que la base de datos esté activa antes de lanzar la interfaz."""
    try:
        conn = obtener_conexion()
        if conn:
            conn.close()
            return True
    except Exception as e:
        print(f"Error crítico de conexión inicial: {e}")
        return False

if __name__ == "__main__":
    print("Iniciando el Gestor de Horas de Extensión...")
    
    # 1. Verificar si hay conexión con PostgreSQL antes de abrir la UI
    if not verificar_sistema():
        # Lanzamos un pequeño entorno raíz temporal solo para mostrar el error visual
        root_error = tk.Tk()
        root_error.withdraw()
        messagebox.showerror(
            "Error de Infraestructura", 
            "No se pudo establecer conexión con PostgreSQL.\n"
            "Asegúrate de que el servicio esté corriendo y las credenciales en config_base sean correctas."
        )
        root_error.destroy()
        sys.exit(1)
        
    # 2. Si la base de datos responde, lanzamos el Login de forma limpia
    app = LoginApp()
    app.mainloop()
