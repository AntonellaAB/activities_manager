import tkinter as tk
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui import config_base as cfg
from dao.menu_dao import MenuDAO
from ui.extension_ui import HorasExtensionUI
from ui.resumen_ui import ResumenUI

class MainMenuView(cfg.PantallaBase):
    def __init__(self, usuario_logueado):
        self.usuario = usuario_logueado 

        # Variables de control para evitar ventanas duplicadas
        self.instancia_registro = None
        self.instancia_resumen = None

        super().__init__(titulo=f"Gestor de Horas - Panel de {self.usuario.nombre}")
        self.crear_interfaz()
        self.load_total_hours()

    def crear_interfaz(self):
        contenedor = tk.Frame(self, bg=cfg.FONDO_PRINCIPAL)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=60, pady=60)
        
        top_frame = tk.Frame(contenedor, bg=cfg.FONDO_PRINCIPAL)
        top_frame.pack(fill=tk.X, pady=(0, 30))

        hours_frame = tk.Frame(top_frame, bg=cfg.FONDO_TARJETA, bd=0, padx=30, pady=30)
        hours_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        lbl_hours_title = tk.Label(
            hours_frame, 
            text=f"ALUMNO: {self.usuario.nombre.upper()} | TIENES :", 
            font=(cfg.FUENTE_FAMILY, 12, "bold"), 
            bg=cfg.FONDO_TARJETA, 
            fg=cfg.FUENTE_COLOR_SECUNDARIO
        )
        lbl_hours_title.pack(anchor="w")
        
        self.lbl_hours_amount = tk.Label(
            hours_frame, 
            text="... HORAS", 
            font=(cfg.FUENTE_FAMILY, 24, "bold"), 
            bg=cfg.FONDO_TARJETA, 
            fg=cfg.FUENTE_COLOR
        )
        self.lbl_hours_amount.pack(anchor="w", pady=(10, 0))

        btn_add = tk.Button(
            top_frame, text="ADD", 
            font=(cfg.FUENTE_FAMILY, 16, "bold"), 
            bg=cfg.BOTON_COLOR1, 
            fg=cfg.FUENTE_COLOR,
            activebackground=cfg.BOTON_COLOR1_HOVER, 
            activeforeground=cfg.FUENTE_COLOR,
            command=self.open_load_hours_ui, 
            height=3, width=15, cursor="hand2", relief="flat"
        )
        btn_add.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))

        bottom_frame = tk.Frame(contenedor, bg=cfg.FONDO_PRINCIPAL)
        bottom_frame.pack(fill=tk.X)

        btn_summary = tk.Button(
            bottom_frame, text="RESUMEN", 
            font=(cfg.FUENTE_FAMILY, 16, "bold"), 
            bg=cfg.BOTON_COLOR2, 
            fg=cfg.FUENTE_COLOR,
            activebackground=cfg.BOTON_COLOR2_HOVER, 
            activeforeground=cfg.FUENTE_COLOR,
            command=self.open_summary_ui, 
            height=3, cursor="hand2", relief="flat"
        )
        btn_summary.pack(fill=tk.X, expand=True)

    def load_total_hours(self):
        horas = MenuDAO.obtener_total_horas(self.usuario.id_user)
        self.lbl_hours_amount.config(text=f"{horas} HORAS")

    def open_load_hours_ui(self):
        # Si la ventana ya existe y sigue abierta, la traemos al frente
        if self.instancia_registro and tk.Toplevel.winfo_exists(self.instancia_registro):
            self.instancia_registro.focus_force()
            return

        # Si no existe, la creamos de cero y guardamos su referencia
        self.instancia_registro = tk.Toplevel(self)
        HorasExtensionUI(self.instancia_registro, self.usuario.id_user, callback_actualizar=self.load_total_hours)

    def open_summary_ui(self):
        if self.instancia_resumen and tk.Toplevel.winfo_exists(self.instancia_resumen):
            self.instancia_resumen.focus_force()
            return

       
        self.instancia_resumen = tk.Toplevel(self)
        ResumenUI(self.instancia_resumen, self.usuario)

'''
if __name__ == "__main__":
    # Simulación de test rápido por si corren el archivo solo
    from models.user import User
    user_test = User(id_user=1, nombre="Estudiante Prueba", rol="alumno")
    app = MainMenuView(user_test)
    app.mainloop()

'''