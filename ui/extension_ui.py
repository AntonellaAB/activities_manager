import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from dao.extension_dao import HorasExtensionDAO
from dao.materias_dao import SubjectDAO  
from models.horas_extension import HorasExtension
from database.conection import obtener_conexion

# Reglas de las horas de extension UA - diccionario
REGLAS_ACTIVIDADES = {
    'INTRA-MURO': {
        'Charlas, Webinars, Conferencias, Visitas (cat1)': {'subtipo': 'cat1', 'horas': 1},
        'Misiones académicas internacionales (cat2)': {'subtipo': 'cat2', 'horas': 5},
        'Programas Nacionales/Regionales (cat3)': {'subtipo': 'cat3', 'horas': 3},
        'Extracurriculares: Deportes, Coro, Ballet (cat4)': {'subtipo': 'cat4', 'horas': 1}
    },
    'EXTRA-MURO': {
        'Asesorías, Capacitaciones y Charlas Comunitarias (cat5)': {'subtipo': 'cat5', 'horas': 5},
        'Proyectos con Enfoque Social de la Carrera (cat6)': {'subtipo': 'cat6', 'horas': 10},
        'Campañas de Concienciación dirigidas a la Sociedad (cat7)': {'subtipo': 'cat7', 'horas': 6}
    }
}

class HorasExtensionUI:
    def __init__(self, root, alumno_id_logueado, callback_actualizar=None):
        self.root = root
        self.alumno_id = alumno_id_logueado
        self.callback_actualizar = callback_actualizar
        
        self.root.title("Registro de Horas de Extensión")
        self.root.geometry("480x580")
        self.root.resizable(False, False)
        
        self.materias_dict = {}
        self.profesores_dict = {}
        self.horas_calculadas = 0  

        self.cargar_datos_desde_bd()
        self.crear_componentes()

    def cargar_datos_desde_bd(self):
        conn = obtener_conexion()
        if conn:
            subjects_lista = SubjectDAO.get_all(conn)
            self.materias_dict = {subj.name: subj.subject_id for subj in subjects_lista}
            conn.close()
            
        self.profesores_dict = HorasExtensionDAO.obtener_profesores_dict()

    def crear_componentes(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        titulo = ttk.Label(main_frame, text="Registrar Horas de Extensión", font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Semestre
        ttk.Label(main_frame, text="Semestre:").grid(row=1, column=0, sticky=tk.W, pady=6)
        self.spin_semestre = ttk.Spinbox(main_frame, from_=1, to=12, width=10, state="readonly")
        self.spin_semestre.set(1)
        self.spin_semestre.grid(row=1, column=1, sticky=tk.W, pady=6)

        # Fecha
        ttk.Label(main_frame, text="Fecha:").grid(row=2, column=0, sticky=tk.W, pady=6)
        self.entry_fecha = DateEntry(main_frame, width=17, date_pattern='yyyy-mm-dd')
        self.entry_fecha.grid(row=2, column=1, sticky=tk.W, pady=6)

        # Ubicación
        ttk.Label(main_frame, text="Ubicación / Lugar:").grid(row=3, column=0, sticky=tk.W, pady=6)
        self.entry_ubicacion = ttk.Entry(main_frame, width=32)
        self.entry_ubicacion.grid(row=3, column=1, sticky=tk.W, pady=6)

        # Materia Asociada
        ttk.Label(main_frame, text="Materia asociada:").grid(row=4, column=0, sticky=tk.W, pady=6)
        self.combo_materia = ttk.Combobox(main_frame, values=list(self.materias_dict.keys()), state="readonly", width=30)
        self.combo_materia.grid(row=4, column=1, sticky=tk.W, pady=6)

        # Profesor Tutor
        ttk.Label(main_frame, text="Profesor tutor:").grid(row=5, column=0, sticky=tk.W, pady=6)
        self.combo_profesor = ttk.Combobox(main_frame, values=list(self.profesores_dict.keys()), state="readonly", width=30)
        self.combo_profesor.grid(row=5, column=1, sticky=tk.W, pady=6)

        

        # Tipo de Actividad (Intra / Extra)
        ttk.Label(main_frame, text="Tipo Actividad:").grid(row=6, column=0, sticky=tk.W, pady=6)
        self.combo_tipo = ttk.Combobox(main_frame, values=list(REGLAS_ACTIVIDADES.keys()), state="readonly", width=30)
        self.combo_tipo.grid(row=6, column=1, sticky=tk.W, pady=6)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.actualizar_subtipos)

        # Subtipo / Categoria especifica
        ttk.Label(main_frame, text="Categoría:").grid(row=7, column=0, sticky=tk.W, pady=6)
        self.combo_subtipo = ttk.Combobox(main_frame, state="readonly", width=30)
        self.combo_subtipo.grid(row=7, column=1, sticky=tk.W, pady=6)
        self.combo_subtipo.bind("<<ComboboxSelected>>", self.calcular_horas_automaticas)

        # ver de horas Asignadas (
        ttk.Label(main_frame, text="Horas a Computar:").grid(row=8, column=0, sticky=tk.W, pady=6)
        self.lbl_visualizar_horas = ttk.Label(main_frame, text="0 horas", font=("Arial", 11, "bold"), foreground="green")
        self.lbl_visualizar_horas.grid(row=8, column=1, sticky=tk.W, pady=6)

        # ------------------------------------------------------

        #  Descripcion 
        ttk.Label(main_frame, text="Descripción:").grid(row=9, column=0, sticky=tk.NW, pady=6)
        self.txt_descripcion = tk.Text(main_frame, width=30, height=4, font=("Arial", 10))
        self.txt_descripcion.grid(row=9, column=1, sticky=tk.W, pady=6)

        btn_guardar = ttk.Button(main_frame, text="Guardar Registro", command=self.procesar_guardado)
        btn_guardar.grid(row=10, column=0, columnspan=2, pady=(25, 0))

    def actualizar_subtipos(self, event):
        """Filtra dinámicamente las categorías dependiendo del tipo elegido."""
        tipo_seleccionado = self.combo_tipo.get()
        categorias_disponibles = list(REGLAS_ACTIVIDADES[tipo_seleccionado].keys())
        
        self.combo_subtipo.config(values=categorias_disponibles)
        self.combo_subtipo.set('')  # Resetea el combo secundario
        self.lbl_visualizar_horas.config(text="0 horas", foreground="gray")
        self.horas_calculadas = 0

    def calcular_horas_automaticas(self, event):
        """Extrae el valor entero de horas predefinido para la categoría elegida."""
        tipo = self.combo_tipo.get()
        subtipo_texto = self.combo_subtipo.get()
        
        if tipo and subtipo_texto:
            self.horas_calculadas = REGLAS_ACTIVIDADES[tipo][subtipo_texto]['horas']
            self.lbl_visualizar_horas.config(text=f"{self.horas_calculadas} horas automáticas", foreground="green")

    def procesar_guardado(self):
        fecha = self.entry_fecha.get_date().strftime('%Y-%m-%d')
        ubicacion = self.entry_ubicacion.get().strip()
        descripcion = self.txt_descripcion.get("1.0", tk.END).strip()
        
        tipo = self.combo_tipo.get()
        subtipo_texto = self.combo_subtipo.get()
        
        # Validaciones de campos obligatorios tradicionales
        if not ubicacion or not descripcion:
            messagebox.showwarning("Campos incompletos", "Ubicación y Descripción son obligatorios.")
            return

        if not self.combo_materia.get() or not self.combo_profesor.get():
            messagebox.showwarning("Selección faltante", "Por favor selecciona Materia y Profesor.")
            return

        # 
        if not tipo or not subtipo_texto:
            messagebox.showwarning("Selección faltante", "Por favor define el Tipo y Categoría de la actividad.")
            return

        # ====================TOPES DEL ALUMNO =============================================
        try:
            subtipo_db = REGLAS_ACTIVIDADES[tipo][subtipo_texto]['subtipo']
            
            
            horas_actuales_subtipo = HorasExtensionDAO.obtener_horas_por_subtipo(self.alumno_id, subtipo_db)
            horas_actuales_tipo = HorasExtensionDAO.obtener_horas_por_tipo(self.alumno_id, tipo)

            # Validar Tope  = 20 Intra-muro / 30 Extra-muro
            tope_global_tipo = 20 if tipo == 'INTRA-MURO' else 30
            if horas_actuales_tipo + self.horas_calculadas > tope_global_tipo:
                messagebox.showerror(
                    "Tope Consolidado Alcanzado", 
                    f"No se puede registrar.\nSuperarías el límite máximo consolidado de {tope_global_tipo} horas para actividades {tipo}."
                )
                return

            # Validar Subcategorías con límites específicos estrictos por código
            if subtipo_db == 'cat4' and (horas_actuales_subtipo + self.horas_calculadas > 5):
                messagebox.showerror("Tope de Subcategoría", "Límite excedido. Las actividades Extracurriculares (cat4) admiten un máximo de 5 horas.")
                return
            if subtipo_db == 'cat3' and (horas_actuales_subtipo + self.horas_calculadas > 15):
                messagebox.showerror("Tope de Subcategoría", "Límite excedido. Los Programas Nacionales (cat3) admiten un máximo de 15 horas.")
                return

        except AttributeError:
            
            pass

        
        materia_id = self.materias_dict[self.combo_materia.get()]
        profesor_id = self.profesores_dict[self.combo_profesor.get()]
        semestre = int(self.spin_semestre.get())

        

        
        nueva_solicitud = HorasExtension(
            alumno_id=self.alumno_id, 
            semestre=semestre, 
            ubicacion=ubicacion,
            materia_id=materia_id, 
            profesor_id=profesor_id,
            fecha=fecha, 
            horas=self.horas_calculadas, 
            informe=descripcion
        )

        exito = HorasExtensionDAO.agregar_horas(nueva_solicitud)

        if exito:
            messagebox.showinfo("¡Correcto!", "Registrado con éxito.")
            if self.callback_actualizar:
                self.callback_actualizar()
            self.root.destroy()
        else:
            messagebox.showerror("Fallo", "Error al guardar en la BD.")