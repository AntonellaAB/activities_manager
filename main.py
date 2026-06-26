import sys
import os
import tkinter as tk
from tkinter import messagebox

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from ui.login import LoginApp
from database.conection import obtener_conexion

def verificar_sistema():
    
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
    
    
    if not verificar_sistema():
        
        root_error = tk.Tk()
        root_error.withdraw()
        messagebox.showerror(
            "Error de Infraestructura", 
            "No se pudo establecer conexión con PostgreSQL.\n"
            "Asegúrate de que el servicio esté corriendo y las credenciales en config_base sean correctas."
        )
        root_error.destroy()
        sys.exit(1)
        
   
    app = LoginApp()
    app.mainloop()
