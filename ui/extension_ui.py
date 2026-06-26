import tkinter as tk
from tkinter import ttk, messagebox
from dao.extension_dao import HorasExtensionDAO
from dao.materias_dao import SubjectDAO  
from models.horas_extension import HorasExtension
from database.conection import obtener_conexion

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

        # 1. Semestre
        ttk.Label(main_frame, text="Semestre:").grid(row=1, column=0, sticky=tk.W, pady=6)
        self.spin_semestre = ttk.Spinbox(main_frame, from_=1, to=12, width=10, state="readonly")
        self.spin_semestre.set(1)
        self.spin_semestre.grid(row=1, column=1, sticky=tk.W, pady=6)

        # 2. Fecha
        ttk.Label(main_frame, text="Fecha (AAAA-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=6)
        self.entry_fecha = ttk.Entry(main_frame, width=20)
        self.entry_fecha.grid(row=2, column=1, sticky=tk.W, pady=6)

        # 3. Ubicación
        ttk.Label(main_frame, text="Ubicación / Lugar:").grid(row=3, column=0, sticky=tk.W, pady=6)
        self.entry_ubicacion = ttk.Entry(main_frame, width=32)
        self.entry_ubicacion.grid(row=3, column=1, sticky=tk.W, pady=6)

        # 4. Materia
        ttk.Label(main_frame, text="Materia asociada:").grid(row=4, column=0, sticky=tk.W, pady=6)
        self.combo_materia = ttk.Combobox(main_frame, values=list(self.materias_dict.keys()), state="readonly", width=30)
        self.combo_materia.grid(row=4, column=1, sticky=tk.W, pady=6)

        # 5. Profesor Tutor
        ttk.Label(main_frame, text="Profesor tutor:").grid(row=5, column=0, sticky=tk.W, pady=6)
        self.combo_profesor = ttk.Combobox(main_frame, values=list(self.profesores_dict.keys()), state="readonly", width=30)
        self.combo_profesor.grid(row=5, column=1, sticky=tk.W, pady=6)

        # 6. Horas
        ttk.Label(main_frame, text="Horas acumuladas:").grid(row=6, column=0, sticky=tk.W, pady=6)
        self.entry_horas = ttk.Entry(main_frame, width=12)
        self.entry_horas.grid(row=6, column=1, sticky=tk.W, pady=6)

        # 7. Descripción
        ttk.Label(main_frame, text="Descripción:").grid(row=7, column=0, sticky=tk.NW, pady=6)
        self.txt_descripcion = tk.Text(main_frame, width=30, height=4, font=("Arial", 10))
        self.txt_descripcion.grid(row=7, column=1, sticky=tk.W, pady=6)

        btn_guardar = ttk.Button(main_frame, text="Guardar Registro", command=self.procesar_guardado)
        btn_guardar.grid(row=8, column=0, columnspan=2, pady=(25, 0))

    def procesar_guardado(self):
        fecha = self.entry_fecha.get().strip()
        ubicacion = self.entry_ubicacion.get().strip()
        horas_str = self.entry_horas.get().strip()
        descripcion = self.txt_descripcion.get("1.0", tk.END).strip()
        
        if not fecha or not ubicacion or not horas_str:
            messagebox.showwarning("Campos incompletos", "Fecha, Ubicación y Horas son obligatorios.")
            return

        if not self.combo_materia.get() or not self.combo_profesor.get():
            messagebox.showwarning("Selección faltante", "Por favor selecciona Materia y Profesor.")
            return

        try:
            horas = int(horas_str)
        except ValueError:
            messagebox.showerror("Error numérico", "Las horas deben ser un número entero.")
            return

        materia_id = self.materias_dict[self.combo_materia.get()]
        profesor_id = self.profesores_dict[self.combo_profesor.get()]
        semestre = int(self.spin_semestre.get())

        nueva_solicitud = HorasExtension(
            alumno_id=self.alumno_id, semestre=semestre, ubicacion=ubicacion,
            materia_id=materia_id, profesor_id=profesor_id,
            fecha=fecha, horas=horas, informe=descripcion
        )

        exito = HorasExtensionDAO.agregar_horas(nueva_solicitud)

        if exito:
            messagebox.showinfo("¡Correcto!", "Registrado con éxito.")
            if self.callback_actualizar:
                self.callback_actualizar()
            self.root.destroy()
        else:
            messagebox.showerror("Fallo", "Error al guardar en la BD.")