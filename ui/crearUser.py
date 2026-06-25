import tkinter as tk
from tkinter import messagebox
import sys
import os

# Asegura que Python encuentre la carpeta 'dao' desde la carpeta 'ui'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_base as cfg
from dao.user_dao import UserDAO

class LoginApp(cfg.PantallaBase):
    def __init__(self):
        super().__init__(titulo="Gestor de Horas de Extension - Login")
        self.user_dao = UserDAO()
        self.crear_interfaz()
    
    def crear_interfaz(self):
        tarjeta_login = tk.Frame(
            self, 
            bg=cfg.FONDO_TARJETA,
            
        )
        tarjeta_login.place(
            x=300,
            y=100,
            width=400,
            height=400    
        )

       
        lbl_titulo = tk.Label(
            tarjeta_login,
            text=("Iniciar Sesion"),
            font=(cfg.FUENTE_FAMILY, 20, "bold"),
            bg=cfg.FONDO_TARJETA,
            fg=cfg.FUENTE_COLOR
        )
        lbl_titulo.place(x=40, y=40)


        lbl_usuario = tk.Label(
            tarjeta_login,
            text=("Nombre de Usuario"),
            font=(cfg.FUENTE_FAMILY, 14),
            fg=cfg.FUENTE_COLOR_SECUNDARIO,
            bg=cfg.FONDO_TARJETA

        )
        lbl_usuario.place(x=40, y=110)

        self.txt_usuario = tk.Entry(
            tarjeta_login,
            font=(cfg.FUENTE_FAMILY, 12),
            bg=cfg.ENTRY_BG,
            fg="#242424",
            bd=1, 
            relief="solid"

        )
        self.txt_usuario.place(x=40, y=140, width=320, height=35)

    def ejecutar_crearUser(self):
        pass
#MAINLOOP ==============================================
if __name__ == "__main__":
    
    app = LoginApp()
    app.mainloop()
