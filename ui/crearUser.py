import tkinter as tk
from tkinter import messagebox
import sys
import os

# Asegura que Python encuentre los paquetes desde la raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui import config_base as cfg  # Corregido para que no crashee desde main.py
from dao.user_dao import UserDAO

class CrearUserApp(cfg.PantallaBase):
    def __init__(self):
        super().__init__(titulo="Gestor de Horas de Extensión - Crear Usuario")
        self.user_dao = UserDAO()
        self.crear_interfaz()
    
    def crear_interfaz(self):
        tarjeta_crear = tk.Frame(
            self, 
            bg=cfg.FONDO_TARJETA,
        )
        tarjeta_crear.place(
            x=150,
            y=100,
            width=700,
            height=400    
        )

        lbl_titulo = tk.Label(
            tarjeta_crear,
            text="Crear Cuenta",
            font=(cfg.FUENTE_FAMILY, 20, "bold"),
            bg=cfg.FONDO_TARJETA,
            fg=cfg.FUENTE_COLOR
        )
        lbl_titulo.place(x=268, y=40, width=165)

        # NOMBRE DE USUARIO
        lbl_usuario = tk.Label(
            tarjeta_crear,
            text="Nombre de Usuario",
            font=(cfg.FUENTE_FAMILY, 14),
            fg=cfg.FUENTE_COLOR_SECUNDARIO,
            bg=cfg.FONDO_TARJETA
        )
        lbl_usuario.place(x=50, y=110)

        self.txt_usuario = tk.Entry(
            tarjeta_crear,
            font=(cfg.FUENTE_FAMILY, 12),
            bg=cfg.ENTRY_BG,
            fg="#242424",
            bd=1, 
            relief="solid"
        )
        self.txt_usuario.place(x=50, y=140, width=250, height=35)

        # EMAIL DEL USUARIO
        lbl_email = tk.Label(
            tarjeta_crear,
            text="Email",
            font=(cfg.FUENTE_FAMILY, 14),
            fg=cfg.FUENTE_COLOR_SECUNDARIO,
            bg=cfg.FONDO_TARJETA
        )
        lbl_email.place(x=50, y=200)

        self.txt_email = tk.Entry(
            tarjeta_crear,
            font=(cfg.FUENTE_FAMILY, 12),
            bg=cfg.ENTRY_BG,
            fg="#242424",
            bd=1, 
            relief="solid"
        )
        self.txt_email.place(x=50, y=230, width=250, height=35)

        # CONTRASENIA
        lbl_password = tk.Label(
            tarjeta_crear,
            text="Contraseña",
            font=(cfg.FUENTE_FAMILY, 14),
            fg=cfg.FUENTE_COLOR_SECUNDARIO,
            bg=cfg.FONDO_TARJETA
        )
        lbl_password.place(x=390, y=110)

        self.txt_password = tk.Entry(
            tarjeta_crear,
            font=(cfg.FUENTE_FAMILY, 12),
            bg=cfg.ENTRY_BG,
            fg="#242424",
            bd=1, 
            relief="solid",
            show="*"
        )
        self.txt_password.place(x=390, y=140, width=250, height=35)

        # CONFIRMAR CONTRASENIA
        lbl_RETYPEpassword = tk.Label(
            tarjeta_crear,
            text="Confirmar contraseña",
            font=(cfg.FUENTE_FAMILY, 14),
            fg=cfg.FUENTE_COLOR_SECUNDARIO,
            bg=cfg.FONDO_TARJETA
        )
        lbl_RETYPEpassword.place(x=390, y=200)

        self.txt_RETYPEpassword = tk.Entry(
            tarjeta_crear,
            font=(cfg.FUENTE_FAMILY, 12),
            bg=cfg.ENTRY_BG,
            fg="#242424",
            bd=1, 
            relief="solid",
            show="*"
        )
        self.txt_RETYPEpassword.place(x=390, y=230, width=250, height=35)

        # BOTON PARA CONFIRMAR 
        self.btn_crear = tk.Button(
            tarjeta_crear,
            text="Crear",
            font=(cfg.FUENTE_FAMILY, 11, "bold"),
            bg=cfg.BOTON_COLOR1,
            fg=cfg.FUENTE_COLOR,
            activebackground=cfg.BOTON_COLOR1_HOVER,
            activeforeground=cfg.FUENTE_COLOR,
            bd=0,
            cursor="hand2",
            command=self.ejecutar_crearUser
        )
        self.btn_crear.place(x=540, y=300, width=100, height=40)

        # BOTON REGRESAR
        self.btn_exit = tk.Button(
            self,
            text="Atras",
            font=(cfg.FUENTE_FAMILY, 11, "bold"),
            bg=cfg.BOTON_COLOR2,
            fg=cfg.FUENTE_COLOR,
            activebackground=cfg.BOTON_COLOR2_HOVER,
            activeforeground=cfg.FUENTE_COLOR,
            bd=0,
            cursor="hand2",
            command=self.ejecutar_volver
        )
        self.btn_exit.place(x=50, y=40, width=80, height=40)

    def ejecutar_crearUser(self):
        usuario = self.txt_usuario.get().strip()
        email = self.txt_email.get().strip()
        password = self.txt_password.get().strip()
        confirm_password = self.txt_RETYPEpassword.get().strip()

        # 1. Validar campos vacíos
        if not usuario or not email or not password or not confirm_password:
            messagebox.showwarning("Campos vacíos", "Por favor rellena todos los datos del formulario.")
            return

        # 2. Validar que las contraseñas coincidan
        if password != confirm_password:
            messagebox.showerror("Error de coincidencia", "Las contraseñas ingresadas no coinciden.")
            return

        # 3. Guardar en la Base de Datos usando el DAO
        try:
            exito = UserDAO.crear_usuario(usuario, email, password, rol='estudiante')
            if exito:
                messagebox.showinfo("¡Éxito!", f"Cuenta para el usuario '{usuario}' creada de forma correcta.")
                self.ejecutar_volver()  # Nos manda de vuelta al login limpito
            else:
                messagebox.showerror("Error de duplicado", f"El nombre de usuario '{usuario}' ya está en uso.")
        except Exception as e:
            messagebox.showerror("Error de Registro", f"Ocurrió un error inesperado: {e}")

    def ejecutar_volver(self):
        self.destroy()
        from ui.login import LoginApp
        back = LoginApp()
        back.mainloop()

if __name__ == "__main__":
    app = CrearUserApp()
    app.mainloop()