# Archivo: ui/main.py
import tkinter as tk
from tkinter import ttk
import psycopg2

# Importamos las constantes de diseño de tu equipo
from ui.config_base import (
    FONDO_PRINCIPAL, FONDO_TARJETA, FUENTE_FAMILY, 
    FUENTE_COLOR, FUENTE_COLOR_SECUNDARIO, 
    BOTON_COLOR1, BOTON_COLOR2
)

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


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


    def load_total_hours(self):
        """Consulta la base de datos y suma las horas de extensión del usuario."""
        # ==============================================================================
        # MODO DE PRUEBA LOCAL (SIN ENLACE A BASE DE DATOS ACTIVADO)
        # ------------------------------------------------------------------------------
        # MIENTRAS HAGAS PRUEBAS LOCALES, dejas estas dos líneas activas para ver el diseño.
        # Puedes modificar el "35 HORAS" por lo que quieras.
        # CUANDO QUIERAS LEER LOS DATOS REALES DE TU POSTGRESQL, COMENTA LAS DOS LÍNEAS DE ABAJO.
        # ==============================================================================
        self.lbl_hours_amount.config(text="35 HORAS")
        return
        
        # ==============================================================================
        # MODO EN VIVO (CON BASE DE DATOS POSTGRESQL)
        # ------------------------------------------------------------------------------
        # Ejecuta la consulta SQL real sumando los registros de la tabla horas_extension
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

    def open_summary_ui(self):
        print("Abriendo ventana de Resumen y Reportes... (Componente de Gio)")


# ==============================================================================
# EJECUCIÓN DIRECTA LOCAL (ENTORNO DE DESARROLLO)
# ------------------------------------------------------------------------------
# Este bloque levanta la app de forma aislada respetando el tamaño de config_base.
# Se puede comentar/eliminar al integrar el proyecto definitivo en un único ejecutable.
# ==============================================================================
if __name__ == "__main__":
    from ui.config_base import PantallaBase
    from database.conection import obtener_conexion
    
    root = PantallaBase("Menú Principal - Desarrollo y Pruebas")
    
    try:
        # Intenta inicializar con base de datos real
        connection_db = obtener_conexion()
        app = MainMenuView(root, controller=None, connection=connection_db, user_id=1)
    except Exception as e:
        # Si da error o estás sin conexión a Postgresql, abre en modo simulado de prueba
        print(f"Ejecutando en Modo Simulado (Sin BD): {e}")
        app = MainMenuView(root, controller=None, connection=None, user_id=1)
        
    app.pack(fill="both", expand=True)
    root.mainloop()


# ==============================================================================
# EJECUCIÓN HASTA QEUE SE INTEGRE CON EL LOGIN (ENTORNO DE DESARROLLO)
# ------------------------------------------------------------------------------
#Para ejecutar como módulo ejecutar en la terminal: python -m ui.menu
#Debe estar posicionado en el PATH principal del proyecto para que funcione correctamente.
# ==============================================================================