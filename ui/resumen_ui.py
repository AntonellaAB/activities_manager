import tkinter as tk
from tkinter import ttk, messagebox
import os

# 1. IMPORTACIÓN DE DISEÑO GENERAL:
# Traemos los colores y tipografías que el equipo definió en 'config_base.py'
# de esta manera la pantalla mantiene la misma estética que el resto del sistema.
from ui.config_base import (
    FONDO_PRINCIPAL, FONDO_TARJETA, FUENTE_FAMILY,
    FUENTE_COLOR, BOTON_COLOR1
)

# 2. DEFINICIÓN DE LA VISTA (PANTALLA DE RESUMEN):
# Definimos la clase como un tk.Frame (un contenedor) en lugar de una ventana suelta (tk.Tk).
# Esto permite que nuestra pantalla se incruste directamente dentro del menú principal dinámico.
class ResumenView(tk.Frame):
    def __init__(self, parent, controller, connection, user_id):
        # Inicializamos el contenedor heredando el color de fondo principal
        super().__init__(parent, bg=FONDO_PRINCIPAL)
        
        # Guardamos las variables de control que nos pasa el sistema de forma global:
        self.controller = controller  # El manejador para cambiar de ventanas
        self.connection = connection  # La conexión activa a la base de datos PostgreSQL
        self.user_id = user_id        # El ID del estudiante que inició sesión (para buscar sus horas)
        
        # Llamamos a la función constructora de los elementos visuales
        self.setup_ui()

    def setup_ui(self):
        # --- ETIQUETA DE TÍTULO ---
        # Creamos el texto superior de la pantalla usando las fuentes del equipo
        lbl_titulo = tk.Label(
            self, text="TABLA DE TODAS LAS ACTIVIDADES", 
            font=(FUENTE_FAMILY, 14, "bold"), bg=FONDO_PRINCIPAL, fg=FUENTE_COLOR
        )
        lbl_titulo.pack(pady=15)

        # --- TARJETA VISUAL DE RESUMEN ---
        # Armamos un recuadro (frame) para destacar las horas acumuladas del usuario
        frame_horas = tk.Frame(self, bg=FONDO_TARJETA, bd=1, relief="solid")
        frame_horas.pack(pady=10, fill="x", padx=30)

        # Texto que muestra las horas. Por requerimiento, arranca con una prueba de 35 horas.
        self.lbl_total_horas = tk.Label(
            frame_horas, text="TIENES: 35 HORAS ACUMULADAS", 
            font=(FUENTE_FAMILY, 12, "bold"), bg=FONDO_TARJETA, fg=FUENTE_COLOR
        )
        self.lbl_total_horas.pack(pady=10)

        # --- TABLA DE DATOS (TREEVIEW) ---
        # Contenedor especial para la tabla y su barra de desplazamiento
        frame_tabla = tk.Frame(self, bg=FONDO_PRINCIPAL)
        frame_tabla.pack(padx=30, pady=10, fill="both", expand=True)

        # Definimos los identificadores de las 5 columnas requeridas
        columnas = ("fecha", "tipo", "materia", "horas", "ubicacion")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=6)
        
        # Asignamos los títulos públicos que el usuario va a leer en la cabecera
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.heading("materia", text="Materia")
        self.tabla.heading("horas", text="Horas")
        self.tabla.heading("ubicacion", text="Ubicación")

        # Configuramos los anchos de columna y las alineaciones del texto (centrado o a la izquierda)
        self.tabla.column("fecha", width=90, anchor="center")
        self.tabla.column("tipo", width=100, anchor="center")
        self.tabla.column("materia", width=140, anchor="w")
        self.tabla.column("horas", width=60, anchor="center")
        self.tabla.column("ubicacion", width=120, anchor="w")

        self.tabla.pack(side="left", fill="both", expand=True)

        # Agregamos la barra de desplazamiento vertical (Scrollbar) para cuando haya muchos datos
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # --- CARGA DE DATOS INICIAL ---
        # Insertamos automáticamente la fila de prueba solicitada por el equipo para testear
        self.cargar_registro_prueba()

        # --- BOTÓN DE DESCARGA ---
        # Creamos el botón interactivo que ejecutará la exportación del archivo plano (.txt)
        self.btn_descargar = tk.Button(
            self, 
            text="DESCARGAR INFORME (TXT) 📥", 
            font=(FUENTE_FAMILY, 10, "bold"), 
            bg=BOTON_COLOR1, 
            fg="white", 
            padx=15, 
            pady=6,
            command=self.generar_informe_txt
        )
        self.btn_descargar.pack(pady=15)

    def cargar_registro_prueba(self):
        """
        Función de simulación: Inserta una fila inicial de prueba directamente 
        en los componentes del Treeview para comprobar que el diseño visual funcione.
        """
        self.tabla.insert("", tk.END, values=("2026-06-25", "INTRA-MURO", "Proyecto Optativa", "35", "Laboratorio GR 218"))

    def generar_informe_txt(self):
        """
        Función del botón Descargar: Crea un documento de texto (.txt) plano,
        con formato estructurado usando caracteres simples para representar las cabeceras.
        """
        try:
            nombre_archivo = "informe_horas_extension.txt"
            
            # Abrimos/creamos el archivo en modo escritura ("w") asegurando formato UTF-8 para las tildes
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write("==================================================\n")
                f.write("         REPORTE DE HORAS DE EXTENSIÓN            \n")
                f.write("==================================================\n")
                f.write(f"ID Alumno logueado: {self.user_id}\n")
                f.write("Total Horas: 35 Horas\n")
                f.write("--------------------------------------------------\n")
                f.write("Detalle de Actividades registradas:\n")
                
                # Bucle FOR: Recorremos cada una de las filas que estén cargadas visualmente en la tabla
                for item in self.tabla.get_children():
                    v = self.tabla.item(item)["values"]
                    # Estructuramos la línea separando las variables con barras verticales
                    f.write(f"- {v[0]} | {v[1]} | {v[2]} | {v[3]} Horas | {v[4]}\n")
                     
                f.write("==================================================\n")
            
            # Si el bloque de arriba funcionó sin romperse, muestra el aviso de éxito en pantalla
            messagebox.showinfo("Éxito", f"¡Informe generado correctamente como '{nombre_archivo}'!")
        except Exception as e:
            # En caso de errores de permisos o fallas del sistema, salta esta alerta
            messagebox.showerror("Error", f"No se pudo generar el archivo TXT: {e}")