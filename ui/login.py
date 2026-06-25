import tkinter as tk
from tkinter import messagebox
import sys
import os

# Asegura que Python encuentre la carpeta 'dao' desde la carpeta 'ui'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_base as cfg
from dao.user_dao import UserDAO
from menu import MainMenuView


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


        lbl_password = tk.Label(
            tarjeta_login,
            text=("Contraseña"),
            font=(cfg.FUENTE_FAMILY, 14),
            fg=cfg.FUENTE_COLOR_SECUNDARIO,
            bg=cfg.FONDO_TARJETA

        )
        lbl_password.place(x=40, y=200)


        self.txt_password = tk.Entry(
            tarjeta_login,
            font=(cfg.FUENTE_FAMILY, 12),
            bg=cfg.ENTRY_BG,
            fg="#242424",
            bd=1, 
            relief="solid",
            show="*"

        )
        self.txt_password.place(x=40, y=230, width=320, height=35)


        self.btn_ingresar = tk.Button(
            tarjeta_login,
            text=("Ingresar"),
            font=(cfg.FUENTE_FAMILY, 11, "bold"),
            bg=cfg.BOTON_COLOR1,
            fg=cfg.FUENTE_COLOR,
            activebackground=cfg.BOTON_COLOR1_HOVER, # Evita el flash gris horrible de Tkinter
            activeforeground=cfg.FUENTE_COLOR,
            bd=0, 
            cursor="hand2",
            command=self.ejecutar_login
            
        )
        self.btn_ingresar.place(x=260, y=300, width=100, height=40)

        
        
        self.btn_crearUser = tk.Button(
            tarjeta_login,
            text=("Crear cuenta"),
            font=(cfg.FUENTE_FAMILY, 11, "bold"),
            bg=cfg.BOTON_COLOR2,
            fg=cfg.FUENTE_COLOR,
            activebackground=cfg.BOTON_COLOR2_HOVER, # Evita el flash gris horrible de Tkinter
            activeforeground=cfg.FUENTE_COLOR,
            bd=0, 
            cursor="hand2",
            command=self.ejecutar_crearUser
            
        )
        self.btn_crearUser.place(x=40, y=300, width=150, height=40)

        

    
    
    def ejecutar_login(self):
        usuario_ingresado = self.txt_usuario.get().strip()
        password_ingresado = self.txt_password.get().strip()

        if not usuario_ingresado or not password_ingresado:
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos para continuar")
            return
        
        try:
            # Aquí capturamos el objeto User completo devuelto por tu DAO
            usuario_logueado = self.user_dao.login(usuario_ingresado, password_ingresado)

            if usuario_logueado is not None:
                messagebox.showinfo("¡Éxito!", f"Bienvenido/a {usuario_logueado.nombre}")

                self.destroy() # Cerramos Login de forma limpia

                # Instanciamos el menú pasándole el objeto completo del usuario
                app_menu = MainMenuView(usuario_logueado)
                app_menu.mainloop()
            else:
                messagebox.showerror("Error de autenticación", "Usuario o contraseña incorrectos.")

        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar con la base de datos: {e}")

    def ejecutar_crearUser(self):
        self.destroy()

        from crearUser import CrearUserApp
        app_crearUser = CrearUserApp()
        app_crearUser.mainloop()

#MAINLOOP ==============================================
if __name__ == "__main__":
    
    app = LoginApp()
    app.mainloop()


