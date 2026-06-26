# Archivo: ui/main.py
import tkinter as tk
from tkinter import ttk
import psycopg2

# ==============================================================================
# 1. IMPORTACIONES DEL PROYECTO
# ------------------------------------------------------------------------------
# Importamos las constantes estéticas del equipo para mantener los colores
from ui.config_base import (
    FONDO_PRINCIPAL, FONDO_TARJETA, FUENTE_FAMILY, 
    FUENTE_COLOR, FUENTE_COLOR_SECUNDARIO, 
    BOTON_COLOR1, BOTON_COLOR2
)

# [CAMBIO INTERFAZ GIO]: Importamos tu archivo de resumen con la tabla para poder usarlo
from ui.resumen_ui import ResumenView

class MainMenuView(tk.Frame):
    def __init__(self, parent, controller, connection, user_id):
        """
        Menú principal dinámico adaptado al diseño de config_base.py.
        :param parent: Ventana contenedora (ej. PantallaBase)
        :param controller: Manejador de cambios de ventana global
        :param connection: Conexión activa a PostgreSQL o None para modo test local
        :param user_id: ID del usuario logueado para calcular sus horas reales
        """
        super().__init__(parent, bg=FONDO_PRINCIPAL)
        self.controller = controller
        self.connection = connection
        self.user_id = user_id
        
        self.setup_ui()
        self.load_total_hours()

    def setup_ui(self):
        self.configure(padx=60, pady=60)
        
        # --- FRAME SUPERIOR (Horas y botón ADD) ---
        top_frame = tk.Frame(self, bg=FONDO_PRINCIPAL)
        top_frame.pack(fill=tk.X, expand=True, pady=(0, 30))

        # Tarjeta "TIENES : X HORAS"
        hours_frame = tk.Frame(top_frame, bg=FONDO_TARJETA, borderwidth=0, padx=30, pady=30)
        hours_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        lbl_hours_title = tk.Label(hours_frame, text="TIENES :", 
        font=(FUENTE_FAMILY, 16, "bold"), 
        bg=FONDO_TARJETA, fg=FUENTE_COLOR_SECUNDARIO)
        lbl_hours_title.pack(anchor="w")
        
        self.lbl_hours_amount = tk.Label(hours_frame, text="... HORAS", 
        font=(FUENTE_FAMILY, 24, "bold"), 
        bg=FONDO_TARJETA, fg=FUENTE_COLOR)
        self.lbl_hours_amount.pack(anchor="w", pady=(10, 0))

        # Botón de "ADD" (Para Vicente)
        btn_add = tk.Button(top_frame, text="ADD", 
                            font=(FUENTE_FAMILY, 16, "bold"), 
                            bg=BOTON_COLOR1, fg=FUENTE_COLOR,
                            activebackground=BOTON_COLOR1, activeforeground=FUENTE_COLOR,
                            command=self.open_load_hours_ui, 
                            height=3, width=15, cursor="hand2", relief="flat")
        btn_add.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))

        # --- FRAME INFERIOR (Botón RESUMEN) ---
        bottom_frame = tk.Frame(self, bg=FONDO_PRINCIPAL)
        bottom_frame.pack(fill=tk.X, expand=True)

        # Botón de "RESUMEN" (Para Gio)
        btn_summary = tk.Button(bottom_frame, text="RESUMEN", 
                                font=(FUENTE_FAMILY, 16, "bold"), 
                                bg=BOTON_COLOR2, fg=FUENTE_COLOR,
                                activebackground=BOTON_COLOR2, activeforeground=FUENTE_COLOR,
                                command=self.open_summary_ui, 
                                height=3, cursor="hand2", relief="flat")
        btn_summary.pack(fill=tk.X, expand=True)

    def load_total_hours(self):
        """Consulta la base de datos y suma las horas de extensión del usuario."""
        # ==============================================================================
        # MODO DE PRUEBA LOCAL (SIN ENLACE A BASE DE DATOS ACTIVADO)
        # ==============================================================================
        self.lbl_hours_amount.config(text="35 HORAS")
        return
        
        # ==============================================================================
        # MODO EN VIVO (CON BASE DE DATOS POSTGRESQL)
        # ==============================================================================
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT COALESCE(SUM(horas), 0) FROM horas_extension WHERE alumno_id = %s;"
                cursor.execute(sql, (self.user_id,))
                total_hours = cursor.fetchone()[0]
                self.lbl_hours_amount.config(text=f"{total_hours} HORAS")
        except psycopg2.Error as e:
            print(f"Error al calcular las horas de extensión: {e}")
            self.lbl_hours_amount.config(text="Error HORAS")

    def open_load_hours_ui(self):
        print("Abriendo ventana de Cargar Horas... (Componente de Vicente)")

    # ==============================================================================
    # 2. FUNCIÓN DEL BOTÓN RESUMEN [CAMBIO INTERFAZ GIO]
    # ------------------------------------------------------------------------------
    # Modificamos esta función para que cuando el usuario haga clic en "RESUMEN",
    # levante e incruste tu nueva pantalla de actividades dentro de la app.
    # ==============================================================================
    def open_summary_ui(self):
        print("Abriendo ventana de Resumen y Reportes... (Componente de Gio)")
        
        # Ocultamos temporalmente los elementos visuales del menú principal (los botones)
        # para dejarle el espacio libre a tu pantalla de resumen
        for widget in self.winfo_children():
            widget.pack_forget()
            
        # Instanciamos tu clase 'ResumenView' pasándole los parámetros obligatorios:
        # master (self), controller, conexión a la BD y el id de usuario logueado.
        self.vista_resumen = ResumenView(
            parent=self, 
            controller=self.controller, 
            connection=self.connection, 
            user_id=self.user_id
        )
        
        # Mostramos tu pantalla ocupando todo el espacio disponible del contenedor
        self.vista_resumen.pack(fill="both", expand=True)


# ==============================================================================
# EJECUCIÓN DIRECTA LOCAL (ENTORNO DE DESARROLLO)
# ------------------------------------------------------------------------------
# Bloque para ejecutar este menú de forma aislada y probar los cambios locales.
# ==============================================================================
if __name__ == "__main__":
    from ui.config_base import PantallaBase
    from database.conection import obtener_conexion
    
    root = PantallaBase("Menú Principal - Desarrollo y Pruebas")
    
    try:
        # Intenta inicializar con base de datos real utilizando el conection.py del equipo
        connection_db = obtener_conexion()
        app = MainMenuView(root, controller=None, connection=connection_db, user_id=1)
    except Exception as e:
        # Si da error pgAdmin o estás sin conexión local, abre en modo simulado de prueba
        print(f"Ejecutando en Modo Simulado (Sin BD): {e}")
        app = MainMenuView(root, controller=None, connection=None, user_id=1)
        
    app.pack(fill="both", expand=True)
    root.mainloop()