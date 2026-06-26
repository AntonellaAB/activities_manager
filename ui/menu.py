import tkinter as tk
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_base as cfg
from dao.menu_dao import MenuDAO

class MainMenuView(cfg.PantallaBase):
    def __init__(self, usuario_logueado):
        """
        Menú principal adaptado que hereda de PantallaBase.
        :param usuario_logueado: Objeto User devuelto por el Login
        """
        # Guardamos los datos del usuario en la sesión de la ventana
        self.usuario = usuario_logueado 
        
        # Inicializa la ventana base con un título personalizado que incluye su nombre
        super().__init__(titulo=f"Gestor de Horas - Panel de {self.usuario.nombre}")
        
        self.crear_interfaz()
        self.load_total_hours()

    def crear_interfaz(self):
        # Contenedor principal para empaquetar con márgenes limpios
        contenedor = tk.Frame(
            self, 
            bg=cfg.FONDO_PRINCIPAL
        )
        contenedor.pack(fill=tk.BOTH, expand=True, padx=60, pady=60)
        
        # --- FRAME SUPERIOR (Horas y botón ADD) ---
        top_frame = tk.Frame(
            contenedor, 
            bg=cfg.FONDO_PRINCIPAL
        )
        top_frame.pack(fill=tk.X, pady=(0, 30))

        # Tarjeta "TIENES : X HORAS"
        hours_frame = tk.Frame(
            top_frame, 
            bg=cfg.FONDO_TARJETA, 
            bd=0, 
            padx=30, 
            pady=30
        )
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

        # Botón de "ADD" (Para Vicente)
        btn_add = tk.Button(
            top_frame, text="ADD", 
            font=(cfg.FUENTE_FAMILY, 16, "bold"), 
            bg=cfg.BOTON_COLOR1, 
            fg=cfg.FUENTE_COLOR,
            activebackground=cfg.BOTON_COLOR1, 
            activeforeground=cfg.FUENTE_COLOR,
            command=self.open_load_hours_ui, 
            height=3, 
            width=15, 
            cursor="hand2", 
            relief="flat"
        )
        btn_add.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))

        # --- FRAME INFERIOR (Botón RESUMEN) ---
        bottom_frame = tk.Frame(
            contenedor, 
            bg=cfg.FONDO_PRINCIPAL
        )
        bottom_frame.pack(fill=tk.X)

        # Botón de "RESUMEN" (Para Gio)
        btn_summary = tk.Button(
            bottom_frame, 
            text="RESUMEN", 
            font=(cfg.FUENTE_FAMILY, 16, "bold"), 
            bg=cfg.BOTON_COLOR2, 
            fg=cfg.FUENTE_COLOR,
            activebackground=cfg.BOTON_COLOR2, 
            activeforeground=cfg.FUENTE_COLOR,
            command=self.open_summary_ui, 
            height=3, cursor="hand2", 
            relief="flat"
        )
        btn_summary.pack(fill=tk.X, expand=True)

    def load_total_hours(self):
        """Llama al DAO para traer las horas usando el id del usuario de la sesión"""
        horas = MenuDAO.obtener_total_horas(self.usuario.id_user)
        self.lbl_hours_amount.config(text=f"{horas} HORAS")

    def open_load_hours_ui(self):
        print(f"Abriendo ADD pasándole el ID de usuario: {self.usuario.id_user}")

    def open_summary_ui(self):
        print(f"Abriendo resumen para el rol: {self.usuario.rol}")

if __name__ == "__main__":
    # Simulación de test rápido por si corren el archivo solo
    from models.user import User
    user_test = User(id_user=1, nombre="Estudiante Prueba", rol="alumno")
    app = MainMenuView(user_test)
    app.mainloop()