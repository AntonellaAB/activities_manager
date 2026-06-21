import tkinter as tk
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
            fg=cfg.FUENTE_COLOR_SECUNDARIO

        )
        lbl_usuario.place(x=40, y=110)

        self.txt_usuario = tk.Entry(
            tarjeta_login,
            font=(cfg.FUENTE_FAMILY, 12),
            bg=cfg.ENTRY_BG,
            fg=cfg.FUENTE_COLOR,
            bd=1, 
            relief="solid"

        )
        self.txt_usuario.place(x=40, y=140, width=320, height=35)


        lbl_password = tk.Label(
            tarjeta_login,
            text=("Contraseña"),
            font=(cfg.FUENTE_FAMILY, 14),
            fg=cfg.FUENTE_COLOR_SECUNDARIO

        )
        lbl_password.place(x=40, y=200)
'''
    def ejecutar_login():
        usuario = self.txt_usuario.get()
        print(f"Intentando login con el usuario desde el DAO: {usuario}")
'''
#MAINLOOP ==============================================
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()



'''


        # 3. BOTÓN PRIMARIO (Acción Importante)
        btn_ingresar = tk.Button(
            tarjeta_login, 
            text="INGRESAR", 
            font=(cfg.FUENTE_FAMILY, 11, "bold"), 
            bg=cfg.BTN_PRIMARIO_BG, 
            fg=cfg.BTN_PRIMARIO_FG,
            activebackground=cfg.BTN_PRIMARIO_BG, # Evita el flash gris horrible de Tkinter
            activeforeground=cfg.BTN_PRIMARIO_FG,
            bd=0, 
            cursor="hand2",
            command=self.ejecutar_login  # Llama a la lógica
        )
        btn_ingresar.place(x=40, y=230, width=320, height=40)

    def ejecutar_login(self):
        usuario = self.txt_usuario.get()
        # Aquí ya puedes usar tu DAO libremente en grupo:
        # resultado = self.user_dao.validar_usuario(usuario, ...)
        print(f"Intentando login con el usuario desde el DAO: {usuario}")



        '''